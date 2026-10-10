"""Tests de la porte lycéens « Mes spécialités » : calcul de la page (JavaScript) = calcul indépendant sur les fichiers bruts."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "tests"))
import build_mes_specialites as ms  # noqa: E402
from jsharness import extract_page  # noqa: E402
from spedago.libelles import EDS  # noqa: E402
from spedago.stats import wilson  # noqa: E402

PAGE = ROOT / "app" / "mes-specialites.html"
pytestmark = pytest.mark.skipif(not PAGE.exists() or shutil.which("node") is None, reason="page ou node absents")
RUNNER = r"""
const C = require(process.argv[2]); const D = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const out = { g: D.doublettes.map((_, d) => C.groupes(D, d)), r: D.doublettes.map((_, d) => C.resume(D, d)),
  f: [[0, 0], [5, 3]].map(([d, g]) => C.fines(D, d, g)), dbl: [[0, 1], [1, 0], [0, 0], [11, 12]].map(([a, b]) => C.doublette(D, a, b)),
  lyc: [0, 100, 500, 1500].map((li) => C.lycee(D, li, [0, 10, 11])) };
process.stdout.write(JSON.stringify(out, (k, v) => (typeof v === 'number' && !isFinite(v) ? null : v)));
"""


@pytest.fixture(scope="module")
def js(tmp_path_factory):
    calc, data = extract_page(PAGE.read_text(encoding="utf-8"))
    d = tmp_path_factory.mktemp("ms")
    (d / "c.js").write_text(calc, encoding="utf-8"); (d / "d.json").write_text(data, encoding="utf-8"); (d / "r.js").write_text(RUNNER, encoding="utf-8")
    out = subprocess.run(["node", str(d / "r.js"), str(d / "c.js"), str(d / "d.json")], capture_output=True, text=True, check=True, timeout=300)
    return json.loads(out.stdout), json.loads(data)


def test_toutes_les_doublettes_reconnues():
    v3, v2 = ms.charge()
    assert v3.d.notna().all() and v2.d.notna().all()
    assert len(set(v3.d)) == 75 and all(a <= b for a, b in v3.d)
    assert v3[v3.niveau_d_agregation == 0].voeux.sum() == 380_190   # bacheliers généraux 2025 (open data Parcoursup)
    with pytest.raises(KeyError):
        ms.doublette("Mathématiques Spécialité,Astrologie")


def test_groupes_identiques_au_calcul_independant(js):
    out, D = js
    v3 = pd.read_csv(ms.RAW / "parcoursup_specialites_v3.csv", sep=";")
    v3["d"] = v3.doublette.map(ms.doublette); v3["groupe"] = v3.regroupement_de_formations.map(ms.nettoie)
    l1 = v3[v3.niveau_d_agregation == 1]
    tot = l1.groupby("groupe")[["voeux", "propositions_d_admissions"]].sum()
    n0 = v3[v3.niveau_d_agregation == 0].set_index("d").voeux
    di = {tuple(d): i for i, d in enumerate(D["doublettes"])}
    gi = {g[0]: i for i, g in enumerate(D["groupes"])}
    checked = 0
    for r in l1.itertuples():
        got = next(x for x in out["g"][di[r.d]] if x["key"] == gi[r.groupe])
        v, p = r.voeux, r.propositions_d_admissions
        assert (got["n"], got["k"]) == (v, p)
        nO, kO = tot.at[r.groupe, "voeux"] - v, tot.at[r.groupe, "propositions_d_admissions"] - p
        assert got["nO"] == nO
        if v:
            lo, hi = wilson(p, v)
            assert abs(got["p"] - p / v) < 1e-12 and abs(got["lo"] - lo) < 1e-12 and abs(got["hi"] - hi) < 1e-12
            assert abs(got["part"] - v / n0[r.d]) < 1e-12
        if nO:
            assert abs(got["pO"] - kO / nO) < 1e-12
        checked += 1
    assert checked == len(l1) > 5000


def test_resume_et_doublette(js):
    out, D = js
    r = out["r"][next(i for i, d in enumerate(D["doublettes"]) if d == [0, 1])]   # maths + physique-chimie
    assert r["n"] == 83_925 and r["rang"] == 1 and abs(r["p"] - 82_650 / 83_925) < 1e-12
    assert out["dbl"][0] == out["dbl"][1] >= 0 and out["dbl"][2] == -1


def test_fines_coherentes(js):
    out, D = js
    for (d, g), rows in zip([[0, 0], [5, 3]], out["f"]):
        assert all(D["formations"][x["key"]][0] == g for x in rows)
        assert all(x["k"] <= x["n"] for x in rows)


def test_mon_lycee_egal_a_la_carte(js):
    out, D = js
    keys = D["carte_specialites"]
    for li, res in zip([0, 100, 500, 1500], out["lyc"]):
        l = D["lycees"][li]
        for r in res:
            ks = [keys.index(k) for k in D["eds"][r["eds"]][2]]
            if not ks:
                assert r["etat"] == "hors_carte"; continue
            codes = [l[4][x] for x in ks]
            attendu = "propose" if 0 in codes else "incertain" if 2 in codes else "absent"
            assert r["etat"] == attendu
            if attendu == "absent":
                kms = [l[5][str(x)][0] for x in ks if str(x) in l[5]]
                assert (r["km"] is None and not kms) or r["km"] == min(kms)
    assert [e[0] for e in EDS] == [e[0] for e in D["eds"]]
