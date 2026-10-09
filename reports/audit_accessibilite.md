# Spédago — audit d'accessibilité (WCAG 2.2, niveau AA) · 10 octobre 2026

Périmètre : les 5 pages du site (accueil, Mon académie, Simulateur, Carte, Boussole), version thème clair (commit 908fc77).
Méthode : axe-core 4.10 (règles WCAG 2.0/2.1/2.2 A-AA + bonnes pratiques) sur ordinateur (1280 px) et téléphone (390 px) ;
parcours clavier scripté (60 tabulations par page) ; contrastes recalculés ; reflow à 320 px ; lecture du code (ARIA, régions dynamiques).
Non fait : test avec un vrai lecteur d'écran (NVDA, VoiceOver), à prévoir avant diffusion.

## Bilan

- **Bon socle :** tous les contrôles ont une étiquette ; le focus est visible partout (0 élément sans contour sur ~65 arrêts) ; aucun piège clavier ;
  aucun focus masqué ; pas de débordement à 320 px ; texte courant contrasté (gris 4,55:1, liens 6,7:1) ; `lang="fr"` sur les documents du dossier `site/`.
- **Non conforme AA :** 6 critères, dont 2 graves pour les lecteurs d'écran (annonces de mise à jour, classement de la Boussole au clavier).

## Constats (par priorité)

| # | Constat | Critère | Niveau | Gravité | Pages | Correctif |
|---|---|---|---|---|---|---|
| 1 | Les résultats se recalculent à chaque filtre sans rien annoncer (0 région `aria-live` sur le site) | 4.1.3 Messages d'état | AA | Élevée | toutes sauf l'accueil | Une zone `role="status"` par page qui résume le résultat (« 14 lycées sans NSI à Poitiers ») |
| 2 | Boussole, vue « Où candidater » : cliquer une ligne du classement ouvre la mention, mais la ligne n'est pas atteignable au clavier | 2.1.1 Clavier | A | Élevée | Boussole | Mettre le nom de mention dans un `<button>` (ou lien) dans la cellule |
| 3 | Pastilles blanches sur fond « incertain » (2,1:1) et « accès voisin » (3,0:1) | 1.4.3 Contraste | AA | Élevée | Carte | Texte foncé sur fond clair teinté, ou fond assombri (≥ 4,5:1) |
| 4 | Bordure des listes déroulantes et champs : 1,23:1 (gris très clair sur blanc) | 1.4.11 Contraste non textuel | AA | Moyenne | toutes | Bordure slate-500 `#64748b` (4,8:1) ; slate-400 `#94a3b8` ne suffit pas (2,6:1) |
| 5 | Points de la carte : « incertain » 1,8:1 et « accès voisin » 2,5:1 sur le fond de carte ; catégories distinguées par la couleur seule | 1.4.11 ; 1.4.1 Couleur | AA ; A | Moyenne | Carte | Couleurs ≥ 3:1 et une forme par catégorie (rond, carré, triangle, croix) ; la fiche et les compteurs donnent déjà le texte |
| 6 | Valeurs « à surveiller » en orange sans explication (règle « +10 points au-dessus de la France » invisible) | 1.4.1 Couleur ; 3.3.2 | A | Moyenne | Mon académie | Légende sous le tableau + icône ou mot (« au-dessus ») en plus de la couleur |
| 7 | Texte gris sur la carte orange « +212 » : 4,48:1 | 1.4.3 | AA | Faible | Mon académie | Gris slate-600 `#475569` |
| 8 | Pas de repère `<main>` (4 pages sur 5) ; contenus hors repères ; pas de lien d'évitement | 1.3.1 ; 2.4.1 Contourner | A | Moyenne | toutes | `<main id="contenu">` + lien « Aller au contenu » en tête de la barre |
| 9 | Onglets de la Boussole : `role="tab"` sans `tabpanel`, ni `aria-controls`, ni flèches ; posés dans un `<nav>` | 4.1.2 Nom, rôle, valeur | A | Moyenne | Boussole | Motif ARIA complet (flèches gauche/droite, `tabindex` itinérant) ou simples boutons à bascule `aria-pressed` |
| 10 | Titres : la Boussole passe de h1 à 30 h3 (pas de h2) | 1.3.1 | A | Faible | Boussole | h2 pour les résultats, h3 par mention |
| 11 | Tableaux sans légende (`caption`) | 1.3.1 (bonne pratique) | — | Faible | Mon académie, Simulateur | `<caption class="sr-only">` |
| 12 | Sélecteur de l'accueil sans étiquette visible (seulement `aria-label`) | 3.3.2 Étiquettes | A | Faible | Accueil | Étiquette visible « Votre académie » |
| 13 | Tableaux défilants du Simulateur sur mobile non focalisables | 2.1.1 (axe : scrollable-region-focusable) | A | Faible | Simulateur | `tabindex="0"` + `role="region"` + nom, ou fiches empilées comme Mon académie |
| 14 | Carte : sélectionner un lycée se fait à la souris sur les points ; au clavier, seulement par le champ « Lycée » (alternative existante) | 2.1.1 | A | Faible (alternative) | Carte | Indiquer l'alternative près de la carte |
| 15 | Flèches « → » en CSS lues par certains lecteurs d'écran | bonne pratique | — | Faible | Accueil | `content: "→" / ""` (texte alternatif vide) |
| 16 | `prefers-reduced-motion` respecté seulement sur la Boussole | 2.3.3 | AAA | Faible | autres | Couper les transitions sous `reduced-motion` dans le CSS commun |
| 17 | À vérifier : la langue de la page principale publiée (enveloppe ajoutée par l'hébergement) | 3.1.1 | A | ? | Accueil publié | Contrôler `lang` sur la version en ligne |

## Ordre de correction proposé

1. Tier 1 (avant toute diffusion) : 1, 2, 3, 4, 8.
2. Tier 2 : 5, 6, 9, 10, 12, 13.
3. Tier 3 : 7, 11, 14, 15, 16, 17 ; puis test réel NVDA + VoiceOver.

Ajouter axe-core aux tests automatiques (Playwright) pour bloquer toute régression.
