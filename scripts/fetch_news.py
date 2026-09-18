import datetime
import re
import feedparser

def clean_html(text):
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:280] + "..." if len(clean) > 280 else clean

def extract_image(entry):
    if 'media_content' in entry and len(entry.media_content) > 0:
        return entry.media_content[0].get('url')
    if 'enclosures' in entry and len(entry.enclosures) > 0:
        for enc in entry.enclosures:
            if enc.get('type', '').startswith('image/'):
                return enc.get('href')
    summary_html = entry.get('summary', '') or entry.get('description', '')
    img_match = re.search(r'<img [^>]*src=["\']([^"\']+)["\']', summary_html)
    if img_match:
        return img_match.group(1)
    return None

def update_axe1():
    url = "https://www.cert.ssi.gouv.fr/feed/"
    feed = feedparser.parse(url)
    
    date_str = datetime.date.today().strftime("%d/%m/%Y")
    new_content = f"\n\n## 📅 Mise à jour du {date_str}\n\n"
    
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        summary = clean_html(entry.get('summary', 'Aucun détail fourni.'))
        pub_date = entry.get('published', '')
        
        # Détections de mots clés pour attribuer un badge visuel
        badge = "🔴 **CRITIQUE**" if "CERTFR-" in title else "🟠 **AVIS / ALERTE**"
        
        new_content += f"=== \"{title[:45]}...\"\n"
        new_content += f"    ### [{title}]({link})\n\n"
        new_content += f"    * **Niveau :** {badge}\n"
        new_content += f"    * **Publié le :** `{pub_date}`\n\n"
        new_content += f"    > {summary}\n\n"
        new_content += f"    [:octicons-link-external-16: Consulter le bulletin officiel du CERT-FR]({link})\n\n"
    
    with open("docs/axe1-securite.md", "a", encoding="utf-8") as f:
        f.write(new_content)

def update_axe2():
    url = "https://www.it-connect.fr/feed/"
    feed = feedparser.parse(url)
    
    date_str = datetime.date.today().strftime("%d/%m/%Y")
    new_content = f"\n\n## 🗓️ Édition du {date_str}\n\n<div class=\"grid cards\" markdown>\n\n"
    
    count = 0
    for entry in feed.entries:
        title_lower = entry.title.lower()
        if any(k in title_lower for k in ["ia", "intelligence artificielle", "powershell", "script", "python", "automation", "copilot"]):
            title = entry.title
            link = entry.link
            summary = clean_html(entry.get('summary', ''))
            img = extract_image(entry)
            
            new_content += f"-   ### [{title}]({link})\n"
            new_content += f"    ---\n"
            if img:
                new_content += f"    ![Image]({img}){{ style=\"height:160px; width:100%; object-fit:cover; border-radius:8px;\" }}\n\n"
            new_content += f"    {summary}\n\n"
            new_content += f"    [:octicons-arrow-right-24: Lire l'article]({link})\n\n"
            
            count += 1
            if count >= 4:
                break
                
    new_content += "</div>\n"
    
    with open("docs/axe2-ia-admin.md", "a", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_axe1()
    update_axe2()
