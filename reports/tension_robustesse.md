# Piste A — contrôles de robustesse (session 2025 sauf mention)

Périmètre : public + privé sous contrat, hors CNED et capacités nulles : 13,026 formations, 670,772 places, 69,412 places vacantes.

Exclus (privé hors contrat + privé enseignement supérieur) : 1,206 formations, 23,920 places vacantes.

## 1-3. Décalage offre/demande selon la granularité (seuils 95 % / 80 %)

| Niveau | Cellules | Cellules avec coexistence | Vacantes des sous-remplies en coexistence | Réaffectables (≤ classés non appelés à côté) |
|---|---|---|---|---|
| académie × filière (analyse initiale) | 302 | 201 | 50,903 (73%) | 46,523 |
| académie × filière × spécialité | 5,250 | 762 | 25,959 (37%) | 19,189 |
| département × filière × spécialité | 7,988 | 551 | 14,903 (21%) | 10,080 |

Lecture : « réaffectables » ne compte une place vacante que si, dans la même cellule, une formation saturée a des candidats classés jamais appelés (borne haute : ces candidats ont pu être admis ailleurs ; les listes d'appel communes, sans rang exploitable, sont ignorées → borne basse sur ce point).

## 4. Sensibilité aux seuils (niveau académie × filière × spécialité)

| Saturée ≥ | Sous-remplie < | Vacantes en coexistence | Réaffectables |
|---|---|---|---|
| 90% | 70% | 23,241 | 16,597 |
| 90% | 80% | 28,800 | 21,276 |
| 90% | 90% | 34,942 | 26,222 |
| 95% | 70% | 21,020 | 15,021 |
| 95% | 80% | 25,959 | 19,189 |
| 95% | 90% | 31,625 | 23,706 |
| 100% | 70% | 16,839 | 11,681 |
| 100% | 80% | 21,060 | 15,212 |
| 100% | 90% | 25,595 | 18,843 |

## 5. Attrition du panel et persistance de la saturation

|   session_t |   sortie_si_saturee |   sortie_si_non_saturee |   persistance_survivantes |   persistance_borne_basse |
|------------:|--------------------:|------------------------:|--------------------------:|--------------------------:|
|        2021 |               0.035 |                   0.063 |                     0.623 |                     0.601 |
|        2022 |               0.029 |                   0.062 |                     0.673 |                     0.653 |
|        2023 |               0.032 |                   0.059 |                     0.733 |                     0.71  |
|        2024 |               0.026 |                   0.044 |                     0.771 |                     0.751 |
|        2025 |               0.031 |                   0.034 |                     0.774 |                     0.75  |

Borne basse : les formations disparues sont comptées comme non saturées. Si l'écart avec la persistance des survivantes est faible, l'attrition ne biaise pas la conclusion.

## 6. Comparabilité de la pression entre filières

La méthodologie officielle définit `nb_voe_pp` comme un effectif de CANDIDATS par formation. Mais quand un vœu regroupe plusieurs formations (listes communes : IFSI, concours d'écoles, licences regroupées), un candidat compte dans chacune : la pression y est mécaniquement gonflée. Ne comparer la pression qu'à l'intérieur d'une filière.

| fili_harmo        |   formations |   part_listes_communes |   candidats_par_place_median |
|:------------------|-------------:|-----------------------:|-----------------------------:|
| Autre formation   |         1662 |                  0.065 |                       10.345 |
| BTS               |         5247 |                  0     |                        9.25  |
| BUT               |          820 |                  0     |                       15.504 |
| CPGE              |          986 |                  0     |                       21.604 |
| EFTS              |          179 |                  0.24  |                        4.233 |
| Ecole d'Ingénieur |          210 |                  0.538 |                       28.362 |
| Ecole de Commerce |            6 |                  0     |                        4.341 |
| IFSI              |          331 |                  0.979 |                       42.777 |
| Licence           |         2798 |                  0.185 |                        7.636 |
| Licence_Las       |          500 |                  0.496 |                       20.375 |
| PASS              |          287 |                  0.986 |                       49.414 |
