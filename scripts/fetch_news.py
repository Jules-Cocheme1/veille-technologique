import os
import urllib.request
import xml.etree.ElementTree as ET

# Configuration des axes de veille et de leurs flux RSS
AXES_CONFIG = {
    "docs/axe1-securite.md": {
        "title": "# Axe 1 : Sécurité & Cybersécurité",
        "description": "Veille axée sur les vulnérabilités, la sécurité des réseaux, la protection des données et les bonnes pratiques de sécurisation informatique.",
        "feeds": [
            "https://www.cert.ssi.gouv.fr/feed/",
            "https://www.ssi.gouv.fr/feed/actualite/"
        ]
    },
    "docs/axe2-ia-admin.md": {
        "title": "# Axe 2 : IA & Administration Système / Réseau",
        "description": "Veille axée sur l'automatisation par l'Intelligence Artificielle, l'optimisation des infrastructures, le Cloud et la gestion des réseaux.",
        "feeds": [
            "https://news.ycombinator.com/rss"
        ]
    },
    "docs/axe3-ia-cyber.md": {
        "title": "# Axe 3 : IA & Cybersécurité",
        "description": "Veille axée sur l'intersection entre IA et sécurité : détection automatique des menaces, attaques ciblant les modèles d'IA, et IA défensive.",
        "feeds": [
            "https://www.zdnet.fr/feeds/rss/actualites/"
        ]
    }
}

def fetch_rss_items(url, limit=5):
    """Récupère et extrait les derniers articles d'un flux RSS."""
    items = []
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # Gestion des formats RSS standard (channel/item)
            channel = root.find('channel')
            if channel is not None:
                for item in channel.findall('item')[:limit]:
                    title = item.findtext('title')
                    link = item.findtext('link')
                    pub_date = item.findtext('pubDate') or ""
                    if title and link:
                        items.append({
                            'title': title.strip(),
                            'link': link.strip(),
                            'date': pub_date.strip()
                        })
    except Exception as e:
        print(f"[Attention] Impossible de lire le flux {url} : {e}")
    return items

def main():
    # S'assurer que le dossier docs existe
    os.makedirs("docs", exist_ok=True)
    
    for filepath, config in AXES_CONFIG.items():
        print(f"Génération de {filepath}...")
        
        # 1. Écrire le titre et la description de la page
        content = [
            config["title"],
            "",
            config["description"],
            "",
            "---",
            "",
            "## 📰 Flux d'actualités récentes",
            ""
        ]
        
        total_articles = 0
        for feed_url in config["feeds"]:
            articles = fetch_rss_items(feed_url)
            for art in articles:
                date_str = f" *({art['date']})*" if art['date'] else ""
                content.append(f"* [{art['title']}]({art['link']}){date_str}")
                total_articles += 1
        
        # Si aucun flux n'a renvoyé d'articles, ajouter un message par défaut
        if total_articles == 0:
            content.append("*Aucune actualité récente récupérée pour le moment. La veille automatique se met à jour régulièrement.*")
        
        content.append("")
        content.append("---")
        content.append("*Page mise à jour automatiquement via GitHub Actions.*")
        
        # 2. Réécriture propre du fichier Markdown
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

if __name__ == "__main__":
    main()
