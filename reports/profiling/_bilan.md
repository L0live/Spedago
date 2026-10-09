# Spédago — bilan du profilage (9 octobre 2026)

17 jeux téléchargés dans `data/raw/` (export CSV `;`, noms de champs bruts). Rapports détaillés par fichier dans ce dossier.

## Piste A — Parcoursup (tension, capacités, PPL art. 2)

| Constat | Conséquence |
|---|---|
| 8 sessions 2018-2025, 10 697 → 14 252 formations | Série longue exploitable |
| Schéma stable 2022-2025 (118 col.) ; 2021 : −4 ; 2020 : −12 ; 2019 : −28 ; 2018 : −35 | Table harmonisée à construire ; 2018-2019 = sous-ensemble de variables |
| `cod_aff_form` absent en 2018-2019 ; `ran_grp*` absents en 2018 (`rang_der_max` à la place) | Panel formation × année propre seulement **2020-2025** |
| Formations 2020 retrouvées en 2025 : 85 % (2024 : 96 %) | Attrition à documenter (fermetures, recodages) |
| 2025 : variables clés quasi complètes (`ran_grp1` manquant 0,4 %) | OK |
| **`acc_tot > capa_fin` dans 13,6 % des formations** | À comprendre avant tout calcul de tension (surbooking ? capacité non finale ?) |
| Vœux/capacité médian : 12,1 (sélectives) vs 9,1 (non sélectives) | Premier indicateur de tension |
| Pas d'origine géographique des candidats (seulement « même académie ») | Limite pour l'analyse territoriale |
| Bonus : `parcoursup_specialites_v3` (bac 2025) — vœux/propositions/acceptations par **doublette de spécialités × formation** | Pont entre A et B |

## Piste B — complexité organisationnelle des lycées

| Constat | Conséquence |
|---|---|
| Triplettes 1re : 2021-2025, ~2 270 lycées GT/an ; doublettes Tle : 2020-2025 | Série de 5-6 ans |
| **Seules les 18 triplettes nationales les plus fréquentes sont nommées**, le reste agrégé en « autres combinaisons » (médiane 20 %, P90 39 %) | Impossible de compter directement les combinaisons distinctes par lycée |
| **Masquage < 5 : les triplettes publiées ne couvrent que 62 % des élèves (médiane)** | Perte d'information massive, surtout dans les petits lycées |
| Spécialités (20 colonnes) : 7 observées par lycée en médiane (0 à 14) | Largeur d'offre mesurable |
| Jointure UAI : triplettes ↔ IPS ≥ 97 %, ↔ éloignement 98 % | Croisements faisables |
| IPS : rupture de série entre `ips_lycees` (2016-2022) et `ap2023` (2023-2026) | Ne pas comparer les niveaux entre les deux séries |

**Piste méthodologique** : le masquage est lui-même un signal. Part non couverte (masquée) + part « autres » ≈ dispersion des élèves dans des petits groupes. À valider (une cellule vide peut valoir 0 ou < 5).

## Piste C — Mon Master

| Constat | Conséquence |
|---|---|
| Sessions 2023 (7 694 formations), 2024 (8 090), 2025 (8 167) | 3 ans |
| Capacité, candidats, classés : complets ; rang du dernier appelé PP manquant 3 %, PC 69 % (normal : formations hors PC) | Probabilité d'accès estimable par formation |
| Ventilation des candidats par statut d'origine (L3, LP, BUT3, master…) | Simulateur par profil d'origine possible |
| Pas de boursiers | Pas d'analyse sociale |
| Schéma 2023 (97 col.) ≠ 2024-2025 (144 col.) | Harmonisation à faire |

## Autres

- `remplacement_2nd_degre` : 30 lignes, un taux moyen par académie (ex. Poitiers 95,6 %, Créteil 92,8 %), une seule année. Inutilisable pour une analyse fine.
- Faux positif du script : `inm` (code mention Mon Master) détecté comme UAI.
