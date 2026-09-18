import os
import urllib.request
import xml.etree.ElementTree as ET

AXES = {
    "docs/axe1-securite.md": {
        "title": "# Axe 1 : Failles de sécurité & Vulnérabilités",
        "desc": "!!! warning \"Périmètre de veille\"\n    Alertes du CERT-FR et bulletins de sécurité critiques.",
        "url": "https://www.cert.ssi.gouv.fr/feed/",
        "tag": "CERT-FR"
    },
    "docs/axe2-ia-admin.md": {
        "title": "# Axe 2 : L'IA dans l'administration systèmes et réseaux",
        "desc": "!!! info \"Périmètre de veille\"\n    Automatisation, scripts et gestion des infrastructures via l'IA.",
        "url": "https://www.it-connect.fr/feed/",
        "tag": "IT-Connect"
    },
    "docs/axe3-ia-cyber.md": {
        "title": "# Axe 3 : IA & Cybersécurité",
        "desc": "!!! example \"Périmètre de veille\"\n    Détection automatisée des menaces et sécurisation des modèles d'IA.",
        "url": "https://www.zdnet.fr/feeds/rss/actualites/",
        "tag": "ZDNet"
    }
}

def get_articles(url, tag, max_items=4):
    items = []
    seen = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            for item in root.findall('.//item')[:max_items]:
                title = item.findtext('title', '').strip()
                link = item.findtext('link', '').strip()
                desc = item.findtext('description', '').strip()
                
                if title and link and link not in seen:
                    seen.add(link)
                    clean_desc = desc.split('<')[0].strip() if '<' in desc else desc
                    if len(clean_desc) > 120:
                        clean_desc = clean_desc[:120] + "..."
                    if not clean_desc:
                        clean_desc = "Consulter le bulletin officiel pour accéder aux détails techniques."
                    
                    items.append({'title': title, 'link': link, 'desc': clean_desc, 'tag': tag})
    except Exception as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
    return items

def main():
    os.makedirs("docs", exist_ok=True)
    
    for filepath, config in AXES.items():
        articles = get_articles(config["url"], config["tag"])
        
        # Structure épurée
        content = [
            config["title"],
            "",
            config["desc"],
            "",
            "---",
            "",
            "## 📰 Dernières actualités",
            "",
            '<div class="grid cards" markdown>',
            ""
        ]
        
        for art in articles:
            content.append(
                f"-   :material-newspaper: **{art['title']}**\n\n"
                f"    ---\n\n"
                f"    {art['desc']}\n\n"
                f"    [:octicons-arrow-right-24: Consulter la source ({art['tag']})]({art['link']})\n"
            )
            
        content.append("</div>")
        content.append("")
        content.append("---")
        content.append("*Page mise à jour automatiquement.*")
        
        # Le mode 'w' ECRASE entièrement le fichier pour effacer l'historique
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

if __name__ == "__main__":
    main()
