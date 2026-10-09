"""Tests Spédago — carte des mutualisations (piste B).  Lancer : python3 -m pytest tests/ -q"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_mutualisation as mu  # noqa: E402

needs_out = pytest.mark.skipif(not mu.OUT_JSON.exists(), reason="sortie mutualisation absente")


def test_haversine_paris_lyon():
    d = mu.haversine_matrix(np.array([48.8566, 45.7640]), np.array([2.3522, 4.8357]))
    assert d[0, 1] == pytest.approx(392, abs=3) and d[0, 0] == 0 and d[0, 1] == d[1, 0]


def test_statuts_et_taux():
    t = pd.DataFrame({"0613_maths_filles": [10, 0, np.nan], "0613_maths_garcons": [5, 0, 0],
                      "01_a_filles": [1, 1, 1], "01_a_garcons": [1, 1, 1]})
    st, cnt, names = mu.specialty_status(t)
    assert names == ["maths"] and st.maths.tolist() == ["o", "n", "m"]
    eff = pd.Series([50, 50, 50])
    lo = mu.take_up_rates(st, cnt, eff, offered_only=False).maths
    hi = mu.take_up_rates(st, cnt, eff, offered_only=True).maths
    assert lo == pytest.approx(15 / 100) and hi == pytest.approx(15 / 50)   # le lycée masqué est exclu des deux


def _toy():
    # O propose la spécialité ; A est à ~5 km de O ; B et C sont à ~60 km, à ~5 km l'un de l'autre ; D est isolé.
    lyc = pd.DataFrame({"uai": list("OABCD"), "statut": ["Public"] * 5, "effectif": [100, 100, 100, 100, 100],
                        "lat": [45.0, 45.045, 45.6, 45.645, 47.0], "lon": [1.0, 1.0, 1.0, 1.0, 1.0]})
    status = pd.DataFrame({"spe": ["o", "n", "n", "n", "n"]})
    return lyc, status, mu.haversine_matrix(lyc.lat.to_numpy(), lyc.lon.to_numpy())


def test_classification_sur_cas_construit():
    lyc, status, dist = _toy()
    pairs, groups = mu.classify(lyc, status, pd.Series({"spe": 0.1}), dist, r_km=20, seuil=12)
    cat = dict(zip(pairs.uai, pairs.categorie))
    assert cat == {"A": "acces_voisin", "B": "ouverture_commune", "C": "ouverture_commune", "D": "isole"}
    assert len(groups) == 1 and sorted(groups[0]["membres"]) == [2, 3] and groups[0]["demande"] == pytest.approx(20)


def test_seuil_non_atteint_et_statut_different():
    lyc, status, dist = _toy()
    pairs, groups = mu.classify(lyc, status, pd.Series({"spe": 0.05}), dist, r_km=20, seuil=12)   # 5 + 5 < 12
    assert groups == [] and set(pairs[pairs.uai.isin(["B", "C"])].categorie) == {"isole"}
    lyc.loc[lyc.uai == "A", "statut"] = "Privé"           # un lycée privé ne compte pas l'offre publique voisine
    pairs, _ = mu.classify(lyc, status, pd.Series({"spe": 0.1}), dist, r_km=20, seuil=12)
    assert dict(zip(pairs.uai, pairs.categorie))["A"] == "isole"


def test_lycee_masque_compte_comme_offre_voisine():
    lyc, status, dist = _toy()
    status = pd.DataFrame({"spe": ["n", "n", "n", "n", "n"]})
    status.loc[0, "spe"] = "m"                            # O masqué : probable petit groupe
    pairs, _ = mu.classify(lyc, status, pd.Series({"spe": 0.1}), dist, r_km=20, seuil=12)
    assert dict(zip(pairs.uai, pairs.categorie))["A"] == "acces_voisin" and "O" not in set(pairs.uai)


def test_taille_de_groupe_plafonnee():
    n = 8
    lyc = pd.DataFrame({"uai": [f"L{i}" for i in range(n)], "statut": ["Public"] * n, "effectif": [30] * n,
                        "lat": [46 + 0.01 * i for i in range(n)], "lon": [2.0] * n})
    status = pd.DataFrame({"spe": ["n"] * n})
    dist = mu.haversine_matrix(lyc.lat.to_numpy(), lyc.lon.to_numpy())
    _, groups = mu.classify(lyc, status, pd.Series({"spe": 0.1}), dist, r_km=20, seuil=12, max_membres=4)
    assert groups and all(len(g["membres"]) <= 4 for g in groups)
    flat = [m for g in groups for m in g["membres"]]
    assert len(flat) == len(set(flat))                  # un lycée n'appartient qu'à un groupe par spécialité


@needs_out
def test_sorties_coherentes():
    d = json.loads(mu.OUT_JSON.read_text(encoding="utf-8"))
    L = d["lycees"]
    lat = np.array([x[6] for x in L]); lon = np.array([x[7] for x in L])
    dist = mu.haversine_matrix(lat, lon)
    statut = [x[3] for x in L]
    for spe, membres, demande, rayon in d["groupes"]:
        assert 2 <= len(membres) <= mu.MAX_MEMBRES and demande >= d["seuil"] - 1e-9
        assert len({statut[m] for m in membres}) == 1
        assert dist[np.ix_(membres, membres)].max() <= 2 * d["rayon_km"] + 1e-6
        assert all(L[m][9][spe] == 4 for m in membres)   # chaque membre est classé « ouverture commune »
    codes = {c for x in L for c in x[9]}
    assert codes <= {0, 1, 2, 3, 4, 5} and 1 not in codes   # toute absence certaine a reçu une catégorie
    pairs = pd.read_csv(mu.OUT_CSV, sep=";")
    assert pairs.categorie.isin(["acces_voisin", "ouverture_commune", "isole"]).all()
    v = pairs[pairs.categorie == "acces_voisin"]
    assert (v.km_offre_la_plus_proche <= d["rayon_km"]).all()
