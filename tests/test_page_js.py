"""Tests Spédago — le calcul exécuté par la page « Boussole des masters » (JavaScript) est-il juste ?

Extrait le bloc <script id="calc"> de la page construite (app/boussole-des-masters.html), l'exécute avec
Node.js sur toutes les formations × profils, et compare à un calcul Python indépendant.
Lancer : python3 -m pytest tests/ -q
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
sys.path.insert(0, str(ROOT / "scripts"))
import build_monmaster as mm  # noqa: E402

sys.path.insert(0, str(ROOT / "tests"))
from jsharness import extract_page  # noqa: E402

PAGE = ROOT / "app" / "boussole-des-masters.html"
pytestmark = pytest.mark.skipif(not PAGE.exists() or shutil.which("node") is None, reason="page construite ou node absents")

PROFILS = ["lg3", "but3", "lp3", "master", "autre", "noninscri", "etab", "hors_etab"]
RUNNER = """
const C = require(process.argv[2]);
const D = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const cfg = JSON.parse(process.argv[4]);
const est = {};
for (const p of cfg.profils) est[p] = D.formations.map((f) => C.estimate(D, f, p));
const ranks = cfg.ranks.map(([p, o]) => C.rankMentions(D, p, o).map((g) => [g.mention, g.formations, g.places, g.n, g.k, g.p, g.lo, g.hi, g.best ? g.best.ifc : null]));
process.stdout.write(JSON.stringify({ est, ranks }, (k, v) => (typeof v === 'number' && !isFinite(v) ? null : v)));
"""


@pytest.fixture(scope="module")
def page_parts(tmp_path_factory):
    html = PAGE.read_text(encoding="utf-8")
    calc, data = extract_page(html)
    d = tmp_path_factory.mktemp("js")
    (d / "calc.js").write_text(calc, encoding="utf-8")
    (d / "data.json").write_text(data, encoding="utf-8")
    (d / "run.js").write_text(RUNNER, encoding="utf-8")
    return d, json.loads(data)


@pytest.fixture(scope="module")
def js(page_parts):
    d, D = page_parts
    acad = D["academies"].index("Poitiers")
    sect = D["secteurs"].index("Informatique")
    cfg = {"profils": PROFILS, "ranks": [["lg3", {}], ["but3", {"academie": str(acad)}], ["noninscri", {"modalite": "1"}],
                                         ["lg3", {"secteur": str(sect), "minCandidats": 10}]]}
    out = subprocess.run(["node", str(d / "run.js"), str(d / "calc.js"), str(d / "data.json"), json.dumps(cfg)],
                         capture_output=True, text=True, check=True, timeout=120)
    return json.loads(out.stdout), cfg, D


def reference_estimate(D: dict, f: list, profil: str) -> tuple:
    S, P = D["sessions"], D["profils"]
    i = P.index(profil)
    pairs = [f[9][(i * len(S) + j) * 2: (i * len(S) + j) * 2 + 2] for j in range(len(S))]
    n = sum(a for a, _ in pairs if a > 0)
    k = sum(b for a, b in pairs if a > 0)
    if n <= 0:
        return (n, k, None, None, None)
    prior = D["priors"].get(str(f[3]), {}).get(profil)
    if prior is None:
        lo, hi = mm.wilson(np.array([k]), np.array([n]))
        return (n, k, k / n, max(0.0, lo[0]), min(1.0, hi[0]))
    m, kap = prior
    a, b = k + kap * m, n - k + kap * (1 - m)
    mean = float(mm.shrink(k, n, m, kap))
    sd = (a * b / ((a + b) ** 2 * (a + b + 1))) ** 0.5
    return (n, k, mean, max(0.0, mean - 1.96 * sd), min(1.0, mean + 1.96 * sd))


def test_estimations_identiques_au_python_sur_tout(js):
    out, cfg, D = js
    ecart_max, compares = 0.0, 0
    for p in cfg["profils"]:
        for f, got in zip(D["formations"], out["est"][p]):
            ref = reference_estimate(D, f, p)
            assert got[0] == ref[0] and got[1] == ref[1]
            if ref[2] is None:
                assert got[2] is None
                continue
            ecart_max = max(ecart_max, *(abs(g - r) for g, r in zip(got[2:], ref[2:])))
            compares += 1
    assert compares > 40_000, compares
    assert ecart_max < 1e-9, ecart_max


def test_classement_des_mentions_identique_au_python(js):
    out, cfg, D = js
    S, last = D["sessions"], len(D["sessions"]) - 1
    for (profil, opts), got in zip(cfg["ranks"], out["ranks"]):
        fm = [f for f in D["formations"]
              if (opts.get("academie") is None or f[2] == int(opts["academie"]))
              and (opts.get("modalite") is None or f[5] == int(opts["modalite"]))
              and (opts.get("secteur") is None or f[6] == int(opts["secteur"]))]
        rows = []
        for f in fm:
            n, k, p, lo, _ = reference_estimate(D, f, profil)
            rows.append({"mention": f[3], "n": n, "k": k, "places": f[7][last] or 0, "lo": lo,
                         "ifc": f[0], "ouverte": f[7][last] is not None})
        t = pd.DataFrame(rows)
        g = t.groupby("mention").agg(formations=("ifc", "size"), places=("places", "sum"), n=("n", "sum"), k=("k", "sum"))
        g = g[g.n >= opts.get("minCandidats", 30)]
        lo, hi = mm.wilson(g.k.to_numpy(), g.n.to_numpy())
        g = g.assign(p=g.k / g.n, lo=np.maximum(lo, 0), hi=np.minimum(hi, 1))
        best = t[(t.n > 0) & t.ouverte].sort_values("lo", ascending=False, kind="stable").groupby("mention").ifc.first()
        js_df = pd.DataFrame(got, columns=["mention", "formations", "places", "n", "k", "p", "lo", "hi", "best"]).set_index("mention")
        assert set(js_df.index) == set(g.index), profil
        j = js_df.loc[g.index]
        for c in ("formations", "places", "n", "k"):
            assert (j[c].to_numpy() == g[c].to_numpy()).all(), c
        for c in ("p", "lo", "hi"):
            assert np.allclose(j[c].to_numpy(float), g[c].to_numpy(float), atol=1e-12), c
        assert (np.diff(js_df.lo.to_numpy(float)) <= 1e-15).all()          # trié par borne basse décroissante
        bl = t[(t.n > 0) & t.ouverte].groupby("mention").lo.max()
        jb = t.set_index("ifc").lo
        for men, ifc in js_df.best.dropna().items():                       # la meilleure formation a bien la borne basse maximale
            assert abs(jb[ifc] - bl[men]) < 1e-12
        del best


def test_cas_limites_js(page_parts):
    d, _ = page_parts
    code = """const C=require(process.argv[2]);const r=[C.posterior(0,0,[0.2,10]),C.posterior(5,10,null),C.posterior(10,10,[0.5,4]),C.wilson(0,5)];
    process.stdout.write(JSON.stringify(r,(k,v)=>typeof v==='number'&&!isFinite(v)?null:v));"""
    (d / "edge.js").write_text(code, encoding="utf-8")
    r = json.loads(subprocess.run(["node", str(d / "edge.js"), str(d / "calc.js")], capture_output=True, text=True, check=True).stdout)
    assert r[0] == [None, None, None]                                     # aucun candidat : pas d'estimation
    lo, hi = mm.wilson(np.array([5]), np.array([10]))
    assert r[1][0] == 0.5 and abs(r[1][1] - lo[0]) < 1e-12               # sans loi a priori : Wilson
    assert abs(r[2][0] - (10 + 2) / 14) < 1e-12 and r[2][2] <= 1         # bornes dans [0, 1]
    assert r[3][0] == 0 and r[3][1] == 0


# ---------- Simulateur des places en tension (piste A) ----------
import simulate_ppl_art2 as sim  # noqa: E402

PAGE_SIM = ROOT / "app" / "simulateur-parcoursup.html"
SIM_RUNNER = """
const C = require(process.argv[2]);
const D = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const grid = JSON.parse(process.argv[4]);
process.stdout.write(JSON.stringify(grid.map((p) => { const r = C.simulate(D, p); return { add: r.add, couvert: r.couvert, nElig: r.nElig,
  nonServis: r.nonServis, ajoutRang: r.ajoutRang, sansRang: r.sansRang, ajoutSansRang: r.ajoutSansRang,
  couvertes: r.couvertes, formationsRang: r.formationsRang, medianeRatio: r.medianeRatio }; })), (k, v) => (typeof v === 'number' && !isFinite(v) ? null : v));
