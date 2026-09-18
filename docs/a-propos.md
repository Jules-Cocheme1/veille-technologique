# ⚙️ Fonctionnement du Portail de Veille

Ce portail est une plateforme automatisée de suivi technologique. Il collecte, structure et publie sans intervention humaine les actualités critiques en cybersécurité et en administration système.

---

## 🔄 Le Pipeline d'Automatisation (Architecture)

La collecte et la publication reposent sur une chaîne d'outils 100 % automatisée hébergée sur **GitHub** :

```mermaid
graph TD
    A["📡 Sources Officielles<br><i>(Flux RSS : CERT-FR, IT-Connect...)</i>"] -->|1. Extraction automatique| B["🤖 GitHub Actions & Python<br><i>(Cron : Tous les lundis à 8h00 UTC)</i>"]
    B -->|2. Nettoyage & Filtrage| C["📝 Génération Markdown<br><i>(Fiches structurées selon les 6 règles)</i>"]
    C -->|3. Compilation| D["🎨 MkDocs Material<br><i>(Génération du site HTML responsive)</i>"]
    D -->|4. Déploiement| E["🌐 GitHub Pages<br><i>(Hébergement public accessible 24/7)</i>"]

    style A fill:#1f2937,stroke:#3b82f6,stroke-width:2px,color:#fff
    style B fill:#1f2937,stroke:#eab308,stroke-width:2px,color:#fff
    style C fill:#1f2937,stroke:#10b981,stroke-width:2px,color:#fff
    style D fill:#1f2937,stroke:#8b5cf6,stroke-width:2px,color:#fff
    style E fill:#1f2937,stroke:#ef4444,stroke-width:2px,color:#fff

📡 D'où proviennent les informations ?AxeSource principaleMéthode d'extractionType de contenu récupéréAxe 1 (Hebdo)CERT-FR (ssi.gouv.fr)Flux RSS officielBulletins de sécurité, failles Zero-Day, alertes d'urgenceAxe 2 (Mensuel)IT-Connect (it-connect.fr)Flux RSS + Filtres PythonArticles sur l'IA, l'AIOps, PowerShell, Python & SysAdminAxe 3 (Trimestriel)Rapports d'éditeursAnalyse synthétique manuelleRapports de tendance (CrowdStrike, Trend Micro, ANSSI)🛠️ Que fait le script Python (fetch_news.py) ?À chaque exécution, le script effectue 5 opérations automatisées :Requête HTTP : Connexion aux serveurs distants pour télécharger les flux XML/RSS.Filtrage par mots-clés : Pour l'Axe 2, sélection stricte des articles liés à l'IA, aux scripts et à l'automatisation.Nettoyage HTML : Suppression du code superflus, des pubs et mise en forme de texte propre.Enrichissement visuel : Extraction automatique de l'image de couverture ou affectation d'un badge de gravité (🔴 Critique / 🟠 Élevé).Génération structurée : Mise en page sous la grille de contrôle des 6 règles (Source, Gravité, Résumé, Impact, Action, Lien).📋 La Grille de Contrôle des 6 RèglesChaque fiche publiée respecte scrupuleusement le schéma suivant :Source & Date : Origine vérifiée et traçabilité temporelle.Niveau de Gravité / Thématique : Classification visuelle directe.Résumé analytique : Synthèse débarrassée du superflu marketing.Impact & Périmètre : Systèmes affectés et risques pour l'infrastructure.Action recommandée : Correctif, patch ou recommandation d'usage.Lien officiel : Accès direct à la publication d'origine.

---

### 2. Activer Mermaid dans `mkdocs.yml`

Pour que MkDocs dessine les schémas Mermaid proprement, ouvre **`mkdocs.yml`** et vérifie que la ligne `pymdownx.superfences` inclut le support de Mermaid comme ci-dessous :

```yaml
site_name: Portail de Veille Technologique
site_description: Cybersécurité, AIOps & Intelligence Artificielle

theme:
  name: material
  language: fr
  palette:
    scheme: slate
    primary: cyan
    accent: deep orange
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.top
    - search.suggest

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - attr_list
  - tables

nav:
  - 🏠 Accueil: index.md
  - 🚨 Axe 1 - Sécurité (Hebdo): axe1-securite.md
  - 🤖 Axe 2 - IA SysAdmin (Mensuel): axe2-ia-admin.md
  - ⚔️ Axe 3 - IA vs Cyber (Trimestriel): axe3-ia-cyber.md
  - ⚙️ Comment ça marche ?: a-propos.md
