# monmaster_2024_2025.csv

- Lignes : **16,257**
- Colonnes : **144**
- Colonnes UAI détectées : ['eta_uai', 'inm']
- Valeurs de `session` : ['2024', '2025']
- Lignes dupliquées : 0
- Doublons sur `eta_uai` : 16137 (attendu > 0 si plusieurs années/formations par UAI)
- Doublons sur `inm` : 13354 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 2 | 2024 | 2025 | 2025, 2024 |
| `pp` | num | 0.0 | 2 | 0 | 1 | 1, 0 |
| `pc` | num | 0.0 | 2 | 0 | 1 | 1, 0 |
| `eta_uai` | txt | 0.0 | 120 |  |  | 0755976N, 0931238R, 0756305W |
| `eta_nom` | txt | 0.0 | 121 |  |  | Université Paris Cité, Université Sorbonne Paris Nord, Université Paris-Panthéon |
| `acad` | txt | 0.0 | 30 |  |  | A01, A24, A23 |
| `acad_lib` | txt | 0.0 | 30 |  |  | Paris, Créteil, Nice |
| `acad_reg` | txt | 0.0 | 17 |  |  | R11, R93, R24 |
| `acad_reg_lib` | txt | 0.0 | 17 |  |  | Île-de-France, Provence-Alpes-Côte d'Azur, Centre-Val de Loire |
| `ifc` | txt | 0.0 | 8953 |  |  | 0900820SVFY8, 0900820SV72L, 0900820S3JVP |
| `inm` | txt | 0.0 | 2903 |  |  | 0900820S, 0900827Z, 0900841Q |
| `mention` | txt | 0.0 | 327 |  |  | BIO-INFORMATIQUE, MONNAIE, BANQUE, FINANCE, ASSURANCE, BIOLOGIE INTEGRATIVE ET P |
| `inmp` | txt | 11.7 | 6509 |  |  | 0900820-06Z, 0900820-09C, 0900820-10D |
| `parcours` | txt | 11.8 | 6705 |  |  | Biologie Informatique - Ingénierie de Plateforme en Biologie, In Silico Drug Des |
| `alternance` | num | 0.0 | 2 | 0 | 1 | 0, 1 |
| `modalite_enseignement` | txt | 1.5 | 24 |  |  | INITIALE,CONTINUE, CONTINUE, INITIALE |
| `lieux` | txt | 0.0 | 2393 |  |  | Université Paris Cité - PARIS (75)/UFR SDV - Campus Grands Moulins - PARIS (75), |
| `lieu_acad` | txt | 0.0 | 32 |  |  | A01, A25, A24 |
| `lieu_acad_lib` | txt | 0.0 | 32 |  |  | Paris, Versailles, Créteil |
| `lieu_reg_acad` | txt | 0.0 | 19 |  |  | R11, R93, R24 |
| `lieu_reg_acad_lib` | txt | 0.0 | 19 |  |  | Île-de-France, Provence-Alpes-Côte d'Azur, Centre-Val de Loire |
| `disci_master` | txt | 0.0 | 10 |  |  | Sc. fondamentales et appliquées (dont STAPS), Economie, gestion et AES, Lettres, |
| `discipline` | num | 0.0 | 13 | 1 | 33 | 9, 31, 5 |
| `disci_lib` | txt | 0.0 | 13 |  |  | Sciences de la vie, de la terre et de l'univers, Pluridisciplinaire droit, scien |
| `secteur_disci` | num | 0.0 | 46 | 1 | 70 | 6, 63, 5 |
| `secteur_disci_lib` | txt | 0.0 | 46 |  |  | Sciences de la vie, biologie, santé, Pluridisciplinaire droit, sciences économiq |
| `col` | num | 0.0 | 146 | 1 | 350 | 30, 15, 5 |
| `n_can_pp` | num | 0.0 | 1502 | 0 | 4592 | 406, 147, 60 |
| `n_can_femme_pp` | num | 0.0 | 1175 | 0 | 2861 | 257, 95, 42 |
| `n_can_etab_pp` | num | 0.0 | 382 | 0 | 806 | 71, 36, 12 |
| `n_can_lieu_acad_pp` | num | 0.0 | 555 | 0 | 1416 | 109, 48, 19 |
| `n_can_lieu_acad_reg_pp` | num | 0.0 | 844 | 0 | 2504 | 248, 89, 40 |
| `n_can_lg3_pp` | num | 0.0 | 1137 | 0 | 3009 | 271, 108, 46 |
| `n_can_femme_lg3_pp` | num | 0.0 | 931 | 0 | 2260 | 179, 75, 32 |
| `n_can_lp3_pp` | num | 0.0 | 123 | 0 | 233 | 5, 3, 0 |
| `n_can_femme_lp3_pp` | num | 0.0 | 83 | 0 | 128 | 3, 2, 0 |
| `n_can_but3_pp` | num | 0.0 | 300 | 0 | 596 | 18, 1, 0 |
| `n_can_femme_but3_pp` | num | 0.0 | 181 | 0 | 313 | 14, 1, 0 |
| `n_can_master_pp` | num | 0.0 | 153 | 0 | 219 | 28, 10, 3 |
| `n_can_femme_master_pp` | num | 0.0 | 112 | 0 | 140 | 14, 3, 2 |
| `n_can_autre_pp` | num | 0.0 | 262 | 0 | 628 | 19, 6, 3 |
| `n_can_femme_autre_pp` | num | 0.0 | 178 | 0 | 327 | 11, 4, 2 |
| `n_can_noninscri_pp` | num | 0.0 | 389 | 0 | 1152 | 65, 19, 8 |
| `n_can_femme_noninscri_pp` | num | 0.0 | 309 | 0 | 1002 | 36, 10, 6 |
| `n_can_pc` | num | 0.0 | 384 | 0 | 1503 | 196, 0, 10 |
| `n_can_femme_pc` | num | 0.0 | 277 | 0 | 1157 | 112, 0, 5 |
| `n_can_etab_pc` | num | 0.0 | 72 | 0 | 118 | 20, 0, 3 |
| `n_can_lieu_acad_pc` | num | 0.0 | 104 | 0 | 261 | 41, 0, 1 |
| `n_can_lieu_acad_reg_pc` | num | 0.0 | 189 | 0 | 523 | 103, 0, 3 |
| `n_can_lg3_pc` | num | 0.0 | 266 | 0 | 905 | 93, 0, 5 |
| `n_can_femme_lg3_pc` | num | 0.0 | 214 | 0 | 713 | 57, 0, 4 |
| `n_can_lp3_pc` | num | 0.0 | 30 | 0 | 45 | 1, 0, 5 |
| `n_can_femme_lp3_pc` | num | 0.0 | 22 | 0 | 38 | 0, 1, 2 |
| `n_can_but3_pc` | num | 0.0 | 45 | 0 | 58 | 6, 0, 1 |
| `n_can_femme_but3_pc` | num | 0.0 | 28 | 0 | 35 | 2, 0, 1 |
| `n_can_master_pc` | num | 0.0 | 57 | 0 | 119 | 25, 0, 5 |
| `n_can_femme_master_pc` | num | 0.0 | 43 | 0 | 86 | 14, 0, 3 |
| `n_can_autre_pc` | num | 0.0 | 70 | 0 | 95 | 20, 0, 5 |
| `n_can_femme_autre_pc` | num | 0.0 | 51 | 0 | 69 | 11, 0, 4 |
| `n_can_noninscri_pc` | num | 0.0 | 140 | 0 | 315 | 51, 0, 5 |
| `n_can_femme_noninscri_pc` | num | 0.0 | 103 | 0 | 229 | 28, 0, 1 |
| `n_clas_total` | num | 0.0 | 870 | 0 | 3319 | 60, 34, 4 |
| `n_clas_femme_total` | num | 0.0 | 713 | 0 | 2861 | 44, 26, 4 |
| `n_clas_etab` | num | 0.0 | 303 | 0 | 786 | 23, 14, 2 |
| `n_clas_lieu_acad` | num | 0.0 | 405 | 0 | 1379 | 38, 19, 2 |
| `n_clas_lieu_acad_reg` | num | 0.0 | 499 | 0 | 1593 | 52, 29, 3 |
| `n_clas_pp` | num | 0.0 | 868 | 0 | 3319 | 59, 34, 4 |
| `n_clas_femme_pp` | num | 0.0 | 698 | 0 | 2861 | 43, 26, 4 |
| `n_clas_pc` | num | 0.0 | 120 | 0 | 251 | 1, 0, 3 |
| `n_clas_femme_pc` | num | 0.0 | 96 | 0 | 213 | 1, 0, 3 |
| `n_clas_lg3_total` | num | 0.0 | 742 | 0 | 2658 | 54, 32, 4 |
| `n_clas_femme_lg3_total` | num | 0.0 | 617 | 0 | 2260 | 38, 25, 4 |
| `n_clas_lp3_total` | num | 0.0 | 61 | 0 | 100 | 0, 1, 2 |
| `n_clas_femme_lp3_total` | num | 0.0 | 38 | 0 | 75 | 0, 1, 2 |
| `n_clas_but3_total` | num | 0.0 | 148 | 0 | 484 | 0, 1, 5 |
| `n_clas_femme_but3_total` | num | 0.0 | 94 | 0 | 208 | 0, 1, 5 |
| `n_clas_master_total` | num | 0.0 | 100 | 0 | 138 | 0, 4, 1 |
| `n_clas_femme_master_total` | num | 0.0 | 81 | 0 | 120 | 0, 4, 1 |
| `n_clas_autre_total` | num | 0.0 | 115 | 0 | 193 | 3, 1, 0 |
| `n_clas_femme_autre_total` | num | 0.0 | 94 | 0 | 144 | 3, 0, 1 |
| `n_clas_noninscri_total` | num | 0.0 | 226 | 0 | 530 | 3, 0, 2 |
| `n_clas_femme_noninscri_total` | num | 0.0 | 194 | 0 | 454 | 3, 0, 1 |
| `n_prop_total` | num | 0.0 | 467 | 0 | 1699 | 58, 28, 4 |
| `n_prop_femme_total` | num | 0.0 | 396 | 0 | 1490 | 44, 20, 4 |
| `n_prop_etab` | num | 0.0 | 198 | 0 | 492 | 22, 12, 2 |
| `n_prop_lieu_acad` | num | 0.0 | 269 | 0 | 787 | 36, 16, 2 |
| `n_prop_lieu_acad_reg` | num | 0.0 | 323 | 0 | 931 | 50, 24, 3 |
| `n_prop_pp` | num | 0.0 | 444 | 0 | 1668 | 57, 28, 4 |
| `n_prop_femme_pp` | num | 0.0 | 386 | 0 | 1464 | 43, 20, 4 |
| `n_prop_pc` | num | 0.0 | 77 | 0 | 126 | 1, 0, 3 |
| `n_prop_femme_pc` | num | 0.0 | 61 | 0 | 98 | 1, 0, 3 |
| `n_prop_lg3_total` | num | 0.0 | 406 | 0 | 1295 | 52, 26, 4 |
| `n_prop_femme_lg3_total` | num | 0.0 | 361 | 0 | 1148 | 38, 19, 4 |
| `n_prop_lp3_total` | num | 0.0 | 29 | 0 | 40 | 0, 1, 17 |
| `n_prop_femme_lp3_total` | num | 0.0 | 20 | 0 | 30 | 0, 1, 8 |
| `n_prop_but3_total` | num | 0.0 | 61 | 0 | 129 | 0, 1, 3 |
| `n_prop_femme_but3_total` | num | 0.0 | 40 | 0 | 77 | 0, 1, 3 |
| `n_prop_master_total` | num | 0.0 | 55 | 0 | 76 | 0, 1, 5 |
| `n_prop_femme_master_total` | num | 0.0 | 48 | 0 | 62 | 0, 1, 3 |
| `n_prop_autre_total` | num | 0.0 | 58 | 0 | 143 | 3, 1, 0 |
| `n_prop_femme_autre_total` | num | 0.0 | 44 | 0 | 68 | 3, 0, 1 |
| `n_prop_noninscri_total` | num | 0.0 | 123 | 0 | 226 | 3, 0, 2 |
| `n_prop_femme_noninscri_total` | num | 0.0 | 107 | 0 | 192 | 3, 0, 1 |
| `n_accept_total` | num | 0.0 | 173 | 0 | 380 | 19, 14, 2 |
| `n_accept_femme_total` | num | 0.0 | 144 | 0 | 333 | 16, 8, 2 |
| `n_accept_etab` | num | 0.0 | 109 | 0 | 236 | 9, 6, 2 |
| `n_accept_lieu_acad` | num | 0.0 | 130 | 0 | 241 | 12, 7, 2 |
| `n_accept_lieu_acad_reg` | num | 0.0 | 137 | 0 | 248 | 16, 12, 2 |
| `n_accept_pp` | num | 0.0 | 169 | 0 | 380 | 18, 14, 2 |
| `n_accept_femme_pp` | num | 0.0 | 139 | 0 | 333 | 15, 8, 2 |
| `n_accept_debut_pp` | num | 0.0 | 95 | 0 | 169 | 9, 7, 2 |
| `n_accept_fin_pp` | num | 0.0 | 158 | 0 | 380 | 18, 12, 2 |
| `n_accept_pc` | num | 0.0 | 44 | 0 | 80 | 1, 0, 3 |
| `n_accept_femme_pc` | num | 0.0 | 37 | 0 | 68 | 1, 0, 3 |
| `n_accept_lg3_total` | num | 0.0 | 140 | 0 | 257 | 17, 12, 2 |
| `n_accept_femme_lg3_total` | num | 0.0 | 120 | 0 | 234 | 14, 7, 2 |
| `n_accept_lp3_total` | num | 0.0 | 24 | 0 | 28 | 0, 1, 13 |
| `n_accept_femme_lp3_total` | num | 0.0 | 16 | 0 | 19 | 0, 1, 5 |
| `n_accept_but3_total` | num | 0.0 | 31 | 0 | 117 | 0, 1, 3 |
| `n_accept_femme_but3_total` | num | 0.0 | 22 | 0 | 72 | 0, 1, 4 |
| `n_accept_master_total` | num | 0.0 | 21 | 0 | 27 | 0, 4, 1 |
| `n_accept_femme_master_total` | num | 0.0 | 18 | 0 | 20 | 0, 3, 1 |
| `n_accept_autre_total` | num | 0.0 | 40 | 0 | 83 | 1, 0, 3 |
| `n_accept_femme_autre_total` | num | 0.0 | 24 | 0 | 35 | 1, 0, 3 |
| `n_accept_noninscri_total` | num | 0.0 | 60 | 0 | 119 | 1, 0, 3 |
| `n_accept_femme_noninscri_total` | num | 0.0 | 55 | 0 | 81 | 1, 0, 2 |
| `rang_dernier_appele_pp` | num | 3.5 | 653 | 1 | 3068 | 59.0, 31.0, 4.0 |
| `rang_dernier_appele_pc` | num | 66.7 | 441 | 1 | 3211 | 60.0, 137.0, 5.0 |
| `n_recrut_comp` | num | 83.2 | 32 | 0 | 60 | 1.0, 3.0, 2.0 |
| `pct_accept_femme` | num | 6.4 | 661 | 0 | 100 | 84.2, 57.1, 100.0 |
| `pct_accept_etab` | num | 6.4 | 713 | 0 | 100 | 47.4, 42.9, 100.0 |
| `pct_accept_lieu_acad` | num | 6.4 | 710 | 0 | 100 | 63.2, 50.0, 100.0 |
| `pct_accept_lieu_acad_reg` | num | 6.4 | 665 | 0 | 100 | 84.2, 85.7, 100.0 |
| `pct_accept_debut_pp` | num | 6.4 | 673 | 0 | 100 | 47.4, 50.0, 100.0 |
| `pct_accept_fin_pp` | num | 6.4 | 494 | 0 | 100 | 94.7, 85.7, 100.0 |
| `pct_accept_lg3` | num | 6.4 | 661 | 0 | 100 | 89.5, 85.7, 100.0 |
| `pct_accept_lp3` | num | 6.4 | 237 | 0 | 100 | 0.0, 7.1, 11.1 |
| `pct_accept_but3` | num | 6.4 | 339 | 0 | 100 | 0.0, 14.3, 3.7 |
| `pct_accept_master` | num | 6.4 | 232 | 0 | 100 | 0.0, 25.0, 9.1 |
| `pct_accept_autre` | num | 6.4 | 298 | 0 | 100 | 5.3, 7.1, 0.0 |
| `pct_accept_noninscri` | num | 6.4 | 452 | 0 | 100 | 5.3, 0.0, 2.5 |
| `id_paysage` | txt | 0.0 | 123 |  |  | 5cZyU, cqyN7, TWBzp |
| `id_paysage_actuel` | txt | 0.0 | 116 |  |  | 5cZyU, cqyN7, TWBzp |
| `uo_lib_actuel` | txt | 0.0 | 116 |  |  | Université Paris Cité, Université Sorbonne Paris Nord, Université Paris-Panthéon |

## Alertes
- `rang_dernier_appele_pc` manquant à plus de 50 %
- `n_recrut_comp` manquant à plus de 50 %