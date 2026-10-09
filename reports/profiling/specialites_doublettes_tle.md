# specialites_doublettes_tle.csv

- Lignes : **13,548**
- Colonnes : **89**
- Colonnes UAI détectées : ['numero_etablissement']
- Valeurs de `rentree_scolaire` : ['2020', '2021', '2022', '2023', '2024', '2025']
- Lignes dupliquées : 0
- Doublons sur `numero_etablissement` : 11245 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `rentree_scolaire` | num | 0.0 | 6 | 2020 | 2025 | 2020, 2021, 2022 |
| `code_regacad` | num | 0.0 | 19 | 0 | 18 | 0, 1, 2 |
| `code_region_insee` | num | 0.0 | 19 | 0 | 94 | 0, 84, 27 |
| `region_academique` | txt | 0.0 | 19 |  |  | OUTRE-MER HORS REGIONS ACADEMIQUES, AUVERGNE-RHONE-ALPES, BOURGOGNE-FRANCHE-COMT |
| `code_acad` | num | 0.0 | 34 | 1 | 70 | 40, 41, 6 |
| `academie` | txt | 0.0 | 34 |  |  | NOUVELLE CALEDONIE, POLYNESIE FRANCAISE, CLERMONT-FERRAND |
| `code_dep` | num | 0.0 | 106 | 1 | 988 | 988, 987, 03 |
| `departement` | txt | 0.0 | 106 |  |  | NOUVELLE CALEDONIE, POLYNESIE FRANCAISE, ALLIER |
| `code_commune` | num | 6.4 | 1116 | 1004 | 9.882e+04 | 98805, 98818, 98821 |
| `commune` | txt | 0.0 | 1116 |  |  | DUMBEA, NOUMEA, PAITA |
| `numero_etablissement` | txt | 0.0 | 2303 |  |  | 9830557N, 9830002K, 9830003L |
| `denomination_principale` | txt | 0.0 | 68 |  |  | LYCEE GENERAL ET TECHNOLOGIQUE, LYCEE POLYVALENT, LYCEE POLYVALENT PRIVE |
| `patronyme` | txt | 0.1 | 1705 |  |  | DICK UKEIWE, LA PEROUSE, JULES GARNIER |
| `secteur` | txt | 0.0 | 2 |  |  | PUBLIC, PRIVE SOUS CONTRAT |
| `effectif_total` | num | 0.1 | 487 | 5 | 658 | 255.0, 317.0, 97.0 |
| `effectif_total_filles` | num | 1.6 | 302 | 0 | 383 | 167.0, 177.0, 46.0 |
| `effectif_total_garcons` | num | 1.6 | 241 | 0 | 299 | 88.0, 140.0, 51.0 |
| `0105_humanites_litterature_et_philosophie_filles` | num | 54.9 | 73 | 0 | 118 | 12.0, 25.0, 24.0 |
| `0105_humanites_litterature_et_philosophie_garcons` | num | 54.9 | 22 | 0 | 31 | 8.0, 6.0, 5.0 |
| `0241_litterature_et_lca_latin_filles` | num | 5.7 | 11 | 0 | 20 | 0.0, 7.0, 18.0 |
| `0241_litterature_et_lca_latin_garcons` | num | 5.7 | 5 | 0 | 12 | 0.0, 8.0, 5.0 |
| `0242_litterature_et_lca_grec_filles` | num | 3.0 | 4 | 0 | 12 | 0.0, 6.0, 12.0 |
| `0242_litterature_et_lca_grec_garcons` | num | 3.0 | 2 | 0 | 5 | 0.0, 5.0 |
| `0300_langues_litterature_et_cultures_etrangeres_et_regionales_filles` | num | 25.3 | 103 | 0 | 116 | 31.0, 42.0, 7.0 |
| `0300_langues_litterature_et_cultures_etrangeres_et_regionales_garcons` | num | 25.3 | 45 | 0 | 51 | 11.0, 13.0, 6.0 |
| `0439_hist_geo_geopolitique_sc_politiques_filles` | num | 11.6 | 113 | 0 | 151 | 40.0, 50.0, 10.0 |
| `0439_hist_geo_geopolitique_sc_politiques_garcons` | num | 11.6 | 63 | 0 | 76 | 19.0, 30.0, 6.0 |
| `0507_sciences_economiques_et_sociales_filles` | num | 7.4 | 129 | 0 | 158 | 69.0, 56.0, 8.0 |
| `0507_sciences_economiques_et_sociales_garcons` | num | 7.4 | 97 | 0 | 112 | 20.0, 39.0, 7.0 |
| `0613_mathematiques_filles` | num | 7.4 | 136 | 0 | 193 | 47.0, 51.0, 17.0 |
| `0613_mathematiques_garcons` | num | 7.4 | 174 | 0 | 221 | 35.0, 68.0, 32.0 |
| `0623_physique_chimie_filles` | num | 8.5 | 109 | 0 | 126 | 35.0, 54.0, 26.0 |
| `0623_physique_chimie_garcons` | num | 8.5 | 128 | 0 | 179 | 31.0, 58.0, 30.0 |
| `0629_sciences_de_la_vie_et_de_la_terre_filles` | num | 13.3 | 96 | 0 | 124 | 39.0, 54.0, 19.0 |
| `0629_sciences_de_la_vie_et_de_la_terre_garcons` | num | 13.3 | 61 | 0 | 76 | 20.0, 40.0, 13.0 |
| `0747_numerique_et_sciences_informatiques_filles` | num | 42.9 | 15 | 0 | 25 | 7.0, 6.0, 0.0 |
| `0747_numerique_et_sciences_informatiques_garcons` | num | 42.9 | 44 | 0 | 57 | 31.0, 5.0, 8.0 |
| `0825_danse_filles` | num | 2.7 | 16 | 0 | 19 | 0.0, 9.0, 14.0 |
| `0825_danse_garcons` | num | 2.7 | 6 | 0 | 12 | 0.0, 12.0, 5.0 |
| `0832_musique_filles` | num | 6.0 | 20 | 0 | 27 | 0.0, 8.0, 10.0 |
| `0832_musique_garcons` | num | 6.0 | 15 | 0 | 19 | 0.0, 5.0, 6.0 |
| `0901_arts_plastiques_filles_37` | num | 17.9 | 49 | 0 | 56 | 0.0, 14.0, 8.0 |
| `0901_arts_plastiques_garcons_38` | num | 17.9 | 16 | 0 | 34 | 0.0, 6.0, 5.0 |
| `1087_educ_physique_pratique_cult_sportive_filles` | num | 3.4 | 24 | 0 | 39 | 0.0, 11.0, 6.0 |
| `1087_educ_physique_pratique_cult_sportive_garcons` | num | 3.4 | 40 | 0 | 48 | 0.0, 15.0, 22.0 |
| `2757_histoire_des_arts_filles` | num | 5.3 | 40 | 0 | 48 | 21.0, 0.0, 16.0 |
| `2757_histoire_des_arts_garcons` | num | 5.3 | 13 | 0 | 20 | 7.0, 0.0, 6.0 |
| `2785_theatre_filles` | num | 8.0 | 24 | 0 | 33 | 0.0, 12.0, 7.0 |
| `2785_theatre_garcons` | num | 8.0 | 9 | 0 | 12 | 0.0, 5.0, 7.0 |
| `2786_arts_du_cirque_filles` | num | 1.9 | 7 | 0 | 13 | 0.0, 8.0, 11.0 |
| `2786_arts_du_cirque_garcons` | num | 1.9 | 6 | 0 | 11 | 0.0, 6.0, 5.0 |
| `2852_cinema_audiovisuel_filles` | num | 4.0 | 38 | 0 | 54 | 0.0, 13.0, 18.0 |
| `2852_cinema_audiovisuel_garcons` | num | 4.0 | 24 | 0 | 34 | 0.0, 12.0, 9.0 |
| `3045_biologie_ecologie_filles` | num | 1.7 | 4 | 0 | 13 | 0.0, 8.0, 13.0 |
| `3045_biologie_ecologie_garcons` | num | 1.7 | 3 | 0 | 11 | 0.0, 11.0, 5.0 |
| `4806_sciences_de_l_ingenieur_et_sc_physiques_filles` | num | 22.6 | 10 | 0 | 13 | 0.0, 7.0, 5.0 |
| `4806_sciences_de_l_ingenieur_et_sc_physiques_garcons` | num | 22.6 | 36 | 0 | 69 | 0.0, 5.0, 6.0 |
| `0001_mathematiques_physique_chimie_filles` | num | 24.7 | 73 | 0 | 115 | 12.0, 27.0, 9.0 |
| `0001_mathematiques_physique_chimie_garcons` | num | 24.7 | 112 | 0 | 130 | 15.0, 43.0, 19.0 |
| `0002_hist_geo_geopolitique_sc_politiques_sciences_economiques_et_sociales_filles` | num | 25.7 | 67 | 0 | 87 | 20.0, 25.0, 27.0 |
| `0002_hist_geo_geopolitique_sc_politiques_sciences_economiques_et_sociales_garcons` | num | 25.7 | 47 | 0 | 55 | 12.0, 16.0, 22.0 |
| `0003_physique_chimie_sciences_de_la_vie_et_de_la_terre_filles` | num | 41.0 | 58 | 0 | 74 | 17.0, 26.0, 14.0 |
| `0003_physique_chimie_sciences_de_la_vie_et_de_la_terre_garcons` | num | 41.0 | 34 | 0 | 50 | 6.0, 14.0, 8.0 |
| `0004_mathematiques_sciences_de_la_vie_et_de_la_terre_filles` | num | 61.1 | 39 | 0 | 62 | 14.0, 15.0, 21.0 |
| `0004_mathematiques_sciences_de_la_vie_et_de_la_terre_garcons` | num | 61.1 | 31 | 0 | 39 | 10.0, 12.0, 17.0 |
| `0005_mathematiques_sciences_economiques_et_sociales_filles` | num | 50.1 | 42 | 0 | 52 | 5.0, 14.0, 12.0 |
| `0005_mathematiques_sciences_economiques_et_sociales_garcons` | num | 50.1 | 47 | 0 | 60 | 5.0, 15.0, 7.0 |
| `0006_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_filles` | num | 62.2 | 42 | 0 | 48 | 13.0, 0.0, 7.0 |
| `0006_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_garcons` | num | 62.2 | 21 | 0 | 24 | 5.0, 0.0, 7.0 |
| `0007_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_filles` | num | 70.0 | 34 | 0 | 41 | 0.0, 13.0, 14.0 |
| `0007_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_garcons` | num | 70.0 | 14 | 0 | 20 | 0.0, 7.0, 6.0 |
| `0008_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_filles` | num | 72.6 | 32 | 0 | 48 | 8.0, 7.0, 6.0 |
| `0008_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_garcons` | num | 72.6 | 12 | 0 | 15 | 0.0, 6.0, 5.0 |
| `0009_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_filles` | num | 71.8 | 27 | 0 | 31 | 5.0, 21.0, 9.0 |
| `0009_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_garcons` | num | 71.8 | 17 | 0 | 20 | 9.0, 6.0, 5.0 |
| `0010_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_filles` | num | 66.3 | 21 | 0 | 31 | 5.0, 0.0, 8.0 |
| `0010_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_garcons` | num | 66.3 | 5 | 0 | 8 | 0.0, 5.0, 6.0 |
| `0011_mathematiques_numerique_et_sciences_informatiques_filles` | num | 42.2 | 9 | 0 | 14 | 0.0, 5.0, 8.0 |
| `0011_mathematiques_numerique_et_sciences_informatiques_garcons` | num | 42.2 | 31 | 0 | 36 | 7.0, 0.0, 14.0 |
| `0012_humanites_litterature_et_philosophie_sciences_economiques_et_sociales_filles` | num | 65.1 | 21 | 0 | 33 | 7.0, 0.0, 6.0 |
| `0012_humanites_litterature_et_philosophie_sciences_economiques_et_sociales_garcons` | num | 65.1 | 8 | 0 | 18 | 0.0, 5.0, 6.0 |
| `0013_hist_geo_geopolitique_sc_politiques_mathematiques_filles` | num | 69.9 | 22 | 0 | 25 | 0.0, 9.0, 10.0 |
| `0013_hist_geo_geopolitique_sc_politiques_mathematiques_garcons` | num | 69.9 | 16 | 0 | 19 | 0.0, 7.0, 6.0 |
| `0014_mathematiques_sciences_inge_et_phy_filles` | num | 22.3 | 8 | 0 | 11 | 0.0, 5.0, 6.0 |
| `0014_mathematiques_sciences_inge_et_phy_garcons` | num | 22.3 | 31 | 0 | 47 | 0.0, 5.0, 6.0 |
| `0015_hist_geo_geopolitique_sc_politiques_sciences_de_la_vie_et_de_la_terre_filles` | num | 67.3 | 11 | 0 | 20 | 0.0, 9.0, 6.0 |
| `0015_hist_geo_geopolitique_sc_politiques_sciences_de_la_vie_et_de_la_terre_garcons` | num | 67.3 | 10 | 0 | 14 | 0.0, 11.0, 5.0 |
| `autres_combinaisons_filles` | num | 44.6 | 102 | 0 | 144 | 43.0, 29.0, 8.0 |
| `autres_combinaisons_garcons` | num | 44.6 | 55 | 0 | 63 | 27.0, 18.0, 8.0 |

