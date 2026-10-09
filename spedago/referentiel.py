"""Spédago — référentiel commun : académies (une graphie canonique) et établissements (UAI).

Les sources écrivent les académies différemment : « Besancon » / « Besançon » / « BESANCON »,
« Nouvelle Calédonie » / « Nouvelle-Calédonie », « ST PIERRE ET MIQUELON », « Etranger » / « Étranger »…
`academie_canonique` ramène toute graphie connue à un nom unique et lève une erreur pour une graphie inconnue
(mieux vaut casser que regrouper à tort).
"""
from __future__ import annotations

import re
import unicodedata

# clé normalisée -> nom canonique affiché
ACADEMIES = {
    "AIX MARSEILLE": "Aix-Marseille", "AMIENS": "Amiens", "BESANCON": "Besançon", "BORDEAUX": "Bordeaux",
    "CLERMONT FERRAND": "Clermont-Ferrand", "CORSE": "Corse", "CRETEIL": "Créteil", "DIJON": "Dijon",
    "GRENOBLE": "Grenoble", "LILLE": "Lille", "LIMOGES": "Limoges", "LYON": "Lyon", "MONTPELLIER": "Montpellier",
    "NANCY METZ": "Nancy-Metz", "NANTES": "Nantes", "NICE": "Nice", "NORMANDIE": "Normandie",
    "ORLEANS TOURS": "Orléans-Tours", "PARIS": "Paris", "POITIERS": "Poitiers", "REIMS": "Reims", "RENNES": "Rennes",
    "STRASBOURG": "Strasbourg", "TOULOUSE": "Toulouse", "VERSAILLES": "Versailles",
    "GUADELOUPE": "Guadeloupe", "GUYANE": "Guyane", "LA REUNION": "La Réunion", "MARTINIQUE": "Martinique",
    "MAYOTTE": "Mayotte", "NOUVELLE CALEDONIE": "Nouvelle-Calédonie", "POLYNESIE FRANCAISE": "Polynésie française",
    "SAINT PIERRE ET MIQUELON": "Saint-Pierre-et-Miquelon", "WALLIS ET FUTUNA": "Wallis-et-Futuna",
    "ETRANGER": "Étranger",
}
IDF = {"Paris", "Créteil", "Versailles"}
OUTRE_MER = {"Guadeloupe", "Guyane", "La Réunion", "Martinique", "Mayotte", "Nouvelle-Calédonie",
             "Polynésie française", "Saint-Pierre-et-Miquelon", "Wallis-et-Futuna"}
METROPOLE = set(ACADEMIES.values()) - OUTRE_MER - {"Étranger"}


def cle(nom: str) -> str:
    s = unicodedata.normalize("NFKD", str(nom)).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[-'’\s]+", " ", s).strip()
    return re.sub(r"^ST ", "SAINT ", s)


def academie_canonique(nom) -> str:
    if nom is None or (isinstance(nom, float) and nom != nom) or str(nom).strip() == "":
        return ""
    k = cle(nom)
    if k not in ACADEMIES:
        raise KeyError(f"académie inconnue : {nom!r} (clé {k!r})")
    return ACADEMIES[k]


def slug(nom: str) -> str:
    """Identifiant d'ancre d'URL (#…) : lettres minuscules et tirets."""
    return cle(nom).lower().replace(" ", "-")
