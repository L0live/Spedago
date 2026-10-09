# Piste C — Mon Master : accès selon le profil (sessions 2024 et 2025)

Source : open data MESR (une ligne = formation × session). Taux = propositions / candidats (phases principale + complémentaire).

## 1. Vue d'ensemble

|   session |   formations |   places |   candidatures |   propositions |   acceptations |
|----------:|-------------:|---------:|---------------:|---------------:|---------------:|
|      2024 |         8090 |   176933 |        2266706 |         446078 |         139563 |
|      2025 |         8167 |   177297 |        2643131 |         453220 |         144885 |

« candidatures » = somme sur les formations des candidats en phase principale (un candidat compte dans chaque formation demandée).

## 2. Taux de proposition national par profil (toutes formations confondues)

| profil                                    |   2024 |   2025 |
|:------------------------------------------|-------:|-------:|
| Autre inscription                         |  0.134 |  0.107 |
| BUT 3e année                              |  0.111 |  0.101 |
| L3 générale                               |  0.212 |  0.19  |
| Licence pro                               |  0.095 |  0.088 |
| Déjà en master                            |  0.16  |  0.136 |
| Non inscrit en 2024-25 / reprise d'études |  0.131 |  0.112 |

Attention : ces taux mélangent l'effet du profil et celui des formations demandées. La section 3 compare à formation identique.

## 3. Écarts à formation identique

Formations où les deux profils ont au moins 10 candidats ; moyenne pondérée ; IC 95 % par bootstrap sur les formations.

| comparaison      |   formations_x_sessions |   taux_a |   taux_b |   ecart_points |   ic95_bas |   ic95_haut |   part_formations_a_superieur |
|:-----------------|------------------------:|---------:|---------:|---------------:|-----------:|------------:|------------------------------:|
| etab − hors_etab |                   12540 |    0.312 |    0.136 |         17.677 |     17.275 |      18.097 |                         0.857 |
| etab − lg3       |                   12548 |    0.334 |    0.198 |         13.581 |     13.255 |      13.95  |                         0.823 |
| but3 − lg3       |                    6862 |    0.112 |    0.165 |         -5.353 |     -5.739 |      -4.946 |                         0.378 |
| lp3 − lg3        |                    3609 |    0.071 |    0.14  |         -6.915 |     -7.392 |      -6.468 |                         0.29  |
| master − lg3     |                    9311 |    0.13  |    0.179 |         -4.921 |     -5.156 |      -4.676 |                         0.247 |
| noninscri − lg3  |                   13260 |    0.116 |    0.194 |         -7.833 |     -8.024 |      -7.633 |                         0.209 |

Biais de composition : les internes sont surtout des L3 générales, les externes comptent plus de LP, BUT et non-inscrits (taux plus faibles). Les données ne croisent pas établissement × profil. La ligne « etab − lg3 » compare les internes à TOUS les L3 générales (internes compris) : c'est une borne BASSE de la prime aux internes à profil comparable.

Lecture : un écart positif signifie que le premier profil reçoit plus souvent une proposition que le second, dans les mêmes formations. Ce n'est PAS un effet causal du profil : les candidats internes ou en BUT peuvent différer par leurs résultats, leur projet, ou ne candidater que là où ils ont de bonnes chances.

## 4. Prime aux candidats internes par secteur disciplinaire