## Alertes
- `0105_humanites_litterature_et_philosophie_filles` manquant à plus de 50 %
- `0105_humanites_litterature_et_philosophie_garcons` manquant à plus de 50 %
- `0004_mathematiques_sciences_de_la_vie_et_de_la_terre_filles` manquant à plus de 50 %
- `0004_mathematiques_sciences_de_la_vie_et_de_la_terre_garcons` manquant à plus de 50 %
- `0005_mathematiques_sciences_economiques_et_sociales_filles` manquant à plus de 50 %
- `0005_mathematiques_sciences_economiques_et_sociales_garcons` manquant à plus de 50 %
- `0006_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_filles` manquant à plus de 50 %
- `0006_langues_litt_et_cultures_etra_et_r_sciences_economiques_et_sociales_garcons` manquant à plus de 50 %
- `0007_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_filles` manquant à plus de 50 %
- `0007_hist_geo_geopolitique_sc_politiques_langues_litt_et_cultures_etra_et_r_garcons` manquant à plus de 50 %
- `0008_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_filles` manquant à plus de 50 %
- `0008_hist_geo_geopolitique_sc_politiques_humanites_litterature_et_philosophie_garcons` manquant à plus de 50 %
- `0009_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_filles` manquant à plus de 50 %
- `0009_sciences_economiques_et_sociales_sciences_de_la_vie_et_de_la_terre_garcons` manquant à plus de 50 %
- `0010_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_filles` manquant à plus de 50 %
- `0010_humanites_litterature_et_philosophie_langues_litt_et_cultures_etra_et_r_garcons` manquant à plus de 50 %
- `0012_humanites_litterature_et_philosophie_sciences_economiques_et_sociales_filles` manquant à plus de 50 %
- `0012_humanites_litterature_et_philosophie_sciences_economiques_et_sociales_garcons` manquant à plus de 50 %
- `0013_hist_geo_geopolitique_sc_politiques_mathematiques_filles` manquant à plus de 50 %
- `0013_hist_geo_geopolitique_sc_politiques_mathematiques_garcons` manquant à plus de 50 %
- `0015_hist_geo_geopolitique_sc_politiques_sciences_de_la_vie_et_de_la_terre_filles` manquant à plus de 50 %
- `0015_hist_geo_geopolitique_sc_politiques_sciences_de_la_vie_et_de_la_terre_garcons` manquant à plus de 50 %