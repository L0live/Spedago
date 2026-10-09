# Piste B — offre et dispersion des spécialités par lycée

Sources DEPP (1re : triplettes 2021-2025 ; terminale : doublettes 2020-2025), IPS voie GT, indice d'éloignement.

## 1. Contrôles sur les sources

- 1re : 20 spécialités, 19 combinaisons (dont « autres ») ; paires filles/garçons incohérentes : 0
- tle : 20 spécialités, 16 combinaisons (dont « autres ») ; paires filles/garçons incohérentes : 0
- Lignes exclues car effectif total masqué : 26
- Somme publiée > effectif : 0 lignes (attendu 0 : partition)
- Jointure IPS (2025) : 99.4% des lycées ; éloignement (2025) : 97.9%
- IPS absent pour la rentrée 2022 (trou entre les deux séries DEPP) et rupture de série en 2023 : pas de comparaison de niveaux d'IPS dans le temps.

## 1bis. Validation du proxy : lycées « neutres » simulés (rentrée 2025)

Même taille et sexe-ratio que 1 000 lycées réels tirés au hasard, combinaisons tirées selon la répartition nationale, secret primaire seul. Si l'observé ≈ simulé, la part non publiée ne serait qu'un artefact de taille.

**1re** (corrélation de rang observé/simulé : 0.65)

| taille   |   sim_neutre |   observe |   ratio |
|:---------|-------------:|----------:|--------:|
| <60      |        0.45  |     0.739 |   1.642 |
| 60-119   |        0.268 |     0.519 |   1.939 |
| 120-199  |        0.178 |     0.399 |   2.235 |
| 200-299  |        0.116 |     0.314 |   2.708 |
| 300+     |        0.08  |     0.213 |   2.676 |

**tle** (corrélation de rang observé/simulé : 0.76)

| taille   |   sim_neutre |   observe |   ratio |
|:---------|-------------:|----------:|--------:|
| <60      |        0.581 |     1     |   1.72  |
| 60-119   |        0.243 |     0.571 |   2.349 |
| 120-199  |        0.13  |     0.344 |   2.643 |
| 200-299  |        0.084 |     0.231 |   2.737 |
| 300+     |        0.062 |     0.158 |   2.567 |

**Attention : cette simulation est biaisée** (parts nationales calculées sur les seules cases publiées, ce qui sous-représente les combinaisons rares et sous-estime le masquage mécanique). Version corrigée dans `reports/piste_B_robustesse.md` : l'observé y est proche du mécanique dans les petits et moyens lycées (ratio ≈ 1 à 1,4) et ne le dépasse nettement que dans les grands (≈ 1,5 à 2,3). La part non publiée est donc SURTOUT un effet de taille ; l'indice ajusté sert à comparer des lycées de taille voisine, avec un signal faible.

## 2. Évolution nationale (médianes par lycée)

| niveau   |   rentree |   lycees |   eleves |   nb_spe_visibles |   nb_spe_max |   part_non_publiee |   part_autres_min |
|:---------|----------:|---------:|---------:|------------------:|-------------:|-------------------:|------------------:|
| 1re      |      2021 |     2251 |   393881 |                 7 |            8 |              0.374 |             0.154 |
| 1re      |      2022 |     2257 |   392744 |                 7 |            9 |              0.382 |             0.155 |
| 1re      |      2023 |     2267 |   387133 |                 7 |            9 |              0.387 |             0.16  |
| 1re      |      2024 |     2277 |   384809 |                 7 |            9 |              0.386 |             0.158 |
| 1re      |      2025 |     2275 |   381562 |                 7 |            9 |              0.385 |             0.148 |
| tle      |      2020 |     2239 |   376432 |                 6 |            8 |              0.336 |             0     |
| tle      |      2021 |     2245 |   375697 |                 6 |            8 |              0.355 |             0.055 |
| tle      |      2022 |     2252 |   383640 |                 6 |            8 |              0.346 |             0.036 |
| tle      |      2023 |     2261 |   384952 |                 6 |            8 |              0.348 |             0     |
| tle      |      2024 |     2265 |   377781 |                 6 |            8 |              0.349 |             0     |
| tle      |      2025 |     2270 |   377102 |                 6 |            8 |              0.337 |             0.04  |

