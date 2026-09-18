import datetime
import re
import feedparser

def extract_image(entry):
    """ Tente de trouver une image dans l'article RSS """
    # 1. Chercher dans media_content
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0].get('url')
    # 2. Chercher dans enclosures (fichiers joints)
    if 'enclosures' in entry and len(entry.enclosures) > 0:
        for enc in entry.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.get('href')
    # 3. Chercher une balise <img> dans la description HTML
    summary_html = entry.get('summary', '') or entry.get('description', '')
    img_match = re.search(r'<img [^>]*src=["\']([^"\']+)["\']', summary_html)
    if img_match:
        return img_match.group(1)
    
    return None

def clean_html(text):
    """ Nettoie les balises HTML de la description pour garder du texte propre """
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:250] + "..." if len(clean) > 250 else clean

def update_axe1():
    url = "https://www.cert.ssi.gouv.fr/feed/"
    feed = feedparser.parse(url)
    
    date_str = datetime.date.today().strftime("%d/%m/%Y")
    new_content = f"\n\n## 🚨 Bulletin du {date_str}\n\n"
    
    for entry in feed.entries[:4]:
        title = entry.title
        link = entry.link
        summary = clean_html(entry.get('summary', 'Pas de description détaillée disponible.'))
        pub_date = entry.get('published', '')
        
        # Format sous forme d'encadré d'alerte MkDocs
        new_content += f"!!! warning \"[{title}]({link})\"\n"
        new_content += f"    **Date d'émission :** {pub_date}  \n"
        new_content += f"    **Analyse / Impact :** {summary}\n\n"
    
    with open("docs/axe1-securite.md", "a", encoding="utf-8") as f:
        f.write(new_content)

def update_axe2():
    url = "https://www.it-connect.fr/feed/"
    feed = feedparser.parse(url)
    
    date_str = datetime.date.today().strftime("%d/%m/%Y")
    new_content = f"\n\n## 🤖 Sélection du mois — {date_str}\n\n"
    
    count = 0
    for entry in feed.entries:
        title_lower = entry.title.lower()
        if any(keyword in title_lower for keyword in ["ia", "intelligence artificielle", "script", "powershell", "python", "automation"]):
            title = entry.title
            link = entry.link
            summary = clean_html(entry.get('summary', ''))
            image_url = extract_image(entry)
            
            new_content += f"### [{title}]({link})\n\n"
            if image_url:
                new_content += f"![Illustration]({image_url}){{ align=left width=250 }}\n\n"
            new_content += f"**Résumé :** {summary}\n\n"
            new_content += f"[👉 Lire l'article complet]({link})\n\n---\n\n"
            
            count += 1
            if count >= 3:
                break
                
    with open("docs/axe2-ia-admin.md", "a", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_axe1()
    update_axe2()
