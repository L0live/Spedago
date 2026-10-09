# parcoursup_2024.csv

- Lignes : **14,079**
- Colonnes : **118**
- Colonnes UAI détectées : ['cod_uai']
- Valeurs de `session` : ['2024']
- Lignes dupliquées : 0
- Doublons sur `cod_uai` : 10083 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 1 | 2024 | 2024 | 2024 |
| `contrat_etab` | txt | 0.0 | 4 |  |  | Privé enseignement supérieur, Public, Privé sous contrat d'association |
| `cod_uai` | txt | 0.0 | 3996 |  |  | 0791199Z, 0301577B, 0342490X |
| `g_ea_lib_vx` | txt | 0.0 | 3641 |  |  | Facultés libres de l'ouest UCO - Niort, Université de Montpellier, Antenne de Nî |
| `dep` | num | 0.5 | 103 | 1 | 987 | 79.0, 30.0, 34.0 |
| `dep_lib` | txt | 0.0 | 104 |  |  | Deux-sèvres, Gard, Hérault |
| `region_etab_aff` | txt | 0.6 | 18 |  |  | Nouvelle Aquitaine, Occitanie, Provence-Alpes-Côte d'Azur |
| `acad_mies` | txt | 0.0 | 32 |  |  | Poitiers, Montpellier, Aix-Marseille |
| `ville_etab` | txt | 0.0 | 1266 |  |  | Niort, Nîmes, Montpellier |
| `lib_for_voe_ins` | txt | 0.0 | 3138 |  |  | Licence - Sciences de l'éducation et de la formation, Licence - Parcours d'Accès |
| `select_form` | txt | 0.0 | 2 |  |  | formation non sélective, formation sélective |
| `fili` | txt | 0.0 | 11 |  |  | Licence, PASS, Licence_Las |
| `lib_comp_voe_ins` | txt | 0.0 | 11851 |  |  | Facultés libres de l'ouest UCO - Niort - Licence - Sciences de l'éducation et de |
| `form_lib_voe_acc` | txt | 0.0 | 53 |  |  | Licence - Sciences humaines et sociales, Licence - Sciences - technologies - san |
| `fil_lib_voe_acc` | txt | 0.0 | 452 |  |  | Sciences de l'éducation et de la formation, Parcours d'Accès Spécifique Santé (P |
| `detail_forma` | txt | 70.9 | 2805 |  |  | Physique - Mathématiques, Parcours Asie du Sud et Himalaya - Tamoul, Jazz et Mus |
| `g_olocalisation_des_formations` | txt | 0.5 | 5804 |  |  | 46.33037, -0.46114, 43.8212, 4.32081, 43.635, 3.84674 |
| `capa_fin` | num | 0.0 | 352 | 0 | 3400 | 60, 42, 38 |
| `voe_tot` | num | 0.0 | 3076 | 0 | 1.743e+04 | 280, 4179, 2168 |
| `voe_tot_f` | num | 0.0 | 2234 | 0 | 1.142e+04 | 257, 2908, 1427 |
| `nb_voe_pp` | num | 0.0 | 3040 | 0 | 1.743e+04 | 224, 4179, 2168 |
| `nb_voe_pp_internat` | num | 93.0 | 227 | 0 | 2730 | 0.0, 1007.0, 32.0 |
| `nb_voe_pp_bg` | num | 0.0 | 2198 | 0 | 1.598e+04 | 135, 3381, 1710 |
| `nb_voe_pp_bg_brs` | num | 0.0 | 714 | 0 | 2291 | 24, 748, 369 |
| `nb_voe_pp_bt` | num | 0.0 | 942 | 0 | 3740 | 30, 113, 52 |
| `nb_voe_pp_bt_brs` | num | 0.0 | 450 | 0 | 1715 | 8, 39, 21 |
| `nb_voe_pp_bp` | num | 0.0 | 596 | 0 | 1442 | 15, 34, 20 |
| `nb_voe_pp_bp_brs` | num | 0.0 | 345 | 0 | 737 | 3, 16, 8 |
| `nb_voe_pp_at` | num | 0.0 | 1336 | 0 | 6218 | 44, 651, 386 |
| `nb_voe_pc` | num | 0.0 | 380 | 0 | 2202 | 56, 0, 10 |
| `nb_voe_pc_bg` | num | 0.0 | 170 | 0 | 849 | 12, 0, 6 |
| `nb_voe_pc_bt` | num | 0.0 | 119 | 0 | 389 | 5, 0, 1 |
| `nb_voe_pc_bp` | num | 0.0 | 83 | 0 | 239 | 5, 0, 1 |
| `nb_voe_pc_at` | num | 0.0 | 274 | 0 | 1031 | 34, 0, 4 |
| `nb_cla_pp` | num | 0.0 | 2530 | 0 | 1.517e+04 | 224, 4179, 2168 |
| `nb_cla_pc` | num | 0.0 | 265 | 0 | 1039 | 56, 0, 10 |
| `nb_cla_pp_internat` | num | 93.0 | 180 | 0 | 720 | 0.0, 209.0, 14.0 |
| `nb_cla_pp_pasinternat` | num | 93.0 | 667 | 0 | 4794 | 481.0, 331.0, 0.0 |
| `nb_cla_pp_bg` | num | 0.0 | 1950 | 0 | 1.31e+04 | 135, 3381, 1710 |
| `nb_cla_pp_bg_brs` | num | 0.0 | 648 | 0 | 2291 | 24, 748, 369 |
| `nb_cla_pp_bt` | num | 0.0 | 774 | 0 | 2350 | 30, 113, 52 |
| `nb_cla_pp_bt_brs` | num | 0.0 | 329 | 0 | 872 | 8, 39, 21 |
| `nb_cla_pp_bp` | num | 0.0 | 475 | 0 | 1345 | 15, 34, 20 |
| `nb_cla_pp_bp_brs` | num | 0.0 | 250 | 0 | 689 | 3, 16, 8 |
| `nb_cla_pp_at` | num | 0.0 | 1089 | 0 | 6183 | 44, 651, 386 |
| `prop_tot` | num | 0.0 | 1618 | 0 | 5525 | 280, 377, 731 |
| `acc_tot` | num | 0.0 | 456 | 0 | 1482 | 30, 41, 36 |
| `acc_tot_f` | num | 0.0 | 334 | 0 | 1040 | 29, 27, 19 |
| `acc_pp` | num | 0.0 | 435 | 0 | 1373 | 24, 41, 36 |
| `acc_pc` | num | 0.0 | 126 | 0 | 363 | 6, 0, 5 |
| `acc_debutpp` | num | 0.0 | 263 | 0 | 1092 | 24.0, 1.0, 0.0 |
| `acc_datebac` | num | 0.0 | 397 | 0 | 1298 | 25.0, 30.0, 6.0 |
| `acc_finpp` | num | 0.0 | 425 | 0 | 1305 | 29.0, 38.0, 28.0 |
| `acc_internat` | num | 93.0 | 64 | 0 | 141 | 0.0, 82.0, 27.0 |
| `acc_brs` | num | 0.0 | 146 | 0 | 297 | 5, 12, 6 |
| `acc_neobac` | num | 0.0 | 380 | 0 | 1195 | 17, 40, 26 |
| `acc_bg` | num | 0.0 | 353 | 0 | 1113 | 9, 40, 26 |
| `acc_bt` | num | 0.0 | 103 | 0 | 169 | 6, 0, 9 |
| `acc_bp` | num | 0.0 | 52 | 0 | 108 | 2, 0, 5 |
| `acc_at` | num | 0.0 | 202 | 0 | 1075 | 13, 1, 10 |
| `acc_mention_nonrenseignee` | num | 0.0 | 9 | 0 | 13 | 0, 1, 3 |
| `acc_sansmention` | num | 0.0 | 176 | 0 | 316 | 5, 0, 11 |
| `acc_ab` | num | 0.0 | 195 | 0 | 489 | 6, 5, 10 |
| `acc_b` | num | 0.0 | 165 | 0 | 531 | 4, 19, 3 |
| `acc_tb` | num | 0.0 | 124 | 0 | 426 | 2, 15, 5 |
| `acc_tbf` | num | 0.0 | 54 | 0 | 188 | 0.0, 1.0, 2.0 |
| `acc_bg_mention` | num | 0.0 | 287 | 0 | 1013 | 5, 40, 15 |
| `acc_bt_mention` | num | 0.0 | 81 | 0 | 161 | 5, 0, 4 |
| `acc_bp_mention` | num | 0.0 | 44 | 0 | 53 | 2, 0, 4 |
| `acc_term` | num | 55.1 | 37 | 0 | 44 | 3.0, 0.0, 2.0 |
| `acc_term_f` | num | 55.1 | 19 | 0 | 18 | 1.0, 0.0, 3.0 |
| `acc_aca_orig` | num | 0.0 | 299 | 0 | 1083 | 9, 35, 11 |
| `acc_aca_orig_idf` | num | 0.0 | 323 | 0 | 1083 | 9, 35, 11 |
| `pct_acc_debutpp` | num | 0.0 | 101 | 0 | 100 | 80.0, 2.0, 0.0 |
| `pct_acc_datebac` | num | 0.0 | 99 | 0 | 100 | 83.0, 73.0, 17.0 |
| `pct_acc_finpp` | num | 0.0 | 82 | 0 | 100 | 97.0, 93.0, 78.0 |
| `pct_f` | num | 0.0 | 100 | 0 | 100 | 97.0, 66.0, 53.0 |
| `pct_aca_orig` | num | 0.0 | 100 | 0 | 100 | 53.0, 88.0, 42.0 |
| `pct_aca_orig_idf` | num | 0.0 | 100 | 0 | 100 | 53.0, 88.0, 42.0 |
| `pct_etab_orig` | num | 0.0 | 97 | 0 | 100 | 0.0, 14.0, 7.0 |
| `pct_bours` | num | 0.0 | 95 | 0 | 100 | 29.0, 30.0, 23.0 |
| `pct_neobac` | num | 0.0 | 99 | 0 | 100 | 57.0, 98.0, 72.0 |
| `pct_mention_nonrenseignee` | num | 0.0 | 20 | 0 | 50 | 0.0, 1.0, 2.0 |
| `pct_sansmention` | num | 0.0 | 97 | 0 | 100 | 29.0, 0.0, 42.0 |
| `pct_ab` | num | 0.0 | 87 | 0 | 100 | 35.0, 12.0, 38.0 |
| `pct_b` | num | 0.0 | 86 | 0 | 100 | 24.0, 48.0, 12.0 |
| `pct_tb` | num | 0.0 | 88 | 0 | 100 | 12.0, 38.0, 8.0 |
| `pct_tbf` | num | 0.0 | 60 | 0 | 100 | 0.0, 2.0, 1.0 |
| `pct_bg` | num | 0.0 | 100 | 0 | 100 | 53.0, 100.0, 93.0 |
| `pct_bg_mention` | num | 0.0 | 100 | 0 | 100 | 29.0, 100.0, 58.0 |
| `pct_bt` | num | 0.0 | 96 | 0 | 100 | 35.0, 0.0, 5.0 |
| `pct_bt_mention` | num | 0.0 | 98 | 0 | 100 | 29.0, 0.0, 2.0 |
| `pct_bp` | num | 0.0 | 98 | 0 | 100 | 12.0, 0.0, 3.0 |
| `pct_bp_mention` | num | 0.0 | 97 | 0 | 100 | 12.0, 0.0, 2.0 |
| `prop_tot_bg` | num | 0.0 | 1271 | 0 | 5134 | 147.0, 347.0, 571.0 |
| `prop_tot_bg_brs` | num | 0.0 | 374 | 0 | 888 | 26.0, 71.0, 124.0 |
| `prop_tot_bt` | num | 0.0 | 434 | 0 | 641 | 35.0, 0.0, 15.0 |
| `prop_tot_bt_brs` | num | 0.0 | 178 | 0 | 342 | 10.0, 0.0, 7.0 |
| `prop_tot_bp` | num | 0.0 | 199 | 0 | 293 | 20.0, 0.0, 6.0 |
| `prop_tot_bp_brs` | num | 0.0 | 110 | 0 | 191 | 5.0, 0.0, 1.0 |
| `prop_tot_at` | num | 0.0 | 642 | 0 | 1967 | 78.0, 30.0, 139.0 |
| `lib_grp1` | txt | 5.2 | 8 |  |  | Tous les candidats, Autres candidats, Groupe par defaut |
| `ran_grp1` | num | 0.6 | 2346 | 1 | 1.62e+04 | 224.0, 1073.0, 5277.0 |
| `lib_grp2` | txt | 57.0 | 7 |  |  | Bacheliers technologiques toutes series, Bacheliers professionnels toutes series |
| `ran_grp2` | num | 56.4 | 441 | 1 | 1342 | 280.0, 407.0, 18.0 |
| `lib_grp3` | txt | 74.3 | 2 |  |  | Bacheliers professionnels toutes series, Bacheliers technologiques toutes series |
| `ran_grp3` | num | 73.6 | 316 | 1 | 1493 | 13.0, 252.0, 76.0 |
| `list_com` | txt | 0.0 | 2 |  |  | Liste d'appel commune à plusieurs formations, Liste d'appel propre à cette forma |
| `tri` | txt | 0.0 | 3 |  |  | 1_universités, 2_Lycées, 3_Autres formations |
| `cod_aff_form` | num | 0.0 | 14079 | 3 | 4.712e+04 | 31827, 31855, 31856 |
| `detail_forma2` | txt | 94.9 | 89 |  |  | Centre de Ressources, d’Expertise et de Performance Sportive d’Auvergne Rhône-Al |
| `lien_form_psup` | txt | 0.5 | 14006 |  |  | https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_t |
| `taux_acces_ens` | num | 0.6 | 100 | 1 | 100 | 100.0, 20.0, 83.0 |
| `part_acces_gen` | num | 0.0 | 101 | 0 | 100 | 72.0, 100.0, 97.0 |
| `part_acces_tec` | num | 0.0 | 88 | 0 | 100 | 18.0, 0.0, 3.0 |
| `part_acces_pro` | num | 0.0 | 99 | 0 | 100 | 9.0, 0.0, 1.0 |
| `etablissement_id_paysage` | txt | 52.4 | 486 |  |  | 7zzqc, evv7S, xJdyB |
| `composante_id_paysage` | txt | 98.3 | 97 |  |  | i2Fja, TDaGr, ysdqj |

## Alertes
- `detail_forma` manquant à plus de 50 %
- `nb_voe_pp_internat` manquant à plus de 50 %
- `nb_cla_pp_internat` manquant à plus de 50 %
- `nb_cla_pp_pasinternat` manquant à plus de 50 %
- `acc_internat` manquant à plus de 50 %
- `acc_term` manquant à plus de 50 %
- `acc_term_f` manquant à plus de 50 %
- `lib_grp2` manquant à plus de 50 %
- `ran_grp2` manquant à plus de 50 %
- `lib_grp3` manquant à plus de 50 %
- `ran_grp3` manquant à plus de 50 %
- `detail_forma2` manquant à plus de 50 %
- `etablissement_id_paysage` manquant à plus de 50 %
- `composante_id_paysage` manquant à plus de 50 %