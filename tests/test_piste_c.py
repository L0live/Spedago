"""Tests Spédago — piste C (Mon Master).  Lancer : python3 -m pytest tests/ -q"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_monmaster as mm  # noqa: E402

JSON = ROOT / "data" / "processed" / "monmaster_simulateur.json"
needs_raw = pytest.mark.skipif(not mm.RAW.exists(), reason="données Mon Master absentes")
needs_json = pytest.mark.skipif(not JSON.exists(), reason="export JSON absent")


def test_wilson_valeurs_de_reference():
    lo, hi = mm.wilson(np.array([5]), np.array([10]))
    assert lo[0] == pytest.approx(0.2366, abs=1e-3) and hi[0] == pytest.approx(0.7634, abs=1e-3)
    lo, hi = mm.wilson(np.array([0]), np.array([0]))
    assert np.isnan(lo[0]) and np.isnan(hi[0])


def test_ecart_intra_formation_neutralise_l_effet_formation():
    # Formation A très sélective, B très ouverte ; dans CHAQUE formation, a et b ont le même taux.
    rows = []
    for ifc, rate, na, nb in (("A", 0.1, 100, 10), ("B", 0.9, 10, 100)):
        rows += [{"session": 2025, "ifc": ifc, "profil": "a", "candidats": na, "propositions": rate * na},
                 {"session": 2025, "ifc": ifc, "profil": "b", "candidats": nb, "propositions": rate * nb}]
    long = pd.DataFrame(rows)
    pooled_a = long[long.profil == "a"].propositions.sum() / long[long.profil == "a"].candidats.sum()
    pooled_b = long[long.profil == "b"].propositions.sum() / long[long.profil == "b"].candidats.sum()
    assert abs(pooled_a - pooled_b) > 0.5          # l'agrégat naïf trompe (paradoxe de Simpson)
    assert mm.within_gap(long, "a", "b")["ecart_points"] == pytest.approx(0, abs=1e-9)


@pytest.fixture(scope="module")
def raw():
    return mm.load()


@pytest.fixture(scope="module")
def long(raw):
    return mm.to_long(raw)


@needs_raw
def test_profils_partitionnent_les_totaux(raw):
    for etape, suff in (("can", "pp"), ("can", "pc"), ("clas", "total"), ("prop", "total"), ("accept", "total")):
        s = sum(raw[f"n_{etape}_{p}_{suff}"] for p in mm.PROFILS)
        tot = raw[f"n_{etape}_{suff}"] if etape != "can" else raw[f"n_can_{suff}"]
        assert (s == tot).all(), (etape, suff)


@needs_raw
def test_bornes_et_coherence(long):
    assert (long.propositions <= long.candidats).all()
    assert (long.acceptations <= long.propositions).all()
    assert (long.candidats >= 0).all()
    t = long.taux_prop.dropna()
    assert t.between(0, 1).all()
    ok = long.candidats > 0
    assert ((long.ic_bas[ok] <= long.taux_prop[ok] + 1e-12) & (long.taux_prop[ok] <= long.ic_haut[ok] + 1e-12)).all()


@needs_raw
def test_etab_plus_hors_etab_egal_total(raw, long):
    w = long[long.profil.isin(["etab", "hors_etab"])].groupby(["session", "ifc"])[["candidats", "propositions"]].sum()
    ref = raw.set_index(["session", "ifc"])
    assert (w.candidats == (ref.n_can_pp + ref.n_can_pc).reindex(w.index)).all()
    assert (w.propositions == ref.n_prop_total.reindex(w.index)).all()


@needs_raw
def test_identifiant_formation_unique_par_session(raw):
    assert not raw.duplicated(["session", "ifc"]).any()


@needs_json
def test_json_reconstruit_les_donnees(long):
    d = json.loads(JSON.read_text(encoding="utf-8"))
    P, S = d["profils"], d["sessions"]
    assert all(len(f[9]) == len(P) * len(S) * 2 for f in d["formations"])
    f = d["formations"][123]
    for i, p in enumerate(P):
        for j, s in enumerate(S):
            n, k = f[9][(i * len(S) + j) * 2: (i * len(S) + j) * 2 + 2]
            ref = long[(long.ifc.astype(str) == f[0]) & (long.profil == p) & (long.session == s)]
            if ref.empty:
                assert (n, k) == (-1, -1)
            else:
                assert (n, k) == (int(ref.candidats.iloc[0]), int(ref.propositions.iloc[0]))
    assert d["mentions"][f[3]] == long[long.ifc.astype(str) == f[0]].sort_values("session").mention.iloc[-1]


# ---------- correction bayésienne ----------

def test_shrink_tire_vers_la_moyenne_a_proportion_de_kappa():
    assert mm.shrink(8, 10, 0.2, 10) == pytest.approx((8 + 2) / 20)          # peu de candidats : fort rappel
    assert mm.shrink(800, 1000, 0.2, 10) == pytest.approx(802 / 1010)        # beaucoup : presque le taux brut


def test_moments_retrouvent_une_loi_beta_simulee():
    rng = np.random.default_rng(3)
    m, kappa = 0.25, 20
    p = rng.beta(m * kappa, (1 - m) * kappa, 4000)
    n = rng.integers(20, 300, 4000)
    k = rng.binomial(n, p)
    m_hat, k_hat = mm._moments(k.astype(float), n.astype(float))
    assert m_hat == pytest.approx(m, abs=0.01) and k_hat == pytest.approx(kappa, rel=0.15)


@needs_raw
def test_correction_ameliore_la_prevision_2025(long):
    bt, _ = mm.backtest(long)
    tous = bt.set_index("couples").loc["tous"]
    assert tous.erreur_abs_corrige_pts < tous.erreur_abs_brut_pts
    petits = bt.set_index("couples").loc["moins de 30 candidats en 2024"]
    assert petits.erreur_abs_corrige_pts < petits.erreur_abs_brut_pts


@needs_json
def test_priors_exportes_pour_chaque_mention():
    d = json.loads(JSON.read_text(encoding="utf-8"))
    used = {f[3] for f in d["formations"]}
    assert used <= {int(k) for k in d["priors"]}
    m, kappa = d["priors"][str(next(iter(used)))]["lg3"]
    assert 0 <= m <= 1 and mm.KAPPA_MIN <= kappa <= mm.KAPPA_MAX
