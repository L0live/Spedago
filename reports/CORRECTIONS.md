# Spédago — journal des corrections (9 octobre 2026)

Conclusions publiées dans les rapports puis corrigées après contrôle. À relire avant toute diffusion.

## Piste A — Parcoursup

| Affirmation initiale | Contrôle | Conclusion corrigée |
|---|---|---|
| ~72 000 places vacantes coexistent avec des formations saturées (même académie × filière) | Granularité trop grossière (BTS Compta ≠ BTS Électrotechnique) ; privé hors contrat inclus | **15 000 à 26 000** selon l'échelle (département ou académie × spécialité, public + privé sous contrat) ; **10 000 à 19 000** réellement face à des candidats classés non appelés (`tension_robustesse.md`) |
| Redéploiement à places constantes : 72-82 % du besoin couvrable, « robuste » | Même défaut de granularité | **17-24 %** au niveau de la spécialité, public + privé sous contrat (`simulation_ppl_art2.md`, §2 et §5) |
| IFSI : pression la plus forte (47 vœux/place) | 98 % des IFSI et des PASS sont en listes d'appel communes : un candidat compte dans chaque formation du regroupement | La pression n'est comparable qu'**à l'intérieur** d'une filière |
| IFSI 2024 : 518 formations, « découpage par site ? » | 9 diplômes paramédicaux classés IFSI en 2024 seulement | Réalignés en « Autre formation » (`fili_harmo`) |
| Persistance de la saturation (77 %) | Attrition du panel | **Confirmée** : borne basse 75 % (écart ≤ 2 points) |

Inchangé : inversion de `list_com` 2024-2025, CNED exclu, persistance de la tension, capacités peu réactives à la pression,
écarts Île-de-France intra-filière (hors IFSI/PASS).

## Piste B — Spécialités

| Affirmation initiale | Contrôle | Conclusion corrigée |
|---|---|---|
| La part non publiée observée vaut ~2× le niveau mécanique du secret statistique | Simulation biaisée (parts nationales sur cases publiées seulement) | Ratio **≈ 1 à 1,4** dans les petits/moyens lycées, **1,5 à 2,3** dans les grands : l'indicateur est **surtout un effet de taille**, signal de dispersion faible |
| Privé : +0,22 spécialité à taille égale | Effets fixes de taille, erreurs regroupées par académie, 3 rentrées | **Non robuste** (non significatif en 2021 et 2025) |
| IPS : moins de spécialités dans les lycées favorisés (« à vérifier ») | 3 rentrées × 2 niveaux, effets fixes de taille, contrôle du type de lycée (LPO) | **Robuste** (−0,15 à −0,25 spécialité par écart-type, t de −3 à −6). Porté par des spécialités plus souvent proposées dans les lycées moins favorisés : sciences de l'ingénieur, EPPCS, HLP, cinéma, NSI, LLCER, SVT (tle) |
| Éloignement : effet passant par la taille | Idem | **Confirmé** : à taille égale, l'éloignement n'enlève pas de spécialités (effet légèrement positif) |

## Outils interactifs (ajout du 9 octobre 2026, soir)

| Point | Contrôle | Correction |
|---|---|---|
| Arrondi `ceil(places × α)` | 100 × 0,07 = 7,000000000000001 en flottant → 8 places | Arrondi à 1e-9 avant le plafond (Python et JS). Aucun effet sur les résultats publiés (α = 5, 10, 20 %) |
| Export du simulateur Parcoursup | Test de parité JS/Python : `liste_commune` relue en 1.0/0.0, convertie en « inconnu » partout | Conversion corrigée ; test de non-régression ajouté |
| Carte des mutualisations : demande | Taux de choix mesuré là où la spécialité est proposée → 1 172 lycées « regroupables » en histoire des arts | Estimation basse par défaut (tous lycées), haute affichée en fourchette |
| Carte : taille des groupes | Groupes de 26 lycées à Paris | Plafond de 4 lycées, les plus proches du pivot |
| Carte : lycées masqués | Lycées à effectifs NSI masqués ignorés comme offre → faux « isolés » à Poitiers | Masqué = offre probable pour les voisins (204 → 74 groupes ; NSI isolés 232 → 178) |

## Référentiel commun et site (10 octobre 2026)

| Point | Contrôle | Correction |
|---|---|---|
| Noms d'académie différents d'une page à l'autre | « Besancon », « Etranger », « Polynésie Française », « Nouvelle Calédonie » selon la source | Graphie canonique unique (`spedago/referentiel.py`) dans toutes les pages ; graphie inconnue = arrêt du script |
| Lycées avec 1re générale absents de l'annuaire | 9 lycées (sans coordonnées) disparaissaient du référentiel | Gardés dans le référentiel ; toujours hors carte (pas de position) |
| « Mon académie » | Nombres recalculés en Python | Identiques au Simulateur, à la Carte, à la Boussole et à la table de tension (tests) |

## Reproductibilité

- `scripts/download_data.py` + `data/raw/MANIFEST.csv` (empreintes SHA-256) ; `requirements.txt` ; `run_all.sh`.
- Pipeline relancé de zéro : sorties identiques à l'archive (hors effet attendu du correctif IFSI : 56 cellules 2024).
- 98 tests (`python3 -m pytest tests/`), dont parité JavaScript/Python des 4 outils et concordance entre pages.
- Externe : places en apprentissage 2025 = 264 386 (CESPM : 264 800), part ≈ 25,6 % (CESPM : « 26 % »).

## Limites qui restent (non vérifiables avec l'open data)

- `capa_fin` : « capacité de l'établissement par formation », sans précision officielle sur la date ni sur le surbooking.
- Aucune donnée individuelle : pas d'origine des candidats, pas de réallocations en chaîne (CASD nécessaire).
- Apprentissage exclu des analyses A (26 % des places).
- Spécialités : secret secondaire non séparable de la dispersion réelle ; aucune donnée d'emploi du temps.
