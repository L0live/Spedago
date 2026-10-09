"""Spédago — piste A : contrôles de robustesse de l'analyse de tension.

Usage : python3 scripts/analyse_tension_fine.py
Entrée  : data/processed/parcoursup_panel_2020_2025.csv.gz
Sortie  : reports/tension_robustesse.md

Répond aux faiblesses de reports/tension.md :
  1. Granularité : le décalage offre/demande mesuré par académie × filière agrège des spécialités
     non substituables (BTS Comptabilité ≠ BTS Électrotechnique). On le refait par spécialité
     (`fil_lib_voe_acc`, 438 modalités) et par département.
  2. Périmètre : public + privé sous contrat seulement (le privé hors contrat et le « privé
     enseignement supérieur » sont un autre marché). CNED et capacités nulles exclus.
  3. Une place vacante ne compte que si une demande classée non servie existe à côté :
     réaffectable = min(vacantes des sous-remplies, classés non appelés des saturées) par cellule.
  4. Sensibilité aux seuils de saturation / sous-remplissage.
  5. Attrition du panel : les formations qui disparaissent biaisent-elles la persistance ?
  6. Comparabilité de la pression entre filières (listes communes, candidatures groupées).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyse_tension import load_panel  # noqa: E402  (exclut CNED et capacités nulles)

ROOT = Path(__file__).resolve().parent.parent
OUT_MD = ROOT / "reports" / "tension_robustesse.md"
PERIMETRE = {"Public", "Privé sous contrat d'association"}
NIVEAUX = {
    "académie × filière (analyse initiale)": ["academie", "fili_harmo"],
    "académie × filière × spécialité": ["academie", "fili_harmo", "fil_lib_voe_acc"],
    "département × filière × spécialité": ["dep", "fili_harmo", "fil_lib_voe_acc"],
}


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    d = df[df.contrat_etab.isin(PERIMETRE)].copy()
    commune = d.liste_commune == True  # noqa: E712
    rang_max = d[["ran_grp1", "ran_grp2", "ran_grp3"]].max(axis=1)
    ok = ~commune & d.liste_commune.notna() & ~d.flag_rang_incoherent.astype(bool)
    d["non_appeles"] = (d.nb_cla_pp - rang_max).clip(lower=0).where(ok)
    d["vacantes"] = (d.capa_fin - d.acc_tot).clip(lower=0)
    return d


def mismatch(d: pd.DataFrame, keys: list[str], sat: float, sous: float) -> dict:
    r = d.acc_tot / d.capa_fin
    x = d.assign(v_sous=d.vacantes.where(r < sous, 0),
                 u_sat=d.non_appeles.where(r >= sat, 0).fillna(0),
                 places_sat=d.capa_fin.where(r >= sat, 0))
    c = x.groupby(keys)[["v_sous", "u_sat", "places_sat"]].sum()
    co = c[(c.places_sat > 0) & (c.v_sous > 0)]
    return {"cellules": len(c), "cellules_coexistence": len(co),
            "vacantes_coexistence": co.v_sous.sum(),
            "reaffectables": np.minimum(c.v_sous, c.u_sat).sum(),
            "vacantes_total": d.vacantes.sum()}


def attrition(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for t in sorted(df.session.unique())[1:]:
        prev = df[df.session == t - 1].set_index("cod_aff_form")
        cur = df[df.session == t].set_index("cod_aff_form")
        sat_prev = (prev.acc_tot / prev.capa_fin) >= 0.95
        present = prev.index.isin(cur.index)
        sat_cur = ((cur.acc_tot / cur.capa_fin) >= 0.95).reindex(prev.index)
        surv = present & sat_prev.to_numpy()
        rows.append({"session_t": t,
                     "sortie_si_saturee": 1 - present[sat_prev.to_numpy()].mean(),
                     "sortie_si_non_saturee": 1 - present[~sat_prev.to_numpy()].mean(),
                     "persistance_survivantes": sat_cur[surv].mean(),
                     "persistance_borne_basse": sat_cur[sat_prev].astype("boolean").fillna(False).astype(bool).mean()})
    return pd.DataFrame(rows)


def main() -> None:
    df = load_panel()
    d25 = prepare(df[df.session == 2025])
    L = ["# Piste A — contrôles de robustesse (session 2025 sauf mention)", "",
         f"Périmètre : public + privé sous contrat, hors CNED et capacités nulles : {len(d25):,} formations, "
         f"{d25.capa_fin.sum():,.0f} places, {d25.vacantes.sum():,.0f} places vacantes.", ""]

    excl = df[(df.session == 2025) & ~df.contrat_etab.isin(PERIMETRE)]
    L += [f"Exclus (privé hors contrat + privé enseignement supérieur) : {len(excl):,} formations, "
          f"{(excl.capa_fin - excl.acc_tot).clip(lower=0).sum():,.0f} places vacantes.", ""]

    L += ["## 1-3. Décalage offre/demande selon la granularité (seuils 95 % / 80 %)", "",
          "| Niveau | Cellules | Cellules avec coexistence | Vacantes des sous-remplies en coexistence | Réaffectables (≤ classés non appelés à côté) |",
          "|---|---|---|---|---|"]
    for lab, keys in NIVEAUX.items():
        m = mismatch(d25, keys, 0.95, 0.80)
        L.append(f"| {lab} | {m['cellules']:,} | {m['cellules_coexistence']:,} | {m['vacantes_coexistence']:,.0f} "
                 f"({m['vacantes_coexistence'] / m['vacantes_total']:.0%}) | {m['reaffectables']:,.0f} |")
    L += ["", "Lecture : « réaffectables » ne compte une place vacante que si, dans la même cellule, une formation saturée "
          "a des candidats classés jamais appelés (borne haute : ces candidats ont pu être admis ailleurs ; "
          "les listes d'appel communes, sans rang exploitable, sont ignorées → borne basse sur ce point).", ""]

    L += ["## 4. Sensibilité aux seuils (niveau académie × filière × spécialité)", "",
          "| Saturée ≥ | Sous-remplie < | Vacantes en coexistence | Réaffectables |", "|---|---|---|---|"]
    for sat in (0.90, 0.95, 1.00):
        for sous in (0.70, 0.80, 0.90):
            m = mismatch(d25, NIVEAUX["académie × filière × spécialité"], sat, sous)
            L.append(f"| {sat:.0%} | {sous:.0%} | {m['vacantes_coexistence']:,.0f} | {m['reaffectables']:,.0f} |")

    att = attrition(df[df.contrat_etab.isin(PERIMETRE)])
    L += ["", "## 5. Attrition du panel et persistance de la saturation", "",
          att.round(3).to_markdown(index=False), "",
          "Borne basse : les formations disparues sont comptées comme non saturées. Si l'écart avec la persistance "
          "des survivantes est faible, l'attrition ne biaise pas la conclusion.", ""]

    f = d25.groupby("fili_harmo").agg(formations=("cod_aff_form", "size"),
                                      part_listes_communes=("liste_commune", lambda s: (s == True).mean()),  # noqa: E712
                                      candidats_par_place_median=("pression", "median")).round(3)
    L += ["## 6. Comparabilité de la pression entre filières", "",
          "La méthodologie officielle définit `nb_voe_pp` comme un effectif de CANDIDATS par formation. "
          "Mais quand un vœu regroupe plusieurs formations (listes communes : IFSI, concours d'écoles, licences regroupées), "
          "un candidat compte dans chacune : la pression y est mécaniquement gonflée. Ne comparer la pression qu'à l'intérieur d'une filière.", "",
          f.reset_index().to_markdown(index=False), ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"-> {OUT_MD}")


if __name__ == "__main__":
    main()
