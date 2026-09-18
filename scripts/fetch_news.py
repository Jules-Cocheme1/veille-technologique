import datetime
import os
import re
import feedparser

def clean_html(text):
    if not text:
        return "Aucune description fournie par la source."
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean[:300] + "..." if len(clean) > 300 else clean

def extract_image(entry):
    try:
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
    except Exception:
        pass
    return None

def update_axe1():
    """ Axe 1 : Sécurité & Failles - Formaté selon la grille des 6 règles """
    try:
        url = "https://www.cert.ssi.gouv.fr/feed/"
        feed = feedparser.parse(url)
        date_str = datetime.date.today().strftime("%d/%m/%Y")
        
        new_content = f"\n\n## 📅 Relevé du {date_str}\n\n"
        
        for entry in feed.entries[:4]:
            title = entry.get('title', 'Alerte de Sécurité').replace('"', "'")
            link = entry.get('link', '#')
            raw_summary = clean_html(entry.get('summary', ''))
            pub_date = entry.get('published', 'Récents')
            
            # Analyse automatique pour la gravité et l'impact
            is_critical = "CERTFR-" in title or "ALE" in title
            severity_badge = "🔴 **CRITIQUE (Action immédiate)**" if is_critical else "🟠 **ÉLEVÉE / AVIS**"
            admonition_type = "danger" if is_critical else "warning"
            
            # Formatage structuré selon les 6 règles
            new_content += f"!!! {admonition_type} \"[{title}]({link})\"\n"
            new_content += f"    * **1. Source & Date :** `CERT-FR` | Publié le `{pub_date}`\n"
            new_content += f"    * **2. Niveau de Gravité :** {severity_badge}\n"
            new_content += f"    * **3. Résumé de la menace :** {raw_summary}\n"
            new_content += f"    * **4. Impact & Périmètre :** Exposition potentielle des composants affectés, risque d'exécution de code ou d'accès non autorisé.\n"
            new_content += f"    * **5. Action recommandée :** Consulter le bulletin officiel, appliquer les correctifs éditeurs ou restreindre les accès réseau exposés.\n"
            new_content += f"    * **6. Lien officiel :** [:octicons-link-external-16: Accéder à la fiche CERT-FR]({link})\n\n"
            
        os.makedirs("docs", exist_ok=True)
        with open("docs/axe1-securite.md", "a", encoding="utf-8") as f:
            f.write(new_content)
            
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'Axe 1: {e}")

def update_axe2():
    """ Axe 2 : IA & Admin Sys/Réseau - Formaté selon la grille des 6 règles """
    try:
        url = "https://www.it-connect.fr/feed/"
        feed = feedparser.parse(url)
        date_str = datetime.date.today().strftime("%d/%m/%Y")
        
        new_content = f"\n\n## 🗓️ Édition du {date_str}\n\n"
        
        count = 0
        for entry in feed.entries:
            title = entry.get('title', 'Article').replace('"', "'")
            title_lower = title.lower()
            
            if any(k in title_lower for k in ["ia", "intelligence artificielle", "powershell", "script", "python", "automation", "copilot"]):
                link = entry.get('link', '#')
                summary = clean_html(entry.get('summary', ''))
                img = extract_image(entry)
                
                # Formatage structuré selon les 6 règles
                new_content += f"### 🤖 [{title}]({link})\n\n"
                if img:
                    new_content += f"![Illustration]({img}){{ style=\"max-height:180px; border-radius:6px;\" }}\n\n"
                
                new_content += f"* **1. Source & Date :** `IT-Connect` | `{date_str}`\n"
                new_content += f"* **2. Thématique :** Automatisation / IA appliquée à l'administration systèmes\n"
                new_content += f"* **3. Synthèse :** {summary}\n"
                new_content += f"* **4. Cas d'usage :** Optimisation des tâches répétitives de gestion d'infrastructure et d'automatisation.\n"
                new_content += f"* **5. Intérêt stratégique :** Réduction des erreurs humaines, gain de temps sur la rédaction de scripts.\n"
                new_content += f"* **6. Source complète :** [:octicons-arrow-right-24: Consulter l'article originel]({link})\n\n---\n\n"
                
                count += 1
                if count >= 3:
                    break
                    
        os.makedirs("docs", exist_ok=True)
        with open("docs/axe2-ia-admin.md", "a", encoding="utf-8") as f:
            f.write(new_content)
            
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'Axe 2: {e}")

if __name__ == "__main__":
    update_axe1()
    update_axe2()
