# Centre de veille technologique

Portail de veille en français consacré à trois thèmes :

- **Sécurité** — alertes et vulnérabilités publiées par le CERT-FR.
- **IA & systèmes** — automatisation, administration et AIOps.
- **IA & cybersécurité** — usages de l'IA dans la cyberdéfense et nouvelles menaces.

Le site est construit avec MkDocs Material. Un tableau de bord interactif permet
de parcourir les articles récents, de filtrer par axe et de lancer une recherche.
Les flux RSS sont collectés chaque jour par GitHub Actions ; les articles d'un axe
dont la source est temporairement indisponible sont conservés.

## Lancer le site en local

```powershell
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Puis ouvrir <http://127.0.0.1:8000/>.

## Déploiement

- GitHub Actions actualise `docs/data/articles.json` et publie le site sur GitHub
  Pages.
- `vercel.json` configure la commande de compilation et le dossier `site/` comme
  sortie pour un déploiement Vercel. Importer ce dépôt dans Vercel et conserver
  le répertoire racine du projet.

Les articles restent la propriété de leurs éditeurs respectifs ; chaque fiche
renvoie vers sa source d'origine.