## 3.1re Rentrée 2025 — par taille et secteur

| taille   | secteur            |   lycees |   nb_spe_visibles |   part_non_publiee |
|:---------|:-------------------|---------:|------------------:|-------------------:|
| <60      | PRIVE SOUS CONTRAT |      209 |                 4 |              0.702 |
| <60      | PUBLIC             |      115 |                 4 |              0.702 |
| 60-119   | PRIVE SOUS CONTRAT |      202 |                 6 |              0.547 |
| 60-119   | PUBLIC             |      288 |                 6 |              0.519 |
| 120-199  | PRIVE SOUS CONTRAT |      214 |                 7 |              0.369 |
| 120-199  | PUBLIC             |      448 |                 7 |              0.412 |
| 200-299  | PRIVE SOUS CONTRAT |       93 |                 8 |              0.283 |
| 200-299  | PUBLIC             |      479 |                 8 |              0.313 |
| 300+     | PRIVE SOUS CONTRAT |       30 |                 8 |              0.164 |
| 300+     | PUBLIC             |      197 |                 9 |              0.215 |

### Par quartile d'IPS (voie GT) — 1re 2025

| ips_voie_gt     |   lycees |   effectif_median |   nb_spe_moyen |   part_lycees_moins_6_spe |   part_non_publiee |   indice_dispersion |
|:----------------|---------:|------------------:|---------------:|--------------------------:|-------------------:|--------------------:|
| Q1 (IPS faible) |      574 |               138 |          6.878 |                     0.148 |              0.417 |               0.005 |
| Q2              |      560 |               165 |          7.121 |                     0.146 |              0.394 |               0.011 |
| Q3              |      562 |               163 |          6.895 |                     0.183 |              0.396 |               0.014 |
| Q4 (IPS fort)   |      565 |               172 |          6.873 |                     0.119 |              0.328 |              -0.039 |

### Par quartile d'éloignement — 1re 2025

| indice_eloignement      |   lycees |   effectif_median |   nb_spe_moyen |   part_lycees_moins_6_spe |   part_non_publiee |   indice_dispersion |
|:------------------------|---------:|------------------:|---------------:|--------------------------:|-------------------:|--------------------:|
| Q1 (éloignement faible) |      588 |             183.5 |          7.083 |                     0.138 |              0.349 |              -0.003 |
| Q2                      |      534 |             184   |          7.204 |                     0.129 |              0.345 |              -0.011 |
| Q3                      |      550 |             171   |          7.047 |                     0.12  |              0.365 |              -0.001 |
| Q4 (éloignement fort)   |      555 |             110   |          6.429 |                     0.205 |              0.479 |               0.022 |

### Régressions (MCO, erreurs robustes) — 1re 2025

Variables standardisées (z) : un coefficient = effet d'un écart-type, toutes choses égales par ailleurs.

**nb_spe_visibles**

|                |   coef |    se |       t |    n |   r2 |
|:---------------|-------:|------:|--------:|-----:|-----:|
| constante      |  6.84  | 0.035 | 197.222 | 2227 | 0.67 |
| log_effectif_z |  1.65  | 0.036 |  45.29  | 2227 | 0.67 |
| ips_z          | -0.234 | 0.032 |  -7.288 | 2227 | 0.67 |
| eloignement_z  |  0.084 | 0.023 |   3.68  | 2227 | 0.67 |
| prive          |  0.216 | 0.071 |   3.023 | 2227 | 0.67 |

**indice_dispersion** (déjà net de la taille)

|               |   coef |    se |      t |    n |    r2 |
|:--------------|-------:|------:|-------:|-----:|------:|
| constante     | -0.003 | 0.004 | -0.831 | 2227 | 0.022 |
| ips_z         | -0.015 | 0.004 | -3.493 | 2227 | 0.022 |
| eloignement_z |  0.002 | 0.005 |  0.348 | 2227 | 0.022 |
| prive         | -0.023 | 0.01  | -2.34  | 2227 | 0.022 |

## 3.tle Rentrée 2025 — par taille et secteur

