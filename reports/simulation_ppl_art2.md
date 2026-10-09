# Simulation — article 2 de la PPL Sénat n° 447 (pression de l'année précédente)

**Statut : exercice de simulation à règles explicites, pas une prévision.** Le texte de loi ne fixe aucune formule.

Paramètres : pression ≥ quantile 75% de la filière, saturation ≥ 95%, redéploiement depuis les formations < 80% de remplissage, plafond S2 = 20%.

## 1. Session 2025 simulée à partir de 2024

- Formations éligibles en 2024 : **2,357** (108,668 places sur 742,462)

| Scénario | Places ajoutées | dont Île-de-France | % des places totales |
|---|---|---|---|
| S1 : +5% dans les formations éligibles | 6,438 | 2,808 | 0.87% |
| S1 : +10% dans les formations éligibles | 11,764 | 5,194 | 1.58% |
| S1 : +20% dans les formations éligibles | 22,277 | 9,935 | 3.00% |
| S2 : classés non appelés, plafond +20% | 15,971 | 7,884 | 2.15% |

Référence : le CESPM estime à environ **7,300** les propositions manquantes en Île-de-France en 2025 (à taux égal avec le reste du pays). Ordre de grandeur seulement : les deux chiffres ne mesurent pas la même chose.

## 2. S3 — financer S1 (+10 %) à places constantes par redéploiement

Redéploiement limité à la même académie × filière × spécialité (`fil_lib_voe_acc`), depuis les seules formations publiques ou privées sous contrat.

- Besoin national : 11,764 places ; couvrable par redéploiement dans la même cellule : **2,334** (20%)
- Île-de-France : besoin 5,194, couvrable 865 (17%)
- Hypothèse encore forte : une place vacante d'un établissement devient une place dans un autre établissement de la même académie et de la même spécialité (locaux et enseignants ne se déplacent pas librement).

## 3. Places ajoutées par filière (2025, S1 +10 % et S2)

| fili_harmo        |   S1 |   S2 |
|:------------------|-----:|-----:|
| Licence           | 4288 | 5415 |
| BTS               | 2315 | 4116 |
| BUT               | 1425 | 2785 |
| Autre formation   | 1086 | 1442 |
| CPGE              |  905 | 1713 |
| Ecole d'Ingénieur |  515 |   74 |
| IFSI              |  509 |    0 |
| Licence_Las       |  305 |  218 |
| PASS              |  226 |    0 |
| EFTS              |  131 |  100 |
| Ecole de Commerce |   59 |  108 |

## 4. Rétro-test : la pression de l'année précédente vise-t-elle les bonnes formations ?

|   session_t |   eligibles_t-1_suivies |   encore_saturees_t |   encore_non_appeles_t |   encore_eligibles_t |   base_saturees_non_eligibles |
|------------:|------------------------:|--------------------:|-----------------------:|---------------------:|------------------------------:|
|        2021 |                    2092 |               0.731 |                  0.802 |                0.598 |                         0.368 |
|        2022 |                    1989 |               0.773 |                  0.801 |                0.652 |                         0.326 |
|        2023 |                    2092 |               0.798 |                  0.772 |                0.688 |                         0.34  |
|        2024 |                    2085 |               0.839 |                  0.753 |                0.727 |                         0.369 |
|        2025 |                    2286 |               0.792 |                  0.76  |                0.708 |                         0.41  |

Lecture : part des formations éligibles en t-1 qui sont encore saturées (resp. avec des classés non appelés) en t, comparée au taux de saturation des formations non éligibles.

## 5. Sensibilité aux seuils (session 2025)

|   quantile_pression |   seuil_saturation |   eligibles |   S1_10% |   S1_10%_idf |    S2 |   S3_part_couverte |   retrotest_encore_saturees |
|--------------------:|-------------------:|------------:|---------:|-------------:|------:|-------------------:|----------------------------:|
|                0.5  |               0.9  |        5004 |    29859 |         9042 | 40178 |                 18 |                          86 |
|                0.5  |               0.95 |        4183 |    26404 |         8133 | 35378 |                 17 |                          79 |
|                0.5  |               1    |        3069 |    14493 |         4415 | 20020 |                 20 |                          63 |
|                0.75 |               0.9  |        2785 |    13510 |         5753 | 18355 |                 21 |                          88 |
|                0.75 |               0.95 |        2357 |    11764 |         5194 | 15971 |                 20 |                          79 |
|                0.75 |               1    |        1838 |     7687 |         2937 | 10360 |                 23 |                          65 |
|                0.9  |               0.9  |        1184 |     4452 |         2211 |  6014 |                 23 |                          89 |
|                0.9  |               0.95 |        1014 |     3838 |         1955 |  5116 |                 21 |                          79 |
|                0.9  |               1    |         835 |     2803 |         1353 |  3749 |                 24 |                          70 |

Lecture : le VOLUME de places dépend fortement des seuils (facteur ~10) — il ne faut donc pas en citer un seul chiffre. La part couvrable par redéploiement et la persistance de la saturation sont, elles, robustes.

## Limites

- Aucune modélisation du comportement des candidats ni des réallocations en chaîne (il faudrait les vœux individuels, accessibles via le CASD).
- `non_appeles` est une borne haute de la demande non satisfaite : un candidat non appelé ici peut être admis ailleurs.
- Les listes d'appel communes ne permettent pas de calculer `non_appeles` : S2 les ignore.
- Le coût (enseignants, locaux) n'est pas chiffré.