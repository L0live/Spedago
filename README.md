# Spédago

Observatoire ouvert, neutre et vérifiable des parcours éducatifs : du lycée (spécialités) à Parcoursup, au master et à l'insertion, avec une comparaison France / régions voisines (Eurostat).

Tout est calculé à partir de données publiques (data.gouv.fr, data.enseignementsup-recherche.gouv.fr, Eurostat), téléchargées avec empreinte SHA-256 (`data/raw/MANIFEST*.csv`) et retraitées par un pipeline Python déterministe. Le site est une application web statique (aucun serveur, aucun compte, aucun traceur) : les préférences restent dans le navigateur.

## Structure

| Dossier | Rôle |
|---|---|
| `scripts/` | téléchargement, profilage, analyses, export des données du site |
| `spedago/` | bibliothèque Python commune (lecture, libellés, JSON-stat, export web) |
| `reports/` | rapports méthodologiques (`.md`) et journal des corrections |
| `web/` | application Vite + TypeScript (8 pages) |
| `design.md` | système visuel : jetons, composants, familles de pages |
| `web/src/calc/` | calculs côté navigateur, typés et testés à l'identique de Python |
| `web/public/data/` | JSON produits par le pipeline (non versionnés) |
| `tests/` | pytest : données, parité Python ↔ TypeScript, accessibilité statique |
| `.github/workflows/site.yml` | CI : pipeline complet puis publication GitHub Pages (chaque push sur `main` et chaque lundi) |

## Lancer en local

Prérequis : Python 3.10+ et Node 22.

```bash
pip install -r requirements.txt
bash run_all.sh                # télécharge, calcule, construit web/dist, lance les tests
cd web && npm run dev          # serveur de développement (http://localhost:5173)
```

`bash run_all.sh --fresh` recalcule tout depuis les données brutes.

Accessibilité (axe-core, WCAG 2.2 AA) sur le site construit, à 1280 et 390 px ; la CI le lance avant chaque publication
et bloque sur une violation grave (versions d'axe-core et Playwright figées dans `tools/package.json`) :

```bash
npm ci --prefix tools && tools/node_modules/.bin/playwright install chromium
(cd web && npx vite preview --port 4173 &)
node tools/check_a11y.mjs web/dist tools/node_modules/axe-core/axe.min.js http://localhost:4173/
```

## Publier sur GitHub Pages

1. Créer un dépôt GitHub et y pousser la branche `main`.
2. Dans *Settings → Pages*, choisir la source **GitHub Actions**.
3. Le workflow `site.yml` reconstruit tout et publie `web/dist`. L'adresse apparaît dans l'onglet *Actions*.

## Licences

- Code : [GNU AGPL-3.0-or-later](LICENSE).
- Données dérivées et textes produits par Spédago : [Licence Ouverte / Open Licence 2.0](LICENCE-DONNEES.md) (Etalab). Les données sources restent sous la licence de leur producteur (Licence Ouverte pour les jeux du MESR et du ministère de l'Éducation nationale ; politique de réutilisation d'Eurostat, CC BY 4.0).
