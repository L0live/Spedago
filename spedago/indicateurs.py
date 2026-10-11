"""Spédago — registre des indicateurs : une fiche méthodologique par nombre publié.

Chaque fiche dit ce que mesure l’indicateur, sur quel champ, à partir de quelles sources (fichiers du
MANIFEST, donc d’empreinte connue), avec quels seuils et quelles limites. Les seuils sont recopiés ici
pour être lisibles ; tests/test_indicateurs.py vérifie qu’ils sont identiques aux constantes des scripts
(module, nom de la constante) : une fiche ne peut pas dériver du calcul sans faire échouer les tests.

Le registre est publié sur la page « Méthodes » (web/methodes.html) par scripts/build_web_meta.py.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Seuil:
    libelle: str
    valeur: float | int | str
    module: str = ""      # script qui porte la constante (scripts/<module>.py), vide si non vérifiable
    constante: str = ""


@dataclass(frozen=True)
class Indicateur:
    id: str
    nom: str
    definition: str
    formule: str
    champ: str
    sources: list[str]                  # fichiers de data/raw (MANIFEST.csv ou MANIFEST_eurostat.csv)
    pages: list[str]                    # pages du site qui l'affichent
    rapport: str                        # rapport méthodologique (reports/)
    limites: list[str]
    seuils: list[Seuil] = field(default_factory=list)
    theme: str = ""

    def to_json(self) -> dict:
        return asdict(self)


PS = [f"parcoursup_{y}.csv" for y in range(2020, 2026)]

INDICATEURS: list[Indicateur] = [
    # ---------------------------------------------------------------- Parcoursup
    Indicateur(
        "ps-pression", "Pression (vœux par place)", theme="Entrée dans le supérieur (Parcoursup)",
        definition="Nombre de candidatures confirmées en phase principale rapporté au nombre de places d’une formation.",
        formule="vœux en phase principale (nb_voe_pp) / places (capa_fin)",
        champ="Formations Parcoursup de capacité non nulle, hors CNED (capacités nominales). L’académie est celle de la formation, pas du candidat.",
        sources=PS, pages=["mon-academie.html", "simulateur-parcoursup.html"], rapport="tension.md",
        limites=["Un candidat est compté dans chaque formation qu’il demande : la pression mesure des candidatures, pas des personnes.",
                 "Formations en listes d’appel communes (IFSI, PASS) : un candidat compte dans chaque formation du regroupement ; la pression n’est comparable qu’à l’intérieur d’une filière.",
                 "L’open data ne donne pas l’origine géographique des candidats."]),
    Indicateur(
        "ps-remplissage", "Remplissage et formations saturées", theme="Entrée dans le supérieur (Parcoursup)",
        definition="Part des places d’une formation occupées par des admis. Une formation est dite saturée au-delà d’un seuil, sous-remplie en deçà d’un autre.",
        formule="admis (acc_tot) / places (capa_fin)",
        champ="Comme la pression. Les analyses de redéploiement se limitent au public et au privé sous contrat.",
        sources=PS, pages=["mon-academie.html", "simulateur-parcoursup.html"], rapport="tension.md",
        seuils=[Seuil("Saturée si remplissage ≥", 0.95, "analyse_tension", "SEUIL_SATURE"),
                Seuil("Sous-remplie si remplissage <", 0.80, "analyse_tension", "SEUIL_SOUS_REMPLIE")],
        limites=["Les deux seuils sont des conventions de Spédago ; la robustesse à leur choix est testée (simulation_ppl_art2.md, §4).",
                 "Places vacantes = places − admis, ramené à 0 si négatif ; le CNED (capacités nominales) en compterait environ 25 000 fictives, d’où son exclusion."]),
    Indicateur(
        "ps-prive", "Part du privé dans l’offre Parcoursup", theme="Entrée dans le supérieur (Parcoursup)",
        definition="Part des formations proposées sur Parcoursup portées par un établissement privé (sous contrat, enseignement supérieur privé ou hors contrat), séparément hors apprentissage et en apprentissage, et part des places correspondantes.",
        formule="formations dont contrat_etab commence par « Privé » / formations de la session ; même calcul sur les places (capa_fin)",
        champ="Toutes les formations de la session sur Parcoursup, jeu principal (hors apprentissage) et jeu apprentissage. Académie = lieu de la formation ; les formations situées à l’étranger ne sont comptées que dans le total national.",
        sources=["parcoursup_2025.csv", "parcoursup_apprentissage.csv"], pages=["mon-academie.html"], rapport="",
        limites=["Compte une offre de formations, pas des inscrits : une formation privée peut avoir peu de places ou rester vide.",
                 "Le privé hors Parcoursup n’est pas compté : selon le comité éthique et scientifique de Parcoursup (8e rapport), aucune donnée n’existe sur les inscriptions de ces formations.",
                 "Le résultat dépend fortement du périmètre : sans l’apprentissage, le privé est minoritaire ; en apprentissage, il est majoritaire. Ne jamais citer une part sans dire lequel."]),
    Indicateur(
        "ps-non-appeles", "Candidats classés jamais appelés", theme="Entrée dans le supérieur (Parcoursup)",
        definition="Candidats classés en phase principale qui n’ont jamais reçu de proposition de la formation.",
        formule="classés en phase principale − rang du dernier appelé",
        champ="Formations à liste d’appel propre (inconnu pour les listes communes).",
        sources=PS, pages=["simulateur-parcoursup.html"], rapport="simulation_ppl_art2.md",
        limites=["Borne haute de la demande non satisfaite : ces candidats ont pu être admis ailleurs, y compris dans un vœu préféré."]),
    Indicateur(
        "ps-simulation", "Places ajoutées par la règle « pression de l’année précédente »", theme="Entrée dans le supérieur (Parcoursup)",
        definition="Simulation, à règles explicites, de l’article 2 de la PPL Sénat n° 447 : places ajoutées aux formations sous pression, et part finançable par redéploiement de places vacantes voisines.",
        formule="éligible = pression ≥ quantile de sa filière ET saturée ET (liste commune OU classés non appelés > 0) ; ajout = +α % des places (S1) ou min(non appelés, β % des places) (S2)",
        champ="Session 2025 simulée à partir de 2024. Redéploiement : même académie × filière × spécialité, places du public et du privé sous contrat, depuis les formations sous-remplies.",
        sources=PS, pages=["simulateur-parcoursup.html", "mon-academie.html"], rapport="simulation_ppl_art2.md",
        seuils=[Seuil("Quantile de pression dans la filière", 0.75, "simulate_ppl_art2", "Q_PRESSION"),
                Seuil("Saturation", 0.95, "simulate_ppl_art2", "SEUIL_SATURE"),
                Seuil("Sous-remplissage (gisement de redéploiement)", 0.80, "simulate_ppl_art2", "SEUIL_SOUS_REMPLIE"),
                Seuil("Plafond du scénario S2", 0.20, "simulate_ppl_art2", "BETA")],
        limites=["Ce n’est pas une prévision : sans données individuelles, les réaffectations en chaîne des candidats ne sont pas modélisées.",
                 "Le texte de loi ne fixe aucune formule ; chaque règle est une interprétation possible, réglable sur la page."]),
    # ---------------------------------------------------------------- Lycée
    Indicateur(
        "spe-offre", "Offre de spécialités par lycée", theme="Lycée (spécialités)",
        definition="Pour chaque lycée ayant une 1re générale, les spécialités suivies par au moins un élève.",
        formule="présente si effectif > 0 ; absente si effectif publié = 0 ; incertaine si la case est masquée",
        champ="Lycées de 1re générale de la rentrée la plus récente, géolocalisés par l’annuaire de l’Éducation nationale.",
        sources=["specialites_triplettes_1ere.csv", "annuaire_lycees.csv"], pages=["mutualisation.html", "mes-specialites.html", "mon-academie.html"],
        rapport="piste_B_specialites.md",
        limites=["Secret statistique : les cases de moins de 5 élèves (et le secret secondaire) sont masquées ; un lycée masqué n’est jamais compté absent.",
                 "Une spécialité suivie dans un autre établissement (convention, CNED) n’apparaît pas forcément."]),
    Indicateur(
        "spe-mutualisation", "Accès voisin et ouverture commune", theme="Lycée (spécialités)",
        definition="Pour un lycée qui ne propose pas une spécialité : un lycée voisin du même statut la propose-t-il (accès voisin) ? Sinon, des voisins qui ne la proposent pas non plus réuniraient-ils assez d’élèves pour un groupe commun ?",
        formule="demande estimée = élèves de 1re × taux de choix national de la spécialité là où elle est proposée",
        champ="Lycées où la spécialité est absente (zéro explicite) ; même statut (public avec public, privé avec privé) ; distance à vol d’oiseau.",
        sources=["specialites_triplettes_1ere.csv", "annuaire_lycees.csv"], pages=["mutualisation.html", "mon-academie.html"], rapport="piste_B_mutualisation.md",
        seuils=[Seuil("Rayon (km)", 20.0, "build_mutualisation", "R_KM"),
                Seuil("Élèves estimés pour un groupe commun", 12, "build_mutualisation", "SEUIL"),
                Seuil("Lycées au plus par groupe commun", 4, "build_mutualisation", "MAX_MEMBRES")],
        limites=["Distance à vol d’oiseau, pas temps de trajet.", "La demande est une estimation (deux hypothèses, basse et haute, dans le rapport)."]),
    Indicateur(
        "spe-propositions", "Propositions selon la doublette de spécialités", theme="Lycée (spécialités)",
        definition="Parmi les bacheliers généraux ayant suivi une doublette de spécialités et demandé une formation, la part qui y a reçu une proposition d’admission.",
        formule="propositions d’admission / candidats ayant confirmé au moins un vœu dans la formation",
        champ="Bacheliers généraux de l’année, niveau national (aucune donnée par lycée ou par établissement d’accueil).",
        sources=["parcoursup_specialites_v3.csv", "parcoursup_specialites_v2.csv"], pages=["mes-specialites.html"], rapport="mes_specialites.md",
        limites=["Taux historique d’un groupe, pas une probabilité individuelle : notes et dossier ne sont pas observés.",
                 "Les « vœux » du jeu comptent des personnes (au moins un vœu), pas des candidatures."]),
    Indicateur(
        "ival", "Résultats des lycées (IVAL)", theme="Lycée (spécialités)",
        definition="Taux de réussite au bac, taux d’accès de la 2de au bac et taux de mentions, avec la valeur ajoutée calculée par la DEPP (écart à l’attendu compte tenu des élèves accueillis).",
        formule="valeurs publiées par la DEPP, session la plus récente",
        champ="Lycées d’enseignement général et technologique.",
        sources=["ival_lycees_gt.csv"], pages=["mes-specialites.html"], rapport="mes_specialites.md",
        limites=["Valeurs reprises telles que publiées ; la valeur ajoutée est un modèle de la DEPP, avec sa propre marge d’incertitude."]),
    Indicateur(
        "poursuite", "Poursuite d’études des néo-bacheliers", theme="Entrée dans le supérieur (Parcoursup)",
        definition="Bacheliers de l’année qui s’inscrivent dans le supérieur l’année suivante, par voie du bac et par filière d’accueil (université, IUT, CPGE, STS, autres).",
        formule="inscrits « flux » + « stable » de chaque filière (leur somme redonne le taux publié) / bacheliers",
        champ="Académie d’obtention du bac, dernière session publiée par le SIES.",
        sources=["poursuite_academie.csv"], pages=["mon-academie.html"], rapport="",
        limites=["Le partage entre « flux » et « stable » n’est pas documenté dans la fiche du jeu : seule la somme est utilisée."]),
    # ---------------------------------------------------------------- Master
    Indicateur(
        "mm-proposition", "Taux de proposition en master", theme="Master (Mon Master)",
        definition="Part des candidats à un master qui ont reçu une proposition d’admission, par profil (L3 générale, licence pro, BUT 3, déjà en master, etc.).",
        formule="propositions / candidats (phase principale + complémentaire) ; intervalle de Wilson à 95 %",
        champ="Formations de Mon Master, sessions 2024 et 2025.",
        sources=["monmaster_2024_2025.csv"], pages=["boussole-des-masters.html", "mon-academie.html"], rapport="piste_C_monmaster.md",
        seuils=[Seuil("Candidats minimum pour afficher un taux", 10, "build_monmaster", "MIN_CANDIDATS")],
        limites=["Taux historique, pas une probabilité individuelle : le dossier n’est pas observé.",
                 "Le taux national par profil mélange l’effet du profil et celui des formations demandées (comparaison à formation identique dans le rapport)."]),
    Indicateur(
        "mm-insertion", "Emploi salarié 18 mois après le master", theme="Master (Mon Master)",
        definition="Part des diplômés sortants en emploi salarié en France 18 mois après le diplôme, par établissement et mention.",
        formule="indicateur InserSup tx_sortants_en_emploi_sal_fr_18 ; repère national par mention = moyenne pondérée par les sortants",
        champ="Masters LMD rattachés à Mon Master par (UAI, mention) ; promotion la plus récente publiée (seule ou cumul de deux pour les petits effectifs).",
        sources=["insersup_master.csv"], pages=["boussole-des-masters.html"], rapport="insertion_master.md",
        seuils=[Seuil("Délai après le diplôme (mois)", 18, "build_insertion", "MOIS")],
        limites=["Emploi salarié en France seulement : les indépendants et l’emploi à l’étranger ne sont pas comptés.",
                 "Environ un quart des formations n’ont pas de rattachement (indicateur non publié ou appariement impossible)."]),
    # ---------------------------------------------------------------- Europe
    Indicateur(
        "eu-mobilite", "Étudiants français en mobilité diplômante", theme="France et voisins (Eurostat)",
        definition="Étudiants dont le pays d’origine est la France (au sens de la collecte UOE : pays de la scolarité antérieure, à défaut nationalité ou résidence), inscrits pour un diplôme entier dans un autre pays (pas les échanges Erasmus), comptés par le pays d’accueil. Aussi, en sens inverse, les étudiants étrangers en France.",
        formule="educ_uoe_mobs02, CITE 5 à 8, total des sexes",
        champ="Pays voisins publiant la donnée (les Pays-Bas ne publient pas de valeur).",
        sources=["eurostat_mobilite_francais_etranger.json", "eurostat_mobilite_etrangers_france.json"], pages=["france-et-voisins.html"], rapport="voisins.md",
        limites=["Les drapeaux Eurostat (rupture de série, définition différente, estimation) sont repris et affichés ; une rupture interdit de lire l’écart comme une évolution."]),
    Indicateur(
        "eu-regions", "Indicateurs régionaux de part et d’autre des frontières", theme="France et voisins (Eurostat)",
        definition="Diplômés du supérieur parmi les 25-34 ans, sorties précoces du système éducatif (18-24 ans), jeunes ni en emploi ni en formation (15-29 ans), par région NUTS 2.",
        formule="moyenne des 3 dernières années disponibles ; drapeau « peu fiable » conservé s’il touche une des années",
        champ="Région NUTS 2 contenant l’académie (anciennes régions) et régions frontalières étrangères.",
        sources=["eurostat_diplomes_sup_25_34.json", "eurostat_sorties_precoces_18_24.json", "eurostat_neet_15_29.json"],
        pages=["france-et-voisins.html"], rapport="voisins.md",
        limites=["Enquête Forces de travail : petits échantillons régionaux, d’où la moyenne sur 3 ans.",
                 "Les régions NUTS 2 ne coïncident pas exactement avec les académies."]),
]


def par_id() -> dict[str, Indicateur]:
    return {i.id: i for i in INDICATEURS}