"""
GRID = [{"regle": r, "pct": pct, "q": q, "sat": sat, "sous": 0.8}
        for r in ("s1", "s2") for pct in (0.07, 0.1, 0.2) for q in (0.5, 0.75, 0.9) for sat in (0.9, 0.95, 1.0)]


@pytest.fixture(scope="module")
def sim_js(tmp_path_factory):
    if not PAGE_SIM.exists():
        pytest.skip("page simulateur absente")
    html = PAGE_SIM.read_text(encoding="utf-8")
    calc, data = extract_page(html)
    d = tmp_path_factory.mktemp("sim")
    (d / "calc.js").write_text(calc, encoding="utf-8")
    (d / "data.json").write_text(data, encoding="utf-8")
    (d / "run.js").write_text(SIM_RUNNER, encoding="utf-8")
    out = subprocess.run(["node", str(d / "run.js"), str(d / "calc.js"), str(d / "data.json"), json.dumps(GRID)],
                         capture_output=True, text=True, check=True, timeout=300)
    return json.loads(out.stdout), json.loads(data), d


def test_simulateur_identique_au_script_python(sim_js):
    res, D, _ = sim_js
    raw = pd.read_csv(sim.PANEL, sep=";", low_memory=False)
    saved = (sim.Q_PRESSION, sim.SEUIL_SATURE, sim.SEUIL_SOUS_REMPLIE)
    try:
        for p, got in zip(GRID, res):
            sim.Q_PRESSION, sim.SEUIL_SATURE, sim.SEUIL_SOUS_REMPLIE = p["q"], p["sat"], p["sous"]
            prev = sim.prepare(raw)
            prev = prev[prev.session == D["session"]]
            assert len(prev) == len(got["add"])
            ref = sim.scenario_s1(prev, p["pct"]) if p["regle"] == "s1" else sim.scenario_s2(prev, p["pct"])
            assert (np.asarray(got["add"]) == ref.to_numpy()).all(), p
            assert got["nElig"] == int(prev.eligible.sum()), p
            if p["regle"] == "s1":
                assert got["couvert"] == int(sim.scenario_s3(prev, p["pct"]).couvert.sum()), p
            # demande non servie : candidats classés non appelés des formations qui reçoivent des places (listes propres)
            vis = ref > 0
            rang = prev.non_appeles.notna() & (prev.liste_commune != 1)
            assert got["nonServis"] == int(prev.non_appeles[vis & rang].sum()), p
            assert got["ajoutRang"] == int(ref[vis & rang].sum()) and got["ajoutSansRang"] == int(ref[vis & ~rang].sum()), p
            assert got["sansRang"] == int((vis & ~rang).sum()), p
            na, ad = prev.non_appeles[vis & rang], ref[vis & rang]
            assert got["formationsRang"] == len(na) and got["couvertes"] == int((na >= ad).sum()), p
            if len(na):
                assert abs(got["medianeRatio"] - float(np.median(na / ad))) < 1e-9, p
            if p["regle"] == "s2":
                assert got["ajoutRang"] <= got["nonServis"]   # la règle 2 n'ajoute jamais plus que les classés non appelés
    finally:
        sim.Q_PRESSION, sim.SEUIL_SATURE, sim.SEUIL_SOUS_REMPLIE = saved


def test_export_liste_commune_renseignee(sim_js):
    _, D, _ = sim_js
    lc = pd.Series([f[9] for f in D["formations"]])
    assert lc.isin([0, 1, -1]).all() and (lc == 1).mean() > 0.08 and (lc == -1).mean() < 0.02


def test_quantile_et_plafond_js(sim_js):
    _, _, d = sim_js
    rng = np.random.default_rng(5)
    v = sorted(rng.random(101).tolist())
    qs = [0.0, 0.33, 0.75, 0.9, 1.0]
    code = ("const C=require(process.argv[2]);const v=JSON.parse(process.argv[3]);"
            "process.stdout.write(JSON.stringify({q:JSON.parse(process.argv[4]).map(q=>C.quantile(v,q)),"
            "c:[C.ceilSafe(100*0.07),C.ceilSafe(30*0.1),C.ceilSafe(7.2)]}))")
    (d / "q.js").write_text(code, encoding="utf-8")
    out = json.loads(subprocess.run(["node", str(d / "q.js"), str(d / "calc.js"), json.dumps(v), json.dumps(qs)],
                                    capture_output=True, text=True, check=True).stdout)
    for q, got in zip(qs, out["q"]):
        assert abs(got - pd.Series(v).quantile(q)) < 1e-12
    assert out["c"] == [7, 3, 8]                      # 100 × 0,07 → 7 (et non 8), 7,2 → 8


# ---------- Carte des spécialités partagées (piste B) ----------
import build_mutualisation as mu  # noqa: E402

PAGE_MUT = ROOT / "app" / "mutualisation.html"
MUT_RUNNER = """
const C = require(process.argv[2]);
const D = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const cfg = JSON.parse(process.argv[4]);
process.stdout.write(JSON.stringify(cfg.map(([sp, st, ac]) => ({ s: C.summary(D, sp, st, ac), g: C.groups(D, sp, st, ac).map((x) => x[1][0]) }))));
"""


@pytest.fixture(scope="module")
def mut_js(tmp_path_factory):
    if not PAGE_MUT.exists():
        pytest.skip("page carte absente")
    html = PAGE_MUT.read_text(encoding="utf-8")
    calc, data = extract_page(html)
    D = json.loads(data)
    acads = ["", "Poitiers", "Créteil", "Strasbourg"]
    assert set(acads[1:]) <= {l[4] for l in D["lycees"]}
    cfg = [[sp, st, ac] for sp in range(len(D["specialites"])) for st in ("", "Public", "Privé") for ac in acads]
    d = tmp_path_factory.mktemp("mut")
    (d / "calc.js").write_text(calc, encoding="utf-8")
    (d / "data.json").write_text(data, encoding="utf-8")
    (d / "run.js").write_text(MUT_RUNNER, encoding="utf-8")
    out = subprocess.run(["node", str(d / "run.js"), str(d / "calc.js"), str(d / "data.json"), json.dumps(cfg)],
                         capture_output=True, text=True, check=True, timeout=120)
    return json.loads(out.stdout), cfg, D


def test_carte_compteurs_identiques_au_python(mut_js):
    """Référence indépendante de l'export : statuts recalculés depuis les sources brutes + catégories du CSV d'analyse."""
    res, cfg, D = mut_js
    lyc, status, _, _, _ = mu.load()
    pairs = pd.read_csv(mu.OUT_CSV, sep=";")
    cat = {"acces_voisin": 3, "ouverture_commune": 4, "isole": 5}
    assert lyc.uai.tolist() == [l[0] for l in D["lycees"]]
    codes = {}
    for j, spname in enumerate(D["specialites"]):
        c = status[spname].map({"o": 0, "m": 2, "n": 1}).to_numpy()
        p = pairs[pairs.specialite == spname]
        pos = {u: i for i, u in enumerate(lyc.uai)}
        for u, k in zip(p.uai, p.categorie):
            c[pos[u]] = cat[k]
        assert (c != 1).all(), spname
        codes[j] = c
    for (sp, st, ac), got in zip(cfg, res):
        vis = ((lyc.statut == st) if st else True) & ((lyc.academie == ac) if ac else True)
        vis = np.asarray(vis, bool) if not isinstance(vis, bool) else np.full(len(lyc), True)
        c = codes[sp][vis]
        eff = lyc.effectif.to_numpy()[vis]
        for k in (0, 2, 3, 4, 5):
            assert got["s"]["n"][str(k)] == int((c == k).sum()), (sp, st, ac, k)
        for k in (3, 4, 5):
            assert got["s"]["eleves"][str(k)] == int(eff[c == k].sum()), (sp, st, ac, k)
        ref = [g for g in D["groupes"] if g[0] == sp and any(vis[m] for m in g[1])]
        ref = sorted(ref, key=lambda g: (-g[2], g[1][0]))
        assert got["g"] == [g[1][0] for g in ref], (sp, st, ac)


def test_carte_sans_filtre_egale_le_rapport(mut_js):
    res, cfg, D = mut_js
    report = mu.OUT_MD.read_text(encoding="utf-8")
    for (sp, st, ac), got in zip(cfg, res):
        if st or ac:
            continue
        name = D["specialites"][sp]
        line = next(l for l in report.splitlines() if l.startswith(f"| {name} |"))
        cells = [c.strip() for c in line.strip("|").split("|")]
        assert int(cells[1]) == got["s"]["n"]["0"] and int(cells[5]) == got["s"]["n"]["3"], name
        assert int(cells[6].split(" ")[0]) == got["s"]["n"]["4"] and int(cells[7]) == got["s"]["n"]["5"], name
        assert int(cells[8].replace(",", "")) == got["s"]["eleves"]["5"], name
