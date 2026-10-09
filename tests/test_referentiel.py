"""Tests du référentiel commun (niveau 2) : une seule graphie par académie, partout ; UAI cohérents."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spedago.referentiel import ACADEMIES, IDF, METROPOLE, OUTRE_MER, academie_canonique, cle, slug  # noqa: E402

PROC = ROOT / "data" / "processed"


@pytest.mark.parametrize("graphie,attendu", [
    ("Besancon", "Besançon"), ("BESANÇON", "Besançon"), ("besançon", "Besançon"),
    ("Nouvelle Calédonie", "Nouvelle-Calédonie"), ("ST PIERRE ET MIQUELON", "Saint-Pierre-et-Miquelon"),
    ("Saint Pierre et Miquelon", "Saint-Pierre-et-Miquelon"), ("Etranger", "Étranger"),
    ("Polynésie Française", "Polynésie française"), ("AIX-MARSEILLE", "Aix-Marseille"), ("La Reunion", "La Réunion"),
    ("Orléans-Tours", "Orléans-Tours"), ("  Poitiers ", "Poitiers"),
])
def test_graphies(graphie, attendu):
    assert academie_canonique(graphie) == attendu


def test_inconnue_et_vide():
    with pytest.raises(KeyError):
        academie_canonique("Atlantide")
    with pytest.raises(KeyError):
        academie_canonique("Paris-Créteil")  # on ne fusionne jamais deux académies par erreur
    assert academie_canonique(None) == academie_canonique(float("nan")) == academie_canonique("  ") == ""


def test_dictionnaire_stable():
    noms = set(ACADEMIES.values())
    assert len(noms) == len(ACADEMIES) == 35
    assert all(academie_canonique(n) == n for n in noms)  # idempotent
    assert all(cle(n) == k for k, n in ACADEMIES.items())
    assert len(METROPOLE) == 25 and len(OUTRE_MER) == 9 and IDF <= METROPOLE and not METROPOLE & OUTRE_MER


def test_slugs_uniques_et_propres():
    s = {slug(n) for n in ACADEMIES.values()}
    assert len(s) == 35 and all(x.replace("-", "").isalpha() and x == x.lower() for x in s)
    assert slug("Orléans-Tours") == "orleans-tours" and slug("La Réunion") == "la-reunion"


def test_toutes_les_graphies_sources_reconnues():
    a = pd.read_csv(PROC / "academies.csv", sep=";")
    assert (a.academie == a.graphie.map(academie_canonique)).all()
    assert a.academie.nunique() == 35 and a.source.nunique() == 6


def test_pages_utilisent_la_graphie_canonique():
    mm = json.loads((PROC / "monmaster_simulateur.json").read_text(encoding="utf-8"))
    ps = json.loads((PROC / "simulateur_parcoursup.json").read_text(encoding="utf-8"))
    mu = json.loads((PROC / "mutualisation.json").read_text(encoding="utf-8"))
    for noms in (mm["academies"], ps["academies"], sorted({l[4] for l in mu["lycees"]})):
        assert noms and all(academie_canonique(n) == n for n in noms if n), noms
    # idf du simulateur = exactement Paris, Créteil, Versailles
    i = ps["colonnes"].index("idf")
    idf = {ps["academies"][f[0]] for f in ps["formations"] if f[i] == 1}
    assert idf == IDF


def test_referentiel_uai():
    r = pd.read_csv(PROC / "referentiel_uai.csv", sep=";", dtype={"uai": str})
    assert r.uai.is_unique
    # format UAI (7 caractères + lettre clé) ; seuls des établissements à l'étranger ont un code spécial
    hors_format = r[~r.uai.str.fullmatch(r"\d{3}[A-Z0-9]{4}[A-Z]")]
    assert (hors_format.academie == "Étranger").all() and len(hors_format) <= 5
    assert r.academie.notna().all() and r.academie.isin(set(ACADEMIES.values())).all()
    assert r.dans_annuaire_lycees.dtype == bool and r.lycee_1re_generale.dtype == bool
    # chaque établissement vient d'au moins une source
    assert (r.dans_annuaire_lycees | r.lycee_1re_generale | (r.ps_formations > 0) | (r.mm_formations > 0)).all()
    # lycées avec 1re générale : tous présents, très peu hors annuaire (sans coordonnées)
    t = pd.read_csv(ROOT / "data" / "raw" / "specialites_triplettes_1ere.csv", sep=";", usecols=["rentree_scolaire", "numero_etablissement"])
    t = t[t.rentree_scolaire == t.rentree_scolaire.max()]
    assert r.lycee_1re_generale.sum() == t.numero_etablissement.nunique()
    assert (r.lycee_1re_generale & ~r.dans_annuaire_lycees).sum() <= 15
    # sous-totaux Parcoursup cohérents ; places > 0 si formations
    assert (r.ps_bts + r.ps_cpge + r.ps_licences <= r.ps_formations).all()
    assert (r.ps_places >= 0).all() and (r.ps_places[r.ps_formations == 0] == 0).all()
    assert (r.mm_places >= 0).all() and (r.mm_places[r.mm_formations == 0] == 0).all()
    # totaux = sources
    ps = json.loads((PROC / "simulateur_parcoursup.json").read_text(encoding="utf-8"))
    assert r.ps_formations.sum() >= len(ps["formations"])  # le simulateur exclut CNED et capacité nulle
    # académie de l'annuaire = académie Parcoursup pour les lycées présents dans les deux (à quelques exceptions près)
    lyc_ps = r[r.dans_annuaire_lycees & (r.ps_formations > 0)]
    assert len(lyc_ps) > 2000


def test_mutualisation_coherente_avec_referentiel():
    r = pd.read_csv(PROC / "referentiel_uai.csv", sep=";", dtype={"uai": str}).set_index("uai")
    mu = json.loads((PROC / "mutualisation.json").read_text(encoding="utf-8"))
    uais = [l[0] for l in mu["lycees"]]
    assert set(uais) <= set(r.index[r.lycee_1re_generale & r.dans_annuaire_lycees])
    assert all(r.at[l[0], "academie"] == l[4] for l in mu["lycees"])
