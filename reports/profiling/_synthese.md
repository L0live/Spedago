# Synthèse du profilage

| Fichier | Lignes | Colonnes | Colonnes UAI | Années |
|---|---|---|---|---|
| MANIFEST.csv | 18 | 6 | — | — |
| eloignement_lycees.csv | 24,883 | 11 | uai | rentree_scolaire: 2020…2025 |
| ips_lycees_2016_2022.csv | 21,777 | 15 | uai | rentree_scolaire: 2016-2017…2021-2022 |
| ips_lycees_ap2023.csv | 10,905 | 48 | uai | rentree_scolaire: 2023-2024…2025-2026 |
| monmaster_2023.csv | 7,694 | 97 | eta_uai, inm | session: 2023…2023 |
| monmaster_2024_2025.csv | 16,257 | 144 | eta_uai, inm | session: 2024…2025 |
| parcoursup_2018.csv | 10,697 | 85 | cod_uai | session: 2018…2018 |
| parcoursup_2019.csv | 11,577 | 92 | cod_uai | session: 2019…2019 |
| parcoursup_2020.csv | 12,760 | 115 | cod_uai | session: 2020…2020 |
| parcoursup_2021.csv | 13,396 | 118 | cod_uai | session: 2021…2021 |
| parcoursup_2022.csv | 13,644 | 118 | cod_uai | session: 2022…2022 |
| parcoursup_2023.csv | 13,869 | 118 | cod_uai | session: 2023…2023 |
| parcoursup_2024.csv | 14,079 | 118 | cod_uai | session: 2024…2024 |
| parcoursup_2025.csv | 14,252 | 118 | cod_uai | session: 2025…2025 |
| parcoursup_apprentissage.csv | 39,032 | 44 | cod_uai | session: 2022…2025 |
| parcoursup_specialites_v3.csv | 17,211 | 10 | — | annee_du_bac: 2025…2025 |
| remplacement_2nd_degre.csv | 30 | 3 | — | — |
| specialites_doublettes_tle.csv | 13,548 | 89 | numero_etablissement | rentree_scolaire: 2020…2025 |
| specialites_triplettes_1ere.csv | 11,337 | 95 | numero_etablissement | rentree_scolaire: 2021…2025 |

## Recouvrement des UAI (jointures)

