# annuaire_lycees.csv

- Lignes : **5,644**
- Colonnes : **14**
- Colonnes UAI détectées : ['identifiant_de_l_etablissement']
- Lignes dupliquées : 1
- Doublons sur `identifiant_de_l_etablissement` : 38 (attendu > 0 si plusieurs années/formations par UAI)

| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |
|---|---|---|---|---|---|---|
| `identifiant_de_l_etablissement` | txt | 0.0 | 5606 |  |  | 0930126G, 0910824B, 0671779V |
| `nom_etablissement` | txt | 0.0 | 4946 |  |  | Lycée polyvalent Auguste Blanqui, Lycée du Sacré-Coeur, Lycée professionnel agri |
| `statut_public_prive` | txt | 0.1 | 2 |  |  | Public, Privé |
| `nom_commune` | txt | 0.0 | 1808 |  |  | Saint-Ouen, La Ville-du-Bois, Erstein |
| `code_departement` | num | 0.0 | 107 | 1 | 988 | 093, 091, 067 |
| `libelle_academie` | txt | 0.0 | 34 |  |  | Créteil, Versailles, Strasbourg |
| `code_bassin_formation` | num | 33.1 | 350 | 1000 | 7.076e+04 | 24931, 25025, 15001 |
| `libelle_bassin_formation` | txt | 33.1 | 350 |  |  | 93 BASSIN 1 (DIST. 1 ET 2), 091F-CENTRE ESSONNE, STRASBOURG |
| `latitude` | num | 0.8 | 4884 | -22.3 | 51.05 | 48.90303260775702, 48.660190289637285, 48.42036023531576 |
| `longitude` | num | 0.8 | 4884 | -63.08 | 167.3 | 2.333941143279612, 2.2630038735938567, 7.6504439331168115 |
| `etat` | txt | 0.0 | 1 |  |  | OUVERT |
| `voie_generale` | num | 26.3 | 2 | 0 | 1 | 1.0, 0.0 |
| `code_nature` | num | 0.0 | 15 | 300 | 400 | 306, 300, 320 |
| `libelle_nature` | txt | 0.0 | 15 |  |  | LYCEE POLYVALENT, LYCEE ENSEIGNT GENERAL ET TECHNOLOGIQUE, LYCEE PROFESSIONNEL |

## Alertes
- valeurs négatives dans `latitude`
- valeurs négatives dans `longitude`