import os
import urllib.request
import xml.etree.ElementTree as ET

AXES_CONFIG = {
    "docs/axe1-securite.md": {
        "title": "# Axe 1 : Failles de sécurité & Vulnérabilités",
        "badge": "!!! warning \"Périmètre de veille\"\n    Suivi automatisé des vulnérabilités critiques, bulletins du CERT-FR et alertes de sécurité.",
        "feeds": [
            {"url": "https://www.cert.ssi.gouv.fr/feed/", "tag": "CERT-FR"}
        ]
    },
    "docs/axe2-ia-admin.md": {
        "title": "# Axe 2 : L'IA dans l'administration systèmes et réseaux",
        "badge": "!!! info \"Périmètre de veille\"\n    Suivi de l'impact des outils IA sur l'automatisation des infrastructures, les scripts et la gestion réseau.",
        "feeds": [
            {"url": "https://www.it-connect.fr/feed/", "tag": "IT-Connect"}
        ]
    },
    "docs/axe3-ia-cyber.md": {
        "title": "# Axe 3 : IA & Cybersécurité",
        "badge": "!!! example \"Périmètre de veille\"\n    Suivi des menaces ciblant l'IA et de l'utilisation de l'IA pour la détection automatisée d'attaques.",
        "feeds": [
            {"url": "https://www.zdnet.fr/feeds/rss/actualites/", "tag": "ZDNet"}
        ]
    }
}

def fetch_rss_items(url, tag, limit=6):
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
                        clean_desc = description.split('<')[0].strip() if '<' in description else description.strip()
                        if len(clean_desc) > 140:
                            clean_desc = clean_desc[:140] + "..."
                        elif not clean_desc:
                            clean_desc = "Consultez l'article officiel pour lire la synthèse complète des informations."
                            
                        items.append({
                            'title': title.strip(),
                            'link': link.strip(),
                            'desc': clean_desc,
                            'tag': tag
                        })
                    if len(items) >= limit:
                        break
    except Exception as e:
        print(f"[Attention] Impossible de lire le flux {url} : {e}")
    return items

def main():
    os.makedirs("docs", exist_ok=True)
    
    for filepath, config in AXES_CONFIG.items():
        print(f"Génération du fichier propre : {filepath}...")
        
        content = [
            config["title"],
            "",
            config["badge"],
            "",
            "---",
            "",
            "## 📰 Flux de veille en direct",
            "",
            '<div class="grid cards" markdown>',
            ""
        ]
        
        articles_added = 0
        for feed_info in config["feeds"]:
            articles = fetch_rss_items(feed_info["url"], feed_info["tag"], limit=6)
            for art in articles:
                card = f"-   :material-newspaper: **{art['title']}**\n\n" \
                       f"    ---\n\n" \
                       f"    {art['desc']}\n\n" \
                       f"    [:octicons-arrow-right-24: Consulter la source ({art['tag']})]({art['link']})"
                content.append(card)
                content.append("")
                articles_added += 1
        
        content.append("</div>")
        content.append("")
        
        if articles_added == 0:
            content.append("*Aucune actualité récupérée pour le moment. Prochaine mise à jour sous peu.*")
            
        content.append("")
        content.append("---")
        content.append("*Page mise à jour automatiquement via GitHub Actions.*")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

if __name__ == "__main__":
    main()
