# Piste B — mutualisation possible des spécialités (1re générale, rentrée 2025)

2,256 lycées géolocalisés (annuaire de l'Éducation nationale). Rayon 20 km, même statut (public avec public, privé avec privé), groupe commun de 4 lycées au plus, envisageable dès 12 élèves estimés.

Demande : estimation BASSE (part des élèves de 1re qui suivent la spécialité, tous lycées confondus) ; entre parenthèses, le nombre de lycées en ouverture commune avec l'estimation HAUTE (part observée là où elle est proposée).

| Spécialité | Lycées qui la proposent | Absente (certain) | Incertaine (masquée) | Taux bas – haut | Accès voisin | Ouverture commune (haute) | Isolés | Élèves de 1re des lycées isolés |
|---|---|---|---|---|---|---|---|---|
| humanites_litterature_et_philosophie | 1253 | 223 | 780 | 17.7% – 18.8% | 205 | 2 (2) | 16 | 557 |
| langues_litterature_et_cultures_etrangeres_et_regionales | 1918 | 117 | 221 | 30.4% – 31.2% | 113 | 0 (0) | 4 | 151 |
| hist_geo_geopolitique_sc_politiques | 2010 | 70 | 176 | 33.5% – 33.9% | 69 | 0 (0) | 1 | 14 |
| sciences_economiques_et_sociales | 2096 | 59 | 101 | 45.4% – 45.9% | 58 | 0 (0) | 1 | 38 |
| mathematiques | 2193 | 3 | 60 | 66.0% – 66.0% | 3 | 0 (0) | 0 | 0 |
| physique_chimie | 2158 | 11 | 87 | 45.6% – 45.6% | 10 | 0 (0) | 1 | 14 |
| sciences_de_la_vie_et_de_la_terre | 2130 | 22 | 104 | 40.2% – 40.2% | 21 | 0 (0) | 1 | 14 |
| sciences_de_l_ingenieur | 288 | 1514 | 454 | 2.8% – 14.0% | 1139 | 27 (90) | 348 | 34,089 |
| numerique_et_sciences_informatiques | 685 | 791 | 780 | 8.9% – 14.9% | 594 | 19 (23) | 178 | 14,928 |
| musique | 67 | 2088 | 101 | 0.3% – 6.9% | 1030 | 0 (613) | 1058 | 150,143 |
| arts_plastiques | 273 | 1561 | 422 | 2.6% – 12.2% | 1108 | 41 (161) | 412 | 44,882 |
| educ_physique_pratique_cult_sportive | 231 | 1943 | 82 | 2.1% – 16.1% | 1134 | 142 (446) | 667 | 81,470 |
| histoire_des_arts | 72 | 2094 | 90 | 0.6% – 11.3% | 904 | 0 (776) | 1190 | 174,867 |
| theatre | 71 | 2041 | 144 | 0.4% – 7.2% | 1081 | 0 (535) | 960 | 134,595 |
| cinema_audiovisuel | 158 | 2033 | 65 | 1.1% – 11.3% | 1059 | 24 (569) | 950 | 128,998 |

## Groupes d'ouverture commune (74)

| specialite                           |   groupes |   lycees |   eleves_estimes |
|:-------------------------------------|----------:|---------:|-----------------:|
| educ_physique_pratique_cult_sportive |        38 |      142 |              599 |
| arts_plastiques                      |        12 |       41 |              202 |
| numerique_et_sciences_informatiques  |         9 |       19 |              194 |
| sciences_de_l_ingenieur              |         8 |       27 |              120 |
| cinema_audiovisuel                   |         6 |       24 |               81 |
| humanites_litterature_et_philosophie |         1 |        2 |               30 |

## Limites

- Absent = zéros explicites ; une case masquée (moins de 5 élèves, ou secret secondaire) laisse le statut incertain pour le lycée lui-même, mais compte comme offre possible pour ses voisins.
- Demande estimée = effectif × taux national (bas ou haut) : ignore les goûts locaux et l'IPS. Le taux bas sous-estime (l'absence d'offre supprime la demande), le taux haut surestime (les lycées qui proposent attirent les élèves intéressés).
- Distance à vol d'oiseau, pas temps de transport. Un groupe commun suppose aussi un enseignant et des horaires alignés.
- Un même lycée peut appartenir à des groupes de spécialités différentes ; les groupes sont choisis de façon gloutonne.
- Bassin de formation inconnu pour 7% des lycées (surtout privés) : la distance remplace le bassin.