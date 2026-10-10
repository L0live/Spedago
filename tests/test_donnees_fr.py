"""Tests des données françaises ajoutées : insertion (InserSup), poursuite d'études (SIES), résultats des lycées (IVAL)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from spedago.referentiel import academie_canonique  # noqa: E402

RAW, PROC = ROOT / "data" / "raw", ROOT / "data" / "processed"
pytestmark = pytest.mark.skipif(not (PROC / "insertion_master.json").exists(), reason="données absentes")


def test_insertion_regle_de_selection():
    I = json.loads((PROC / "insertion_master.json").read_text(encoding="utf-8"))
    raw = pd.read_csv(RAW / "insersup_master.csv", sep=";", low_memory=False, dtype={"promo": str})
    raw["tx"] = pd.to_numeric(raw.tx_sortants_en_emploi_sal_fr_18.replace("nd", np.nan), errors="coerce") / 100
    m = pd.read_csv(PROC / "monmaster_formations.csv", sep=";", low_memory=False)
    m = m[m.profil == "lg3"].sort_values("session").drop_duplicates("ifc", keep="last").set_index("ifc")
    ok, tot = I["couverture"]
    assert tot == len(m) and 0.6 < ok / tot < 0.9
    rng = np.random.default_rng(3)
    for ifc in rng.choice(list(I["formations"]), 200, replace=False):
        tx, n, promo, _ = I["formations"][ifc]
        r = m.loc[ifc]
        cand = raw[((raw.etablissement == r.eta_uai) | (raw.uai_fresq == r.eta_uai)) & (raw.libelle_diplome == r.mention) & raw.tx.notna()]
        fin = cand.promo.str.split(",").map(lambda x: max(map(int, x)))
        best = cand[fin == fin.max()]
        best = best[~best.promo.str.contains(",")] if (~best.promo.str.contains(",")).any() else best
        assert promo == best.promo.iloc[0].replace(",", "-") and abs(tx - best.tx.iloc[0]) < 1e-4, ifc
    assert all(0 <= v[0] <= 1 and v[1] > 0 for v in I["formations"].values())
    assert all(0 <= v <= 1 for v in I["mentions"].values())


def test_insertion_dans_la_boussole():
    data = (ROOT / "web" / "public" / "data" / "boussole.json").read_text(encoding="utf-8")
    page = (ROOT / "web" / "boussole-des-masters.html").read_text(encoding="utf-8")
    assert '"insertion":{"mois":18' in data and "Insertion à 18 mois" in page


def test_poursuite_academies_egale_france():
    D = json.loads((PROC / "mon_academie.json").read_text(encoding="utf-8"))
    p = pd.read_csv(RAW / "poursuite_academie.csv", sep=";")
    p = p[p.rentree_session == D["rentree_poursuite"]]
    fr = {r[0]: r for r in D["france"]["pours"]}
    for voie, g in p.groupby("voie_du_baccalaureat"):
        tot = sum(g[c].sum() for c in g.columns if c.endswith(("_flux", "_stable")))
        assert fr[voie][1] == g.bacheliers.sum() and abs(sum(fr[voie][2:]) - tot) <= 5
    # la somme des académies présentes redonne la France (aucune académie perdue au renommage)
    noms = {academie_canonique(a) for a in p.aca_lib}
    acads = [a for a in D["academies"] if a["pours"]]
    assert {a["nom"] for a in acads} == noms - {"Étranger"}
    for i, voie in enumerate(fr):
        assert sum(a["pours"][i][1] for a in acads) == fr[voie][1]
    # ordre de grandeur publié : ~ 78 % des bacheliers poursuivent
    t = sum(sum(r[2:]) for r in D["france"]["pours"]) / sum(r[1] for r in D["france"]["pours"])
    assert 0.7 < t < 0.85


def test_ival_des_lycees():
    D = json.loads((PROC / "mes_specialites.json").read_text(encoding="utf-8"))
    iv = pd.read_csv(RAW / "ival_lycees_gt.csv", sep=";", low_memory=False)
    iv = iv[iv.annee == D["annee_ival"]].drop_duplicates("uai").set_index("uai")
    n = 0
    for l in D["lycees"][::50]:
        if l[6] is None:
            assert l[0] not in iv.index; continue
        for got, col in zip(l[6][:2], ["taux_reu_total", "va_reu_total"]):
            ref = iv.at[l[0], col]
            assert (got is None and pd.isna(ref)) or got == ref, (l[0], col)
        n += 1
    assert n > 30 and sum(1 for l in D["lycees"] if l[6]) / len(D["lycees"]) > 0.9
