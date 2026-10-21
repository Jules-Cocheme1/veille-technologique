# Méthodologie & transparence

## Collecte et publication

Les flux RSS sont interrogés chaque jour par un workflow GitHub Actions. Les articles sont normalisés, filtrés par mots-clés, puis regroupés par axe dans le tableau de bord. La page affiche l'heure de collecte, le nombre de publications disponibles et les sources représentées.

Si un flux est momentanément inaccessible, les publications déjà collectées pour cet axe sont conservées et l'échec apparaît dans les journaux du workflow. La fréquence indiquée sur chaque axe est la fréquence de lecture et d'analyse recommandée, pas la fréquence de collecte.

## Sources et critères de sélection

| Axe | Source principale | Sélection |
| --- | --- | --- |
| Failles & vulnérabilités | [CERT-FR](https://www.cert.ssi.gouv.fr/) | Bulletins et avis publiés par le CERT-FR |
| IA & administration | [IT-Connect](https://www.it-connect.fr/) | Termes liés à l'IA, à l'automatisation et aux opérations systèmes |
| IA & cybersécurité | [SecurityWeek](https://www.securityweek.com/) | Présence conjointe de termes liés à l'IA et à la cybersécurité |

Les filtres automatisés ne comprennent pas toujours le contexte. Une publication manquante ou mal classée est possible ; consultez la source d'origine pour confirmer les informations.

## Interprétation et priorisation

Les publications sont présentées par date, sans classement automatique de gravité, de crédibilité ou d'impact. Les mots-clés servent au repérage, pas à la qualification d'un risque. Avant toute décision, vérifiez le contenu complet, la date, la source et l'applicabilité à votre environnement. Les repères propres à chaque axe facilitent cette analyse sans se substituer à une expertise ni à une évaluation locale.

## Limites

- Les titres et résumés proviennent des flux des éditeurs et peuvent être incomplets.
- Cette veille ne remplace pas une évaluation de risque, un conseil professionnel ou les recommandations d'un éditeur.
- Les liens mènent vers des sites tiers, dont le contenu et la disponibilité ne sont pas contrôlés ici.

Le site est compilé avec MkDocs Material et publié sur GitHub Pages. Le dépôt prévoit également un déploiement Vercel.
