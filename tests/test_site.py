"""Tests du site (niveau 3) : navigation commune, ancres d'académie, page « Mon académie ».

« Mon académie » recalcule ses nombres en Python ; on vérifie qu'ils sont IDENTIQUES à ceux que les autres pages
calculent dans le navigateur (SimCalc, MutCalc) ou embarquent (Boussole), et aux tables d'analyse publiées.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
from jsharness import extract_page  # noqa: E402
from spedago.pages import PAGES, nav  # noqa: E402
from spedago.referentiel import ACADEMIES, academie_canonique, slug  # noqa: E402
from spedago.stats import wilson  # noqa: E402

APP, SITE, PROC = ROOT / "app", ROOT / "site", ROOT / "data" / "processed"
NOMS = {f: APP / f for f, _, _ in PAGES}
pytestmark = pytest.mark.skipif(shutil.which("node") is None or not all(p.exists() for p in NOMS.values()),
                                reason="node ou pages construites absents")

RUNNER = r"""
const fs = require('fs'), cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const S = require(cfg.commun), Sim = require(cfg.sim), Mut = require(cfg.mut), A = require(cfg.acad);
const DS = JSON.parse(fs.readFileSync(cfg.simData, 'utf8')), DM = JSON.parse(fs.readFileSync(cfg.mutData, 'utf8'));
const DA = JSON.parse(fs.readFileSync(cfg.acadData, 'utf8'));
const out = { slugs: cfg.noms.map(S.slug) };
const r = Sim.simulate(DS, {}), g = Sim.groupBy(DS, r, Sim.COL.A);
out.sim = Object.fromEntries(g.map((x) => [DS.academies[x.key], [x.ajout, r.couvertA.get(x.key) || 0, x.visees]]));
out.simFr = [r.total, r.couvert, r.add.filter((x) => x > 0).length];
out.mut = {};
for (const a of DA.academies) out.mut[a.nom] = DM.specialites.map((_, sp) => { const s = Mut.summary(DM, sp, "", a.nom); return [s.n, s.eleves, Mut.groups(DM, sp, "", a.nom).length]; });
out.wilson = cfg.kn.map(([k, n]) => A.wilson(k, n));
out.spe = DA.academies.map((a) => (a.spe ? A.speRows(a.spe.spe).map((x) => x.sp) : null));
out.ps = DA.academies.map((a) => (a.ps ? A.ps(a.ps.total) : null));
out.mm = DA.academies.map((a) => (a.mm ? A.mm(a.mm.total) : null));
out.idx = A.indexOf(DA, "poitiers");
process.stdout.write(JSON.stringify(out, (k, v) => (typeof v === 'number' && !isFinite(v) ? null : v)));
"""
DROLES = ["Saint-Étienne", "L’Haÿ-les-Roses", "  ST DENIS ", "Aix--Marseille", "Œuvre d'art", "a'b c-d"]


@pytest.fixture(scope="module")
def js(tmp_path_factory):
    d = tmp_path_factory.mktemp("site")
    commun = re.search(r'<script id="commun">(.*?)</script>', (APP / "_commun.html").read_text(encoding="utf-8"), re.S).group(1)
    (d / "commun.js").write_text(commun, encoding="utf-8")
    datas = {}
    for key, page in (("sim", "simulateur-parcoursup.html"), ("mut", "mutualisation.html"), ("acad", "mon-academie.html")):
        calc, data = extract_page(NOMS[page].read_text(encoding="utf-8"))
        (d / f"{key}.js").write_text(calc, encoding="utf-8")
        (d / f"{key}.json").write_text(data, encoding="utf-8")
        datas[key] = json.loads(data)
    kn = [[0, 0], [0, 5], [5, 5], [3, 10], [17, 364], [986, 3575]]
    cfg = {"commun": str(d / "commun.js"), "sim": str(d / "sim.js"), "mut": str(d / "mut.js"), "acad": str(d / "acad.js"),
           "simData": str(d / "sim.json"), "mutData": str(d / "mut.json"), "acadData": str(d / "acad.json"),
           "noms": list(ACADEMIES.values()) + DROLES, "kn": kn}
    (d / "cfg.json").write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
    (d / "run.js").write_text(RUNNER, encoding="utf-8")
    out = subprocess.run(["node", str(d / "run.js"), str(d / "cfg.json")], capture_output=True, text=True, check=True, timeout=300)
    return json.loads(out.stdout), datas, cfg


# ---------- ancres d'académie et navigation ----------

def test_slug_js_identique_au_python(js):
    out, _, cfg = js
    assert out["slugs"] == [slug(n) for n in cfg["noms"]]


def test_navigation_commune_sur_toutes_les_pages():
    commun = (APP / "_commun.html").read_text(encoding="utf-8")
    for f, _, _ in PAGES:
        html = NOMS[f].read_text(encoding="utf-8")
        assert "__" not in re.sub(r'<script type="application/json" id="data">.*?</script>', "", html, flags=re.S) \
            .replace("__proto__", ""), f"jeton non remplacé dans {f}"
        assert html.count('<nav class="site-nav"') == 1 and nav(f) in html, f
        assert html.count(f'data-page="{f}" aria-current="page"') == 1, f
        assert html.count('<script id="commun">') == 1 and commun.strip() in html, f
        assert "prefers-color-scheme: dark" not in html and 'data-theme="dark"' not in html, f"thème sombre restant dans {f}"
        hrefs = re.findall(r'href="([^"#]+)', nav(f))
        assert sorted(set(hrefs)) == sorted(NOMS), (f, hrefs)
    assert "color-scheme: light" in commun and "--orange:" in commun
    for t in APP.glob("*_template.html"):
        s = t.read_text(encoding="utf-8")
        assert "__COMMUN__" in s and "__NAV__" in s, t.name
        assert "--bg:" not in s and "fonts.googleapis" not in s, f"styles de base dupliqués dans {t.name}"


def test_documents_complets_du_site():
    for f, _, _ in PAGES:
        s = (SITE / f).read_text(encoding="utf-8")
        assert s.startswith("<!doctype html>") and '<meta charset="utf-8">' in s and s.rstrip().endswith("</html>")
        assert NOMS[f].read_text(encoding="utf-8") in s, f"site/{f} périmé : relancer scripts/build_site.py"


def test_les_outils_lisent_l_ancre():
    for f, sel in (("boussole-des-masters.html", 'Spedago.pick($("academie"))'), ("mutualisation.html", 'Spedago.pick($("acad"))'),
                   ("mon-academie.html", 'Spedago.pick($("acad"))'), ("simulateur-parcoursup.html", "Spedago.hashSlug()")):
        assert sel in NOMS[f].read_text(encoding="utf-8"), f


# ---------- « Mon académie » : mêmes nombres que les autres pages ----------

def test_academies_canoniques_et_ancres_uniques(js):
    _, datas, _ = js
    A = datas["acad"]["academies"]
    assert [a["slug"] for a in A] == [slug(a["nom"]) for a in A] and len({a["slug"] for a in A}) == len(A)
    assert all(academie_canonique(a["nom"]) == a["nom"] for a in A) and "Étranger" not in {a["nom"] for a in A}
    assert len(A) >= 30


def test_parcoursup_egal_table_de_tension(js):
    _, datas, _ = js
    D = datas["acad"]
    t = pd.read_csv(PROC / "tension_academie_filiere.csv", sep=";")
    t = t[t.session == D["session"]].assign(academie=lambda x: x.academie.map(academie_canonique))
    cols = ["formations", "places", "admis", "voeux_pp", "places_saturees", "vacantes"]
    n = 0
    for a in D["academies"]:
        if not a["ps"]:
            continue
        ref = t[t.academie == a["nom"]].set_index("fili_harmo")
        assert len(ref) == len(a["ps"]["filieres"]), a["nom"]
        for r in a["ps"]["filieres"]:
            assert r[1:] == [int(round(v)) for v in ref.loc[D["filieres"][r[0]], cols]], (a["nom"], r)
            n += 1
        assert a["ps"]["total"] == [int(round(v)) for v in ref[cols].sum()], a["nom"]
    assert n > 250
    assert D["france"]["ps"]["total"] == [int(round(v)) for v in t[cols].sum()]


def test_regle_de_depart_egale_le_simulateur(js):
    out, datas, _ = js
    D = datas["acad"]
    for a in D["academies"]:
        if a["ps"]:
            assert a["ps"]["sim"] == out["sim"][a["nom"]], a["nom"]
    assert D["france"]["ps"]["sim"] == out["simFr"]
    assert sum(a["ps"]["sim"][0] for a in D["academies"] if a["ps"]) <= out["simFr"][0]  # Étranger exclu


def test_specialites_egales_la_carte(js):
    out, datas, _ = js
    D = datas["acad"]
    for a in D["academies"]:
        got = out["mut"][a["nom"]]
        if not a["spe"]:
            assert all(sum(n.values()) == 0 for n, _, _ in got), a["nom"]
            continue
        for sp, (n, el, ng) in enumerate(got):
            r = a["spe"]["spe"][sp]
            assert r[:5] == [n["0"], n["2"], n["3"], n["4"], n["5"]], (a["nom"], sp)
            assert r[5:8] == [el["3"], el["4"], el["5"]] and r[8] == ng, (a["nom"], sp)
        assert a["spe"]["lycees"] == sum(got[0][0].values())


def test_masters_egaux_a_la_boussole(js):
    _, datas, _ = js
    D = datas["acad"]
    B = json.loads(extract_page(NOMS["boussole-des-masters.html"].read_text(encoding="utf-8"))[1])
    s = B["sessions"].index(D["session"]); ns = len(B["sessions"])
    P = B["profils"]
    part = [P.index(p) for p in ("lg3", "lp3", "but3", "master", "autre", "noninscri")]
    tot = {}
    for f in B["formations"]:
        st = f[9]
        cell = lambda p, j: st[(p * ns + s) * 2 + j]  # noqa: E731
        if cell(P.index("lg3"), 0) < 0:
            continue  # formation absente en 2025
        a = B["academies"][f[2]]
        t = tot.setdefault(a, [0] * 6)
        t[0] += 1; t[1] += f[7][s] or 0
        t[2] += sum(max(cell(p, 0), 0) for p in part); t[3] += sum(max(cell(p, 1), 0) for p in part)
        t[4] += max(cell(P.index("lg3"), 0), 0); t[5] += max(cell(P.index("lg3"), 1), 0)
    for a in D["academies"]:
        if a["mm"]:
            assert a["mm"]["total"] == tot[a["nom"]], a["nom"]
    assert D["france"]["mm"]["total"] == [sum(v[i] for v in tot.values()) for i in range(6)]


def test_calculs_de_la_page(js):
    out, datas, cfg = js
    D = datas["acad"]
    lo, hi = wilson([k for k, _ in cfg["kn"]], [n for _, n in cfg["kn"]])
    for (l, h), a, b in zip(out["wilson"], lo, hi):
        assert (l is None and np.isnan(a)) or abs(l - a) < 1e-12 and abs(h - b) < 1e-12
    for a, order, p, m in zip(D["academies"], out["spe"], out["ps"], out["mm"]):
        if a["spe"]:
            ref = sorted(range(len(a["spe"]["spe"])), key=lambda i: (-a["spe"]["spe"][i][4], -a["spe"]["spe"][i][7], i))
            assert order == ref
        if a["ps"]:
            t = a["ps"]["total"]
            assert abs(p["vpp"] - t[3] / t[1]) < 1e-12 and abs(p["partSat"] - t[4] / t[1]) < 1e-12
        if a["mm"]:
            t = a["mm"]["total"]
            assert m["tauxL3"] is None and t[4] == 0 or abs(m["tauxL3"] - t[5] / t[4]) < 1e-12
    assert D["academies"][out["idx"]]["nom"] == "Poitiers"
