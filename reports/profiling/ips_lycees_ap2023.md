# ips_lycees_ap2023.csv

- Lignes : **10,905**
- Colonnes : **48**
- Colonnes UAI détectées : ['uai']
- Valeurs de `rentree_scolaire` : ['2023-2024', '2024-2025', '2025-2026']
- Lignes dupliquées : 0
- Doublons sur `uai` : 7217 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `rentree_scolaire` | txt | 0.0 | 3 |  |  | 2023-2024, 2024-2025, 2025-2026 |
| `code_region` | num | 0.0 | 22 | 1 | 18 | 01, 09, 18 |
| `code_region_insee` | num | 0.0 | 19 | 0 | 94 | 84, 32, 93 |
| `region_academique` | txt | 0.0 | 22 |  |  | AUVERGNE-RHONE-ALPES, HAUTS-DE-FRANCE, PROVENCE-ALPES-COTE D'AZUR |
| `code_academie` | num | 0.0 | 34 | 1 | 70 | 10, 20, 6 |
| `academie` | txt | 0.0 | 34 |  |  | LYON, AMIENS, CLERMONT-FERRAND |
| `code_du_departement` | num | 0.0 | 107 | 1 | 987 | 01, 02, 03 |
| `departement` | txt | 0.0 | 107 |  |  | AIN, AISNE, ALLIER |
| `code_insee_de_la_commune` | num | 0.0 | 1434 | 1004 | 9.913e+04 | 01034, 01160, 01427 |
| `nom_de_la_commune` | txt | 0.0 | 1426 |  |  | BELLEY, FERNEY VOLTAIRE, TREVOUX |
| `uai` | txt | 0.0 | 3688 |  |  | 0010069V, 0010072Y, 0011276G |
| `nom_de_l_etablissement` | txt | 0.0 | 3755 |  |  | LYCEE GENERAL ET TECHNOLOGIQUE PRIVE ENSEMBLE SCOLAIRE LAMARTINE, LYCEE POLYVALE |
| `secteur` | txt | 0.0 | 2 |  |  | privé sous contrat, public |
| `type_de_lycee` | txt | 0.0 | 3 |  |  | LEGT, LPO, LP |
| `ips_voie_gt` | num | 31.5 | 845 | 53.7 | 162.6 | 118.7, 123.8, 128.4 |
| `ips_voie_pro` | num | 42.7 | 638 | 58.8 | 151.2 | 94.7, 86.5, 97.9 |
| `ips_post_bac` | num | 44.5 | 829 | 58.2 | 159.4 | 94.1, 80.4, 85.6 |
| `ips_etab` | num | 0.0 | 914 | 58.8 | 162.6 | 118.7, 121.3, 127.6 |
| `ecart_type_voie_gt` | num | 31.5 | 273 | 6.7 | 45.9 | 29.7, 34.3, 32.9 |
| `ecart_type_voie_pro` | num | 42.7 | 215 | 12.6 | 45.2 | 26.6, 25.8, 31.5 |
| `ecart_type_etablissement` | num | 0.0 | 265 | 10.3 | 45.9 | 29.7, 34.7, 33.3 |
| `ips_national_legt` | num | 0.4 | 3 | 118.5 | 120.2 | 118.5, 119.6, 120.2 |
| `ips_national_lpo` | num | 0.4 | 3 | 103.5 | 104.4 | 103.5, 104.2, 104.4 |
| `ips_national_lp` | num | 0.4 | 3 | 88.9 | 89.9 | 88.9, 89.5, 89.9 |
| `ips_national_legt_prive` | num | 0.4 | 3 | 132.4 | 134.7 | 132.4, 134.0, 134.7 |
| `ips_national_legt_public` | num | 0.4 | 3 | 113.9 | 115.2 | 113.9, 114.7, 115.2 |
| `ips_national_lpo_prive` | num | 0.4 | 3 | 116.2 | 117.7 | 116.2, 117.4, 117.7 |
| `ips_national_lpo_public` | num | 0.4 | 3 | 101.1 | 102 | 101.1, 101.7, 102.0 |
| `ips_national_lp_prive` | num | 0.4 | 3 | 103.8 | 105.5 | 103.8, 104.7, 105.5 |
| `ips_national_lp_public` | num | 0.4 | 3 | 85.3 | 86.3 | 85.3, 85.9, 86.3 |
| `ips_academique_legt` | num | 0.0 | 74 | 70.9 | 137.7 | 121.1, 110.1, 115.5 |
| `ips_academique_lpo` | num | 0.0 | 77 | 70 | 115.5 | 103.8, 95.3, 103.9 |
| `ips_academique_lp` | num | 0.0 | 68 | 58.8 | 98.2 | 92.8, 86.0, 91.8 |
| `ips_academique_legt_prive` | num | 0.3 | 76 | 109.9 | 150.3 | 135.4, 125.2, 123.7 |
| `ips_academique_legt_public` | num | 0.0 | 77 | 70.9 | 131.4 | 114.1, 105.7, 112.8 |
| `ips_academique_lpo_prive` | num | 10.7 | 67 | 90.5 | 137.3 | 118.0, 108.2, 109.2 |
| `ips_academique_lpo_public` | num | 0.0 | 81 | 70 | 115.5 | 102.9, 95.3, 103.3 |
| `ips_academique_lp_prive` | num | 4.2 | 71 | 81.7 | 129.9 | 108.6, 100.8, 103.0 |
| `ips_academique_lp_public` | num | 0.0 | 69 | 58.8 | 93.5 | 84.3, 83.2, 88.2 |
| `ips_departemental_legt` | num | 0.0 | 182 | 70.9 | 138 | 120.4, 104.0, 111.8 |
| `ips_departemental_lpo` | num | 0.3 | 173 | 70 | 119.4 | 106.8, 95.1, 95.3 |
| `ips_departemental_lp` | num | 0.0 | 163 | 58.8 | 106.5 | 94.0, 84.4, 89.9 |
| `ips_departemental_legt_prive` | num | 2.3 | 184 | 100.5 | 154.9 | 127.3, 116.7, 117.6 |
| `ips_departemental_legt_public` | num | 0.6 | 182 | 70.9 | 131.4 | 119.2, 100.9, 111.0 |
| `ips_departemental_lpo_prive` | num | 25.7 | 142 | 90.5 | 141.9 | 129.1, 98.3, 117.0 |
| `ips_departemental_lpo_public` | num | 0.3 | 168 | 70 | 118.4 | 105.2, 95.1, 95.2 |
| `ips_departemental_lp_prive` | num | 10.7 | 174 | 73.1 | 134.1 | 105.5, 97.0, 97.5 |
| `ips_departemental_lp_public` | num | 0.0 | 154 | 58.8 | 98.8 | 89.2, 80.9, 85.5 |

## Alertes
- aucune