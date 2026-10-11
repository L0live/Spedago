"""Reproductibilité : un même fichier source donne les mêmes sorties, quel que soit l'ordre de ses lignes ;
et la part du privé sur Parcoursup publiée par « Mon académie » se recalcule depuis les fichiers bruts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from spedago.referentiel import annuaire_unique  # noqa: E402

RAW, PROC, WEB_DATA = ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "web" / "public" / "data"


def _annuaire() -> pd.DataFrame:
    p = RAW / "annuaire_lycees.csv"
    if not p.exists():
        pytest.skip("annuaire absent (lancer scripts/download_data.py)")
    return pd.read_csv(p, sep=";", dtype=str).rename(columns={"identifiant_de_l_etablissement": "uai"})


def test_annuaire_unique_independant_de_l_ordre():
    a = _annuaire()
    ref = annuaire_unique(a).set_index("uai")
    assert ref.index.is_unique and len(ref) == a.uai.nunique()
    for seed in range(5):
        autre = annuaire_unique(a.sample(frac=1, random_state=seed)).set_index("uai").loc[ref.index]
        pd.testing.assert_frame_equal(autre, ref)


def test_annuaire_unique_prefere_le_lycee_au_site_secondaire():
    a = pd.DataFrame({"uai": ["X"] * 3, "voie_generale": ["0", "1", "1"],
                      "nom_etablissement": ["Lycée A - pôle enseignement supérieur", "Annexe du lycée A", "Lycée A"],
                      "nom_commune": ["Ville", "Bourg", "Ville"]})
    for seed in range(4):
        assert annuaire_unique(a.sample(frac=1, random_state=seed)).nom_etablissement.tolist() == ["Lycée A"]


def test_export_insertion_trie():
    p = PROC / "insertion_master.json"
    if not p.exists():
        pytest.skip("insertion absente")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert list(d["formations"]) == sorted(d["formations"]) and list(d["mentions"]) == sorted(d["mentions"])


def test_part_du_prive_recalculee_depuis_les_bruts():
    M = json.loads((WEB_DATA / "mon_academie.json").read_text(encoding="utf-8"))
    hors = pd.read_csv(RAW / f"parcoursup_{M['session']}.csv", sep=";", low_memory=False)
    app = pd.read_csv(RAW / "parcoursup_apprentissage.csv", sep=";", low_memory=False)
    app = app[app.session == M["session"]]
    for cle_, d in (("hors_app", hors), ("app", app)):
        prive = d.contrat_etab.str.startswith("Privé")
        attendu = [len(d), int(prive.sum()), int(d.contrat_etab.eq("Privé hors contrat").sum()),
                   int(d.capa_fin.sum()), int(d.capa_fin[prive].sum())]
        assert M["france"]["prive"][cle_] == attendu
        # les académies (hors étranger) ne dépassent jamais le total national
        somme = [sum(a["prive"][cle_][i] for a in M["academies"] if a["prive"] and cle_ in a["prive"]) for i in range(5)]
        assert all(s <= t for s, t in zip(somme, attendu))
    # ordre de grandeur publié dans la fiche « ps-prive » : minoritaire hors apprentissage, majoritaire en apprentissage
    h, a = M["france"]["prive"]["hors_app"], M["france"]["prive"]["app"]
    assert h[1] / h[0] < 0.5 < a[1] / a[0]


def test_parts_du_prive_calculees_par_la_page(tmp_path):
    """AcadCalc.prive / somme (TypeScript, exécuté par la page) redonnent les parts calculées en Python."""
    import subprocess
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from jsharness import disponible, extract_page
    if not disponible():
        pytest.skip("node ou esbuild absent")
    code, data = extract_page("mon-academie")
    (tmp_path / "calc.js").write_text(code, encoding="utf-8")
    (tmp_path / "data.json").write_text(data, encoding="utf-8")
    (tmp_path / "run.js").write_text(
        "const C = require(process.argv[2]), D = require(process.argv[3]);\n"
        "const out = [D.france, ...D.academies].map((a) => { const p = a.prive || {}; return [C.prive(p.hors_app).part, C.prive(p.app).partPlaces,"
        " C.prive(C.somme(p.hors_app, p.app)).part, C.prive(C.somme(p.hors_app, p.app)).formations]; });\n"
        "console.log(JSON.stringify(out));\n", encoding="utf-8")
    js = json.loads(subprocess.run(["node", str(tmp_path / "run.js"), str(tmp_path / "calc.js"), str(tmp_path / "data.json")],
                                   capture_output=True, text=True, check=True).stdout)
    D = json.loads(data)
    nan = float("nan")
    for a, (p_h, pl_a, p_t, n_t) in zip([D["france"], *D["academies"]], js):
        h, ap = (a.get("prive") or {}).get("hors_app"), (a.get("prive") or {}).get("app")
        ratio = lambda x, y: x / y if y else nan  # noqa: E731
        exp = [ratio(h[1], h[0]) if h else nan, ratio(ap[4], ap[3]) if ap else nan]
        tot = [sum(v) for v in zip(h or [0] * 5, ap or [0] * 5)]
        for v, e in zip([p_h, pl_a, p_t], [*exp, ratio(tot[1], tot[0])]):
            assert (v is None and e != e) or v == pytest.approx(e, abs=1e-12), a.get("nom")
        assert n_t == tot[0]
