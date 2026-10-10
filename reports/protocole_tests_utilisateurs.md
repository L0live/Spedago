# Spédago — protocole de tests utilisateurs (phase 0)

Objectif : vérifier, avant toute diffusion, que chaque public trouve sa réponse, la comprend correctement et sait ce que le chiffre ne dit pas.
Format : 5 séances individuelles de 30 à 40 min, une par profil, en présentiel ou en visio avec partage d'écran. Penser à voix haute ; l'animateur n'aide pas, il relance (« qu'est-ce que vous cherchez ? »).
Matériel : le site publié (GitHub Pages), le téléphone du participant pour les profils élèves, un ordinateur pour les autres. Enregistrement de l'écran seulement avec accord écrit ; aucune donnée personnelle conservée au-delà des notes anonymisées.

## Profils (recruter une personne par ligne)

| # | Profil | Appareil | Page d'entrée |
|---|---|---|---|
| P1 | Élève de 2de (avec un parent si possible), choix des spécialités à venir | téléphone | Accueil |
| P2 | Élève de terminale, Parcoursup en cours | téléphone | Mes spécialités |
| P3 | Étudiant·e de L3 préparant ses candidatures en master | téléphone ou ordinateur | Boussole des masters |
| P4 | Décideur local (rectorat, région, élu, proviseur) | ordinateur | Mon académie |
| P5 | Journaliste ou chargé·e d'études qui doit citer un chiffre | ordinateur | Accueil |

Si possible, l'un des cinq utilise un lecteur d'écran (NVDA ou VoiceOver) ou la navigation au clavier seule.

## Tâches (par profil)

- **P1** : « Vous hésitez entre maths + physique et SES + HGGSP. Que font ensuite les élèves qui ont choisi chacune ? Votre lycée propose-t-il ces spécialités ? »
- **P2** : « Avec vos spécialités, quelle part des élèves qui ont demandé une licence de psychologie y ont reçu une proposition ? Est-ce votre chance personnelle ? »
- **P3** : « Pour votre mention, où un étudiant de votre profil a-t-il le plus souvent reçu une proposition ? Et que deviennent les diplômés 18 mois après ? »
- **P4** : « Dans votre académie, quelles filières sont saturées, et combien de lycées n'ont pas une spécialité à moins de 20 km ? Exportez le tableau. »
- **P5** : « Trouvez un chiffre sur les places vacantes de Parcoursup que vous pourriez citer, avec sa source et son champ. »

Tâche commune à tous, en fin de séance : « Envoyez cette vue à quelqu'un » (copie du lien) puis « Où verriez-vous comment ce chiffre est calculé ? » (page Méthodes).

## Ce qu'on mesure

| Mesure | Recueil | Seuil d'alerte |
|---|---|---|
| Réussite de la tâche | observée : réussie / avec hésitation / échec | 2 échecs ou plus sur 5 pour une même page |
| Interprétation | « Expliquez-moi ce chiffre avec vos mots » ; noter tout contresens | un taux de groupe lu comme une chance individuelle ; une simulation lue comme une prévision |
| Temps jusqu'à la première réponse | chronomètre | plus de 3 min |
| Confiance et neutralité | « Qui a fait ce site, à votre avis ? Vous fiez-vous à ces chiffres ? Pourquoi ? » | site perçu comme officiel ou militant |
| Facilité perçue | une question, échelle de 1 à 7 (SEQ) après chaque tâche | moyenne inférieure à 5 |

## Après les séances

1. Synthèse d'une page : constats classés par gravité (0 à 4, comme `critique_design.md`), avec citation du participant.
2. Les contresens d'interprétation sont prioritaires sur les problèmes d'ergonomie : ils touchent la mission même du site.
3. Chaque correction apportée est notée dans `CORRECTIONS.md` si elle change ce qu'un chiffre veut dire.
