import datetime
import feedparser

def update_axe1():
    # Flux RSS du CERT-FR
    url = "https://www.cert.ssi.gouv.fr/feed/"
    feed = feedparser.parse(url)
    
    date_str = datetime.date.today().strftime("%d/%m/%Y")
    new_content = f"\n\n### Veille du {date_str}\n\n"
    
    # Récupérer les 5 derniers articles
    for entry in feed.entries[:5]:
        new_content += f"- **[{entry.title}]({entry.link})**\n  *{entry.published}*\n"
    
    # Ajouter au fichier axe1-securite.md
    with open("docs/axe1-securite.md", "a", encoding="utf-8") as f:
        f.write(new_content)

def update_axe2():
    # Flux RSS d'IT-Connect (section sysadmin/IA)
    url = "https://www.it-connect.fr/feed/"
    feed = feedparser.parse(url)
    
    date_str = datetime.date.today().strftime("%d/%m/%Y")
    new_content = f"\n\n### Sélection du mois - {date_str}\n\n"
    
    count = 0
    for entry in feed.entries:
        # Filtrer les articles qui parlent d'IA ou d'administration
        title_lower = entry.title.lower()
        if "ia" in title_lower or "intelligence artificielle" in title_lower or "script" in title_lower:
            new_content += f"- **[{entry.title}]({entry.link})**\n"
            count += 1
            if count >= 3:
                break
                
    with open("docs/axe2-ia-admin.md", "a", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_axe1()
    update_axe2()
