# Piste B — contrôles de robustesse

## 1. Simulation neutre : parts nationales naïves vs corrigées (rentrée 2025)

Naïf : parts calculées sur les cases publiées (sous-représente les combinaisons rares). Corrigé : masse masquée de chaque lycée × sexe répartie entre ses cases masquées.

**1re**

| taille   |   sim_naif |   observe |   sim_corrige |   ratio_naif |   ratio_corrige |
|:---------|-----------:|----------:|--------------:|-------------:|----------------:|
| <60      |      0.434 |     0.716 |         0.756 |        1.649 |           0.947 |
| 60-119   |      0.269 |     0.527 |         0.482 |        1.961 |           1.093 |
| 120-199  |      0.176 |     0.401 |         0.345 |        2.279 |           1.163 |
| 200-299  |      0.116 |     0.315 |         0.206 |        2.716 |           1.524 |
| 300+     |      0.08  |     0.213 |         0.115 |        2.678 |           1.858 |

**tle**

| taille   |   sim_naif |   observe |   sim_corrige |   ratio_naif |   ratio_corrige |
|:---------|-----------:|----------:|--------------:|-------------:|----------------:|
| <60      |      0.6   |     1     |         0.788 |        1.667 |           1.269 |
| 60-119   |      0.244 |     0.562 |         0.434 |        2.301 |           1.294 |
| 120-199  |      0.131 |     0.335 |         0.24  |        2.551 |           1.398 |
| 200-299  |      0.085 |     0.23  |         0.132 |        2.706 |           1.747 |
| 300+     |      0.06  |     0.155 |         0.069 |        2.596 |           2.251 |

## 2-3. Régressions à effets fixes de taille (déciles), erreurs regroupées par académie, 3 rentrées

Coefficients pour un écart-type d'IPS ou d'éloignement ; `prive` = privé sous contrat vs public ; `lpo` = lycée polyvalent vs LEGT (contrôle du type de lycée).

| niveau   | variable_expliquee   | variable      |   coef_2021 |   coef_2023 |   coef_2025 |   t_2021 |   t_2023 |   t_2025 |
|:---------|:---------------------|:--------------|------------:|------------:|------------:|---------:|---------:|---------:|
| 1re      | nb_spe_visibles      | eloignement_z |       0.076 |       0.108 |       0.068 |    2.853 |    5.019 |    1.931 |
| 1re      | nb_spe_visibles      | ips_z         |      -0.16  |      -0.251 |      -0.189 |   -4.373 |   -6.449 |   -3.318 |
| 1re      | nb_spe_visibles      | lpo           |      -0.189 |      -0.135 |      -0.198 |   -3.3   |   -2.733 |   -3.469 |
| 1re      | nb_spe_visibles      | prive         |      -0.063 |       0.143 |      -0.009 |   -0.784 |    1.585 |   -0.112 |
| 1re      | part_non_publiee     | eloignement_z |       0.02  |       0.009 |       0.007 |    3.63  |    2.334 |    1.106 |
| 1re      | part_non_publiee     | ips_z         |      -0.013 |      -0.013 |      -0.026 |   -2.464 |   -2.478 |   -4.248 |
| 1re      | part_non_publiee     | lpo           |       0.003 |       0.01  |       0.013 |    0.32  |    1.136 |    1.887 |
| 1re      | part_non_publiee     | prive         |       0.019 |       0.007 |       0.018 |    1.93  |    0.493 |    1.458 |
| tle      | nb_spe_visibles      | eloignement_z |       0.098 |       0.097 |       0.062 |    3.302 |    4.074 |    1.74  |
| tle      | nb_spe_visibles      | ips_z         |      -0.208 |      -0.218 |      -0.251 |   -3.697 |   -3.868 |   -4.683 |
| tle      | nb_spe_visibles      | lpo           |      -0.134 |      -0.071 |      -0.115 |   -2.599 |   -1.594 |   -3.01  |
| tle      | nb_spe_visibles      | prive         |       0.074 |       0.014 |      -0.044 |    0.829 |    0.173 |   -0.554 |
| tle      | part_non_publiee     | eloignement_z |       0.015 |       0.016 |       0.018 |    3.012 |    2.638 |    3.5   |
| tle      | part_non_publiee     | ips_z         |      -0.026 |      -0.024 |      -0.024 |   -5.6   |   -6.906 |   -6.972 |
| tle      | part_non_publiee     | lpo           |       0.014 |       0.007 |       0.009 |    1.965 |    0.834 |    1.303 |
| tle      | part_non_publiee     | prive         |       0.001 |       0.011 |       0.014 |    0.114 |    0.984 |    1.6   |