| taille   | secteur            |   lycees |   nb_spe_visibles |   part_non_publiee |
|:---------|:-------------------|---------:|------------------:|-------------------:|
| <60      | PRIVE SOUS CONTRAT |      220 |                 2 |              1     |
| <60      | PUBLIC             |      116 |                 3 |              0.904 |
| 60-119   | PRIVE SOUS CONTRAT |      211 |                 5 |              0.527 |
| 60-119   | PUBLIC             |      292 |                 6 |              0.569 |
| 120-199  | PRIVE SOUS CONTRAT |      204 |                 6 |              0.317 |
| 120-199  | PUBLIC             |      434 |                 7 |              0.342 |
| 200-299  | PRIVE SOUS CONTRAT |       86 |                 6 |              0.229 |
| 200-299  | PUBLIC             |      492 |                 7 |              0.234 |
| 300+     | PRIVE SOUS CONTRAT |       24 |                 7 |              0.124 |
| 300+     | PUBLIC             |      191 |                 8 |              0.162 |

### Par quartile d'IPS (voie GT) — tle 2025

| ips_voie_gt     |   lycees |   effectif_median |   nb_spe_moyen |   part_lycees_moins_6_spe |   part_non_publiee |   indice_dispersion |
|:----------------|---------:|------------------:|---------------:|--------------------------:|-------------------:|--------------------:|
| Q1 (IPS faible) |      572 |             138   |          6.024 |                     0.278 |              0.394 |               0.002 |
| Q2              |      559 |             164   |          6.154 |                     0.261 |              0.343 |               0     |
| Q3              |      561 |             160   |          5.834 |                     0.321 |              0.327 |               0     |
| Q4 (IPS fort)   |      564 |             164.5 |          5.684 |                     0.387 |              0.288 |              -0.029 |

### Par quartile d'éloignement — tle 2025

| indice_eloignement      |   lycees |   effectif_median |   nb_spe_moyen |   part_lycees_moins_6_spe |   part_non_publiee |   indice_dispersion |
|:------------------------|---------:|------------------:|---------------:|--------------------------:|-------------------:|--------------------:|
| Q1 (éloignement faible) |      586 |               186 |          6.009 |                     0.307 |              0.279 |              -0.015 |
| Q2                      |      533 |               181 |          6.159 |                     0.257 |              0.285 |              -0.01  |
| Q3                      |      550 |               169 |          6.071 |                     0.278 |              0.339 |               0     |
| Q4 (éloignement fort)   |      553 |               106 |          5.488 |                     0.396 |              0.496 |               0     |

### Régressions (MCO, erreurs robustes) — tle 2025

Variables standardisées (z) : un coefficient = effet d'un écart-type, toutes choses égales par ailleurs.

**nb_spe_visibles**

|                |   coef |    se |       t |    n |    r2 |
|:---------------|-------:|------:|--------:|-----:|------:|
| constante      |  5.863 | 0.036 | 164.148 | 2222 | 0.673 |
| log_effectif_z |  1.667 | 0.034 |  49.759 | 2222 | 0.673 |
| ips_z          | -0.288 | 0.033 |  -8.683 | 2222 | 0.673 |
| eloignement_z  |  0.09  | 0.031 |   2.907 | 2222 | 0.673 |
| prive          |  0.133 | 0.076 |   1.757 | 2222 | 0.673 |

**indice_dispersion** (déjà net de la taille)

|               |   coef |    se |      t |    n |    r2 |
|:--------------|-------:|------:|-------:|-----:|------:|
| constante     |  0.001 | 0.003 |  0.35  | 2222 | 0.037 |
| ips_z         | -0.008 | 0.004 | -1.956 | 2222 | 0.037 |
| eloignement_z |  0.01  | 0.004 |  2.815 | 2222 | 0.037 |
| prive         | -0.046 | 0.009 | -4.977 | 2222 | 0.037 |

## Limites

- `part_non_publiee` mélange secret primaire (petites cellules) et secondaire : c'est un PROXY de dispersion, monotone mais non linéaire.
- Le masquage est par sexe : une combinaison suivie par 3 filles et 3 garçons est entièrement masquée alors qu'elle forme un groupe de 6.
- Les combinaisons sont nationales (les 18 ou 15 plus fréquentes) : « autres » n'est pas détaillé.
- Aucune donnée d'emploi du temps : l'indice mesure une CONTRAINTE potentielle (élèves éclatés entre combinaisons), pas le morcellement réel.
- Corrélations descriptives, pas d'effet causal.