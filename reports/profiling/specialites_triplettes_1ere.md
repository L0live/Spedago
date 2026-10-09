# specialites_triplettes_1ere.csv

- Lignes : **11,337**
- Colonnes : **95**
- Colonnes UAI détectées : ['numero_etablissement']
- Valeurs de `rentree_scolaire` : ['2021', '2022', '2023', '2024', '2025']
- Lignes dupliquées : 0
- Doublons sur `numero_etablissement` : 9037 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `rentree_scolaire` | num | 0.0 | 5 | 2021 | 2025 | 2021, 2022, 2023 |
| `code_region_academique` | num | 0.0 | 19 | 0 | 18 | 1, 9, 18 |
| `code_region_insee` | num | 0.0 | 19 | 0 | 94 | 84, 32, 93 |
| `region_academique` | txt | 0.0 | 19 |  |  | AUVERGNE-RHONE-ALPES, HAUTS-DE-FRANCE, PROVENCE-ALPES-COTE D'AZUR |
| `code_acad` | num | 0.0 | 34 | 1 | 70 | 10, 20, 6 |
| `academie` | txt | 0.0 | 34 |  |  | LYON, AMIENS, CLERMONT-FERRAND |
| `code_dep` | num | 0.0 | 106 | 1 | 988 | 01, 02, 03 |
| `departement` | txt | 0.0 | 106 |  |  | AIN, AISNE, ALLIER |
| `code_commune` | num | 6.1 | 1117 | 1004 | 9.882e+04 | 01053, 01427, 02381 |
| `commune` | txt | 0.0 | 1117 |  |  | BOURG-EN-BRESSE, TREVOUX, HIRSON |
| `numero_etablissement` | txt | 0.0 | 2300 |  |  | 0010014K, 0010016M, 0011276G |
| `denomination_principale` | txt | 0.0 | 68 |  |  | LYCEE GENERAL ET TECHNOLOGIQUE, LYCEE POLYVALENT, LYCEE GENERAL PRIVE |
| `patronyme` | txt | 0.0 | 1715 |  |  | EDGAR QUINET, JOSEPH-MARIE CARRIAT, DU VAL DE SAONE |
| `secteur` | txt | 0.0 | 2 |  |  | PUBLIC, PRIVE SOUS CONTRAT |
| `effectif_total` | num | 0.1 | 485 | 5 | 649 | 245.0, 238.0, 332.0 |
| `effectif_total_filles` | num | 1.3 | 302 | 0 | 376 | 184.0, 98.0, 198.0 |
| `effectif_total_garcons` | num | 1.3 | 244 | 0 | 298 | 61.0, 140.0, 134.0 |
| `0105_humanites_litterature_et_philosophie_filles` | num | 29.0 | 109 | 0 | 147 | 67.0, 47.0, 24.0 |
| `0105_humanites_litterature_et_philosophie_garcons` | num | 29.0 | 35 | 0 | 49 | 6.0, 18.0, 7.0 |
| `0241_litterature_et_lca_latin_filles` | num | 6.5 | 18 | 0 | 29 | 9.0, 0.0, 5.0 |
| `0241_litterature_et_lca_latin_garcons` | num | 6.5 | 8 | 0 | 13 | 0.0, 5.0, 13.0 |
| `0242_litterature_et_lca_grec_filles` | num | 3.5 | 8 | 0 | 14 | 0.0, 7.0, 14.0 |
| `0242_litterature_et_lca_grec_garcons` | num | 3.5 | 4 | 0 | 7 | 0.0, 7.0, 5.0 |
| `0300_langues_litterature_et_cultures_etrangeres_et_regionales_filles` | num | 9.3 | 142 | 0 | 177 | 84.0, 39.0, 71.0 |
| `0300_langues_litterature_et_cultures_etrangeres_et_regionales_garcons` | num | 9.3 | 72 | 0 | 98 | 17.0, 31.0, 28.0 |
| `0439_hist_geo_geopolitique_sc_politiques_filles` | num | 6.8 | 141 | 0 | 197 | 69.0, 36.0, 57.0 |
| `0439_hist_geo_geopolitique_sc_politiques_garcons` | num | 6.8 | 85 | 0 | 101 | 28.0, 26.0, 36.0 |
| `0507_sciences_economiques_et_sociales_filles` | num | 4.4 | 159 | 0 | 188 | 80.0, 55.0, 91.0 |
| `0507_sciences_economiques_et_sociales_garcons` | num | 4.4 | 117 | 0 | 148 | 37.0, 48.0, 54.0 |
| `0613_mathematiques_filles` | num | 2.9 | 196 | 0 | 236 | 81.0, 57.0, 122.0 |
| `0613_mathematiques_garcons` | num | 2.9 | 203 | 0 | 269 | 38.0, 117.0, 88.0 |
| `0623_physique_chimie_filles` | num | 4.5 | 128 | 0 | 160 | 53.0, 34.0, 72.0 |
| `0623_physique_chimie_garcons` | num | 4.5 | 156 | 0 | 206 | 25.0, 84.0, 61.0 |
| `0629_sciences_de_la_vie_et_de_la_terre_filles` | num | 4.5 | 137 | 0 | 179 | 70.0, 36.0, 93.0 |
| `0629_sciences_de_la_vie_et_de_la_terre_garcons` | num | 4.5 | 95 | 0 | 115 | 21.0, 46.0, 41.0 |
| `0673_sciences_de_l_ingenieur_filles` | num | 20.6 | 23 | 0 | 29 | 8.0, 7.0, 0.0 |
| `0673_sciences_de_l_ingenieur_garcons` | num | 20.6 | 82 | 0 | 115 | 43.0, 40.0, 9.0 |
| `0747_numerique_et_sciences_informatiques_filles` | num | 32.8 | 32 | 0 | 47 | 0.0, 7.0, 13.0 |
| `0747_numerique_et_sciences_informatiques_garcons` | num | 32.8 | 78 | 0 | 102 | 0.0, 11.0, 19.0 |
| `0825_danse_filles` | num | 2.5 | 20 | 0 | 25 | 0.0, 6.0, 8.0 |
| `0825_danse_garcons` | num | 2.5 | 8 | 0 | 13 | 0.0, 8.0, 7.0 |
| `0832_musique_filles` | num | 4.9 | 29 | 0 | 41 | 0.0, 12.0, 9.0 |
| `0832_musique_garcons` | num | 4.9 | 18 | 0 | 25 | 0.0, 8.0, 5.0 |
| `0901_arts_plastiques_filles_39` | num | 17.3 | 57 | 0 | 66 | 5.0, 0.0, 11.0 |
| `0901_arts_plastiques_garcons_40` | num | 17.3 | 17 | 0 | 20 | 0.0, 5.0, 6.0 |
| `1087_educ_physique_pratique_cult_sportive_filles` | num | 3.2 | 28 | 0 | 36 | 0.0, 10.0, 5.0 |
| `1087_educ_physique_pratique_cult_sportive_garcons` | num | 3.2 | 51 | 0 | 68 | 0.0, 14.0, 10.0 |
| `2757_histoire_des_arts_filles` | num | 4.3 | 53 | 0 | 63 | 0.0, 12.0, 27.0 |
| `2757_histoire_des_arts_garcons` | num | 4.3 | 16 | 0 | 20 | 0.0, 6.0, 5.0 |
| `2785_theatre_filles` | num | 6.8 | 29 | 0 | 37 | 0.0, 7.0, 12.0 |
| `2785_theatre_garcons` | num | 6.8 | 11 | 0 | 15 | 0.0, 7.0, 6.0 |
| `2786_arts_du_cirque_filles` | num | 1.7 | 9 | 0 | 13 | 0.0, 12.0, 13.0 |
| `2786_arts_du_cirque_garcons` | num | 1.7 | 9 | 0 | 17 | 0.0, 5.0, 17.0 |
| `2852_cinema_audiovisuel_filles` | num | 3.0 | 47 | 0 | 70 | 0.0, 31.0, 13.0 |
| `2852_cinema_audiovisuel_garcons` | num | 3.0 | 27 | 0 | 36 | 0.0, 17.0, 9.0 |
| `3045_biologie_ecologie_filles` | num | 1.4 | 1 | 0 | 0 | 0.0 |
| `3045_biologie_ecologie_garcons` | num | 1.4 | 1 | 0 | 0 | 0.0 |
| `01_mathematiques_physique_chimie_sciences_de_la_vie_et_de_la_terre_filles` | num | 10.9 | 93 | 0 | 106 | 36.0, 24.0, 53.0 |
| `01_mathematiques_physique_chimie_sciences_de_la_vie_et_de_la_terre_garcons` | num | 10.9 | 76 | 0 | 115 | 14.0, 29.0, 20.0 |
| `02_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_so` | num | 48.1 | 45 | 0 | 69 | 19.0, 16.0, 12.0 |
| `02_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_s0` | num | 48.1 | 26 | 0 | 32 | 8.0, 10.0, 12.0 |
| `03_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_economiques_et_sociales_filles` | num | 53.3 | 50 | 0 | 63 | 15.0, 0.0, 5.0 |
| `03_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_economiques_et_sociales_garcons` | num | 53.3 | 45 | 0 | 60 | 6.0, 0.0, 11.0 |
| `04_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_sciences_economiques_et` | num | 64.9 | 35 | 0 | 44 | 8.0, 0.0, 19.0 |
| `04_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_sciences_economiques_et0` | num | 64.9 | 14 | 0 | 19 | 6.0, 0.0, 10.0 |
| `05_mathematiques_numerique_et_sciences_informatiques_physique_chimie_filles` | num | 45.0 | 18 | 0 | 27 | 0.0, 8.0, 6.0 |
| `05_mathematiques_numerique_et_sciences_informatiques_physique_chimie_garcons` | num | 45.0 | 54 | 0 | 63 | 0.0, 8.0, 10.0 |
| `06_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_langues_litt_et_cultures` | num | 69.5 | 34 | 0 | 45 | 5.0, 0.0, 16.0 |
| `06_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_langues_litt_et_culture0` | num | 69.5 | 10 | 0 | 13 | 0.0, 6.0, 5.0 |
| `07_mathematiques_physique_chimie_sciences_de_l_ingenieur_filles` | num | 23.2 | 22 | 0 | 29 | 6.0, 7.0, 0.0 |
| `07_mathematiques_physique_chimie_sciences_de_l_ingenieur_garcons` | num | 23.2 | 68 | 0 | 113 | 36.0, 27.0, 8.0 |
| `08_mathematiques_physique_chimie_sciences_economiques_et_sociales_filles` | num | 65.8 | 27 | 0 | 37 | 0.0, 8.0, 6.0 |
| `08_mathematiques_physique_chimie_sciences_economiques_et_sociales_garcons` | num | 65.8 | 47 | 0 | 56 | 0.0, 8.0, 11.0 |
| `09_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_economiques_et_sociales_filles` | num | 70.2 | 25 | 0 | 28 | 8.0, 0.0, 5.0 |
| `09_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_economiques_et_sociales_garcons` | num | 70.2 | 20 | 0 | 24 | 0.0, 5.0, 14.0 |
| `10_mathematiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_filles` | num | 75.2 | 21 | 0 | 32 | 7.0, 10.0, 0.0 |
| `10_mathematiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_garcons` | num | 75.2 | 17 | 0 | 22 | 6.0, 7.0, 0.0 |
| `11_hist_geo_geopolitique_sc_politiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la` | num | 73.4 | 21 | 0 | 29 | 0.0, 6.0, 7.0 |
| `11_hist_geo_geopolitique_sc_politiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la0` | num | 73.4 | 14 | 0 | 17 | 0.0, 5.0, 11.0 |
| `12_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_s` | num | 62.9 | 20 | 0 | 25 | 0.0, 10.0, 7.0 |
| `12_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_0` | num | 62.9 | 8 | 0 | 12 | 0.0, 5.0, 7.0 |
| `13_langues_litt_et_cultures_etra_et_r_mathematiques_physique_chimie_filles` | num | 73.3 | 14 | 0 | 18 | 10.0, 0.0, 9.0 |
| `13_langues_litt_et_cultures_etra_et_r_mathematiques_physique_chimie_garcons` | num | 73.3 | 23 | 0 | 26 | 5.0, 0.0, 9.0 |
| `14_hist_geo_geopolitique_sc_politiques_mathematiques_physique_chimie_filles` | num | 66.7 | 18 | 0 | 24 | 0.0, 5.0, 8.0 |
| `14_hist_geo_geopolitique_sc_politiques_mathematiques_physique_chimie_garcons` | num | 66.7 | 22 | 0 | 27 | 0.0, 5.0, 6.0 |
| `15_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_t` | num | 62.9 | 13 | 0 | 17 | 6.0, 0.0, 12.0 |
| `15_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_0` | num | 62.9 | 8 | 0 | 14 | 0.0, 5.0, 10.0 |
| `16_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_de_la_vie_et_de_la_terre_filles` | num | 61.8 | 7 | 0 | 10 | 0.0, 5.0, 6.0 |
| `16_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_de_la_vie_et_de_la_terre_garcons` | num | 61.8 | 6 | 0 | 10 | 0.0, 5.0, 8.0 |
| `17_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_de_la_vie_et_de_la_terre_filles` | num | 58.4 | 8 | 0 | 15 | 0.0, 7.0, 6.0 |
| `17_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_de_la_vie_et_de_la_terre_garcons` | num | 58.4 | 5 | 0 | 8 | 0.0, 8.0, 5.0 |
| `18_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_mathematiques_filles` | num | 59.3 | 9 | 0 | 17 | 0.0, 5.0, 17.0 |
| `18_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_mathematiques_garcons` | num | 59.3 | 6 | 0 | 9 | 0.0, 6.0, 8.0 |
| `autres_combinaisons_filles` | num | 27.6 | 133 | 0 | 169 | 71.0, 11.0, 43.0 |
| `autres_combinaisons_garcons` | num | 27.6 | 81 | 0 | 97 | 9.0, 17.0, 42.0 |

