import os
import urllib.request
import xml.etree.ElementTree as ET

# Configuration des axes de veille
AXES_CONFIG = {
    "docs/axe1-securite.md": {
        "title": "# Axe 1 : Failles de sécurité & Vulnérabilités",
        "description": "*Mise à jour automatique régulière.*",
        "feeds": ["https://www.cert.ssi.gouv.fr/feed/"]
    },
    "docs/axe2-ia-admin.md": {
        "title": "# Axe 2 : L'IA dans l'administration systèmes et réseaux",
        "description": "*Mise à jour automatique régulière.*",
        "feeds": ["https://www.it-connect.fr/feed/"]
    },
    "docs/axe3-ia-cyber.md": {
        "title": "# Axe 3 : IA & Cybersécurité",
        "description": "*Mise à jour automatique régulière.*",
        "feeds": ["https://www.zdnet.fr/feeds/rss/actualites/"]
    }
}

def fetch_rss_items(url, limit=5):
    """Récupère et extrait les derniers articles d'un flux RSS sans doublons."""
    items = []
    seen_links = set()
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            channel = root.find('channel')
            if channel is not None:
                for item in channel.findall('item'):
                    title = item.findtext('title')
                    link = item.findtext('link')
                    description = item.findtext('description') or ""
                    
                    if title and link and link not in seen_links:
                        seen_links.add(link)
                        # Nettoyage sommaire de la description
                        clean_desc = description.split('<')[0].strip() if '<' in description else description.strip()
                        if len(clean_desc) > 200:
                            clean_desc = clean_desc[:200] + "..."
                            
                        items.append({
                            'title': title.strip(),
                            'link': link.strip(),
                            'desc': clean_desc
                        })
                    if len(items) >= limit:
                        break
    except Exception as e:
        print(f"[Attention] Impossible de lire le flux {url} : {e}")
    return items

def main():
    os.makedirs("docs", exist_ok=True)
    
    for filepath, config in AXES_CONFIG.items():
        print(f"Génération unique de {filepath}...")
        
        # On construit TOUT le contenu dans une liste pour tout réécrire d'un coup
        content = [
            config["title"],
            "",
            config["description"],
            "",
            "---",
            "",
            "## 📰 Dernières actualités",
            ""
        ]
        
        articles_added = 0
        for feed_url in config["feeds"]:
            articles = fetch_rss_items(feed_url, limit=5)
            for art in articles:
                content.append(f"### [{art['title']}]({art['link']})")
                if art['desc']:
                    content.append(f"> {art['desc']}")
                content.append(f"[:octicons-arrow-right-24: Lire l'article]({art['link']})")
                content.append("")
                content.append("---")
                content.append("")
                articles_added += 1
        
        if articles_added == 0:
            content.append("*Aucune actualité disponible pour le moment.*")
            
        content.append("")
        content.append("*Page régénérée automatiquement via GitHub Actions.*")
        
        # Le mode 'w' écrase entièrement l'ancien fichier pour éliminer toute répétition
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

if __name__ == "__main__":
    main()
