# monmaster_2023.csv

- Lignes : **7,694**
- Colonnes : **97**
- Colonnes UAI détectées : ['eta_uai', 'inm']
- Valeurs de `session` : ['2023']
- Lignes dupliquées : 0
- Doublons sur `eta_uai` : 7579 (attendu > 0 si plusieurs années/formations par UAI)
- Doublons sur `inm` : 4994 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 1 | 2023 | 2023 | 2023 |
| `eta_uai` | txt | 0.0 | 115 |  |  | 0442953W, 0490811R, 0134009M |
| `eta_nom` | txt | 0.0 | 113 |  |  | Nantes Université, Facultés libres de l'Ouest, Aix-Marseille Université |
| `ifc` | txt | 0.0 | 7694 |  |  | 1302893N6B42, 1302893N2CIN, 1303247Y45CL |
| `inm` | txt | 0.0 | 2700 |  |  | 1302893N, 1303247Y, 1401449P |
| `mention` | txt | 0.0 | 320 |  |  | METIERS DE L'ENSEIGNEMENT, DE L'EDUCATION ET DE LA FORMATION (MEEF), 2ND DEGRE,  |
| `inmp` | txt | 15.4 | 5595 |  |  | 1302893-05K, 1302893-70F, 1303247-34V |
| `parcours` | txt | 15.4 | 5119 |  |  | Domaine Scientifique et Industriel (DSI), Lettres modernes, Enseigner en lycée p |
| `alternance` | num | 0.0 | 2 | 0 | 1 | 0, 1 |
| `modalite_enseignement` | txt | 1.7 | 16 |  |  | INITIALE,CONTINUE,HYBRIDE, INITIALE,HYBRIDE, APPRENTISSAGE,CONTRAT_PRO |
| `lieux_formation` | txt | 0.0 | 1464 |  |  | Institut National Supérieur du Professorat et de l'Éducation (INSPE) - LE MANS ( |
| `disci_master` | txt | 0.0 | 6 |  |  | M.E.E.F., Sc. fondamentales et appliquées (dont S.T.A.P.S.), Lettres, langues, a |
| `discipline` | num | 0.0 | 13 | 1 | 33 | 6, 9, 32 |
| `secteur_disci` | num | 0.0 | 46 | 1 | 70 | 34, 6, 67 |
| `col` | num | 0.0 | 137 | 1 | 415 | 15, 87, 8 |
| `n_can` | num | 0.0 | 1089 | 0 | 3529 | 17, 10, 60 |
| `n_can_femme` | num | 0.0 | 859 | 0 | 3034 | 6, 23, 35 |
| `n_can_etab` | num | 0.0 | 290 | 0 | 735 | 0, 16, 11 |
| `n_can_acad` | num | 0.0 | 418 | 0 | 1164 | 1, 7, 22 |
| `n_can_acad_reg` | num | 0.0 | 590 | 0 | 1672 | 1, 7, 28 |
| `n_can_lg3` | num | 0.0 | 870 | 0 | 2756 | 4, 8, 38 |
| `n_can_femme_lg3` | num | 0.0 | 695 | 0 | 2402 | 1, 6, 15 |
| `n_can_lp3` | num | 0.0 | 134 | 0 | 310 | 4, 0, 1 |
| `n_can_femme_lp3` | num | 0.0 | 86 | 0 | 147 | 1, 0, 3 |
| `n_can_master` | num | 0.0 | 93 | 0 | 217 | 3, 1, 2 |
| `n_can_femme_master` | num | 0.0 | 67 | 0 | 137 | 1, 0, 28 |
| `n_can_autre` | num | 0.0 | 136 | 0 | 353 | 1, 7, 0 |
| `n_can_femme_autre` | num | 0.0 | 109 | 0 | 235 | 1, 0, 4 |
| `n_can_noninscri` | num | 0.0 | 312 | 0 | 828 | 5, 0, 11 |
| `n_can_femme_noninscri` | num | 0.0 | 257 | 0 | 750 | 2, 0, 4 |
| `n_clas` | num | 0.0 | 594 | 0 | 3518 | 10, 9, 51 |
| `n_clas_femme` | num | 0.0 | 477 | 0 | 3025 | 2, 6, 17 |
| `n_clas_etab` | num | 0.0 | 215 | 0 | 583 | 0, 15, 11 |
| `n_clas_acad` | num | 0.0 | 287 | 0 | 946 | 0, 6, 19 |
| `n_clas_acad_reg` | num | 0.0 | 347 | 0 | 1062 | 0, 6, 23 |
| `n_clas_lg3` | num | 0.0 | 508 | 0 | 2752 | 2, 7, 32 |
| `n_clas_femme_lg3` | num | 0.0 | 424 | 0 | 2399 | 0, 6, 12 |
| `n_clas_lp3` | num | 0.0 | 69 | 0 | 174 | 4, 0, 1 |
| `n_clas_femme_lp3` | num | 0.0 | 39 | 0 | 47 | 1, 0, 3 |
| `n_clas_master` | num | 0.0 | 59 | 0 | 122 | 2, 1, 3 |
| `n_clas_femme_master` | num | 0.0 | 52 | 0 | 95 | 0, 1, 13 |
| `n_clas_autre` | num | 0.0 | 66 | 0 | 133 | 0, 1, 5 |
| `n_clas_femme_autre` | num | 0.0 | 55 | 0 | 108 | 0, 2, 21 |
| `n_clas_noninscri` | num | 0.0 | 182 | 0 | 535 | 2, 0, 10 |
| `n_clas_femme_noninscri` | num | 0.0 | 156 | 0 | 447 | 1, 0, 3 |
| `n_prop` | num | 0.0 | 343 | 0 | 1235 | 10, 9, 36 |
| `n_prop_femme` | num | 0.0 | 292 | 0 | 1085 | 2, 6, 9 |
| `n_prop_etab` | num | 0.0 | 164 | 0 | 457 | 0, 14, 9 |
| `n_prop_acad` | num | 0.0 | 211 | 0 | 732 | 0, 6, 17 |
| `n_prop_acad_reg` | num | 0.0 | 241 | 0 | 778 | 0, 6, 20 |
| `n_prop_lg3` | num | 0.0 | 294 | 0 | 992 | 2, 7, 22 |
| `n_prop_femme_lg3` | num | 0.0 | 255 | 0 | 889 | 0, 6, 5 |
| `n_prop_lp3` | num | 0.0 | 46 | 0 | 71 | 4, 0, 1 |
| `n_prop_femme_lp3` | num | 0.0 | 29 | 0 | 32 | 1, 0, 2 |
| `n_prop_master` | num | 0.0 | 39 | 0 | 61 | 2, 1, 14 |
| `n_prop_femme_master` | num | 0.0 | 29 | 0 | 40 | 0, 1, 13 |
| `n_prop_autre` | num | 0.0 | 43 | 0 | 86 | 0, 1, 3 |
| `n_prop_femme_autre` | num | 0.0 | 32 | 0 | 40 | 0, 1, 20 |
| `n_prop_noninscri` | num | 0.0 | 98 | 0 | 208 | 2, 0, 9 |
| `n_prop_femme_noninscri` | num | 0.0 | 87 | 0 | 189 | 1, 0, 3 |
| `n_accept` | num | 0.0 | 141 | 0 | 323 | 3, 2, 5 |
| `n_accept_femme` | num | 0.0 | 123 | 0 | 270 | 0, 1, 54 |
| `n_accept_etab` | num | 0.0 | 91 | 0 | 233 | 0, 2, 1 |
| `n_accept_acad` | num | 0.0 | 100 | 0 | 254 | 0, 2, 1 |
| `n_accept_acad_reg` | num | 0.0 | 106 | 0 | 257 | 0, 2, 1 |
| `n_accept_debut_pp` | num | 0.0 | 80 | 0 | 165 | 3, 2, 0 |
| `n_accept_lg3` | num | 0.0 | 112 | 0 | 252 | 0, 2, 20 |
| `n_accept_femme_lg3` | num | 0.0 | 99 | 0 | 222 | 0, 1, 16 |
| `n_accept_lp3` | num | 0.0 | 29 | 0 | 40 | 0, 1, 3 |
| `n_accept_femme_lp3` | num | 0.0 | 18 | 0 | 22 | 0, 3, 5 |
| `n_accept_master` | num | 0.0 | 16 | 0 | 22 | 2, 1, 0 |
| `n_accept_femme_master` | num | 0.0 | 13 | 0 | 13 | 0, 6, 2 |
| `n_accept_autre` | num | 0.0 | 30 | 0 | 46 | 0, 1, 19 |
| `n_accept_femme_autre` | num | 0.0 | 21 | 0 | 22 | 0, 12, 1 |
| `n_accept_noninscri` | num | 0.0 | 47 | 0 | 98 | 1, 0, 3 |
| `n_accept_femme_noninscri` | num | 0.0 | 40 | 0 | 89 | 0, 1, 17 |
| `n_recrut_comp` | num | 55.6 | 39 | 0 | 65 | 3.0, 16.0, 0.0 |
| `rang_dernier` | num | 0.0 | 471 | 0 | 2797 | 10, 9, 49 |
| `pct_accept_femme` | num | 7.4 | 524 | 0 | 100 | 0.0, 20.0, 78.3 |
| `pct_accept_etab` | num | 7.4 | 541 | 0 | 100 | 0.0, 40.0, 20.0 |
| `pct_accept_acad` | num | 7.4 | 535 | 0 | 100 | 0.0, 100.0, 40.0 |
| `pct_accept_acad_reg` | num | 7.4 | 542 | 0 | 100 | 0.0, 100.0, 40.0 |
| `pct_accept_debut_pp` | num | 7.4 | 557 | 0 | 100 | 100.0, 40.0, 0.0 |
| `pct_accept_lg3` | num | 7.4 | 499 | 0 | 100 | 0.0, 40.0, 29.0 |
| `pct_accept_lp3` | num | 7.4 | 211 | 0 | 100 | 0.0, 20.0, 4.3 |
| `pct_accept_master` | num | 7.4 | 171 | 0 | 100 | 66.7, 50.0, 0.0 |
| `pct_accept_autre` | num | 7.4 | 199 | 0 | 100 | 0.0, 50.0, 27.5 |
| `pct_accept_noninscri` | num | 7.4 | 375 | 0 | 100 | 33.3, 0.0, 60.0 |
| `id_paysage` | txt | 0.0 | 115 |  |  | qUCQp, 7zzqc, xJdyB |
| `id_paysage_actuel` | txt | 0.0 | 113 |  |  | qUCQp, 7zzqc, xJdyB |
| `uo_lib_actuel` | txt | 0.0 | 113 |  |  | Nantes Université, Facultés libres de l'Ouest, Aix-Marseille Université |
| `disci_lib` | txt | 0.0 | 13 |  |  | Sciences humaines et sociales, Sciences de la vie, de la terre et de l'univers,  |
| `secteur_disci_lib` | txt | 0.0 | 46 |  |  | Sciences de l'éducation, Sciences de la vie, biologie, santé, Pluridisciplinaire |
| `acad` | txt | 0.0 | 30 |  |  | A17, A02, A01 |
| `acad_lib` | txt | 0.0 | 30 |  |  | Nantes, Aix-Marseille, Paris |
| `acad_reg` | txt | 0.0 | 17 |  |  | R52, R93, R11 |
| `acad_reg_lib` | txt | 0.0 | 17 |  |  | Pays de la Loire, Provence-Alpes-Côte d'Azur, Île-de-France |

## Alertes
- `n_recrut_comp` manquant à plus de 50 %