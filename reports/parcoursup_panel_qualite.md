# Table Parcoursup harmonisée 2020-2025 — contrôle qualité

- Lignes : **82,000** ; formations distinctes : **16,960**
- Doublons (formation, session) : **0**
- Formations présentes les 6 années : **10,826**

## Par session

| Session | Formations | Places | Admis | Places vacantes | % formations admis > places | % rang incohérent |
|---|---|---|---|---|---|---|
| 2020 | 12,760 | 752,094 | 673,692 | 88,445 | 14.3% | 2.1% |
| 2021 | 13,396 | 766,905 | 652,449 | 121,766 | 9.9% | 1.3% |
| 2022 | 13,644 | 766,205 | 635,308 | 138,465 | 11.0% | 0.5% |
| 2023 | 13,869 | 771,221 | 638,078 | 139,682 | 10.9% | 0.4% |
| 2024 | 14,079 | 770,362 | 649,547 | 129,708 | 13.5% | 0.0% |
| 2025 | 14,252 | 769,351 | 660,752 | 119,033 | 13.6% | 0.0% |

## Corrections appliquées

- `list_com` inversé dans les sources 2024-2025 → variable corrigée `liste_commune` (booléen).
- `list_com` absent en 2020 → imputé depuis 2021 pour 12,128 formations (sur 12,760).
- `fili_harmo` : DUT (2020) → BUT.
- `academie` : « Besançon » (2022) → « Besancon » ; `idf` = Paris, Créteil, Versailles.
- `ind_admis_hors_pp_pc` : admis hors phases PP/PC, non nul pour 7.0% des lignes, jamais négatif (0 cas) — `acc_tot` reste la référence.
- `flag_cned` : 104 lignes CNED (capacités nominales), 25,701 places vacantes en 2025 — à exclure des analyses de tension.
- IFSI 2024 (518 formations au lieu de ~340) : 9 diplômes paramédicaux classés « IFSI » cette année-là seulement (« Autre formation » les autres années) -> réalignés dans `fili_harmo`.
- `capa_fin` : définition officielle « Capacité de l'établissement par formation », sans autre précision (méthodologie 2024 et 2025).
- `nb_voe_pp` / `voe_tot` : la méthodologie précise qu'il s'agit d'effectifs de CANDIDATS par formation (un candidat compte dans chaque formation demandée).

## Stabilité des modalités de `fili` (nb de formations)

| fili              |   2020 |   2021 |   2022 |   2023 |   2024 |   2025 |
|:------------------|-------:|-------:|-------:|-------:|-------:|-------:|
| Autre formation   |   1578 |   1713 |   1689 |   1749 |   1605 |   1815 |
| BTS               |   5173 |   5246 |   5303 |   5339 |   5345 |   5351 |
| BUT               |      0 |    803 |    809 |    816 |    819 |    820 |
| CPGE              |    847 |    968 |    974 |    983 |    982 |    986 |
| DUT               |    804 |      0 |      0 |      0 |      0 |      0 |
| EFTS              |    221 |    224 |    229 |    231 |    240 |    243 |
| Ecole d'Ingénieur |    402 |    457 |    454 |    472 |    523 |    585 |
| Ecole de Commerce |    144 |    172 |    193 |    208 |    222 |    256 |
| IFSI              |    329 |    331 |    337 |    340 |    518 |    344 |
| Licence           |   2578 |   2693 |   2847 |   2903 |   3019 |   3052 |
| Licence_Las       |    457 |    521 |    537 |    550 |    522 |    513 |
| PASS              |    227 |    268 |    272 |    278 |    284 |    287 |

## Indicateurs dérivés — session 2025

|                             |   count |   mean |    std |   min |   25% |    50% |    75% |      max |
|:----------------------------|--------:|-------:|-------:|------:|------:|-------:|-------:|---------:|
| ind_tension_voeux_par_place |   14248 | 20.207 | 33.478 | 0     | 5.374 | 10.537 | 22.625 |  904.667 |
| ind_part_classes_appeles    |   12298 |  0.62  |  0.294 | 0.011 | 0.376 |  0.573 |  1     |    1     |
| ind_taux_remplissage        |   14248 |  0.836 |  0.259 | 0     | 0.731 |  0.933 |  1     |    2.941 |
| ind_places_vacantes         |   14252 |  8.352 | 60.799 | 0     | 0     |  2     |  7     | 2919     |
| ind_admis_hors_pp_pc        |   14252 |  0     |  0     | 0     | 0     |  0     |  0     |    0     |
| ind_pct_brs_voeux           |   14202 |  0.212 |  0.117 | 0     | 0.128 |  0.195 |  0.277 |    1     |
| ind_pct_brs_classes         |   14136 |  0.197 |  0.12  | 0     | 0.11  |  0.18  |  0.262 |    1     |
| ind_pct_brs_propositions    |   14148 |  0.213 |  0.126 | 0     | 0.124 |  0.195 |  0.282 |    1     |
| ind_pct_brs_admis           |   13954 |  0.228 |  0.176 | 0     | 0.1   |  0.2   |  0.322 |    1     |