## Alertes
- `03_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_economiques_et_sociales_filles` manquant à plus de 50 %
- `03_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_economiques_et_sociales_garcons` manquant à plus de 50 %
- `04_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_sciences_economiques_et` manquant à plus de 50 %
- `04_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_sciences_economiques_et0` manquant à plus de 50 %
- `06_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_langues_litt_et_cultures` manquant à plus de 50 %
- `06_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_langues_litt_et_culture0` manquant à plus de 50 %
- `08_mathematiques_physique_chimie_sciences_economiques_et_sociales_filles` manquant à plus de 50 %
- `08_mathematiques_physique_chimie_sciences_economiques_et_sociales_garcons` manquant à plus de 50 %
- `09_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_economiques_et_sociales_filles` manquant à plus de 50 %
- `09_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_economiques_et_sociales_garcons` manquant à plus de 50 %
- `10_mathematiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_filles` manquant à plus de 50 %
- `10_mathematiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_garcons` manquant à plus de 50 %
- `11_hist_geo_geopolitique_sc_politiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la` manquant à plus de 50 %
- `11_hist_geo_geopolitique_sc_politiques_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la0` manquant à plus de 50 %
- `12_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_s` manquant à plus de 50 %
- `12_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_0` manquant à plus de 50 %
- `13_langues_litt_et_cultures_etra_et_r_mathematiques_physique_chimie_filles` manquant à plus de 50 %
- `13_langues_litt_et_cultures_etra_et_r_mathematiques_physique_chimie_garcons` manquant à plus de 50 %
- `14_hist_geo_geopolitique_sc_politiques_mathematiques_physique_chimie_filles` manquant à plus de 50 %
- `14_hist_geo_geopolitique_sc_politiques_mathematiques_physique_chimie_garcons` manquant à plus de 50 %
- `15_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_t` manquant à plus de 50 %
- `15_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_0` manquant à plus de 50 %
- `16_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_de_la_vie_et_de_la_terre_filles` manquant à plus de 50 %
- `16_langues_litt_et_cultures_etra_et_r_mathematiques_sciences_de_la_vie_et_de_la_terre_garcons` manquant à plus de 50 %
- `17_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_de_la_vie_et_de_la_terre_filles` manquant à plus de 50 %
- `17_hist_geo_geopolitique_sc_politiques_mathematiques_sciences_de_la_vie_et_de_la_terre_garcons` manquant à plus de 50 %
- `18_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_mathematiques_filles` manquant à plus de 50 %
- `18_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_mathematiques_garcons` manquant à plus de 50 %