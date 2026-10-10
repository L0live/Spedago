# ival_lycees_gt.csv

- Lignes : **32,485**
- Colonnes : **88**
- Colonnes UAI détectées : ['uai']
- Valeurs de `annee` : ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
- Lignes dupliquées : 0
- Doublons sur `uai` : 29939 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `annee` | num | 0.0 | 14 | 2012 | 2025 | 2018, 2019, 2020 |
| `uai` | txt | 0.0 | 2546 |  |  | 0470063N, 0640017W, 0640055M |
| `libelle_uai` | txt | 0.0 | 2521 |  |  | LYCEE NOTRE DAME LA COMPASSION, LYCEE EXPERIMENTAL A.MALRAUX, LYCEE LOUIS BARTHO |
| `secteur` | txt | 0.0 | 2 |  |  | privé sous contrat, public |
| `code_commune` | num | 0.0 | 1191 | 1004 | 9.913e+04 | 47157, 64122, 64445 |
| `libelle_commune` | txt | 0.0 | 1419 |  |  | MARMAE, BIARRITZ, PAU |
| `code_departement` | num | 0.0 | 101 | 1 | 976 | 47, 64, 79 |
| `libelle_departement` | txt | 0.0 | 101 |  |  | LOT-ET-GARONNE, PYRENEES-ATLANTIQUES, DEUX-SEVRES |
| `libelle_academie` | txt | 0.0 | 30 |  |  | BORDEAUX, POITIERS, LIMOGES |
| `code_region` | num | 0.0 | 18 | 1 | 94 | 75, 76, 84 |
| `libelle_region` | txt | 0.0 | 18 |  |  | NOUVELLE-AQUITAINE, OCCITANIE, AUVERGNE-RHONE-ALPES |
| `presents_total` | num | 0.0 | 689 | 1 | 1026 | 91, 225, 445 |
| `taux_reu_total` | num | 0.0 | 63 | 0 | 100 | 95.0, 99.0, 100.0 |
| `va_reu_total` | num | 1.4 | 65 | -78 | 36 | 2.0, 0.0, 5.0 |
| `taux_acces_2nde` | num | 0.5 | 95 | 0 | 100 | 69.0, 76.0, 83.0 |
| `va_acces_2nde` | num | 1.8 | 91 | -77 | 46 | -10.0, 0.0, 1.0 |
| `taux_men_total` | num | 35.7 | 98 | 0 | 100 | 37.0, 47.0, 62.0 |
| `va_men_total` | num | 36.7 | 75 | -39 | 46 | -9.0, -5.0, 1.0 |
| `presents_l` | num | 50.4 | 136 | 1 | 161 | 14.0, 24.0, 65.0 |
| `presents_es` | num | 45.2 | 196 | 1 | 236 | 9.0, 68.0, 130.0 |
| `presents_s` | num | 41.6 | 304 | 3 | 346 | 22.0, 111.0, 180.0 |
| `presents_gnle` | num | 66.4 | 472 | 6 | 654 | 136.0, 174.0, 313.0 |
| `presents_sti2d` | num | 75.7 | 196 | 1 | 271 | 133.0, 75.0, 21.0 |
| `presents_std2a` | num | 96.1 | 73 | 1 | 87 | 33.0, 19.0, 30.0 |
| `presents_stmg` | num | 45.8 | 212 | 1 | 480 | 18.0, 70.0, 32.0 |
| `presents_stl` | num | 88.4 | 126 | 2 | 164 | 22.0, 20.0, 41.0 |
| `presents_st2s` | num | 80.5 | 150 | 1 | 170 | 28.0, 36.0, 23.0 |
| `presents_s2tmd` | num | 99.0 | 30 | 1 | 31 | 7.0, 21.0, 6.0 |
| `presents_sthr` | num | 97.1 | 97 | 2 | 113 | 20.0, 38.0, 41.0 |
| `taux_reu_l` | num | 50.4 | 65 | 0 | 100 | 86.0, 88.0, 92.0 |
| `taux_reu_es` | num | 45.2 | 71 | 0 | 100 | 89.0, 97.0, 95.0 |
| `taux_reu_s` | num | 41.6 | 69 | 0 | 100 | 95.0, 96.0, 100.0 |
| `taux_reu_gnle` | num | 66.4 | 44 | 44 | 100 | 85.0, 99.0, 98.0 |
| `taux_reu_sti2d` | num | 75.7 | 52 | 0 | 100 | 86.0, 84.0, 100.0 |
| `taux_reu_std2a` | num | 96.1 | 32 | 50 | 100 | 100.0, 95.0, 97.0 |
| `taux_reu_stmg` | num | 45.8 | 62 | 0 | 100 | 100.0, 97.0, 80.0 |
| `taux_reu_stl` | num | 88.4 | 51 | 42 | 100 | 100.0, 88.0, 89.0 |
| `taux_reu_st2s` | num | 80.5 | 61 | 0 | 100 | 96.0, 97.0, 100.0 |
| `taux_reu_s2tmd` | num | 99.0 | 17 | 0 | 100 | 100.0, 95.0, 93.0 |
| `taux_reu_sthr` | num | 97.1 | 41 | 32 | 100 | 85.0, 95.0, 93.0 |
| `va_reu_l` | num | 54.0 | 80 | -63 | 44 | -5.0, -3.0, -4.0 |
| `va_reu_es` | num | 46.2 | 82 | -60 | 49 | 6.0, -1.0, 2.0 |
| `va_reu_s` | num | 42.3 | 74 | -60 | 52 | 2.0, 0.0, 5.0 |
| `va_reu_gnle` | num | 66.9 | 41 | -19 | 36 | -4.0, 1.0, 0.0 |
| `va_reu_sti2d` | num | 76.2 | 59 | -34 | 27 | -8.0, -6.0, 4.0 |
| `va_reu_std2a` | num | 96.2 | 26 | -24 | 8 | 2.0, -4.0, 0.0 |
| `va_reu_stmg` | num | 46.8 | 65 | -48 | 34 | 8.0, 6.0, 1.0 |
| `va_reu_stl` | num | 89.2 | 57 | -37 | 30 | 3.0, 5.0, -8.0 |
| `va_reu_st2s` | num | 80.8 | 57 | -35 | 28 | -1.0, 3.0, -8.0 |
| `va_reu_s2tmd` | num | 99.3 | 15 | -10 | 7 | -2.0, -4.0, 2.0 |
| `va_reu_sthr` | num | 97.4 | 43 | -35 | 15 | -9.0, -1.0, 6.0 |
| `eff_2nde` | num | 0.2 | 716 | 0 | 927 | 99.0, 221.0, 433.0 |
| `eff_1ere` | num | 0.2 | 702 | 0 | 915 | 103.0, 251.0, 447.0 |
| `eff_term` | num | 21.4 | 695 | 0 | 1040 | 85.0, 229.0, 435.0 |
| `taux_acces_1ere` | num | 0.2 | 77 | 0 | 100 | 87.0, 91.0, 90.0 |
| `taux_acces_term` | num | 21.4 | 50 | 24 | 100 | 96.0, 97.0, 98.0 |
| `va_acces_1ere` | num | 1.5 | 77 | -79 | 44 | -4.0, -2.0, -1.0 |
| `va_acces_term` | num | 22.6 | 51 | -51 | 38 | 2.0, 0.0, 1.0 |
| `taux_men_l` | num | 77.8 | 96 | 0 | 100 | 57.0, 54.0, 100.0 |
| `taux_men_es` | num | 75.2 | 99 | 0 | 100 | 22.0, 32.0, 58.0 |
| `taux_men_s` | num | 73.8 | 99 | 0 | 100 | 45.0, 50.0, 72.0 |
| `taux_men_gnle` | num | 66.4 | 89 | 9 | 100 | 54.0, 72.0, 77.0 |
| `taux_men_sti2d` | num | 83.0 | 98 | 0 | 100 | 31.0, 35.0, 76.0 |
| `taux_men_std2a` | num | 97.1 | 77 | 11 | 100 | 94.0, 89.0, 70.0 |
| `taux_men_stmg` | num | 64.9 | 98 | 0 | 100 | 39.0, 51.0, 81.0 |
| `taux_men_stl` | num | 92.2 | 91 | 0 | 100 | 68.0, 65.0, 46.0 |
| `taux_men_st2s` | num | 87.2 | 92 | 0 | 100 | 25.0, 67.0, 61.0 |
| `taux_men_s2tmd` | num | 99.3 | 44 | 0 | 100 | 71.0, 86.0, 67.0 |
| `taux_men_sthr` | num | 98.2 | 82 | 4 | 100 | 45.0, 63.0, 39.0 |
| `va_men_l` | num | 79.7 | 96 | -47 | 56 | 14.0, 8.0, -4.0 |
| `va_men_es` | num | 75.6 | 90 | -50 | 53 | -7.0, -5.0, -4.0 |
| `va_men_s` | num | 74.0 | 85 | -40 | 56 | -4.0, -10.0, 4.0 |
| `va_men_gnle` | num | 66.9 | 66 | -37 | 46 | 11.0, -2.0, -3.0 |
| `va_men_sti2d` | num | 83.3 | 84 | -40 | 56 | -22.0, -6.0, 18.0 |
| `va_men_std2a` | num | 97.2 | 63 | -42 | 28 | 24.0, 13.0, 6.0 |
| `va_men_stmg` | num | 65.6 | 97 | -47 | 56 | 0.0, 11.0, 26.0 |
| `va_men_stl` | num | 92.8 | 83 | -50 | 51 | 5.0, 9.0, -15.0 |
| `va_men_st2s` | num | 87.5 | 81 | -41 | 52 | -28.0, 9.0, 5.0 |
| `va_men_s2tmd` | num | 99.5 | 45 | -61 | 21 | 12.0, -10.0, 11.0 |
| `va_men_sthr` | num | 98.4 | 61 | -30 | 42 | -15.0, 12.0, -8.0 |
| `nb_mentions_tb_avecf_g` | num | 79.7 | 40 | 1 | 83 | 2.0, 3.0, 13.0 |
| `nb_mentions_tb_sansf_g` | num | 73.5 | 132 | 1 | 200 | 11.0, 19.0, 55.0 |
| `nb_mentions_b_g` | num | 73.1 | 158 | 1 | 201 | 14.0, 43.0, 87.0 |
| `nb_mentions_ab_g` | num | 73.0 | 167 | 1 | 196 | 47.0, 60.0, 85.0 |
| `nb_mentions_tb_avecf_t` | num | 98.2 | 6 | 1 | 7 | 1.0, 2.0, 3.0 |
| `nb_mentions_tb_sansf_t` | num | 85.7 | 21 | 1 | 27 | 2.0, 1.0, 3.0 |
| `nb_mentions_b_t` | num | 78.1 | 55 | 1 | 62 | 10.0, 6.0, 11.0 |
| `nb_mentions_ab_t` | num | 77.4 | 97 | 1 | 110 | 16.0, 15.0, 14.0 |

