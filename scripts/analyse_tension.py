"""Spédago — piste A : tension sur Parcoursup par filière et académie (2020-2025).

Usage : python3 scripts/analyse_tension.py
Entrée  : data/processed/parcoursup_panel_2020_2025.csv.gz (build_parcoursup_panel.py)
Sorties : data/processed/tension_academie_filiere.csv
          reports/tension.md

Définitions (au niveau formation) :
  pression    = vœux en phase principale / places (capa_fin)  — « taux de pression »
  remplissage = admis / places
  saturée     = remplissage ≥ SEUIL_SATURE ; sous-remplie = remplissage < SEUIL_SOUS_REMPLIE
L'académie est celle de la FORMATION, pas du candidat (l'open data ne donne pas l'origine).
Les vœux comptent des candidatures : un candidat est compté dans chaque formation demandée.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "data" / "processed" / "parcoursup_panel_2020_2025.csv.gz"
OUT_CSV = ROOT / "data" / "processed" / "tension_academie_filiere.csv"
OUT_MD = ROOT / "reports" / "tension.md"

SEUIL_SATURE = 0.95
SEUIL_SOUS_REMPLIE = 0.80
HORS_METROPOLE = {"Etranger", "Guadeloupe", "Guyane", "La Réunion", "Martinique", "Mayotte",
                  "Nouvelle-Calédonie", "Polynésie Française"}


def load_panel(path: Path = PANEL) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", low_memory=False)
    # Exclusions : capacité nulle ; CNED (capacités nominales d'enseignement à distance, ~25 000 places vacantes fictives)
    df = df[~df["flag_capacite_nulle"] & ~df["flag_cned"]].copy()
    df["pression"] = df["nb_voe_pp"] / df["capa_fin"]
    df["remplissage"] = df["acc_tot"] / df["capa_fin"]
    df["saturee"] = df["remplissage"] >= SEUIL_SATURE
    df["sous_remplie"] = df["remplissage"] < SEUIL_SOUS_REMPLIE
    return df


def aggregate(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    g = df.assign(places_saturees=df.capa_fin.where(df.saturee, 0),
                  vacantes_sous_remplies=df.ind_places_vacantes.where(df.sous_remplie, 0))
    a = g.groupby(keys).agg(
        formations=("cod_aff_form", "size"), places=("capa_fin", "sum"), admis=("acc_tot", "sum"),
        vacantes=("ind_places_vacantes", "sum"), voeux_pp=("nb_voe_pp", "sum"),
        places_saturees=("places_saturees", "sum"), vacantes_sous_remplies=("vacantes_sous_remplies", "sum"),
        pression_mediane=("pression", "median"))
    a["voeux_par_place"] = a.voeux_pp / a.places
    a["taux_remplissage"] = a.admis / a.places
    a["taux_vacance"] = a.vacantes / a.places
    a["part_places_saturees"] = a.places_saturees / a.places
    return a.reset_index()


def coexistence(df: pd.DataFrame, session: int) -> pd.DataFrame:
    """Cellules (académie × filière) où des formations saturées coexistent avec des places vacantes
    dans des formations sous-remplies : signe d'un décalage offre/demande à l'intérieur de la cellule."""
    d = df[df.session == session]
    a = aggregate(d, ["academie", "fili_harmo"])
    a["coexistence"] = (a.places_saturees > 0) & (a.vacantes_sous_remplies > 0)
    return a


def persistence(df: pd.DataFrame) -> pd.DataFrame:
    """La pression et la saturation de l'année t-1 prédisent-elles celles de l'année t ?"""
    rows = []
    for t in sorted(df.session.unique())[1:]:
        prev = df[df.session == t - 1].set_index("cod_aff_form")
        cur = df[df.session == t].set_index("cod_aff_form")
        j = prev[["pression", "saturee", "capa_fin"]].join(cur[["pression", "saturee", "capa_fin"]], lsuffix="_prev", how="inner")
        rows.append({
            "session": t, "formations_suivies": len(j),
            # Spearman = Pearson sur les rangs (évite la dépendance à scipy)
            "spearman_pression": j.pression_prev.rank().corr(j.pression.rank()),
            "p_sature_si_sature_avant": j.loc[j.saturee_prev, "saturee"].mean(),
            "p_sature_si_non_sature_avant": j.loc[~j.saturee_prev, "saturee"].mean(),
        })
    return pd.DataFrame(rows)


def capacity_response(df: pd.DataFrame) -> pd.DataFrame:
    """Les capacités réagissent-elles déjà à la pression ? Variation des places entre t-1 et t
    selon le quintile de pression (dans la filière) en t-1, formations présentes les deux années."""
    out = []
    for t in sorted(df.session.unique())[1:]:
        prev = df[df.session == t - 1].set_index("cod_aff_form")
        cur = df[df.session == t].set_index("cod_aff_form")
        j = prev[["pression", "capa_fin", "fili_harmo"]].join(cur[["capa_fin"]], rsuffix="_t", how="inner")
        j["quintile"] = j.groupby("fili_harmo").pression.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) + 1)
        j["session"] = t
        out.append(j)
    j = pd.concat(out)
    r = j.groupby("quintile").agg(formations=("capa_fin", "size"), places_avant=("capa_fin", "sum"), places_apres=("capa_fin_t", "sum"))
    r["variation_places_pct"] = (r.places_apres / r.places_avant - 1) * 100
    r["part_formations_en_hausse"] = j.assign(h=j.capa_fin_t > j.capa_fin).groupby("quintile").h.mean()
    return r.reset_index()


def fmt(df: pd.DataFrame, pct: tuple = (), ints: tuple = (), dec: tuple = ()) -> str:
    d = df.copy()
    for c in pct: d[c] = (d[c] * 100).map("{:.1f} %".format)
    for c in ints: d[c] = d[c].map("{:,.0f}".format)
    for c in dec: d[c] = d[c].map("{:.2f}".format)
    return d.to_markdown(index=False)


def main() -> None:
    df = load_panel()
    detail = aggregate(df, ["session", "academie", "fili_harmo"])
    detail.to_csv(OUT_CSV, sep=";", index=False)

    L = ["# Piste A — tension sur Parcoursup (2020-2025)", "",
         f"Formations à capacité nulle et CNED (capacités nominales) exclues. Saturée : remplissage ≥ {SEUIL_SATURE:.0%} ; "
         f"sous-remplie : < {SEUIL_SOUS_REMPLIE:.0%}. Académie = lieu de la formation.", ""]

    nat = aggregate(df, ["session"])
    L += ["## 1. National", "", fmt(nat[["session", "formations", "places", "admis", "vacantes", "voeux_par_place", "taux_remplissage", "part_places_saturees"]],
                                     pct=("taux_remplissage", "part_places_saturees"), ints=("formations", "places", "admis", "vacantes"), dec=("voeux_par_place",)), ""]

    d25 = df[df.session == 2025]
    fil = aggregate(d25, ["fili_harmo"]).sort_values("voeux_par_place", ascending=False)
    L += ["## 2. Par filière (2025)", "", fmt(fil[["fili_harmo", "formations", "places", "vacantes", "voeux_par_place", "taux_vacance", "part_places_saturees"]],
                                              pct=("taux_vacance", "part_places_saturees"), ints=("formations", "places", "vacantes"), dec=("voeux_par_place",)), ""]

    met = d25[~d25.academie.isin(HORS_METROPOLE)]
    idf = aggregate(met.assign(zone=np.where(met.idf, "Île-de-France", "Autres académies métropole")), ["fili_harmo", "zone"])
    piv = idf.pivot(index="fili_harmo", columns="zone", values=["voeux_par_place", "taux_vacance"])
    piv.columns = [f"{a} — {b}" for a, b in piv.columns]
    L += ["## 3. Île-de-France vs reste de la métropole, par filière (2025)", "", piv.round(3).reset_index().to_markdown(index=False), ""]

    acad = aggregate(met, ["academie"]).sort_values("voeux_par_place", ascending=False)
    L += ["## 4. Par académie (2025, métropole)", "", fmt(acad[["academie", "places", "vacantes", "voeux_par_place", "taux_vacance", "part_places_saturees"]],
                                                          pct=("taux_vacance", "part_places_saturees"), ints=("places", "vacantes"), dec=("voeux_par_place",)), ""]

    co = coexistence(df, 2025)
    tot_vac = d25.ind_places_vacantes.sum()
    L += ["## 5. Décalage offre/demande à l'intérieur d'une même académie × filière (2025)", "",
          f"- Cellules académie × filière : {len(co)} ; avec coexistence saturation / sous-remplissage : **{co.coexistence.sum()}**",
          f"- Places vacantes dans des formations sous-remplies de ces cellules : **{co.loc[co.coexistence, 'vacantes_sous_remplies'].sum():,.0f}** "
          f"(sur {tot_vac:,.0f} places vacantes au total)",
          f"- Places dans des formations saturées de ces cellules : {co.loc[co.coexistence, 'places_saturees'].sum():,.0f}",
          "- **ATTENTION : chiffre surestimé.** Ce niveau agrège des spécialités non substituables et inclut le privé hors contrat. "
          "Au niveau académie × filière × spécialité, public + privé sous contrat, le chiffre tombe à environ un tiers : "
          "voir `reports/tension_robustesse.md`.", ""]

    pers = persistence(df)
    L += ["## 6. Persistance de la tension (t-1 → t)", "", fmt(pers, pct=("p_sature_si_sature_avant", "p_sature_si_non_sature_avant"), ints=("formations_suivies",), dec=("spearman_pression",)), ""]

    resp = capacity_response(df)
    L += ["## 7. Les places réagissent-elles déjà à la pression ? (2021-2025 empilées)", "",
          "Quintile de pression de l'année t-1 calculé au sein de chaque filière (1 = faible, 5 = forte).", "",
          fmt(resp, pct=("part_formations_en_hausse",), ints=("formations", "places_avant", "places_apres"), dec=("variation_places_pct",)), ""]

    L += ["## Limites", "",
          "- Vœux ≠ candidats : un même candidat compte dans chaque formation demandée ; la pression mesure la demande relative, pas des personnes.",
          "- Académie de la formation, pas du candidat : on ne mesure pas la mobilité ni l'origine.",
          "- `capa_fin` peut différer de la capacité réellement ouverte en cours de procédure (surbooking).",
          "- Corrélations descriptives : aucune relation causale n'est établie."]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"-> {OUT_MD}\n-> {OUT_CSV}")


if __name__ == "__main__":
    main()
