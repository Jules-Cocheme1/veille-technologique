import os
import urllib.request
import xml.etree.ElementTree as ET

AXES_CONFIG = {
    "docs/axe1-securite.md": {
        "title": "# Axe 1 : Failles de sécurité & Vulnérabilités",
        "intro": "!!! warning \"Périmètre de veille\"\n    Suivi des bulletins du CERT-FR, vulnérabilités critiques et alertes de sécurité.",
        "feeds": [{"url": "https://www.cert.ssi.gouv.fr/feed/", "source": "CERT-FR"}]
    },
    "docs/axe2-ia-admin.md": {
        "title": "# Axe 2 : L'IA dans l'administration systèmes et réseaux",
        "intro": "!!! info \"Périmètre de veille\"\n    Suivi de l'impact des outils IA sur l'automatisation des infrastructures et la gestion réseau.",
        "feeds": [{"url": "https://www.it-connect.fr/feed/", "source": "IT-Connect"}]
    },
    "docs/axe3-ia-cyber.md": {
        "title": "# Axe 3 : IA & Cybersécurité",
        "intro": "!!! example \"Périmètre de veille\"\n    Suivi des menaces ciblant l'IA et de l'utilisation de l'IA pour la détection d'attaques.",
        "feeds": [{"url": "https://www.zdnet.fr/feeds/rss/actualites/", "source": "ZDNet"}]
    }
}

def fetch_rss_items(url, source, limit=5):
    items = []
    seen = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            channel = root.find('channel')
            if channel is not None:
                for item in channel.findall('item'):
                    title = item.findtext('title')
                    link = item.findtext('link')
                    desc = item.findtext('description') or ""
                    
                    if title and link and link not in seen:
                        seen.add(link)
                        # Nettoyage de la description
                        clean_desc = desc.split('<')[0].strip() if '<' in desc else desc.strip()
                        if len(clean_desc) > 150:
                            clean_desc = clean_desc[:150] + "..."
                        if not clean_desc:
                            clean_desc = "Consultez la source officielle pour lire l'intégralité du bulletin d'information."
                            
                        items.append({
                            'title': title.strip(),
                            'link': link.strip(),
                            'desc': clean_desc,
                            'source': source
                        })
                    if len(items) >= limit:
                        break
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
    return items

def main():
    os.makedirs("docs", exist_ok=True)
    
    for filepath, config in AXES_CONFIG.items():
        print(f"Purge et regénération propre de : {filepath}")
        
        # Structure de page aérée et propre avec Grid Cards
        lines = [
            config["title"],
            "",
            config["intro"],
            "",
            "---",
            "",
            "## 📰 Dernières actualités",
            "",
            '<div class="grid cards" markdown>',
            ""
        ]
        
        count = 0
        for feed in config["feeds"]:
            articles = fetch_rss_items(feed["url"], feed["source"], limit=5)
            for art in articles:
                card = f"-   :material-newspaper: **{art['title']}**\n\n" \
                       f"    ---\n\n" \
                       f"    {art['desc']}\n\n" \
                       f"    [:octicons-arrow-right-24: Lire l'article ({art['source']})]({art['link']})"
                lines.append(card)
                lines.append("")
                count += 1
                
        lines.append("</div>")
        lines.append("")
        
        if count == 0:
            lines.append("*Aucune actualité récupérée pour le moment.*")
            
        lines.append("")
        lines.append("---")
        lines.append("*Page régénérée automatiquement.*")
        
        # Le mode 'w' ECRASE entièrement l'ancien fichier (supprime tout le bazar)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

if __name__ == "__main__":
    main()