| secteur                                                                       |   formations_x_sessions |   taux_a |   taux_b |   ecart_points |   ic95_bas |   ic95_haut |
|:------------------------------------------------------------------------------|------------------------:|---------:|---------:|---------------:|-----------:|------------:|
| Génie civil                                                                   |                      46 |    0.564 |    0.083 |         48.097 |     42.177 |      54.288 |
| Théologie catholique                                                          |                       3 |    0.882 |    0.469 |         41.271 |     19.302 |      52.206 |
| Littérature générale et comparée                                              |                       7 |    0.735 |    0.381 |         35.405 |     27.067 |      44.027 |
| Mathématiques                                                                 |                     254 |    0.465 |    0.181 |         28.421 |     25.11  |      32.092 |
| Physique et chimie                                                            |                      20 |    0.478 |    0.204 |         27.455 |     19.646 |      35.18  |
| Pluridisciplinaire sciences                                                   |                      48 |    0.451 |    0.186 |         26.48  |     20.868 |      32.288 |
| STAPS                                                                         |                     305 |    0.399 |    0.144 |         25.557 |     22.916 |      28.073 |
| Physique                                                                      |                     154 |    0.546 |    0.3   |         24.58  |     21.091 |      27.948 |
| Histoire                                                                      |                     445 |    0.503 |    0.26  |         24.346 |     22.268 |      26.434 |
| Informatique                                                                  |                     483 |    0.299 |    0.057 |         24.134 |     21.955 |      26.135 |
| Archéologie, ethnologie, préhistoire, anthropologie                           |                      77 |    0.581 |    0.34  |         24.095 |     20.115 |      28.42  |
| Langues et littératures étrangères                                            |                     217 |    0.591 |    0.354 |         23.752 |     20.771 |      26.945 |
| Sciences de l'univers, de la Terre, de l'espace, de la mer                    |                     180 |    0.435 |    0.198 |         23.672 |     20.672 |      26.443 |
| Philosophie, épistémologie                                                    |                     100 |    0.614 |    0.378 |         23.642 |     19.968 |      27.111 |
| Mécanique, génie mécanique, ingénierie mécanique                              |                     163 |    0.375 |    0.145 |         23.045 |     19.535 |      26.61  |
| Sciences de l'éducation                                                       |                    1388 |    0.586 |    0.356 |         22.96  |     21.22  |      24.662 |
| Administration économique et sociale                                          |                      41 |    0.331 |    0.102 |         22.92  |     18.5   |      27.515 |
| Électronique, génie électrique, électronique - électrotechnique - automatique |                     190 |    0.287 |    0.069 |         21.803 |     18.718 |      25.042 |
| Géographie                                                                    |                     153 |    0.392 |    0.185 |         20.707 |     18.002 |      23.186 |
| Arts                                                                          |                     283 |    0.393 |    0.191 |         20.193 |     16.638 |      24.203 |
| Chimie                                                                        |                     260 |    0.37  |    0.169 |         20.148 |     17.642 |      22.872 |
| Mathématique et informatique                                                  |                      28 |    0.31  |    0.112 |         19.807 |     14.917 |      26.069 |
| Mathématiques appliquées et sciences sociales                                 |                      28 |    0.285 |    0.099 |         18.637 |     12.157 |      26.815 |
| Sciences juridiques                                                           |                    1724 |    0.294 |    0.108 |         18.607 |     17.728 |      19.561 |
| Génie des procédés, matériaux                                                 |                      41 |    0.318 |    0.139 |         17.884 |     12.865 |      22.724 |
| Sciences de la vie, biologie, santé                                           |                     976 |    0.318 |    0.142 |         17.643 |     16.534 |      18.684 |
| Pluridisciplinaire sciences fondamentales et applications                     |                     131 |    0.277 |    0.103 |         17.428 |     14.699 |      21.022 |
| Technologie et sciences industrielles                                         |                      82 |    0.217 |    0.057 |         15.976 |     11.956 |      20.472 |
| Pluridisciplinaire lettres, sciences du langage, arts                         |                      73 |    0.507 |    0.348 |         15.945 |     10.918 |      21.499 |
| Psychologie, sciences cognitives                                              |                     423 |    0.203 |    0.045 |         15.837 |     14.897 |      16.981 |
| Aménagement                                                                   |                     348 |    0.308 |    0.155 |         15.288 |     13.647 |      16.845 |
| Langues et littératures françaises                                            |                     114 |    0.522 |    0.373 |         14.905 |     10.656 |      18.618 |
| Sciences du langage, linguistique                                             |                     168 |    0.444 |    0.297 |         14.622 |     11.714 |      17.681 |
| Pluridisciplinaire droit, sciences économiques, AES                           |                     190 |    0.204 |    0.06  |         14.423 |     12.405 |      16.316 |
| Français, langue étrangère                                                    |                      28 |    0.426 |    0.287 |         13.876 |      8.863 |      20.995 |
| Sciences politiques                                                           |                     197 |    0.209 |    0.07  |         13.846 |     11.279 |      17.036 |
| Pluridisciplinaire sciences économiques et gestion                            |                      45 |    0.292 |    0.158 |         13.482 |      9.681 |      17.042 |
| Sciences économiques                                                          |                     533 |    0.253 |    0.126 |         12.706 |     11.292 |      14.177 |
| Langues étrangères appliquées                                                 |                     323 |    0.318 |    0.198 |         12     |     10.465 |      13.706 |
| Sciences de gestion                                                           |                    1342 |    0.168 |    0.048 |         11.994 |     11.141 |      12.832 |
| Pluridisciplinaire droit, sciences politiques                                 |                       4 |    0.288 |    0.178 |         11.012 |      7.554 |      18.191 |
| Pluridisciplinaire lettres, langues, sciences humaines                        |                     219 |    0.278 |    0.175 |         10.339 |      7.79  |      13.13  |
| Sociologie, démographie                                                       |                     157 |    0.336 |    0.233 |         10.25  |      7.85  |      13.031 |
| Pluridisciplinaire sciences humaines et sociales                              |                     190 |    0.263 |    0.175 |          8.849 |      6.902 |      10.821 |
| Sciences de l'information et la communication                                 |                     347 |    0.203 |    0.121 |          8.154 |      6.372 |       9.875 |
| Sciences religieuses                                                          |                      12 |    0.46  |    0.407 |          5.282 |     -4.746 |      16.024 |

