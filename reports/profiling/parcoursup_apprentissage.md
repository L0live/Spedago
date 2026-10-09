# parcoursup_apprentissage.csv

- Lignes : **39,032**
- Colonnes : **44**
- Colonnes UAI détectées : ['cod_uai']
- Valeurs de `session` : ['2022', '2023', '2024', '2025']
- Lignes dupliquées : 0
- Doublons sur `cod_uai` : 34491 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `session` | num | 0.0 | 4 | 2022 | 2025 | 2023, 2024, 2022 |
| `cod_uai` | txt | 0.0 | 4541 |  |  | 0340011C, 0660010C, 0660011D |
| `g_ea_lib_vx` | txt | 0.0 | 4752 |  |  | Lycée polyvalent Jean Moulin, Lycée François Arago, Lycée Jean Lurcat |
| `contrat_etab` | txt | 0.0 | 4 |  |  | Public, Privé sous contrat d'association, Privé hors contrat |
| `dep` | num | 0.0 | 102 | 1 | 978 | 034, 066, 042 |
| `dep_lib` | txt | 0.0 | 102 |  |  | Hérault, Pyrénées-Orientales, Loire |
| `region_etab_aff_id` | txt | 0.0 | 18 |  |  | R76, R84, R75 |
| `region_etab_aff` | txt | 0.0 | 18 |  |  | Occitanie, Auvergne-Rhône-Alpes, Nouvelle-Aquitaine |
| `acad_mies_id` | txt | 0.0 | 30 |  |  | A11, A10, A13 |
| `acad_mies` | txt | 0.0 | 30 |  |  | Montpellier, Lyon, Poitiers |
| `ville_etab` | txt | 0.0 | 1500 |  |  | Béziers, Perpignan, Saint-Etienne |
| `cod_aff_form` | num | 0.0 | 14559 | 2029 | 5.049e+04 | 25628, 25637, 25642 |
| `fili` | txt | 0.0 | 16 |  |  | 5_BTS, 13_Mention Complémentaire, 10_EFTS |
| `lib_for_voe_ins` | txt | 0.0 | 631 |  |  | BTS - Production - Electrotechnique - en apprentissage, BTS - Services - Comptab |
| `select_form` | num | 0.0 | 2 | 0 | 1 | True, False |
| `lib_comp_voe_ins` | txt | 0.0 | 17232 |  |  | Lycée polyvalent Jean Moulin - BTS - Production - Electrotechnique - en apprenti |
| `detail_forma` | txt | 99.7 | 64 |  |  | Animation du football, Formation Marine nationale (Bac +1) - Maintenance électri |
| `form_lib_voe_acc` | txt | 0.0 | 27 |  |  | BTS - Production, BTS - Services, Mention complémentaire |
| `fil_lib_voe_acc` | txt | 0.0 | 521 |  |  | Electrotechnique - en apprentissage, Comptabilité et gestion - en apprentissage, |
| `lien_form_psup` | txt | 6.3 | 22172 |  |  | https://dossier.parcoursup.fr/Candidats/public/fiches/afficherFicheFormation?g_t |
| `g_olocalisation_des_formations` | txt | 6.3 | 4505 |  |  | 43.3432, 3.23372, 42.695, 2.88619, 42.6923, 2.9089 |
| `capa_fin` | num | 0.0 | 130 | 0 | 1000 | 15, 18, 35 |
| `ges_can` | num | 0.0 | 2 | 0 | 1 | True, False |
| `voe_tot` | num | 0.0 | 994 | 0 | 7911 | 2, 0, 4 |
| `voe_tot_f` | num | 0.0 | 690 | 0 | 4099 | 0, 1, 2 |
| `nb_voe_ap_bg` | num | 0.0 | 361 | 0 | 2452 | 1, 0, 2 |
| `nb_voe_ap_bg_brs` | num | 0.0 | 153 | 0 | 647 | 0, 1, 2 |
| `nb_voe_ap_bt` | num | 0.0 | 465 | 0 | 2830 | 0, 1, 2 |
| `nb_voe_ap_bt_brs` | num | 0.0 | 246 | 0 | 1122 | 0, 1, 2 |
| `nb_voe_ap_bp` | num | 0.0 | 376 | 0 | 1350 | 0, 2, 1 |
| `nb_voe_ap_bp_brs` | num | 0.0 | 202 | 0 | 524 | 0, 1, 2 |
| `nb_voe_bp_app` | num | 0.0 | 62 | 0 | 79 | 0, 1, 2 |
| `nb_voe_ap_at` | num | 0.0 | 476 | 0 | 2351 | 1, 0, 4 |
| `prop_tot` | num | 0.0 | 97 | 0 | 372 | 0, 1, 2 |
| `prop_tot_bg` | num | 0.0 | 32 | 0 | 55 | 0, 1, 2 |
| `prop_tot_bg_brs` | num | 0.0 | 9 | 0 | 14 | 0, 1, 2 |
| `prop_tot_bt` | num | 0.0 | 38 | 0 | 63 | 0, 1, 2 |
| `prop_tot_bt_brs` | num | 0.0 | 18 | 0 | 24 | 0, 1, 3 |
| `prop_tot_bp` | num | 0.0 | 41 | 0 | 59 | 0, 1, 3 |
| `prop_tot_bp_brs` | num | 0.0 | 12 | 0 | 20 | 0, 1, 3 |
| `prop_tot_at` | num | 0.0 | 65 | 0 | 226 | 0, 1, 2 |
| `nb_rech_con` | num | 0.0 | 789 | 0 | 3296 | 2, 0, 3 |
| `nb_ref_classe` | num | 0.0 | 575 | 0 | 6697 | 0, 2, 3 |
| `nb_ref_place` | num | 0.0 | 95 | 0 | 4077 | 0, 2, 7 |

## Alertes
- `detail_forma` manquant à plus de 50 %