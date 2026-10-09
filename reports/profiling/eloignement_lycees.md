# eloignement_lycees.csv

- Lignes : **24,883**
- Colonnes : **11**
- Colonnes UAI détectées : ['uai']
- Valeurs de `rentree_scolaire` : ['2020', '2021', '2022', '2023', '2024', '2025']
- Lignes dupliquées : 0
- Doublons sur `uai` : 20430 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `rentree_scolaire` | num | 0.0 | 6 | 2020 | 2025 | 2022, 2023, 2024 |
| `uai` | txt | 0.0 | 4453 |  |  | 0930965U, 0331460H, 0410899E |
| `code_departement` | num | 0.0 | 101 | 1 | 976 | 93, 33, 41 |
| `departement` | txt | 0.0 | 101 |  |  | SEINE-SAINT-DENIS, GIRONDE, LOIR-ET-CHER |
| `code_academie` | num | 0.0 | 30 | 1 | 70 | 24, 4, 18 |
| `academie` | txt | 0.0 | 30 |  |  | CRETEIL, BORDEAUX, ORLEANS-TOURS |
| `code_region` | num | 0.0 | 18 | 1 | 18 | 10, 15, 4 |
| `code_region_insee` | num | 0.0 | 18 | 1 | 94 | 11, 75, 24 |
| `region` | txt | 0.0 | 18 |  |  | ILE-DE-FRANCE, NOUVELLE-AQUITAINE, CENTRE-VAL DE LOIRE |
| `patronyme` | txt | 0.0 | 7560 |  |  | LYCÉE GÉNÉRAL PRIVÉ HENRI MATISSE, LYCÉE PROFESSIONNEL LES CHARTRONS, LYCÉE POLY |
| `indice_eloignement` | num | 0.0 | 563 | 91.8 | 282.1 | 97.4, 97.5, 97.6 |

## Alertes
- aucune