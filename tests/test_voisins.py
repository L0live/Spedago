"""Tests de la page « France et voisins » : décodage JSON-stat, séries de mobilité, lignes des graphiques en points."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "tests"))
import build_voisins as bv  # noqa: E402
from jsharness import extract_page  # noqa: E402
from spedago.jsonstat import lire  # noqa: E402
from spedago.referentiel import academie_canonique  # noqa: E402

PAGE = ROOT / "app" / "france-et-voisins.html"
pytestmark = pytest.mark.skipif(not PAGE.exists() or shutil.which("node") is None, reason="page ou node absents")


@pytest.fixture(scope="module")
def js(tmp_path_factory):
    calc, data = extract_page(PAGE.read_text(encoding="utf-8"))
    D = json.loads(data)
    d = tmp_path_factory.mktemp("v")
    (d / "c.js").write_text(calc, encoding="utf-8"); (d / "d.json").write_text(data, encoding="utf-8")
    (d / "r.js").write_text("const C=require(process.argv[2]);const D=JSON.parse(require('fs').readFileSync(process.argv[3],'utf8'));"
                            "process.stdout.write(JSON.stringify({l:D.academies.map((_,i)=>D.indicateurs.map(([k])=>C.lignes(D,i,k))),"
                            "s:D.mobilite.pays.map(([c])=>C.serie(D,c))}))", encoding="utf-8")
    out = subprocess.run(["node", str(d / "r.js"), str(d / "c.js"), str(d / "d.json")], capture_output=True, text=True, check=True)
    return json.loads(out.stdout), D


def test_jsonstat_valeurs_connues():
    m = lire(bv.RAW / "eurostat_mobilite_francais_etranger.json")
    be = m[(m.geo == "BE") & (m.isced11 == "ED5-8")].set_index("time")
    assert be.at["2023", "valeur"] == 19104 and be.at["2020", "statut"] == "bd"   # contrôlé sur l'API le 10/10/2026
    # le total CITE 5-8 = somme des niveaux 5, 6, 7, 8 (quand tous sont publiés)
    for geo in ("BE", "ES", "DE"):
        x = m[(m.geo == geo) & (m.time == "2024")].set_index("isced11").valeur
        assert abs(x["ED5-8"] - x[["ED5", "ED6", "ED7", "ED8"]].sum()) <= 2


def test_academies_et_regions_completes(js):
    _, D = js
    assert all(academie_canonique(a[0]) == a[0] for a in D["academies"]) and len(D["academies"]) == 30
    codes = {c for a in D["academies"] for c in a[2] + a[3]}
    assert codes <= set(D["regions"]) and all(D["regions"][c]["v"] for c in codes)
    assert {c[:2] for a in D["academies"] for c in a[3]} <= {"BE", "LU", "DE", "CH", "IT", "ES"}


def test_lignes_egales_au_python(js):
    out, D = js
    for ai, a in enumerate(D["academies"]):
        for ki, (key, _, _) in enumerate(D["indicateurs"]):
            rows = out["l"][ai][ki]
            roles = [r["role"] for r in rows]
            assert roles == sorted(roles, key=["moi", "voisine", "ref"].index)
            assert [r["code"] for r in rows if r["role"] == "moi"] == a[2]
            refs = [r["code"] for r in rows if r["role"] == "ref"]
            assert refs[0] == "FR" and refs[-1] == "EU27_2020"
            for r in rows:
                assert r["v"] == D["regions"][r["code"]]["v"][key][0]


def test_moyenne_trois_ans(js):
    _, D = js
    d = lire(bv.RAW / "eurostat_diplomes_sup_25_34.json")
    g = d[(d.geo == "FRI3") & d.valeur.notna()].sort_values("time").tail(3)
    assert D["regions"]["FRI3"]["v"]["diplomes_sup_25_34"][0] == round(float(g.valeur.mean()), 1)


def test_series_mobilite(js):
    out, D = js
    m = lire(bv.RAW / "eurostat_mobilite_francais_etranger.json")
    for (c, _), s in zip(D["mobilite"]["pays"], out["s"]):
        x = m[(m.geo == c) & (m.isced11 == "ED5-8")].set_index("time")
        for r in s:
            if r["sortants"] is not None:
                assert r["sortants"] == int(x.at[r["annee"], "valeur"]) and r["flagS"] == x.at[r["annee"], "statut"]