Lecture : |t| > 2 ≈ significatif à 5 %. Un signe stable sur les 3 rentrées renforce la conclusion.

## 4. Offre de chaque spécialité selon l'IPS, à taille égale — 1re 2025

Effet d'un écart-type d'IPS sur la probabilité qu'un lycée propose la spécialité (points de probabilité), effets fixes de taille, erreurs regroupées par académie.

| specialite                                               |   part_lycees_proposant |   effet_ips_1_ecart_type |      t |
|:---------------------------------------------------------|------------------------:|-------------------------:|-------:|
| educ_physique_pratique_cult_sportive                     |                   0.102 |                   -0.037 | -4.499 |
| humanites_litterature_et_philosophie                     |                   0.554 |                   -0.035 | -2.83  |
| sciences_de_l_ingenieur                                  |                   0.127 |                   -0.023 | -4.01  |
| cinema_audiovisuel                                       |                   0.07  |                   -0.019 | -4.367 |
| langues_litterature_et_cultures_etrangeres_et_regionales |                   0.847 |                   -0.015 | -1.349 |
| numerique_et_sciences_informatiques                      |                   0.305 |                   -0.012 | -1.575 |
| theatre                                                  |                   0.032 |                   -0.011 | -2.404 |
| sciences_de_la_vie_et_de_la_terre                        |                   0.942 |                   -0.01  | -2.488 |
| musique                                                  |                   0.029 |                   -0.01  | -3.654 |
| arts_plastiques                                          |                   0.121 |                   -0.009 | -1.65  |
| histoire_des_arts                                        |                   0.032 |                   -0.009 | -4.06  |
| physique_chimie                                          |                   0.954 |                   -0     | -0.112 |
| mathematiques                                            |                   0.969 |                    0.001 |  0.43  |
| hist_geo_geopolitique_sc_politiques                      |                   0.888 |                    0.005 |  0.993 |
| sciences_economiques_et_sociales                         |                   0.925 |                    0.01  |  2.067 |

## 4. Offre de chaque spécialité selon l'IPS, à taille égale — tle 2025

Effet d'un écart-type d'IPS sur la probabilité qu'un lycée propose la spécialité (points de probabilité), effets fixes de taille, erreurs regroupées par académie.

| specialite                                               |   part_lycees_proposant |   effet_ips_1_ecart_type |      t |
|:---------------------------------------------------------|------------------------:|-------------------------:|-------:|
| langues_litterature_et_cultures_etrangeres_et_regionales |                   0.665 |                   -0.067 | -3.986 |
| sciences_de_la_vie_et_de_la_terre                        |                   0.842 |                   -0.059 | -3.741 |
| humanites_litterature_et_philosophie                     |                   0.307 |                   -0.043 | -4.069 |
| educ_physique_pratique_cult_sportive                     |                   0.082 |                   -0.035 | -6.321 |
| numerique_et_sciences_informatiques                      |                   0.148 |                   -0.027 | -3.602 |
| sciences_de_l_ingenieur_et_sc_physiques                  |                   0.07  |                   -0.023 | -4.955 |
| cinema_audiovisuel                                       |                   0.059 |                   -0.018 | -3.778 |
| arts_plastiques                                          |                   0.091 |                    0.003 |  0.398 |
| mathematiques                                            |                   0.936 |                    0.004 |  1.474 |
| hist_geo_geopolitique_sc_politiques                      |                   0.824 |                    0.007 |  1.709 |
| sciences_economiques_et_sociales                         |                   0.898 |                    0.009 |  2.284 |
| physique_chimie                                          |                   0.914 |                    0.011 |  3.022 |
