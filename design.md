# Système visuel de Spédago

Règles communes à toutes les pages du site. Toute refonte de page part de ce fichier ; si une page a besoin de
quelque chose qu'il n'autorise pas, on modifie d'abord ce fichier, pas la page seule.

Les valeurs vivent dans `web/src/styles/commun.css` ; ce document dit **quand** et **comment** les employer.
S'appliquent en plus, et priment sur toute considération visuelle :
- accessibilité WCAG 2.2 AA (axe sans violation grave sur ordinateur et téléphone, reflow à 320 px, annonce de chaque recalcul) ;
- secret statistique : une case masquée n'est jamais affichée ni comptée comme zéro ;
- un taux de groupe n'est jamais présenté comme une probabilité individuelle.

## Principe

Un observatoire public : le lecteur vient vérifier un fait, pas être convaincu. Le design sert la lecture des
nombres et de leurs limites. Ton : éditorial et sobre — une serif de titre, des filets, peu de couleur, pas d'effet.

- **Neutralité.** Aucun indicateur n'est mis en avant aux dépens d'un autre par la mise en page : pas de chiffre
  « vedette » choisi par le site. Quand plusieurs chiffres ouvrent une page, ils ont le même poids.
- **Chaque chiffre dit d'où il vient.** Tout chiffre clé passe par `stat(fiche, …)` (`web/src/lib/dom.ts`) : valeur,
  libellé, champ, lien vers sa fiche de la page Méthodes. Un test le vérifie.
- **Les limites restent visibles.** Une mise en page plus compacte ne cache jamais un avertissement (voir § Textes).

## Couleur

Neutres slate, deux couleurs fonctionnelles, règle 60-30-10 : neutres partout, **bleu pour agir**, **orange pour signaler**.
Jamais de couleur décorative, de dégradé de fond ni de blanc pur (la surface est teintée).

| Rôle | Jetons |
|---|---|
| Fond, surface, texte | `--bg`, `--surface`, `--ink`, `--muted` |
| Filets | `--line` (séparation), `--line-strong` (survol, soulignés), `--track` (fond de jauge) |
| Agir : liens, boutons secondaires, focus, sélection | `--accent`, `--accent-strong`, `--accent-soft`, `--accent-line`, `--accent-mark` |
| Signaler : académie choisie, valeur à surveiller, public « décideurs » | `--orange`, `--orange-ink`, `--orange-deep`, `--orange-soft`, `--orange-line` |
| Données : niveaux et catégories | `--good`, `--warn` (barres seulement), `--bad`, `--amber`, `--violet` |

- Une feuille de page ne contient **aucune** couleur en dur (hex, `rgb()`, `white`) ; une couleur manquante s'ajoute
  d'abord à `commun.css`. Une page peut donner un **nom local** à un jeton commun pour ses catégories
  (ex. `--offre: var(--good)` sur la carte), jamais une nouvelle valeur.
- Texte : contraste ≥ 4,5:1 sur `--surface` et `--bg` ; éléments graphiques porteurs de sens ≥ 3:1.
- Une couleur de données n'est jamais le seul porteur d'information : libellé, forme ou valeur l'accompagnent.

## Typographie

- **Titres et chiffres** : Newsreader 600 (`--display`), toujours en romain. **Texte et interface** : Public Sans 400–700 (`--body`).
- Échelle (`--text-*`) : 12 · 13 · 14 · 15 (texte courant) · 16 (champs de saisie) · 18 · 20 · 24 · 28 px.
  Aucun texte sous 12 px (y compris `small`, en-têtes de tableau, graduations de graphique).
