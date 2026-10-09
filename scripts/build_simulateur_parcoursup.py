"""Spédago — piste A : données et page du « Simulateur de places Parcoursup ».

Usage : python3 scripts/build_simulateur_parcoursup.py
Entrées : data/processed/parcoursup_panel_2020_2025.csv.gz, app/simulateur_template.html
Sorties : data/processed/simulateur_parcoursup.json, app/simulateur-parcoursup.html

La page applique, dans le navigateur, les mêmes règles que scripts/simulate_ppl_art2.py à la dernière session
(2025) pour montrer ce qu'elles donneraient l'année suivante. La parité JS/Python est testée
(tests/test_page_js.py).

Une ligne par formation (hors CNED, capacité > 0) :
  [académie, filière, spécialité, idf 0/1, mobilisable 0/1, places, admis, candidats PP, non_appelés (-1 = inconnu),
   liste commune (1/0, -1 = inconnu)]
« mobilisable » = public ou privé sous contrat (places que l'État peut redéployer).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import simulate_ppl_art2 as sim  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "data" / "processed" / "simulateur_parcoursup.json"
TPL = ROOT / "app" / "simulateur_template.html"
OUT_PAGE = ROOT / "app" / "simulateur-parcoursup.html"
SESSION = 2025


def export(df: pd.DataFrame, session: int = SESSION) -> dict:
    d = df[df.session == session].copy()
    dicts = {}
    for c in ("academie", "fili_harmo", "fil_lib_voe_acc"):
        vals = sorted(d[c].fillna("").astype(str).unique().tolist())
        dicts[c] = (vals, {v: i for i, v in enumerate(vals)})
    mob = d.contrat_etab.isin(sim.PERIMETRE_GISEMENT)
    # liste_commune est relue en flottant (1.0 / 0.0 / NaN) : comparer, ne pas mapper sur des booléens
    lc = np.where(d.liste_commune.isna(), -1, (d.liste_commune == 1).astype(int))
    na = d.non_appeles.fillna(-1).round().astype(int)
    rows = np.column_stack([
        d.academie.fillna("").astype(str).map(dicts["academie"][1]),
        d.fili_harmo.fillna("").astype(str).map(dicts["fili_harmo"][1]),
        d.fil_lib_voe_acc.fillna("").astype(str).map(dicts["fil_lib_voe_acc"][1]),
        d.idf.astype(int), mob.astype(int), d.capa_fin.round().astype(int), d.acc_tot.round().astype(int),
        d.nb_voe_pp.round().astype(int), na, lc]).tolist()
    return {"session": session, "academies": dicts["academie"][0], "filieres": dicts["fili_harmo"][0],
            "specialites": dicts["fil_lib_voe_acc"][0], "perimetre_mobilisable": sorted(sim.PERIMETRE_GISEMENT),
            "colonnes": ["academie", "filiere", "specialite", "idf", "mobilisable", "places", "admis", "candidats_pp",
                         "non_appeles", "liste_commune"], "formations": rows}


def main() -> None:
    raw = pd.read_csv(sim.PANEL, sep=";", low_memory=False)
    df = sim.prepare(raw)
    data = export(df)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if TPL.exists():
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        OUT_PAGE.write_text(TPL.read_text(encoding="utf-8").replace("__DATA__", payload), encoding="utf-8")
        print(f"-> {OUT_PAGE} ({OUT_PAGE.stat().st_size / 1e6:.1f} Mo)")
    print(f"{len(data['formations']):,} formations -> {OUT_JSON}")


if __name__ == "__main__":
    main()
