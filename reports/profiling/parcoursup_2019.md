# parcoursup_2019.csv

- Lignes : **11,577**
- Colonnes : **92**
- Colonnes UAI détectées : ['cod_uai']
- Valeurs de `session` : ['2019']
- Lignes dupliquées : 0
- Doublons sur `cod_uai` : 8070 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 1 | 2019 | 2019 | 2019 |
| `contrat_etab` | txt | 0.0 | 2 |  |  | Public, Privé |
| `cod_uai` | txt | 0.0 | 3507 |  |  | 0142257C, 0311086M, 0622238W |
| `g_ea_lib_vx` | txt | 0.0 | 3156 |  |  | I.U.T de Caen ( Antenne de Vire ), I.U.T de Toulouse, I.U.T. de Béthune |
| `dep` | num | 0.0 | 103 | 1 | 987 | 14, 31, 62 |
| `dep_lib` | txt | 0.0 | 103 |  |  | Calvados, Haute-Garonne, Pas-de-Calais |
| `region_etab_aff` | txt | 0.0 | 20 |  |  | Normandie, Occitanie, Hauts-de-France |
| `acad_mies` | txt | 0.0 | 33 |  |  | Caen, Toulouse, Lille |
| `fili` | txt | 0.0 | 8 |  |  | DUT, Licence, PACES |
| `form_lib_voe_acc` | txt | 0.0 | 48 |  |  | DUT - Production, DUT - Service, Licence - Droit-économie-gestion |
| `regr_forma` | txt | 97.0 | 22 |  |  | Concours Advance, Concours Puissance Alpha, LaSalle Grandes Ecoles |
| `fil_lib_voe_acc` | txt | 0.0 | 552 |  |  | Hygiène Sécurité Environnement, Techniques de commercialisation, Génie mécanique |
| `detail_forma` | txt | 75.2 | 2525 |  |  | Information - Communication, Double Licence Langues Etrangères Appliquées Anglai |
| `lien_form_psup` | txt | 5.4 | 10953 |  |  | https://dossier.parcoursup.fr/Candidat/carte?g_ti_cod=2945&g_ta_cod=2945, https: |
| `g_olocalisation_des_formations` | txt | 1.5 | 11405 |  |  | 48.8405, -0.8792, 43.5651, 1.4571598, 50.5171, 2.6572402 |
| `capa_fin` | num | 0.2 | 363 | 1 | 3100 | 52.0, 164.0, 65.0 |
| `voe_tot` | num | 0.0 | 2599 | 0 | 1.69e+04 | 699, 6041, 623 |
| `voe_tot_f` | num | 0.0 | 1859 | 0 | 1.218e+04 | 218, 3053, 38 |
| `nb_voe_pp` | num | 0.0 | 2562 | 0 | 1.69e+04 | 699, 6041, 493 |
| `nb_voe_pp_internat` | num | 92.7 | 501 | 0 | 4781 | 0.0, 299.0, 523.0 |
| `nb_voe_pp_bg` | num | 0.0 | 1733 | 0 | 1.357e+04 | 393, 3305, 274 |
| `nb_voe_pp_bg_brs` | num | 0.0 | 508 | 0 | 2139 | 37, 477, 34 |
| `nb_voe_pp_bt` | num | 0.0 | 886 | 0 | 2235 | 175, 1627, 146 |
| `nb_voe_pp_bt_brs` | num | 0.0 | 346 | 0 | 588 | 27, 384, 32 |
| `nb_voe_pp_bp` | num | 0.0 | 548 | 0 | 1341 | 32, 86, 2 |
| `nb_voe_pp_bp_brs` | num | 0.0 | 247 | 0 | 410 | 8, 28, 0 |
| `nb_voe_pp_at` | num | 0.0 | 1127 | 0 | 8137 | 99, 1023, 71 |
| `nb_voe_pc` | num | 0.0 | 436 | 0 | 2343 | 0, 130, 23 |
| `nb_voe_pc_bg` | num | 0.0 | 160 | 0 | 991 | 0, 46, 5 |
| `nb_voe_pc_bt` | num | 0.0 | 149 | 0 | 669 | 0, 16, 3 |
| `nb_voe_pc_bp` | num | 0.0 | 111 | 0 | 274 | 0, 4, 3 |
| `nb_voe_pc_at` | num | 0.0 | 298 | 0 | 1032 | 0, 64, 12 |
| `nb_cla_pp` | num | 0.0 | 2045 | 0 | 1.682e+04 | 638, 2760, 354 |
| `nb_cla_pc` | num | 0.0 | 274 | 0 | 682 | 0, 51, 11 |
| `nb_cla_pp_internat` | num | 92.7 | 423 | 0 | 4781 | 0.0, 215.0, 523.0 |
| `nb_cla_pp_pasinternat` | num | 92.7 | 557 | 0 | 4418 | 130.0, 275.0, 0.0 |
| `nb_cla_pp_bg` | num | 0.0 | 1483 | 0 | 1.295e+04 | 381, 1400, 185 |
| `nb_cla_pp_bg_brs` | num | 0.0 | 452 | 0 | 2139 | 37, 163, 22 |
| `nb_cla_pp_bt` | num | 0.0 | 674 | 0 | 1689 | 144, 969, 112 |
| `nb_cla_pp_bt_brs` | num | 0.0 | 244 | 0 | 434 | 19, 206, 23 |
| `nb_cla_pp_bp` | num | 0.0 | 411 | 0 | 943 | 27, 0, 1 |
| `nb_cla_pp_bp_brs` | num | 0.0 | 181 | 0 | 301 | 5, 0, 26 |
| `nb_cla_pp_at` | num | 0.0 | 934 | 0 | 7499 | 86, 391, 56 |
| `prop_tot` | num | 0.0 | 1347 | 0 | 8795 | 261, 596, 281 |
| `rang_der_max` | num | 51.3 | 1475 | 1 | 9951 | 2710.0, 538.0, 519.0 |
| `acc_tot` | num | 0.0 | 493 | 0 | 2680 | 57, 178, 56 |
| `acc_tot_f` | num | 0.0 | 364 | 0 | 1775 | 16, 116, 0 |
| `acc_pp` | num | 0.0 | 464 | 0 | 2447 | 57, 177, 39 |
| `acc_pc` | num | 0.0 | 145 | 0 | 335 | 0, 17, 2 |
| `acc_debutpp` | num | 0.0 | 270 | 0 | 1548 | 6.0, 39.0, 18.0 |
| `acc_datebac` | num | 0.0 | 422 | 0 | 2435 | 47.0, 166.0, 39.0 |
| `acc_finpp` | num | 0.0 | 460 | 0 | 2590 | 57.0, 176.0, 51.0 |
| `acc_internat` | num | 92.7 | 64 | 0 | 142 | 0.0, 15.0, 35.0 |
| `acc_brs` | num | 0.0 | 152 | 0 | 454 | 9, 25, 8 |
| `acc_neobac` | num | 0.0 | 410 | 0 | 2311 | 48, 156, 41 |
| `acc_bg` | num | 0.0 | 371 | 0 | 2160 | 31, 72, 25 |
| `acc_bt` | num | 0.0 | 112 | 0 | 179 | 13, 84, 3 |
| `acc_bp` | num | 0.0 | 59 | 0 | 148 | 4, 0, 3 |
| `acc_at` | num | 0.0 | 216 | 0 | 554 | 9, 22, 15 |
| `acc_mention_nonrenseignee` | num | 0.0 | 31 | 0 | 52 | 0, 1, 5 |
| `acc_sansmention` | num | 0.0 | 268 | 0 | 720 | 25, 12, 7 |
| `acc_ab` | num | 0.0 | 190 | 0 | 581 | 15, 48, 10 |
| `acc_b` | num | 0.0 | 137 | 0 | 511 | 6, 70, 5 |
| `acc_tb` | num | 0.0 | 141 | 0 | 590 | 2, 25, 1 |
| `acc_bg_mention` | num | 0.0 | 260 | 0 | 1499 | 13, 67, 4 |
| `acc_bt_mention` | num | 0.0 | 72 | 0 | 110 | 7, 76, 9 |
| `acc_bp_mention` | num | 0.0 | 38 | 0 | 54 | 3, 0, 9 |
| `acc_term` | num | 48.5 | 40 | 0 | 54 | 6.0, 5.0, 0.0 |
| `acc_term_f` | num | 48.5 | 24 | 0 | 28 | 4.0, 0.0, 1.0 |
| `acc_aca_orig` | num | 0.0 | 341 | 0 | 2006 | 25, 122, 33 |
| `acc_aca_orig_idf` | num | 0.0 | 356 | 0 | 2006 | 25, 122, 33 |
| `pct_acc_debutpp` | num | 0.4 | 2241 | 0 | 100 | 10.5263157895, 21.9101123596, 32.1428571429 |
| `pct_acc_datebac` | num | 0.4 | 1980 | 0 | 100 | 82.4561403509, 93.2584269663, 69.6428571429 |
| `pct_acc_finpp` | num | 0.4 | 1543 | 0 | 100 | 100.0, 98.8764044944, 91.0714285714 |
| `pct_f` | num | 0.4 | 2201 | 0 | 100 | 28.06640625, 65.15625, 0.0 |
| `pct_aca_orig` | num | 1.2 | 1652 | 0 | 100 | 52.078125, 78.203125, 80.484375 |
| `pct_aca_orig_idf` | num | 1.2 | 1521 | 0 | 100 | 52.078125, 78.203125, 80.484375 |
| `pct_etab_orig` | num | 48.6 | 517 | 0 | 100 | 18.1796875, 9.615234375, 0.0 |
| `pct_bours` | num | 1.2 | 1460 | 0 | 100 | 18.75, 16.0234375, 19.51171875 |
| `pct_neobac` | num | 0.4 | 1973 | 0 | 100 | 84.203125, 87.625, 73.203125 |
| `pct_mention_nonrenseignee` | num | 1.2 | 608 | 0 | 100 | 0.0, 0.640991210938, 0.959594726562 |
| `pct_sansmention` | num | 1.2 | 1677 | 0 | 100 | 52.078125, 7.69140625, 60.96875 |
| `pct_ab` | num | 1.2 | 1455 | 0 | 100 | 31.25, 30.765625, 24.38671875 |
| `pct_b` | num | 1.2 | 1506 | 0 | 100 | 12.5, 44.8671875, 12.193359375 |
| `pct_tb` | num | 1.2 | 1290 | 0 | 100 | 4.166015625, 16.0234375, 2.43896484375 |
| `pct_bg` | num | 1.2 | 1526 | 0 | 100 | 64.578125, 46.1484375, 60.96875 |
| `pct_bg_mention` | num | 1.2 | 1776 | 0 | 100 | 27.08203125, 42.9453125, 9.755859375 |
| `pct_bt` | num | 1.2 | 1460 | 0 | 100 | 27.08203125, 53.84375, 31.70703125 |
| `pct_bt_mention` | num | 1.2 | 1316 | 0 | 100 | 14.58203125, 48.7109375, 21.94921875 |
| `pct_bp` | num | 1.2 | 1149 | 0 | 100 | 8.33203125, 0.0, 7.31640625 |
| `pct_bp_mention` | num | 1.2 | 954 | 0 | 100 | 6.25, 0.0, 7.31640625 |
| `tri` | txt | 0.0 | 4 |  |  | 1_universités, 2_Lycées, 3_Autres formations |

## Alertes
- `regr_forma` manquant à plus de 50 %
- `detail_forma` manquant à plus de 50 %
- `nb_voe_pp_internat` manquant à plus de 50 %
- `nb_cla_pp_internat` manquant à plus de 50 %
- `nb_cla_pp_pasinternat` manquant à plus de 50 %
- `rang_der_max` manquant à plus de 50 %
- `acc_internat` manquant à plus de 50 %