- Un même rang de titre a la même taille sur toutes les pages : `h1` fluide (32–46 px ; 40–60 px sur l'accueil),
  `h2` de section 24 px, `h2` de panneau d'outil et de « Lire ces chiffres » 20 px, chiffre clé 28 px.
- Nombres en `tabular-nums` partout où ils se comparent.
- Capitales espacées : seulement pour les libellés de champ de formulaire et les noms de groupe de la navigation.
  Pas de surtitre en capitales au-dessus des titres.
- Paragraphes limités à 75 caractères par ligne, même en pleine largeur. Apostrophe typographique (’) dans le texte affiché.

## Espace et mise en page

- **Pleine largeur** : la page occupe l'écran, avec une gouttière `--gutter` de 16 à 40 px. Seuls les textes ont une largeur maximale.
- Espacements sur l'échelle de 4 px (`--space-2xs` 4 → `--space-2xl` 48). Rythme vertical : 32 px entre blocs ;
  48 px et un filet avant la section de fin « Lire ces chiffres / Ce que la page ne dit pas ».
- **Un seul niveau de contenant.** Une carte (`.bloc`, `.stat`, `.panel`) ne contient jamais une autre carte : à
  l'intérieur, on sépare par des filets. Une seule élévation (`--shadow-sm`) ; `--shadow-md` pour les panneaux flottants.
- Pas de bande colorée épaisse sur un côté de carte.
- Téléphone : rien ne déborde à 320 px ; les tableaux deviennent des fiches (libellé au-dessus de chaque valeur) ;
  un lien ou un bouton tient sur une ligne.

## Composants communs

| Composant | Règle |
|---|---|
| Navigation | Marque, porte « Élèves », porte « Décideurs », outils (copier le lien, profil). Sous 640 px : repliée derrière « Menu » ; visible sans JavaScript. Identique sur toutes les pages (produite par `spedago/pages.py`). |
| Ligne « champ · source » (`.source`) | Sous un titre de page ou de section, en casse normale, 13 px, `--muted`. Dit sur quoi porte la section (« Entrée dans le supérieur · Parcoursup 2025 »). |
| Chiffre clé | Toujours par `stat()`. En carte quand les chiffres sont seuls sur la page ; en rangée à filets dans un bloc. |
| Bloc de section (`.bloc`) | Surface, filet, rayon 12 px, 24 px de marge intérieure (16 px sur téléphone). |
| Tableau | En-têtes 13 px en casse normale ; triable par bouton dans l'en-tête ; export CSV par `.btn-ghost` dans une `.toolbar`. |
| Jauge | Barre = valeur de la page, trait = repère de comparaison ; orange seulement si l'écart est signalé dans le texte. |
| Boutons | Secondaire : `.btn-ghost` (texte bleu, filet). Action principale d'une page (au plus une) : fond `--orange-ink` ou `--ink`, texte `--surface`. Pas d'effet d'échelle au survol. |
| Fin de page | « Lire ces chiffres » et « Ce que la page ne dit pas » côte à côte (empilés sur téléphone), puis le pied de page (sources, licences). |

## Mouvement et interaction

- Transitions de couleur et de fond seulement, 150 ms, `--ease-out`. Pas d'apparition au défilement, pas de compteur animé.
- `prefers-reduced-motion` : aucune transition.
- Anneau de focus 2 px `--accent`, visible immédiatement, jamais animé.
- Succès silencieux ; chaque recalcul est annoncé par `aria-live` (valeurs et libellés, sans le texte des liens).

## Familles de pages

La forme d'une page dépend de sa tâche. Les pages d'une même famille partagent la même structure ; couleurs,
typographie et composants sont communs à toutes.

### Entrée — accueil (`index.html`)
Un **index** : la page est la liste des outils.
- En tête : titre, une phrase, les trois chiffres de cadrage (avec champ et fiche).
- Puis un groupe par public — « Lycéens et étudiants », « Décideurs, élus, rectorats, syndicats, journalistes » —
  dont le titre porte la couleur du public (`--accent` / `--orange-ink`), sans bande ni carte. Une ligne par outil
  (nom, une phrase, flèche), séparée par des filets ; toute la ligne est cliquable.
- Le choix d'académie reste dans le groupe « Décideurs », comme raccourci vers « Mon académie ».
- Puis « Comment c'est fait ».

### Conclusion d'abord — Mon académie, France et voisins
Un **rapport** sur un territoire.
- En tête : le sélecteur, puis le nom du territoire en grand et une **bande de chiffres clés à poids égal**
  (même taille, filets entre eux, sans cartes). Aucun chiffre n'est agrandi seul.
- Puis une section par thème, séparées par des filets et l'espace (pas une pile de cartes) : titre, ligne
  « champ · source », phrase de constat chiffrée, tableau ou graphique, renvoi vers l'outil détaillé.

### Réglage d'abord — Simulateur, Boussole des masters, Mes spécialités
Un **outil** : on règle, on lit le résultat.
- En-tête compact : titre et chapeau court (voir § Textes), ligne « champ · source ».
- Réglages immédiatement après : en **colonne** collante à gauche quand ils sont nombreux (Simulateur), en
  **barre** au-dessus des résultats quand ils tiennent sur une ligne (Boussole, Mes spécialités).
- Les chiffres clés résument le résultat courant et sont annoncés à chaque recalcul.

### Carte — Carte des spécialités partagées
Une **carte** organise la page.
- En-tête compact, filtres au-dessus de la carte, puis la carte en premier et en grand (au plus 85 % de la hauteur d'écran).
- La légende porte les comptes : une entrée par catégorie (pastille, libellé, nombre, champ et fiche).
- La fiche du lycée et les ouvertures communes à côté de la carte (dessous sur téléphone), puis la liste des lycées.

### Lecture — Méthodes
Un **document**.
- Sur grand écran : sommaire fixe à gauche, fiches à droite. Sur téléphone : sommaire en tête.
- Chaque fiche est une section de texte séparée par un filet (pas une carte) : titre, thème, définition, calcul,
  champ, sources, seuils, limites. La fiche visée par un lien (`#id`) est signalée par un filet orange.

## Textes

- Le chapeau d'un outil dit ce que fait la page en une ou deux phrases. Tout chapeau réécrit est soumis à l'auteur avant publication.
- Avertissements conservés mot pour mot et toujours visibles sans clic :
  - Boussole : « Des taux passés, pas une prédiction : votre dossier compte plus que votre profil. »
  - Mes spécialités : « Ce sont des résultats passés, au niveau national : votre dossier compte plus que vos spécialités. »
  - Simulateur : la règle simulée est un choix parmi d'autres, la proposition de loi ne disant pas comment l'appliquer.
- Un taux de groupe n'est jamais formulé comme une chance individuelle (« la part des candidats… », pas « vos chances »).
- Les noms de champ et de source reprennent ceux des fiches de `spedago/indicateurs.py`.

## Écarts restants

Les pages déjà conformes aux règles communes (couleur, typographie, espace, composants) ne le sont pas encore toutes à
leur famille. Écarts connus au moment de l'écriture, résorbés par la refonte page par page :
- Carte des spécialités : compteurs séparés de la légende.
- Mon académie, France et voisins : chiffres en cartes, sections en pile de cartes.
- Simulateur, Boussole, Mes spécialités : chapeaux longs ; filtres de Mes spécialités en carte.

## Ce qu'une refonte ne touche pas

- Les calculs (`web/src/calc/`), les données, les scripts Python et les textes des fiches Méthodes.
- Les identifiants HTML lus par le TypeScript (`el()` échoue si l'un manque) et les ancres d'URL.
- Les annonces `aria-live`, l'ordre de tabulation logique, les libellés des contrôles.
- Vérifications à chaque page refaite : `npm run build`, pytest, axe (ordinateur et téléphone, aucune violation),
  captures à 1440, 375 et 320 px, aucun défilement horizontal.