## 5. Mentions les plus et les moins accessibles (≥ 10 formations, 2024-2025 cumulés)

**Les moins accessibles**

| mention                                                              |   formations |   candidats |   propositions |   taux_prop |
|:---------------------------------------------------------------------|-------------:|------------:|---------------:|------------:|
| RELATIONS INTERNATIONALES                                            |           17 |       39154 |           1595 |       0.041 |
| GESTION DE PRODUCTION, LOGISTIQUE, ACHATS                            |           48 |       55530 |           2488 |       0.045 |
| QUALITE, HYGIENE, SECURITE                                           |           14 |       17477 |            849 |       0.049 |
| PSYCHOLOGIE CLINIQUE, PSYCHOPATHOLOGIE ET PSYCHOLOGIE DE LA SANTE    |           40 |       52453 |           2563 |       0.049 |
| COMPTABILITE-CONTROLE-AUDIT                                          |           81 |      107370 |           5330 |       0.05  |
| GESTION DES RESSOURCES HUMAINES                                      |           75 |       83410 |           4171 |       0.05  |
| CONTROLE DE GESTION ET AUDIT ORGANISATIONNEL                         |           61 |       67397 |           3404 |       0.051 |
| FINANCE                                                              |           68 |      100247 |           5310 |       0.053 |
| PSYCHOLOGIE                                                          |          121 |      164194 |           8955 |       0.055 |
| ENTREPRENEURIAT ET MANAGEMENT DE PROJETS                             |           39 |       28429 |           1702 |       0.06  |
| RESEAUX ET TELECOMMUNICATION                                         |           20 |       12308 |            743 |       0.06  |
| MANAGEMENT DES PME-PMI                                               |           12 |        4503 |            295 |       0.066 |
| DROIT NOTARIAL                                                       |           37 |       48825 |           3454 |       0.071 |
| METHODES INFORMATIQUES APPLIQUEES A LA GESTION DES ENTREPRISES-MIAGE |           43 |       44023 |           3158 |       0.072 |
| MARKETING, VENTE                                                     |          150 |      120719 |           8833 |       0.073 |

**Les plus accessibles**