## Alertes
- valeurs négatives dans `va_reu_total`
- valeurs négatives dans `va_acces_2nde`
- valeurs négatives dans `va_men_total`
- `presents_l` manquant à plus de 50 %
- `presents_gnle` manquant à plus de 50 %
- `presents_sti2d` manquant à plus de 50 %
- `presents_std2a` manquant à plus de 50 %
- `presents_stl` manquant à plus de 50 %
- `presents_st2s` manquant à plus de 50 %
- `presents_s2tmd` manquant à plus de 50 %
- `presents_sthr` manquant à plus de 50 %
- `taux_reu_l` manquant à plus de 50 %
- `taux_reu_gnle` manquant à plus de 50 %
- `taux_reu_sti2d` manquant à plus de 50 %
- `taux_reu_std2a` manquant à plus de 50 %
- `taux_reu_stl` manquant à plus de 50 %
- `taux_reu_st2s` manquant à plus de 50 %
- `taux_reu_s2tmd` manquant à plus de 50 %
- `taux_reu_sthr` manquant à plus de 50 %
- valeurs négatives dans `va_reu_l`
- `va_reu_l` manquant à plus de 50 %
- valeurs négatives dans `va_reu_es`
- valeurs négatives dans `va_reu_s`
- valeurs négatives dans `va_reu_gnle`
- `va_reu_gnle` manquant à plus de 50 %
- valeurs négatives dans `va_reu_sti2d`
- `va_reu_sti2d` manquant à plus de 50 %
- valeurs négatives dans `va_reu_std2a`
- `va_reu_std2a` manquant à plus de 50 %
- valeurs négatives dans `va_reu_stmg`
- valeurs négatives dans `va_reu_stl`
- `va_reu_stl` manquant à plus de 50 %
- valeurs négatives dans `va_reu_st2s`
- `va_reu_st2s` manquant à plus de 50 %
- valeurs négatives dans `va_reu_s2tmd`
- `va_reu_s2tmd` manquant à plus de 50 %
- valeurs négatives dans `va_reu_sthr`
- `va_reu_sthr` manquant à plus de 50 %
- valeurs négatives dans `va_acces_1ere`
- valeurs négatives dans `va_acces_term`
- `taux_men_l` manquant à plus de 50 %
- `taux_men_es` manquant à plus de 50 %
- `taux_men_s` manquant à plus de 50 %
- `taux_men_gnle` manquant à plus de 50 %
- `taux_men_sti2d` manquant à plus de 50 %
- `taux_men_std2a` manquant à plus de 50 %
- `taux_men_stmg` manquant à plus de 50 %
- `taux_men_stl` manquant à plus de 50 %
- `taux_men_st2s` manquant à plus de 50 %
- `taux_men_s2tmd` manquant à plus de 50 %
- `taux_men_sthr` manquant à plus de 50 %
- valeurs négatives dans `va_men_l`
- `va_men_l` manquant à plus de 50 %
- valeurs négatives dans `va_men_es`
- `va_men_es` manquant à plus de 50 %
- valeurs négatives dans `va_men_s`
- `va_men_s` manquant à plus de 50 %
- valeurs négatives dans `va_men_gnle`
- `va_men_gnle` manquant à plus de 50 %
- valeurs négatives dans `va_men_sti2d`
- `va_men_sti2d` manquant à plus de 50 %
- valeurs négatives dans `va_men_std2a`
- `va_men_std2a` manquant à plus de 50 %
- valeurs négatives dans `va_men_stmg`
- `va_men_stmg` manquant à plus de 50 %
- valeurs négatives dans `va_men_stl`
- `va_men_stl` manquant à plus de 50 %
- valeurs négatives dans `va_men_st2s`
- `va_men_st2s` manquant à plus de 50 %
- valeurs négatives dans `va_men_s2tmd`
- `va_men_s2tmd` manquant à plus de 50 %
- valeurs négatives dans `va_men_sthr`
- `va_men_sthr` manquant à plus de 50 %
- `nb_mentions_tb_avecf_g` manquant à plus de 50 %
- `nb_mentions_tb_sansf_g` manquant à plus de 50 %
- `nb_mentions_b_g` manquant à plus de 50 %
- `nb_mentions_ab_g` manquant à plus de 50 %
- `nb_mentions_tb_avecf_t` manquant à plus de 50 %
- `nb_mentions_tb_sansf_t` manquant à plus de 50 %
- `nb_mentions_b_t` manquant à plus de 50 %
- `nb_mentions_ab_t` manquant à plus de 50 %