| A | B | UAI communs | % de A | % de B |
|---|---|---|---|---|
| eloignement_lycees.csv | ips_lycees_2016_2022.csv | 3609 | 81% | 98% |
| eloignement_lycees.csv | ips_lycees_ap2023.csv | 3605 | 81% | 98% |
| eloignement_lycees.csv | monmaster_2023.csv | 0 | 0% | 0% |
| eloignement_lycees.csv | monmaster_2023.csv | 0 | 0% | 0% |
| eloignement_lycees.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| eloignement_lycees.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| eloignement_lycees.csv | parcoursup_2018.csv | 2206 | 50% | 74% |
| eloignement_lycees.csv | parcoursup_2019.csv | 2289 | 51% | 65% |
| eloignement_lycees.csv | parcoursup_2020.csv | 2351 | 53% | 63% |
| eloignement_lycees.csv | parcoursup_2021.csv | 2385 | 54% | 62% |
| eloignement_lycees.csv | parcoursup_2022.csv | 2387 | 54% | 61% |
| eloignement_lycees.csv | parcoursup_2023.csv | 2399 | 54% | 61% |
| eloignement_lycees.csv | parcoursup_2024.csv | 2393 | 54% | 60% |
| eloignement_lycees.csv | parcoursup_2025.csv | 2398 | 54% | 59% |
| eloignement_lycees.csv | parcoursup_apprentissage.csv | 1805 | 41% | 40% |
| eloignement_lycees.csv | specialites_doublettes_tle.csv | 2258 | 51% | 98% |
| eloignement_lycees.csv | specialites_triplettes_1ere.csv | 2260 | 51% | 98% |
| ips_lycees_2016_2022.csv | ips_lycees_ap2023.csv | 3576 | 97% | 97% |
| ips_lycees_2016_2022.csv | monmaster_2023.csv | 0 | 0% | 0% |
| ips_lycees_2016_2022.csv | monmaster_2023.csv | 0 | 0% | 0% |
| ips_lycees_2016_2022.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| ips_lycees_2016_2022.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| ips_lycees_2016_2022.csv | parcoursup_2018.csv | 1965 | 53% | 66% |
| ips_lycees_2016_2022.csv | parcoursup_2019.csv | 2037 | 55% | 58% |
| ips_lycees_2016_2022.csv | parcoursup_2020.csv | 2089 | 57% | 56% |
| ips_lycees_2016_2022.csv | parcoursup_2021.csv | 2111 | 57% | 55% |
| ips_lycees_2016_2022.csv | parcoursup_2022.csv | 2105 | 57% | 54% |
| ips_lycees_2016_2022.csv | parcoursup_2023.csv | 2114 | 57% | 53% |
| ips_lycees_2016_2022.csv | parcoursup_2024.csv | 2107 | 57% | 53% |
| ips_lycees_2016_2022.csv | parcoursup_2025.csv | 2117 | 57% | 52% |
| ips_lycees_2016_2022.csv | parcoursup_apprentissage.csv | 1548 | 42% | 34% |
| ips_lycees_2016_2022.csv | specialites_doublettes_tle.csv | 2239 | 61% | 97% |
| ips_lycees_2016_2022.csv | specialites_triplettes_1ere.csv | 2238 | 61% | 97% |
| ips_lycees_ap2023.csv | monmaster_2023.csv | 0 | 0% | 0% |
| ips_lycees_ap2023.csv | monmaster_2023.csv | 0 | 0% | 0% |
| ips_lycees_ap2023.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| ips_lycees_ap2023.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| ips_lycees_ap2023.csv | parcoursup_2018.csv | 1992 | 54% | 67% |
| ips_lycees_ap2023.csv | parcoursup_2019.csv | 2067 | 56% | 59% |
| ips_lycees_ap2023.csv | parcoursup_2020.csv | 2126 | 58% | 57% |
| ips_lycees_ap2023.csv | parcoursup_2021.csv | 2153 | 58% | 56% |
| ips_lycees_ap2023.csv | parcoursup_2022.csv | 2151 | 58% | 55% |
| ips_lycees_ap2023.csv | parcoursup_2023.csv | 2165 | 59% | 55% |
| ips_lycees_ap2023.csv | parcoursup_2024.csv | 2161 | 59% | 54% |
| ips_lycees_ap2023.csv | parcoursup_2025.csv | 2171 | 59% | 53% |
| ips_lycees_ap2023.csv | parcoursup_apprentissage.csv | 1574 | 43% | 35% |
| ips_lycees_ap2023.csv | specialites_doublettes_tle.csv | 2274 | 62% | 99% |
| ips_lycees_ap2023.csv | specialites_triplettes_1ere.csv | 2278 | 62% | 99% |
| monmaster_2023.csv | monmaster_2023.csv | 0 | 0% | 0% |
| monmaster_2023.csv | monmaster_2024_2025.csv | 110 | 96% | 92% |
| monmaster_2023.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2018.csv | 68 | 59% | 2% |
| monmaster_2023.csv | parcoursup_2019.csv | 68 | 59% | 2% |
| monmaster_2023.csv | parcoursup_2020.csv | 73 | 63% | 2% |
| monmaster_2023.csv | parcoursup_2021.csv | 78 | 68% | 2% |
| monmaster_2023.csv | parcoursup_2022.csv | 80 | 70% | 2% |
| monmaster_2023.csv | parcoursup_2023.csv | 83 | 72% | 2% |
| monmaster_2023.csv | parcoursup_2024.csv | 86 | 75% | 2% |
| monmaster_2023.csv | parcoursup_2025.csv | 81 | 70% | 2% |
| monmaster_2023.csv | parcoursup_apprentissage.csv | 11 | 10% | 0% |
| monmaster_2023.csv | specialites_doublettes_tle.csv | 0 | 0% | 0% |
| monmaster_2023.csv | specialites_triplettes_1ere.csv | 0 | 0% | 0% |
| monmaster_2023.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| monmaster_2023.csv | monmaster_2024_2025.csv | 2621 | 97% | 90% |
| monmaster_2023.csv | parcoursup_2018.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2019.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2020.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2021.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2022.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2023.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2024.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_2025.csv | 0 | 0% | 0% |
| monmaster_2023.csv | parcoursup_apprentissage.csv | 0 | 0% | 0% |
| monmaster_2023.csv | specialites_doublettes_tle.csv | 0 | 0% | 0% |
| monmaster_2023.csv | specialites_triplettes_1ere.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | monmaster_2024_2025.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2018.csv | 69 | 57% | 2% |
| monmaster_2024_2025.csv | parcoursup_2019.csv | 69 | 57% | 2% |
| monmaster_2024_2025.csv | parcoursup_2020.csv | 74 | 62% | 2% |
| monmaster_2024_2025.csv | parcoursup_2021.csv | 79 | 66% | 2% |
| monmaster_2024_2025.csv | parcoursup_2022.csv | 82 | 68% | 2% |
| monmaster_2024_2025.csv | parcoursup_2023.csv | 87 | 72% | 2% |
| monmaster_2024_2025.csv | parcoursup_2024.csv | 91 | 76% | 2% |
| monmaster_2024_2025.csv | parcoursup_2025.csv | 89 | 74% | 2% |
| monmaster_2024_2025.csv | parcoursup_apprentissage.csv | 12 | 10% | 0% |
| monmaster_2024_2025.csv | specialites_doublettes_tle.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | specialites_triplettes_1ere.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2018.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2019.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2020.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2021.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2022.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2023.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2024.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_2025.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | parcoursup_apprentissage.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | specialites_doublettes_tle.csv | 0 | 0% | 0% |
| monmaster_2024_2025.csv | specialites_triplettes_1ere.csv | 0 | 0% | 0% |
| parcoursup_2018.csv | parcoursup_2019.csv | 2899 | 98% | 83% |
| parcoursup_2018.csv | parcoursup_2020.csv | 2872 | 97% | 77% |
| parcoursup_2018.csv | parcoursup_2021.csv | 2843 | 96% | 73% |
| parcoursup_2018.csv | parcoursup_2022.csv | 2824 | 95% | 72% |
| parcoursup_2018.csv | parcoursup_2023.csv | 2797 | 94% | 71% |
| parcoursup_2018.csv | parcoursup_2024.csv | 2766 | 93% | 69% |
| parcoursup_2018.csv | parcoursup_2025.csv | 2738 | 92% | 67% |
| parcoursup_2018.csv | parcoursup_apprentissage.csv | 1431 | 48% | 32% |
| parcoursup_2018.csv | specialites_doublettes_tle.csv | 1518 | 51% | 66% |
| parcoursup_2018.csv | specialites_triplettes_1ere.csv | 1517 | 51% | 66% |
| parcoursup_2019.csv | parcoursup_2020.csv | 3461 | 99% | 92% |
| parcoursup_2019.csv | parcoursup_2021.csv | 3424 | 98% | 88% |
| parcoursup_2019.csv | parcoursup_2022.csv | 3379 | 96% | 86% |
| parcoursup_2019.csv | parcoursup_2023.csv | 3349 | 95% | 84% |
| parcoursup_2019.csv | parcoursup_2024.csv | 3287 | 94% | 82% |
| parcoursup_2019.csv | parcoursup_2025.csv | 3253 | 93% | 80% |
| parcoursup_2019.csv | parcoursup_apprentissage.csv | 1553 | 44% | 34% |
| parcoursup_2019.csv | specialites_doublettes_tle.csv | 1521 | 43% | 66% |
| parcoursup_2019.csv | specialites_triplettes_1ere.csv | 1521 | 43% | 66% |
| parcoursup_2020.csv | parcoursup_2021.csv | 3693 | 98% | 95% |
| parcoursup_2020.csv | parcoursup_2022.csv | 3635 | 97% | 93% |
| parcoursup_2020.csv | parcoursup_2023.csv | 3598 | 96% | 91% |
| parcoursup_2020.csv | parcoursup_2024.csv | 3535 | 94% | 88% |
| parcoursup_2020.csv | parcoursup_2025.csv | 3495 | 93% | 86% |
| parcoursup_2020.csv | parcoursup_apprentissage.csv | 1614 | 43% | 36% |
| parcoursup_2020.csv | specialites_doublettes_tle.csv | 1531 | 41% | 66% |
| parcoursup_2020.csv | specialites_triplettes_1ere.csv | 1530 | 41% | 67% |
| parcoursup_2021.csv | parcoursup_2022.csv | 3788 | 98% | 96% |
| parcoursup_2021.csv | parcoursup_2023.csv | 3733 | 96% | 94% |
| parcoursup_2021.csv | parcoursup_2024.csv | 3658 | 95% | 92% |
| parcoursup_2021.csv | parcoursup_2025.csv | 3617 | 93% | 89% |
| parcoursup_2021.csv | parcoursup_apprentissage.csv | 1661 | 43% | 37% |
| parcoursup_2021.csv | specialites_doublettes_tle.csv | 1535 | 40% | 67% |
| parcoursup_2021.csv | specialites_triplettes_1ere.csv | 1534 | 40% | 67% |
| parcoursup_2022.csv | parcoursup_2023.csv | 3819 | 97% | 96% |
| parcoursup_2022.csv | parcoursup_2024.csv | 3750 | 96% | 94% |
| parcoursup_2022.csv | parcoursup_2025.csv | 3703 | 94% | 91% |
| parcoursup_2022.csv | parcoursup_apprentissage.csv | 1676 | 43% | 37% |
| parcoursup_2022.csv | specialites_doublettes_tle.csv | 1538 | 39% | 67% |
| parcoursup_2022.csv | specialites_triplettes_1ere.csv | 1536 | 39% | 67% |
| parcoursup_2023.csv | parcoursup_2024.csv | 3873 | 98% | 97% |
| parcoursup_2023.csv | parcoursup_2025.csv | 3822 | 96% | 94% |
| parcoursup_2023.csv | parcoursup_apprentissage.csv | 1662 | 42% | 37% |
| parcoursup_2023.csv | specialites_doublettes_tle.csv | 1536 | 39% | 67% |
| parcoursup_2023.csv | specialites_triplettes_1ere.csv | 1535 | 39% | 67% |
| parcoursup_2024.csv | parcoursup_2025.csv | 3925 | 98% | 97% |
| parcoursup_2024.csv | parcoursup_apprentissage.csv | 1667 | 42% | 37% |
| parcoursup_2024.csv | specialites_doublettes_tle.csv | 1530 | 38% | 66% |
| parcoursup_2024.csv | specialites_triplettes_1ere.csv | 1528 | 38% | 66% |
| parcoursup_2025.csv | parcoursup_apprentissage.csv | 1678 | 41% | 37% |
| parcoursup_2025.csv | specialites_doublettes_tle.csv | 1537 | 38% | 67% |
| parcoursup_2025.csv | specialites_triplettes_1ere.csv | 1535 | 38% | 67% |
| parcoursup_apprentissage.csv | specialites_doublettes_tle.csv | 942 | 21% | 41% |
| parcoursup_apprentissage.csv | specialites_triplettes_1ere.csv | 941 | 21% | 41% |
| specialites_doublettes_tle.csv | specialites_triplettes_1ere.csv | 2294 | 100% | 100% |