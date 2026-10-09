# parcoursup_2022.csv

- Lignes : **13,644**
- Colonnes : **118**
- Colonnes UAI détectées : ['cod_uai']
- Valeurs de `session` : ['2022']
- Lignes dupliquées : 0
- Doublons sur `cod_uai` : 9718 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 1 | 2022 | 2022 | 2022 |
| `contrat_etab` | txt | 0.0 | 4 |  |  | Public, Privé enseignement supérieur, Privé sous contrat d'association |
| `cod_uai` | txt | 0.0 | 3926 |  |  | 0693521C, 0720916E, 0730858L |
| `g_ea_lib_vx` | txt | 0.0 | 3570 |  |  | I.U.T LUMIERE Lyon 2, Le Mans Université, Université Savoie Mont Blanc - Chambér |
| `dep` | num | 0.0 | 104 | 1 | 987 | 69, 72, 73 |
| `dep_lib` | txt | 0.0 | 104 |  |  | Rhône, Sarthe, Savoie |
| `region_etab_aff` | txt | 0.0 | 21 |  |  | Auvergne-Rhône-Alpes, Pays de la Loire, Ile-de-France |
| `acad_mies` | txt | 0.0 | 32 |  |  | Lyon, Nantes, Grenoble |
| `ville_etab` | txt | 0.0 | 1248 |  |  | Bron, Le Mans, Jacob-Bellecombette |
| `lib_for_voe_ins` | txt | 0.0 | 3204 |  |  | BUT - Management de la Logistique et des Transports (Seconde année en apprentiss |
| `select_form` | txt | 0.0 | 2 |  |  | formation sélective, formation non sélective |
| `fili` | txt | 0.0 | 11 |  |  | BUT, Licence, Licence_Las |
| `lib_comp_voe_ins` | txt | 0.0 | 11529 |  |  | I.U.T LUMIERE Lyon 2 - BUT - Management de la Logistique et des Transports (Seco |
| `form_lib_voe_acc` | txt | 0.0 | 54 |  |  | BUT - Service, Licence - Arts-lettres-langues, Licence - Sciences humaines et so |
| `fil_lib_voe_acc` | txt | 0.0 | 455 |  |  | Management de la Logistique et des Transports, Langues étrangères appliquées, So |
| `detail_forma` | txt | 71.0 | 2623 |  |  | LEA anglais / allemand, LEA Anglais/Espagnol, Droits français et espagnol |
| `g_olocalisation_des_formations` | txt | 0.0 | 5698 |  |  | 45.724, 4.91585, 48.0171, 0.15753, 45.558, 5.91097 |
| `capa_fin` | num | 0.0 | 360 | 0 | 3400 | 57, 80, 100 |
| `voe_tot` | num | 0.0 | 2987 | 1 | 1.708e+04 | 414, 153, 568 |
| `voe_tot_f` | num | 0.0 | 2195 | 0 | 1.005e+04 | 130, 118, 417 |
| `nb_voe_pp` | num | 0.0 | 2937 | 0 | 1.708e+04 | 389, 126, 512 |
| `nb_voe_pp_internat` | num | 92.9 | 566 | 0 | 5181 | 2970.0, 1452.0, 3347.0 |
| `nb_voe_pp_bg` | num | 0.0 | 2104 | 0 | 1.554e+04 | 138, 89, 358 |
| `nb_voe_pp_bg_brs` | num | 0.0 | 686 | 0 | 2187 | 29, 21, 66 |
| `nb_voe_pp_bt` | num | 0.0 | 954 | 0 | 3009 | 136, 13, 59 |
| `nb_voe_pp_bt_brs` | num | 0.0 | 462 | 0 | 1314 | 49, 4, 16 |
| `nb_voe_pp_bp` | num | 0.0 | 614 | 0 | 1702 | 13, 3, 28 |
| `nb_voe_pp_bp_brs` | num | 0.0 | 359 | 0 | 863 | 5, 2, 7 |
| `nb_voe_pp_at` | num | 0.0 | 1418 | 0 | 5935 | 102, 21, 82 |
| `nb_voe_pc` | num | 0.0 | 342 | 0 | 1202 | 25, 27, 56 |
| `nb_voe_pc_bg` | num | 0.0 | 133 | 0 | 482 | 0, 6, 11 |
| `nb_voe_pc_bt` | num | 0.0 | 103 | 0 | 558 | 20, 2, 3 |
| `nb_voe_pc_bp` | num | 0.0 | 84 | 0 | 206 | 0, 3, 2 |
| `nb_voe_pc_at` | num | 0.0 | 253 | 0 | 678 | 5, 16, 40 |
| `nb_cla_pp` | num | 0.0 | 2486 | 0 | 1.382e+04 | 169, 125, 512 |
| `nb_cla_pc` | num | 0.0 | 236 | 0 | 941 | 6, 14, 28 |
| `nb_cla_pp_internat` | num | 92.9 | 429 | 0 | 3695 | 834.0, 443.0, 596.0 |
| `nb_cla_pp_pasinternat` | num | 92.9 | 644 | 0 | 4332 | 1014.0, 592.0, 747.0 |
| `nb_cla_pp_bg` | num | 0.0 | 1861 | 0 | 1.277e+04 | 70, 89, 358 |
| `nb_cla_pp_bg_brs` | num | 0.0 | 637 | 0 | 2187 | 8, 21, 66 |
| `nb_cla_pp_bt` | num | 0.0 | 762 | 0 | 1641 | 57, 13, 59 |
| `nb_cla_pp_bt_brs` | num | 0.0 | 335 | 0 | 701 | 14, 4, 16 |
| `nb_cla_pp_bp` | num | 0.0 | 459 | 0 | 1066 | 2, 3, 13 |
| `nb_cla_pp_bp_brs` | num | 0.0 | 261 | 0 | 488 | 0, 2, 7 |
| `nb_cla_pp_at` | num | 0.0 | 1177 | 0 | 5567 | 40, 20, 82 |
| `prop_tot` | num | 0.0 | 1537 | 0 | 5188 | 126, 139, 433 |
| `acc_tot` | num | 0.0 | 466 | 0 | 1526 | 56, 21, 88 |
| `acc_tot_f` | num | 0.0 | 332 | 0 | 1074 | 18, 15, 62 |
| `acc_pp` | num | 0.0 | 438 | 0 | 1526 | 51, 14, 72 |
| `acc_pc` | num | 0.0 | 115 | 0 | 529 | 5, 7, 16 |
| `acc_debutpp` | num | 0.0 | 243 | 0 | 1012 | 22.0, 14.0, 20.0 |
| `acc_datebac` | num | 0.0 | 419 | 0 | 1523 | 51.0, 16.0, 69.0 |
| `acc_finpp` | num | 0.0 | 440 | 0 | 1523 | 51.0, 19.0, 74.0 |
| `acc_internat` | num | 92.9 | 63 | 0 | 141 | 9.0, 10.0, 29.0 |
| `acc_brs` | num | 0.0 | 148 | 0 | 317 | 9, 6, 11 |
| `acc_neobac` | num | 0.0 | 388 | 0 | 1259 | 38, 16, 62 |
| `acc_bg` | num | 0.0 | 363 | 0 | 1087 | 14, 12, 48 |
| `acc_bt` | num | 0.0 | 103 | 0 | 181 | 24, 2, 10 |
| `acc_bp` | num | 0.0 | 54 | 0 | 132 | 0, 2, 4 |
| `acc_at` | num | 0.0 | 213 | 0 | 1020 | 18, 5, 26 |
| `acc_mention_nonrenseignee` | num | 0.0 | 6 | 0 | 6 | 0, 1, 2 |
| `acc_sansmention` | num | 0.0 | 185 | 0 | 390 | 18, 8, 24 |
| `acc_ab` | num | 0.0 | 194 | 0 | 484 | 15, 5, 25 |
| `acc_b` | num | 0.0 | 166 | 0 | 480 | 4, 1, 13 |
| `acc_tb` | num | 0.0 | 126 | 0 | 398 | 1, 2, 0 |
| `acc_tbf` | num | 0.0 | 59 | 0 | 255 | 0.0, 1.0, 34.0 |
| `acc_bg_mention` | num | 0.0 | 289 | 0 | 915 | 10, 6, 31 |
| `acc_bt_mention` | num | 0.0 | 81 | 0 | 167 | 10, 1, 3 |
| `acc_bp_mention` | num | 0.0 | 46 | 0 | 69 | 0, 1, 4 |
| `acc_term` | num | 54.0 | 39 | 0 | 46 | 2.0, 0.0, 1.0 |
| `acc_term_f` | num | 54.0 | 21 | 0 | 20 | 2.0, 0.0, 4.0 |
| `acc_aca_orig` | num | 0.0 | 305 | 0 | 1008 | 19, 14, 54 |
| `acc_aca_orig_idf` | num | 0.0 | 329 | 0 | 1012 | 19, 14, 54 |
| `pct_acc_debutpp` | num | 0.0 | 101 | 0 | 100 | 39.0, 67.0, 23.0 |
| `pct_acc_datebac` | num | 0.0 | 92 | 0 | 100 | 91.0, 76.0, 78.0 |
| `pct_acc_finpp` | num | 0.0 | 80 | 0 | 100 | 91.0, 90.0, 84.0 |
| `pct_f` | num | 0.0 | 101 | 0 | 100 | 32.0, 71.0, 70.0 |
| `pct_aca_orig` | num | 0.0 | 100 | 0 | 100 | 50.0, 88.0, 87.0 |
| `pct_aca_orig_idf` | num | 0.0 | 99 | 0 | 100 | 50.0, 88.0, 87.0 |
| `pct_etab_orig` | num | 54.3 | 97 | 0 | 100 | 9.0, 0.0, 14.0 |
| `pct_bours` | num | 0.0 | 97 | 0 | 100 | 24.0, 38.0, 18.0 |
| `pct_neobac` | num | 0.0 | 99 | 0 | 100 | 68.0, 76.0, 70.0 |
| `pct_mention_nonrenseignee` | num | 0.0 | 22 | 0 | 100 | 0.0, 3.0, 1.0 |
| `pct_sansmention` | num | 0.0 | 95 | 0 | 100 | 47.0, 50.0, 39.0 |
| `pct_ab` | num | 0.0 | 86 | 0 | 100 | 39.0, 31.0, 40.0 |
| `pct_b` | num | 0.0 | 86 | 0 | 100 | 11.0, 6.0, 21.0 |
| `pct_tb` | num | 0.0 | 90 | 0 | 100 | 3.0, 12.0, 0.0 |
| `pct_tbf` | num | 0.0 | 65 | 0 | 79 | 0.0, 5.0, 36.0 |
| `pct_bg` | num | 0.0 | 101 | 0 | 100 | 37.0, 75.0, 77.0 |
| `pct_bg_mention` | num | 0.0 | 101 | 0 | 100 | 26.0, 38.0, 50.0 |
| `pct_bt` | num | 0.0 | 94 | 0 | 100 | 63.0, 12.0, 16.0 |
| `pct_bt_mention` | num | 0.0 | 94 | 0 | 100 | 26.0, 6.0, 5.0 |
| `pct_bp` | num | 0.0 | 98 | 0 | 100 | 0.0, 12.0, 6.0 |
| `pct_bp_mention` | num | 0.0 | 95 | 0 | 100 | 0.0, 6.0, 4.0 |
| `prop_tot_bg` | num | 0.0 | 1183 | 0 | 4573 | 35.0, 92.0, 312.0 |
| `prop_tot_bg_brs` | num | 0.0 | 360 | 0 | 754 | 8.0, 22.0, 54.0 |
| `prop_tot_bt` | num | 0.0 | 365 | 0 | 623 | 58.0, 15.0, 34.0 |
| `prop_tot_bt_brs` | num | 0.0 | 148 | 0 | 311 | 16.0, 4.0, 11.0 |
| `prop_tot_bp` | num | 0.0 | 181 | 0 | 375 | 2.0, 6.0, 11.0 |
| `prop_tot_bp_brs` | num | 0.0 | 104 | 0 | 215 | 0.0, 4.0, 6.0 |
| `prop_tot_at` | num | 0.0 | 655 | 0 | 2040 | 31.0, 26.0, 76.0 |
| `lib_grp1` | txt | 0.5 | 11 |  |  | Tous les candidats sauf les Bac technologiques, Tous les candidats, Groupe par d |
| `ran_grp1` | num | 0.5 | 2277 | 1 | 1.773e+04 | 89.0, 125.0, 512.0 |
| `lib_grp2` | txt | 55.3 | 5 |  |  | Bacheliers technologiques toutes séries, Bacheliers professionnels toutes séries |
| `ran_grp2` | num | 55.3 | 432 | 1 | 1575 | 63.0, 278.0, 172.0 |
| `lib_grp3` | txt | 72.3 | 2 |  |  | Bacheliers technologiques toutes séries, Bacheliers professionnels toutes séries |
| `ran_grp3` | num | 72.3 | 329 | 1 | 989 | 95.0, 94.0, 75.0 |
| `list_com` | txt | 0.0 | 2 |  |  | Liste d'appel propre à cette formation, Liste d'appel commune à plusieurs format |
| `tri` | txt | 0.0 | 3 |  |  | 1_universités, 2_Lycées, 3_Autres formations |
| `cod_aff_form` | num | 0.0 | 13644 | 2 | 3.898e+04 | 8578, 8737, 8808 |
| `detail_forma2` | txt | 95.1 | 97 |  |  | Concours Puissance Alpha, Concours GalaxY, Université du littoral - Site de Cala |
| `lien_form_psup` | txt | 4.0 | 13095 |  |  | https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_t |
| `taux_acces_ens` | num | 0.7 | 100 | 1 | 100 | 32.0, 99.0, 100.0 |
| `part_acces_gen` | num | 0.2 | 101 | 0 | 100 | 45.0, 87.0, 81.0 |
| `part_acces_tec` | num | 0.2 | 93 | 0 | 100 | 52.0, 13.0, 15.0 |
| `part_acces_pro` | num | 0.2 | 98 | 0 | 100 | 2.0, 0.0, 3.0 |
| `etablissement_id_paysage` | txt | 52.2 | 483 |  |  | CUBKB, 9xlel, zCa4j |
| `composante_id_paysage` | txt | 98.4 | 95 |  |  | i2Fja, S9Fza, 8ZZJd |

## Alertes
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
- `detail_forma2` manquant à plus de 50 %
- `etablissement_id_paysage` manquant à plus de 50 %
- `composante_id_paysage` manquant à plus de 50 %