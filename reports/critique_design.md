# Spédago — critique du design et de l'expérience · 10 octobre 2026

Cadre : heuristiques de Nielsen (H1-H10), lois de l'UX, architecture de l'information, écriture d'interface.
Gravité : 0 (aucun) à 4 (bloquant).

## Contexte

- **Lycéen·ne (2de-terminale)** : choisir ses spécialités, préparer Parcoursup. Usage court, sur téléphone, souvent avec un parent.
- **Étudiant·e (L2-L3)** : choisir où candidater en master. Usage court, répété pendant la phase de candidature.
- **Décideurs** (rectorat, région, élus, syndicats, journalistes) : comprendre un territoire, chiffrer une mesure, citer un nombre. Usage plus long, sur ordinateur, avec export.

Posture : outils « transitoires » (entrer, trouver, repartir). Le site doit donc servir vite la question de chacun, puis permettre d'aller plus loin.

## Ce qui fonctionne

- Une hiérarchie claire, un style unique, des nombres alignés et lisibles.
- L'académie suit d'une page à l'autre (#ancre). C'est la seule personnalisation transversale.
- L'honnêteté : limites affichées, « ce que la page ne dit pas », comparaison France systématique.

## Problèmes, par gravité

| # | Problème | Principe | Gravité | Recommandation |
|---|---|---|---|---|
| 1 | **Aucun profil persistant.** L'élève ressaisit académie, spécialités, mention et profil à chaque outil ; rien ne survit à la fermeture | H7 Flexibilité ; mémoire de travail ; 3.3.7 Saisie redondante | 3 | « Mon profil » commun (rôle, académie, lycée, spécialités, licence/mention), gardé dans le navigateur et dans l'adresse, lu par toutes les pages |
| 2 | **La porte « Élèves » ne sert pas les lycéens**, le public le plus nombreux : elle ne contient que la Boussole des masters | Architecture de l'information : modèle mental | 3 | Outil lycéen « Mes spécialités → mes formations » (vœux et propositions Parcoursup selon la doublette) + « mon lycée la propose-t-il, sinon où ? » |
| 3 | **Mon académie ne se filtre ni ne se compare** : une académie à la fois, tri fixe, pas de filière choisie, pas d'export | H7 ; surcharge de choix sans comparaison | 3 | Comparateur 2-3 académies ou « académies semblables » ; filtres filière/spécialité ; tri des colonnes ; export CSV ; impression |
| 4 | **Carte : la couleur la plus fréquente (ocre, « accès voisin ») domine**, alors que la catégorie qui appelle une action (« sans solution proche ») est noyée ; la carte ne zoome pas sur l'académie choisie | Effet Von Restorff inversé ; H1 | 3 | Atténuer « proposée » et « voisin », mettre en avant « sans solution » et « ouverture commune » ; zoom sur l'académie ; liste triable des lycées |
| 5 | **Filtres différents d'une page à l'autre** : colonne latérale (Simulateur), barre (Carte, Boussole), un seul menu (Mon académie) | H4 Cohérence ; loi de Jakob | 2 | Un composant de filtres commun, même place et même ordre (académie, public/privé, filière/spécialité), avec « réinitialiser » |
| 6 | **Libellés bruts** : « Licence_Las », « Ecole d'Ingénieur », « EFTS », spécialités sans accents (« Humanites litterature… »), mentions de master en capitales sans accents | H2 Langage de l'utilisateur | 2 | Table de libellés commune (dans le référentiel) |
| 7 | **Vocabulaire des quantités mouvant** : vœux, candidatures, candidats, propositions, admis ; définitions seulement en bas de page | H10 Aide en contexte ; H2 | 2 | Infobulle ou glossaire au point d'usage (« vœu = une demande ; un candidat en fait plusieurs ») |
| 8 | **Un résultat hypothétique présenté comme un fait** : la carte « +212 places » (règle de simulation) a le même poids que les comptages réels, et la plus forte couleur | Écriture responsable ; hiérarchie visuelle | 2 | La sortir des chiffres clés ou l'étiqueter « simulation » ; garder l'orange pour l'académie choisie et les alertes |
| 9 | **Règle « à surveiller » invisible** (+10 points au-dessus de la France), aucune légende | H6 Reconnaître plutôt que se souvenir | 2 | Légende, et choix du seuil par l'utilisateur |
| 10 | **Simulateur : 33 académies sans tri ni recherche** ; l'académie choisie n'est que surlignée, non filtrée | H7 ; loi de Hick | 2 | Tri par colonne, filtre académie, « mon académie » épinglée en tête |
| 11 | **Boussole : pas de liste de favoris ni de comparaison** de 2-3 masters ; aucune donnée d'insertion | H7 ; tâche réelle de l'étudiant | 2 | « Ma sélection » (comparer côte à côte) + insertion à 18-30 mois (InserSup) |
| 12 | **Pas de date ni de source au point d'usage** : un nombre cité hors contexte perd son année | Confiance ; H1 | 2 | Petite mention « Parcoursup 2025 » sous chaque chiffre clé ; lien vers la source |
| 13 | **Libellés de navigation ≠ titres de page** (« Carte des spécialités » / « Carte des spécialités partagées ») | H4 ; orientation | 1 | Aligner les deux |
| 14 | **Accueil déséquilibré** : la porte « Élèves » est à moitié vide à côté de la porte « Décideurs » | Proportion ; région commune | 1 | Se règle avec #2 |
| 15 | **Pas de partage d'une vue précise** (filtres complets dans l'adresse), seulement l'académie | H7 ; partage décideurs | 2 | Tous les filtres dans l'ancre (`#poitiers/nsi/public`), bouton « copier le lien » |

## Synthèse

Le site est juste et lisible, mais encore **un catalogue d'outils et pas un compagnon personnel**.
Les trois chantiers à plus fort effet :
1. le profil commun (#1, #5, #15) ;
2. l'outil lycéen (#2) ;
3. la comparaison et les filtres côté décideurs (#3, #4, #10).