| mention                                                                        |   formations |   candidats |   propositions |   taux_prop |
|:-------------------------------------------------------------------------------|-------------:|------------:|---------------:|------------:|
| THEOLOGIE CATHOLIQUE                                                           |           10 |         224 |            149 |       0.665 |
| HISTOIRE, CIVILISATIONS, PATRIMOINE                                            |           77 |       17597 |           8114 |       0.461 |
| MONDES ANCIENS                                                                 |           15 |        1679 |            774 |       0.461 |
| ARTS DE LA SCENE ET DU SPECTACLE VIVANT                                        |           20 |        4835 |           2187 |       0.452 |
| LANGUES, LITTERATURES ET CIVILISATIONS ETRANGERES ET REGIONALES                |          274 |       33667 |          14944 |       0.444 |
| MUSICOLOGIE                                                                    |           29 |        3434 |           1522 |       0.443 |
| INFORMATION ET MEDIATION SCIENTIFIQUE ET TECHNIQUE                             |           11 |        2043 |            899 |       0.44  |
| METIERS DE L'ENSEIGNEMENT, DE L'EDUCATION ET DE LA FORMATION (MEEF), 1ER DEGRE |          184 |      271362 |         118645 |       0.437 |
| LETTRES                                                                        |           76 |       24777 |          10399 |       0.42  |
| PHYSIQUE FONDAMENTALE ET APPLICATIONS                                          |           53 |       14809 |           6154 |       0.416 |

## Limites

- Taux historiques par profil, pas des probabilités individuelles : dossier, notes et projet ne sont pas observés.
- Un candidat compte dans chaque formation demandée ; les candidats qui se désistent avant toute proposition restent au dénominateur.
- Hors champ de la plateforme : étudiants « Études en France », redoublants, admissions de droit, certains masters internationaux.
- Deux sessions seulement (2024, 2025) : les taux d'une formation peuvent varier fortement d'une année à l'autre.
- Les comparaisons de profils ne sont pas causales (sélection des candidatures).
## 6. Prévision : le taux d'une année annonce-t-il celui de l'année suivante ?

Taux 2024 utilisés pour prévoir 2025. « Corrigé » = moyenne a posteriori bayésienne empirique (k + κ·m)/(n + κ), avec une loi a priori Bêta par mention × profil estimée sur 2024 seulement (pas de fuite vers 2025). Erreurs pondérées par le nombre de candidats 2025.

| couples                       |     n |   erreur_abs_brut_pts |   erreur_abs_corrige_pts |   spearman_brut |   spearman_corrige |
|:------------------------------|------:|----------------------:|-------------------------:|----------------:|-------------------:|
| tous                          | 26175 |                 5.857 |                    5.637 |           0.867 |              0.875 |
| moins de 30 candidats en 2024 |  3906 |                10.782 |                    9.087 |           0.785 |              0.801 |
| 30 candidats ou plus en 2024  | 22269 |                 5.673 |                    5.509 |           0.886 |              0.889 |

**Calibration** (moyenne prévue vs moyenne observée en 2025, par tranche de prévision)

| tranche        |   n_brut |   prevu_brut |   observe_brut |   n_corrige |   prevu_corrige |   observe_corrige |
|:---------------|---------:|-------------:|---------------:|------------:|----------------:|------------------:|
| (-0.001, 0.05] |     6422 |        0.017 |          0.032 |        5798 |           0.024 |             0.029 |
| (0.05, 0.1]    |     3352 |        0.075 |          0.076 |        3758 |           0.074 |             0.071 |
| (0.1, 0.2]     |     4634 |        0.149 |          0.139 |        4918 |           0.147 |             0.137 |
| (0.2, 0.3]     |     3613 |        0.249 |          0.223 |        3726 |           0.248 |             0.225 |
| (0.3, 0.5]     |     4782 |        0.393 |          0.335 |        4853 |           0.39  |             0.343 |
| (0.5, 1.01]    |     3372 |        0.659 |          0.537 |        3122 |           0.636 |             0.55  |

Part restante de l'écart : hausse générale des candidatures en 2025 (+17 % en phase principale), qui fait baisser tous les taux.