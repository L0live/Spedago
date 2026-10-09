# parcoursup_2020.csv

- Lignes : **12,760**
- Colonnes : **115**
- Colonnes UAI détectées : ['cod_uai']
- Valeurs de `session` : ['2020']
- Lignes dupliquées : 0
- Doublons sur `cod_uai` : 9007 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 1 | 2020 | 2020 | 2020 |
| `contrat_etab` | txt | 0.0 | 4 |  |  | Public, Privé enseignement supérieur, Privé hors contrat |
| `cod_uai` | txt | 0.0 | 3753 |  |  | 0031121C, 0440984F, 0751719L |
| `g_ea_lib_vx` | txt | 0.0 | 3395 |  |  | Université Clermont Auvergne - Antenne de Vichy - UFR STAPS, Université de Nante |
| `dep` | num | 0.0 | 103 | 1 | 987 | 03, 44, 75 |
| `dep_lib` | txt | 0.0 | 103 |  |  | Allier, Loire-Atlantique, Paris |
| `region_etab_aff` | txt | 0.0 | 20 |  |  | Auvergne-Rhône-Alpes, Pays de la Loire, Ile-de-France |
| `acad_mies` | txt | 0.0 | 32 |  |  | Clermont-Ferrand, Nantes, Paris |
| `select_form` | txt | 0.0 | 2 |  |  | formation non selec, formation selective |
| `fili` | txt | 0.0 | 11 |  |  | Licence, Licence_Las, PASS |
| `lib_comp_voe_ins` | txt | 0.0 | 11125 |  |  | Université Clermont Auvergne - Antenne de Vichy - UFR STAPS - Licence - Sciences |
| `form_lib_voe_acc` | txt | 0.0 | 50 |  |  | Licence - Sciences - technologies - santé, Licence - Arts-lettres-langues, Licen |
| `regr_forma` | txt | 96.0 | 53 |  |  | Institut Paul Bocuse, South Champagne Business School, Concours Puissance Alpha |
| `fil_lib_voe_acc` | txt | 0.0 | 517 |  |  | Sciences et Techniques des Activités Physiques et Sportives, Sciences pour l'ing |
| `detail_forma` | txt | 73.4 | 2410 |  |  | Passerelle Kiné, Physique-Chimie-Géosciences-Sciences de l'ingénieur : Sciences  |
| `lien_form_psup` | txt | 1.4 | 12580 |  |  | https://dossier.parcoursup.fr/Candidat/carte?ACTION=2&g_ti_cod=23471&g_ta_cod=23 |
| `g_olocalisation_des_formations` | txt | 1.4 | 4930 |  |  | 46.1196, 3.42528, 47.236, -1.55534, 48.8452, 2.39666 |
| `capa_fin` | num | 0.0 | 359 | 1 | 3400 | 45.0, 60.0, 20.0 |
| `voe_tot` | num | 0.0 | 2820 | 0 | 1.627e+04 | 973, 1219, 129 |
| `voe_tot_f` | num | 0.0 | 2024 | 0 | 1.012e+04 | 524, 350, 99 |
| `nb_voe_pp` | num | 0.0 | 2779 | 0 | 1.627e+04 | 973, 1200, 115 |
| `nb_voe_pp_internat` | num | 93.4 | 483 | 0 | 4599 | 88.0, 0.0, 431.0 |
| `nb_voe_pp_bg` | num | 0.0 | 1947 | 0 | 1.491e+04 | 747, 850, 66 |
| `nb_voe_pp_bg_brs` | num | 0.0 | 606 | 0 | 2382 | 72, 119, 9 |
| `nb_voe_pp_bt` | num | 0.0 | 905 | 0 | 2553 | 47, 62, 3 |
| `nb_voe_pp_bt_brs` | num | 0.0 | 410 | 0 | 1159 | 7, 14, 0 |
| `nb_voe_pp_bp` | num | 0.0 | 590 | 0 | 1446 | 3, 2, 7 |
| `nb_voe_pp_bp_brs` | num | 0.0 | 335 | 0 | 671 | 1, 0, 2 |
| `nb_voe_pp_at` | num | 0.0 | 1244 | 0 | 6209 | 176, 286, 39 |
| `nb_voe_pc` | num | 0.0 | 474 | 0 | 1755 | 0, 19, 14 |
| `nb_voe_pc_bg` | num | 0.0 | 194 | 0 | 792 | 0, 3, 7 |
| `nb_voe_pc_bt` | num | 0.0 | 169 | 0 | 1090 | 0, 61, 6 |
| `nb_voe_pc_bp` | num | 0.0 | 134 | 0 | 543 | 0, 52, 1 |
| `nb_voe_pc_at` | num | 0.0 | 318 | 0 | 979 | 0, 16, 11 |
| `nb_cla_pp` | num | 0.0 | 2368 | 0 | 1.497e+04 | 973, 1200, 115 |
| `nb_cla_pc` | num | 0.0 | 283 | 0 | 933 | 0, 13, 14 |
| `nb_cla_pp_internat` | num | 93.4 | 222 | 0 | 3733 | 25.0, 0.0, 211.0 |
| `nb_cla_pp_pasinternat` | num | 93.4 | 559 | 0 | 4084 | 127.0, 544.0, 402.0 |
| `nb_cla_pp_bg` | num | 0.0 | 1734 | 0 | 1.234e+04 | 747, 850, 66 |
| `nb_cla_pp_bg_brs` | num | 0.0 | 549 | 0 | 2382 | 72, 119, 9 |
| `nb_cla_pp_bt` | num | 0.0 | 735 | 0 | 1855 | 47, 62, 3 |
| `nb_cla_pp_bt_brs` | num | 0.0 | 319 | 0 | 693 | 7, 14, 0 |
| `nb_cla_pp_bp` | num | 0.0 | 467 | 0 | 1446 | 3, 2, 7 |
| `nb_cla_pp_bp_brs` | num | 0.0 | 252 | 0 | 671 | 1, 0, 2 |
| `nb_cla_pp_at` | num | 0.0 | 1088 | 0 | 4870 | 176, 286, 39 |
| `prop_tot` | num | 0.0 | 1448 | 0 | 5297 | 83, 674, 102 |
| `acc_tot` | num | 0.0 | 492 | 0 | 1589 | 45, 53, 18 |
| `acc_tot_f` | num | 0.0 | 353 | 0 | 1109 | 23, 8, 10 |
| `acc_pp` | num | 0.0 | 456 | 0 | 1530 | 45, 46, 13 |
| `acc_pc` | num | 0.0 | 151 | 0 | 350 | 0, 7, 5 |
| `acc_debutpp` | num | 0.0 | 256 | 0 | 887 | 23.0, 1.0, 2.0 |
| `acc_datebac` | num | 0.0 | 420 | 0 | 1526 | 44.0, 46.0, 13.0 |
| `acc_finpp` | num | 0.0 | 448 | 0 | 1526 | 45.0, 46.0, 16.0 |
| `acc_internat` | num | 93.4 | 65 | 0 | 141 | 14.0, 0.0, 48.0 |
| `acc_brs` | num | 0.0 | 162 | 0 | 341 | 3, 7, 0 |
| `acc_neobac` | num | 0.0 | 409 | 0 | 1401 | 45, 34, 9 |
| `acc_bg` | num | 0.0 | 371 | 0 | 1401 | 45, 31, 8 |
| `acc_bt` | num | 0.0 | 106 | 0 | 173 | 0, 3, 1 |
| `acc_bp` | num | 0.0 | 62 | 0 | 128 | 0, 1, 17 |
| `acc_at` | num | 0.0 | 215 | 0 | 482 | 0, 19, 9 |
| `acc_mention_nonrenseignee` | num | 0.0 | 16 | 0 | 26 | 0, 1, 3 |
| `acc_sansmention` | num | 0.0 | 209 | 0 | 423 | 0, 20, 4 |
| `acc_ab` | num | 0.0 | 203 | 0 | 477 | 9, 11, 2 |
| `acc_b` | num | 0.0 | 171 | 0 | 597 | 25, 3, 1 |
| `acc_tb` | num | 0.0 | 167 | 0 | 865 | 11, 0, 2 |
| `acc_bg_mention` | num | 0.0 | 310 | 0 | 1386 | 45, 13, 4 |
| `acc_bt_mention` | num | 0.0 | 82 | 0 | 124 | 0, 1, 5 |
| `acc_bp_mention` | num | 0.0 | 49 | 0 | 66 | 0, 1, 10 |
| `acc_term` | num | 52.8 | 39 | 0 | 50 | 0.0, 3.0, 6.0 |
| `acc_term_f` | num | 52.8 | 24 | 0 | 25 | 0.0, 3.0, 1.0 |
| `acc_aca_orig` | num | 0.0 | 340 | 0 | 1032 | 43, 29, 1 |
| `acc_aca_orig_idf` | num | 0.0 | 363 | 0 | 1218 | 43, 29, 8 |
| `pct_acc_debutpp` | num | 0.5 | 2189 | 0 | 100 | 51.11, 1.89, 11.11 |
| `pct_acc_datebac` | num | 0.5 | 2094 | 0 | 100 | 97.78, 86.79, 72.22 |
| `pct_acc_finpp` | num | 0.5 | 1618 | 0 | 100 | 100.0, 86.79, 88.89 |
| `pct_f` | num | 0.5 | 2428 | 0 | 100 | 51.11, 15.09, 55.56 |
| `pct_aca_orig` | num | 1.2 | 1854 | 0 | 100 | 95.56, 85.29, 11.11 |
| `pct_aca_orig_idf` | num | 1.2 | 1719 | 0 | 100 | 95.56, 85.29, 88.89 |
| `pct_etab_orig` | num | 52.9 | 551 | 0 | 100 | 0.0, 30.0, 37.5 |
| `pct_bours` | num | 1.2 | 1606 | 0 | 100 | 6.67, 20.59, 0.0 |
| `pct_neobac` | num | 0.5 | 2142 | 0 | 100 | 100.0, 64.15, 50.0 |
| `pct_mention_nonrenseignee` | num | 1.2 | 457 | 0 | 100 | 0.0, 1.1111111111111112, 0.7832898172323759 |
| `pct_sansmention` | num | 1.2 | 1730 | 0 | 100 | 0.0, 58.82352941176471, 44.44444444444444 |
| `pct_ab` | num | 1.2 | 1680 | 0 | 100 | 20.0, 32.35294117647059, 22.22222222222222 |
| `pct_b` | num | 1.2 | 1710 | 0 | 100 | 55.55555555555556, 8.823529411764707, 11.11111111111111 |
| `pct_tb` | num | 1.2 | 1593 | 0 | 100 | 24.444444444444443, 0.0, 22.22222222222222 |
| `pct_bg` | num | 1.2 | 1746 | 0 | 100 | 100.0, 91.17647058823528, 88.88888888888889 |
| `pct_bg_mention` | num | 1.2 | 1863 | 0 | 100 | 100.0, 38.24, 44.44 |
| `pct_bt` | num | 1.2 | 1621 | 0 | 100 | 0.0, 8.823529411764707, 25.0 |
| `pct_bt_mention` | num | 1.2 | 1362 | 0 | 100 | 0.0, 2.94, 5.56 |
| `pct_bp` | num | 1.2 | 1212 | 0 | 100 | 0.0, 11.11111111111111, 18.88888888888889 |
| `pct_bp_mention` | num | 1.2 | 1001 | 0 | 100 | 0.0, 11.11, 2.61 |
| `prop_tot_bg` | num | 0.0 | 1144 | 0 | 4882 | 83.0, 446.0, 56.0 |
| `prop_tot_bg_brs` | num | 0.0 | 350 | 0 | 943 | 9.0, 65.0, 7.0 |
| `prop_tot_bt` | num | 0.0 | 326 | 0 | 1178 | 0.0, 21.0, 3.0 |
| `prop_tot_bt_brs` | num | 0.0 | 144 | 0 | 454 | 0.0, 4.0, 25.0 |
| `prop_tot_bp` | num | 0.0 | 171 | 0 | 829 | 0.0, 5.0, 1.0 |
| `prop_tot_bp_brs` | num | 0.0 | 101 | 0 | 393 | 0.0, 1.0, 15.0 |
| `prop_tot_at` | num | 0.0 | 585 | 0 | 1928 | 0.0, 207.0, 38.0 |
| `lib_grp1` | txt | 1.8 | 28 |  |  | Tous les candidats, Bacheliers technologiques toutes séries, Tous les candidats  |
| `ran_grp1` | num | 1.8 | 1911 | 1 | 1.393e+04 | 90.0, 1933.0, 115.0 |
| `lib_grp2` | txt | 53.3 | 18 |  |  | Tous les candidats sauf les Bac technologiques, Bacheliers technologiques toutes |
| `ran_grp2` | num | 53.3 | 468 | 1 | 8430 | 320.0, 214.0, 68.0 |
| `lib_grp3` | txt | 69.9 | 9 |  |  | Tous les candidats sauf les Bac technologiques et Bac professionnels, Bacheliers |
| `ran_grp3` | num | 69.9 | 224 | 1 | 1.004e+04 | 11.0, 20.0, 59.0 |
| `lib_grp4` | txt | 99.9 | 5 |  |  | Bac S, Bac S Sciences de l'Ingénieur, Bac S SVT/EAT spécialités Math/Physique/IS |
| `ran_grp4` | num | 99.9 | 14 | 89 | 9066 | 89.0, 1771.0, 9066.0 |
| `lib_grp5` | txt | 99.9 | 5 |  |  | Bac S SVT/EAT spécialités Math/Physique/ISN/EAT, Bac S SVT/EAT spécialité SVT, B |
| `ran_grp5` | num | 99.9 | 14 | 19 | 5040 | 3258.0, 335.0, 159.0 |
| `taux_adm_psup` | num | 1.8 | 100 | 1 | 100 | 9.0, 87.0, 100.0 |
| `taux_adm_psup_pro` | num | 8.3 | 97 | 0 | 100 | 0.0, 17.0, 20.0 |
| `taux_adm_psup_gen` | num | 8.3 | 100 | 0 | 100 | 100.0, 78.0, 57.0 |
| `taux_adm_psup_techno` | num | 8.3 | 93 | 0 | 100 | 0.0, 6.0, 36.0 |
| `tri` | txt | 0.0 | 3 |  |  | 1_universités, 2_Lycées, 3_Autres formations |
| `cod_aff_form` | num | 0.0 | 12760 | 2 | 3.07e+04 | 23471, 23843, 24135 |

## Alertes
- `regr_forma` manquant à plus de 50 %
- `detail_forma` manquant à plus de 50 %
- `nb_voe_pp_internat` manquant à plus de 50 %
- `nb_cla_pp_internat` manquant à plus de 50 %
- `nb_cla_pp_pasinternat` manquant à plus de 50 %
- `acc_internat` manquant à plus de 50 %
- `acc_term` manquant à plus de 50 %
- `acc_term_f` manquant à plus de 50 %
- `pct_etab_orig` manquant à plus de 50 %
- `lib_grp2` manquant à plus de 50 %
- `ran_grp2` manquant à plus de 50 %
- `lib_grp3` manquant à plus de 50 %
- `ran_grp3` manquant à plus de 50 %
- `lib_grp4` manquant à plus de 50 %
- `ran_grp4` manquant à plus de 50 %
- `lib_grp5` manquant à plus de 50 %
- `ran_grp5` manquant à plus de 50 %