"""Spédago — libellés lisibles, communs à toutes les pages (les clés des données ne changent pas)."""
from __future__ import annotations

# Filières Parcoursup (fili_harmo) -> libellé affiché
FILIERES = {
    "Autre formation": "Autres formations", "BTS": "BTS", "BUT": "BUT", "CPGE": "Classes prépa (CPGE)",
    "EFTS": "Travail social (EFTS)", "Ecole d'Ingénieur": "Écoles d'ingénieurs", "Ecole de Commerce": "Écoles de commerce",
    "IFSI": "Soins infirmiers (IFSI)", "Licence": "Licences", "Licence_Las": "Licences accès santé (L.AS)",
    "PASS": "Parcours accès santé (PASS)",
}

# Spécialités de 1re (clés DEPP de la carte) -> libellé officiel
SPECIALITES = {
    "humanites_litterature_et_philosophie": "Humanités, littérature et philosophie",
    "langues_litterature_et_cultures_etrangeres_et_regionales": "Langues, littératures et cultures étrangères et régionales",
    "hist_geo_geopolitique_sc_politiques": "Histoire-géographie, géopolitique et sciences politiques",
    "sciences_economiques_et_sociales": "Sciences économiques et sociales",
    "mathematiques": "Mathématiques", "physique_chimie": "Physique-chimie",
    "sciences_de_la_vie_et_de_la_terre": "Sciences de la vie et de la Terre",
    "sciences_de_l_ingenieur": "Sciences de l'ingénieur",
    "numerique_et_sciences_informatiques": "Numérique et sciences informatiques",
    "musique": "Musique", "arts_plastiques": "Arts plastiques",
    "educ_physique_pratique_cult_sportive": "Éducation physique, pratiques et culture sportives",
    "histoire_des_arts": "Histoire des arts", "theatre": "Théâtre", "cinema_audiovisuel": "Cinéma-audiovisuel",
}

# Profils Mon Master proposés à l'étudiant
PROFILS_MASTER = {"lg3": "En L3 générale", "lp3": "En licence pro", "but3": "En BUT 3e année", "master": "Déjà en master",
                  "autre": "Autre inscription", "noninscri": "Reprise d'études"}

# Enseignements de spécialité de terminale générale :
# (identifiant, libellé, nom dans les données Parcoursup, clés de la carte des spécialités de 1re)
EDS = [
    ("maths", "Mathématiques", "Mathématiques Spécialité", ["mathematiques"]),
    ("pc", "Physique-chimie", "Physique-Chimie Spécialité", ["physique_chimie"]),
    ("svt", "Sciences de la vie et de la Terre", "Sciences de la vie et de la Terre Spécialité", ["sciences_de_la_vie_et_de_la_terre"]),
    ("ses", "Sciences économiques et sociales", "Sciences Economiques et Sociales Spécialité", ["sciences_economiques_et_sociales"]),
    ("hggsp", "Histoire-géographie, géopolitique et sciences politiques", "Histoire-Géographie, Géopolitique et Sciences politiques",
     ["hist_geo_geopolitique_sc_politiques"]),
    ("hlp", "Humanités, littérature et philosophie", "Humanités, Littérature et Philosophie", ["humanites_litterature_et_philosophie"]),
    ("llcer", "Langues, littératures et cultures étrangères et régionales", "Langues, littératures et cultures étrangères et régionales",
     ["langues_litterature_et_cultures_etrangeres_et_regionales"]),
    ("nsi", "Numérique et sciences informatiques", "Numérique et Sciences Informatiques", ["numerique_et_sciences_informatiques"]),
    ("si", "Sciences de l'ingénieur", "Sciences de l'ingénieur et sciences physiques", ["sciences_de_l_ingenieur"]),
    ("eppcs", "Éducation physique, pratiques et culture sportives", "Éducation physique, pratiques et culture sportives",
     ["educ_physique_pratique_cult_sportive"]),
    ("arts", "Arts (musique, arts plastiques, théâtre, cinéma, histoire des arts)", "Art",
     ["musique", "arts_plastiques", "histoire_des_arts", "theatre", "cinema_audiovisuel"]),
    ("llca", "Littérature et langues et cultures de l'Antiquité", "Littérature et langues et cultures de l'Antiquité", []),
    ("bio", "Biologie-écologie (lycées agricoles)", "Biologie/Ecologie", []),
]
