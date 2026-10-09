# ips_lycees_2016_2022.csv

- Lignes : **21,777**
- Colonnes : **15**
- Colonnes UAI détectées : ['uai']
- Valeurs de `rentree_scolaire` : ['2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
- Lignes dupliquées : 0
- Doublons sur `uai` : 18080 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `rentree_scolaire` | txt | 0.0 | 6 |  |  | 2016-2017, 2018-2019, 2019-2020 |
| `academie` | txt | 0.0 | 32 |  |  | LYON, AMIENS, CLERMONT-FERRAND |
| `code_du_departement` | num | 0.4 | 99 | 1 | 976 | 1.0, 2.0, 3.0 |
| `departement` | txt | 0.0 | 101 |  |  | AIN, AISNE, ALLIER |
| `uai` | txt | 0.0 | 3697 |  |  | 0010010F, 0010034G, 0010070W |
| `nom_de_l_etablissment` | txt | 0.0 | 4022 |  |  | LYCEE GENERAL ET TECHNOLOGIQUE DU BUGEY, LYCEE POLYVALENT PAUL PAINLEVE, LYCEE G |
| `code_insee_de_la_commune` | num | 0.4 | 1408 | 1004 | 9.78e+04 | 1034.0, 1283.0, 1053.0 |
| `nom_de_la_commune` | txt | 0.0 | 1431 |  |  | BELLEY, OYONNAX, BOURG EN BRESSE |
| `secteur` | txt | 0.0 | 2 |  |  | public, privé sous contrat |
| `type_de_lycee` | txt | 0.0 | 3 |  |  | LEGT, LPO, LP |
| `ips_voie_gt` | num | 32.1 | 896 | 51.9 | 159.1 | 109.5, 92.2, 126.5 |
| `ips_voie_pro` | num | 42.3 | 701 | 47.3 | 136.5 | 73.4, 84.6, 83.7 |
| `ips_ensemble_gt_pro` | num | 0.0 | 962 | 49.5 | 159.1 | 109.5, 86.5, 126.5 |
| `ecart_type_de_l_ips_voie_gt` | num | 66.0 | 279 | 0 | 49.2 | 28.8, 35.1, 36.0 |
| `ecart_type_de_l_ips_voie_pro` | num | 71.2 | 249 | 0 | 49.5 | 31.2, 28.3, 33.9 |

## Alertes
- `ecart_type_de_l_ips_voie_gt` manquant à plus de 50 %
- `ecart_type_de_l_ips_voie_pro` manquant à plus de 50 %