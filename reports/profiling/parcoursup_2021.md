# parcoursup_2021.csv

- Lignes : **13,396**
- Colonnes : **118**
- Colonnes UAI détectées : ['cod_uai']
- Valeurs de `session` : ['2021']
- Lignes dupliquées : 0
- Doublons sur `cod_uai` : 9527 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 1 | 2021 | 2021 | 2021 |
| `contrat_etab` | txt | 0.0 | 4 |  |  | Public, Privé enseignement supérieur, Privé hors contrat |
| `cod_uai` | txt | 0.0 | 3869 |  |  | 0751719L, 0753605L, 0801344B |
| `g_ea_lib_vx` | txt | 0.0 | 3505 |  |  | Université Sorbonne Nouvelle Paris 3, FAC LIBRE THEOLOGIE PROTESTANT, Université |
| `dep` | num | 0.0 | 104 | 1 | 987 | 75, 80, 77 |
| `dep_lib` | txt | 0.0 | 104 |  |  | Paris, Somme, Seine-et-Marne |
| `region_etab_aff` | txt | 0.0 | 21 |  |  | Ile-de-France, Hauts-de-France, Bretagne |
| `acad_mies` | txt | 0.0 | 32 |  |  | Paris, Amiens, Créteil |
| `ville_etab` | txt | 0.0 | 1229 |  |  | Paris  5e  Arrondissement, Paris 14e  Arrondissement, Amiens |
| `select_form` | txt | 0.0 | 2 |  |  | formation non sélective, formation sélective |
| `fili` | txt | 0.0 | 11 |  |  | Licence, BUT, Licence_Las |
| `lib_comp_voe_ins` | txt | 0.0 | 11421 |  |  | Université Sorbonne Nouvelle Paris 3 - Licence - Langues, littératures & civilis |
| `form_lib_voe_acc` | txt | 0.0 | 51 |  |  | Licence - Arts-lettres-langues, Licence - Sciences humaines et sociales, BUT - P |
| `lib_for_voe_ins` | txt | 0.0 | 3448 |  |  | Licence - Langues, littératures & civilisations étrangères et régionales - Parco |
| `fil_lib_voe_acc` | txt | 0.0 | 521 |  |  | Langues, littératures & civilisations étrangères et régionales, Théologie, Philo |
| `detail_forma` | txt | 68.0 | 2944 |  |  | Arabe - Mineure Hébreu, Arabe Grands débutants (Licence en 4 ans), Espagnol |
| `detail_forma2` | txt | 95.3 | 81 |  |  | Concours SESAME, Campus de l'excellence sportive de Bretagne, Regroupement Auver |
| `g_olocalisation_des_formations` | txt | 1.1 | 5306 |  |  | 48.8452, 2.39666, 48.8342, 2.3375, 49.90428, 2.29963 |
| `capa_fin` | num | 0.0 | 362 | 0 | 3400 | 6, 50, 90 |
| `voe_tot` | num | 0.0 | 2964 | 0 | 1.819e+04 | 20, 320, 330 |
| `voe_tot_f` | num | 0.0 | 2166 | 0 | 1.055e+04 | 14, 232, 270 |
| `nb_voe_pp` | num | 0.0 | 2954 | 0 | 1.819e+04 | 15, 320, 207 |
| `nb_voe_pp_internat` | num | 92.8 | 549 | 0 | 5818 | 195.0, 1638.0, 94.0 |
| `nb_voe_pp_bg` | num | 0.0 | 2073 | 0 | 1.648e+04 | 4, 90, 147 |
| `nb_voe_pp_bg_brs` | num | 0.0 | 663 | 0 | 2411 | 0, 37, 30 |
| `nb_voe_pp_bt` | num | 0.0 | 948 | 0 | 3203 | 1, 31, 9 |
| `nb_voe_pp_bt_brs` | num | 0.0 | 449 | 0 | 1132 | 1, 20, 2 |
| `nb_voe_pp_bp` | num | 0.0 | 652 | 0 | 1658 | 0, 18, 2 |
| `nb_voe_pp_bp_brs` | num | 0.0 | 390 | 0 | 836 | 0, 11, 1 |
| `nb_voe_pp_at` | num | 0.0 | 1371 | 0 | 6493 | 10, 181, 49 |
| `nb_voe_pc` | num | 0.0 | 397 | 0 | 1901 | 5, 0, 123 |
| `nb_voe_pc_bg` | num | 0.0 | 154 | 0 | 628 | 0, 40, 4 |
| `nb_voe_pc_bt` | num | 0.0 | 128 | 0 | 527 | 1, 0, 8 |
| `nb_voe_pc_bp` | num | 0.0 | 101 | 0 | 420 | 0, 11, 5 |
| `nb_voe_pc_at` | num | 0.0 | 270 | 0 | 1189 | 4, 0, 64 |
| `nb_cla_pp` | num | 0.0 | 2482 | 0 | 1.521e+04 | 15, 314, 207 |
| `nb_cla_pc` | num | 0.0 | 261 | 0 | 1828 | 5, 0, 117 |
| `nb_cla_pp_internat` | num | 92.8 | 487 | 0 | 5818 | 174.0, 308.0, 74.0 |
| `nb_cla_pp_pasinternat` | num | 92.8 | 648 | 0 | 5209 | 246.0, 621.0, 96.0 |
| `nb_cla_pp_bg` | num | 0.0 | 1868 | 0 | 1.249e+04 | 4, 90, 147 |
| `nb_cla_pp_bg_brs` | num | 0.0 | 607 | 0 | 2411 | 0, 37, 30 |
| `nb_cla_pp_bt` | num | 0.0 | 766 | 0 | 1885 | 1, 31, 9 |
| `nb_cla_pp_bt_brs` | num | 0.0 | 334 | 0 | 747 | 1, 20, 2 |
| `nb_cla_pp_bp` | num | 0.0 | 495 | 0 | 1404 | 0, 18, 2 |
| `nb_cla_pp_bp_brs` | num | 0.0 | 289 | 0 | 674 | 0, 11, 1 |
| `nb_cla_pp_at` | num | 0.0 | 1163 | 0 | 5050 | 10, 175, 49 |
| `prop_tot` | num | 0.0 | 1493 | 0 | 5078 | 18, 186, 303 |
| `acc_tot` | num | 0.0 | 462 | 0 | 1569 | 6, 48, 88 |
| `acc_tot_f` | num | 0.0 | 335 | 0 | 1127 | 4, 32, 71 |
| `acc_pp` | num | 0.0 | 450 | 0 | 1547 | 3, 48, 44 |
| `acc_pc` | num | 0.0 | 128 | 0 | 1012 | 3, 0, 44 |
| `acc_debutpp` | num | 0.0 | 247 | 0 | 1176 | 1.0, 5.0, 17.0 |
| `acc_datebac` | num | 0.0 | 401 | 0 | 1417 | 3.0, 41.0, 44.0 |
| `acc_finpp` | num | 0.0 | 442 | 0 | 1504 | 3.0, 46.0, 74.0 |
| `acc_internat` | num | 92.8 | 61 | 0 | 141 | 0.0, 1.0, 9.0 |
| `acc_brs` | num | 0.0 | 153 | 0 | 334 | 0, 8, 16 |
| `acc_neobac` | num | 0.0 | 402 | 0 | 1283 | 1, 22, 61 |
| `acc_bg` | num | 0.0 | 365 | 0 | 1179 | 0, 14, 46 |
| `acc_bt` | num | 0.0 | 110 | 0 | 167 | 1, 5, 7 |
| `acc_bp` | num | 0.0 | 59 | 0 | 128 | 0, 3, 8 |
| `acc_at` | num | 0.0 | 207 | 0 | 1027 | 5, 26, 27 |
| `acc_mention_nonrenseignee` | num | 0.0 | 20 | 0 | 27 | 0, 1, 2 |
| `acc_sansmention` | num | 0.0 | 174 | 0 | 363 | 1, 10, 27 |
| `acc_ab` | num | 0.0 | 212 | 0 | 532 | 0, 10, 23 |
| `acc_b` | num | 0.0 | 180 | 0 | 556 | 0, 2, 6 |
| `acc_tb` | num | 0.0 | 129 | 0 | 444 | 0, 4, 1 |
| `acc_tbf` | num | 0.0 | 59 | 0 | 275 | 0.0, 1.0, 12.0 |
| `acc_bg_mention` | num | 0.0 | 311 | 0 | 1168 | 0, 6, 26 |
| `acc_bt_mention` | num | 0.0 | 91 | 0 | 162 | 0, 3, 1 |
| `acc_bp_mention` | num | 0.0 | 46 | 0 | 54 | 0, 3, 6 |
| `acc_term` | num | 53.6 | 39 | 0 | 46 | 8.0, 10.0, 0.0 |
| `acc_term_f` | num | 53.6 | 23 | 0 | 25 | 7.0, 10.0, 0.0 |
| `acc_aca_orig` | num | 0.0 | 319 | 0 | 1062 | 0, 2, 11 |
| `acc_aca_orig_idf` | num | 0.0 | 339 | 0 | 1124 | 1, 17, 53 |
| `pct_acc_debutpp` | num | 0.8 | 2125 | 0 | 100 | 16.67, 10.42, 19.32 |
| `pct_acc_datebac` | num | 0.8 | 2153 | 0 | 100 | 50.0, 85.42, 66.67 |
| `pct_acc_finpp` | num | 0.8 | 1514 | 0 | 100 | 50.0, 95.83, 84.09 |
| `pct_f` | num | 0.8 | 935 | 0 | 100 | 66.6875, 80.6875, 50.0 |
| `pct_aca_orig` | num | 1.7 | 828 | 0 | 100 | 0.0, 9.099609375, 18.0 |
| `pct_aca_orig_idf` | num | 1.7 | 757 | 0 | 100 | 100.0, 77.296875, 86.890625 |
| `pct_etab_orig` | num | 53.7 | 411 | 0 | 100 | 36.3984375, 37.0, 0.0 |
| `pct_bours` | num | 1.7 | 630 | 0 | 100 | 0.0, 36.3984375, 26.19921875 |
| `pct_neobac` | num | 0.8 | 793 | 0 | 100 | 16.69921875, 45.796875, 69.296875 |
| `pct_mention_nonrenseignee` | num | 1.7 | 117 | 0 | 100 | 0.0, 1.599853515625, 0.29998779296875 |
| `pct_sansmention` | num | 1.7 | 700 | 0 | 100 | 100.0, 45.5, 44.296875 |
| `pct_ab` | num | 1.7 | 671 | 0 | 100 | 0.0, 45.5, 37.6953125 |
| `pct_b` | num | 1.7 | 676 | 0 | 100 | 0.0, 9.099609375, 9.798828125 |
| `pct_tb` | num | 1.7 | 588 | 0 | 100 | 0.0, 6.6, 2.1 |
| `pct_tbf` | num | 1.7 | 250 | 0 | 100 | 0.0, 0.3, 5.6 |
| `pct_bg` | num | 1.7 | 813 | 0 | 100 | 0.0, 63.59375, 75.390625 |
| `pct_bg_mention` | num | 1.7 | 880 | 0 | 100 | 0.0, 27.296875, 42.59375 |
| `pct_bt` | num | 1.7 | 649 | 0 | 100 | 100.0, 22.69921875, 11.5 |
| `pct_bt_mention` | num | 1.7 | 584 | 0 | 100 | 0.0, 13.599609375, 1.599853515625 |
| `pct_bp` | num | 1.7 | 559 | 0 | 100 | 0.0, 13.599609375, 13.099609375 |
| `pct_bp_mention` | num | 1.7 | 483 | 0 | 100 | 0.0, 13.599609375, 9.798828125 |
| `prop_tot_bg` | num | 0.0 | 1171 | 0 | 4166 | 4.0, 65.0, 177.0 |
| `prop_tot_bg_brs` | num | 0.0 | 345 | 0 | 744 | 0.0, 21.0, 38.0 |
| `prop_tot_bt` | num | 0.0 | 355 | 0 | 638 | 2.0, 16.0, 17.0 |
| `prop_tot_bt_brs` | num | 0.0 | 146 | 0 | 364 | 1.0, 14.0, 6.0 |
| `prop_tot_bp` | num | 0.0 | 189 | 0 | 465 | 0.0, 13.0, 10.0 |
| `prop_tot_bp_brs` | num | 0.0 | 105 | 0 | 228 | 0.0, 7.0, 8.0 |
| `prop_tot_at` | num | 0.0 | 611 | 0 | 1824 | 12.0, 92.0, 96.0 |
| `lib_grp1` | txt | 6.0 | 12 |  |  | Tous les candidats, Tous les candidats sauf les Bac technologiques, Groupe par d |
| `ran_grp1` | num | 6.0 | 1953 | 1 | 1.584e+04 | 14.0, 240.0, 207.0 |
| `lib_grp2` | txt | 55.1 | 6 |  |  | Bacheliers technologiques toutes séries, Bacheliers professionnels toutes séries |
| `ran_grp2` | num | 55.1 | 387 | 1 | 775 | 165.0, 268.0, 168.0 |
| `lib_grp3` | txt | 71.3 | 4 |  |  | Bacheliers professionnels toutes séries, Bacheliers technologiques toutes séries |
| `ran_grp3` | num | 71.3 | 255 | 1 | 578 | 23.0, 32.0, 12.0 |
| `list_com` | txt | 0.0 | 2 |  |  | Liste d'appel propre à cette formation, Liste d'appel commune à plusieurs format |
| `tri` | txt | 0.0 | 3 |  |  | 1_universités, 2_Lycées, 3_Autres formations |
| `cod_aff_form` | num | 0.0 | 13396 | 2 | 3.505e+04 | 24023, 24029, 24037 |
| `lien_form_psup` | txt | 1.1 | 13252 |  |  | https://dossier.parcoursup.fr/Candidat/carte?g_ti_cod=24023&g_ta_cod=24023, http |
| `taux_adm_psup` | num | 1.6 | 100 | 1 | 100 | 93.0, 75.0, 100.0 |
| `taux_adm_psup_gen` | num | 0.8 | 100 | 0 | 100 | 50.0, 58.0, 72.0 |
| `taux_adm_psup_techno` | num | 0.8 | 97 | 0 | 100 | 33.0, 19.0, 11.0 |
| `taux_adm_psup_pro` | num | 0.8 | 97 | 0 | 100 | 17.0, 21.0, 7.0 |
| `etablissement_id_paysage` | txt | 53.1 | 481 |  |  | 8k883, l4myZ, 8j5s2 |
| `composante_id_paysage` | txt | 98.7 | 86 |  |  | Nn3jE, B8z9z, 7ZCCO |

## Alertes
- `detail_forma` manquant à plus de 50 %
- `detail_forma2` manquant à plus de 50 %
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
- `etablissement_id_paysage` manquant à plus de 50 %
- `composante_id_paysage` manquant à plus de 50 %