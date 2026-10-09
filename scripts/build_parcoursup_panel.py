"""Spédago — piste A : table Parcoursup harmonisée 2020-2025 (formation × session).

Usage : python3 scripts/build_parcoursup_panel.py
Entrée  : data/raw/parcoursup_{2020..2025}.csv
Sorties : data/processed/parcoursup_panel_2020_2025.csv.gz
          reports/parcoursup_panel_qualite.md

Périmètre : 2020-2025, seules années avec l'identifiant stable `cod_aff_form`.
Les variables conservées sont l'intersection des schémas 2020-2025 (106 colonnes).
Les indicateurs dérivés sont préfixés `ind_` ; les drapeaux qualité `flag_`.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.io import to_csv_gz  # noqa: E402
from spedago.stats import ratio  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
REP = ROOT / "reports"
YEARS = range(2020, 2026)

# Colonnes textuelles (identifiants, libellés) — tout le reste est converti en numérique.
TEXT_COLS = {
    "session", "cod_uai", "cod_aff_form", "contrat_etab", "region_etab_aff", "dep", "dep_lib",
    "acad_mies", "select_form", "fili", "form_lib_voe_acc", "fil_lib_voe_acc", "detail_forma",
    "lib_comp_voe_ins", "g_ea_lib_vx", "g_olocalisation_des_formations", "lien_form_psup",
    "lib_grp1", "lib_grp2", "lib_grp3", "tri", "list_com",
}


def load() -> pd.DataFrame:
    frames = [pd.read_csv(RAW / f"parcoursup_{y}.csv", sep=";", low_memory=False, dtype=str) for y in YEARS]
    common = sorted(set.intersection(*(set(f.columns) for f in frames)))
    # list_com n'existe pas toutes les années mais est nécessaire pour interpréter les rangs
    keep = common + (["list_com"] if "list_com" not in common else [])
    df = pd.concat([f.reindex(columns=keep) for f in frames], ignore_index=True)
    for c in df.columns:
        if c not in TEXT_COLS:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["session"] = df["session"].astype(int)
    df["cod_aff_form"] = df["cod_aff_form"].astype(str).str.strip()
    df["cod_uai"] = df["cod_uai"].astype(str).str.strip().str.upper()
    return harmonize(df)


def harmonize(df: pd.DataFrame) -> pd.DataFrame:
    """Corrections d'incohérences constatées dans les sources (voir rapport qualité)."""
    # 1. `list_com` : libellés inversés dans les sources 2024 et 2025. Preuve : sur les formations
    #    présentes en 2023 et 2025, ~1 600 passent de « commune » à « propre » et ~11 200 de
    #    « propre » à « commune » ; le taux de rang > classés suit l'étiquette inversée.
    commune = df["list_com"].str.contains("commune", case=False, na=False)
    inverted = df["session"].isin([2024, 2025])
    df["liste_commune"] = np.where(df["list_com"].isna(), np.nan, np.where(inverted, ~commune, commune))
    # 2. `list_com` absent en 2020 : on reporte la valeur 2021 de la même formation (si elle existe).
    v2021 = df.loc[df.session == 2021].set_index("cod_aff_form")["liste_commune"]
    m2020 = df.session == 2020
    df.loc[m2020, "liste_commune"] = df.loc[m2020, "cod_aff_form"].map(v2021)
    df["liste_commune_imputee_2021"] = m2020 & df["liste_commune"].notna()
    # 3. Filières : le DUT (2020) devient BUT (2021+).
    df["fili_harmo"] = df["fili"].replace({"DUT": "BUT"})
    #    En 2024 seulement, 9 diplômes paramédicaux (orthophonie, ergothérapie, DTS imagerie…, 175 formations)
    #    sont classés « IFSI » ; ils sont en « Autre formation » toutes les autres années -> on aligne.
    df.loc[(df["fili"] == "IFSI") & (df["fil_lib_voe_acc"] != "D.E Infirmier"), "fili_harmo"] = "Autre formation"
    # 4. Académies : graphie variable selon les années (« Besançon » en 2022 seulement).
    df["academie"] = df["acad_mies"].replace({"Besançon": "Besancon"})
    df["idf"] = df["academie"].isin(["Paris", "Créteil", "Versailles"])
    return df


def derive(df: pd.DataFrame) -> pd.DataFrame:
    voe_neobac = df[["nb_voe_pp_bg", "nb_voe_pp_bt", "nb_voe_pp_bp"]].sum(axis=1, min_count=1)
    voe_brs = df[["nb_voe_pp_bg_brs", "nb_voe_pp_bt_brs", "nb_voe_pp_bp_brs"]].sum(axis=1, min_count=1)
    cla_neobac = df[["nb_cla_pp_bg", "nb_cla_pp_bt", "nb_cla_pp_bp"]].sum(axis=1, min_count=1)
    cla_brs = df[["nb_cla_pp_bg_brs", "nb_cla_pp_bt_brs", "nb_cla_pp_bp_brs"]].sum(axis=1, min_count=1)
    prop_neobac = df[["prop_tot_bg", "prop_tot_bt", "prop_tot_bp"]].sum(axis=1, min_count=1)
    prop_brs = df[["prop_tot_bg_brs", "prop_tot_bt_brs", "prop_tot_bp_brs"]].sum(axis=1, min_count=1)
    rang_max = df[["ran_grp1", "ran_grp2", "ran_grp3"]].max(axis=1)

    commune = df["liste_commune"] == True  # noqa: E712 (NaN -> False)
    rang_incoherent = (rang_max > df["nb_cla_pp"]) & ~commune
    new = {
        "ind_tension_voeux_par_place": ratio(df["nb_voe_pp"], df["capa_fin"]),
        # Part des classés effectivement appelés (≈ 1 : quasi tout le monde est appelé ; ≪ 1 : très sélectif).
        # Non interprétable pour les listes communes (rang partagé entre formations) ni quand le rang
        # dépasse le nombre de classés sur une liste propre (incohérence source) -> NaN.
        "ind_part_classes_appeles": ratio(rang_max, df["nb_cla_pp"]).where(~commune & df["liste_commune"].notna() & ~rang_incoherent),
        "ind_taux_remplissage": ratio(df["acc_tot"], df["capa_fin"]),
        "ind_places_vacantes": (df["capa_fin"] - df["acc_tot"]).clip(lower=0),
        # acc_tot ≥ acc_pp + acc_pc toujours : l'écart = admissions hors phases principale/complémentaire
        "ind_admis_hors_pp_pc": df["acc_tot"] - df["acc_pp"].fillna(0) - df["acc_pc"].fillna(0),
        # Part de boursiers parmi les néo-bacheliers, à chaque étape de la procédure
        "ind_pct_brs_voeux": ratio(voe_brs, voe_neobac),
        "ind_pct_brs_classes": ratio(cla_brs, cla_neobac),
        "ind_pct_brs_propositions": ratio(prop_brs, prop_neobac),
        "ind_pct_brs_admis": ratio(df["acc_brs"], df["acc_neobac"]),
        "flag_admis_sup_capacite": df["acc_tot"] > df["capa_fin"],
        "flag_capacite_nulle": df["capa_fin"].fillna(0) <= 0,
        # CNED : capacités nominales (jusqu'à 3 400 places, remplies à ~10 %) -> à exclure des analyses de tension
        "flag_cned": df["g_ea_lib_vx"].fillna("").str.strip().str.upper().eq("CNED"),
        # Rang > classés attendu pour les listes communes ; ailleurs c'est une anomalie
        "flag_rang_incoherent": rang_incoherent,
        "flag_formation_presente_6_ans": df.groupby("cod_aff_form")["session"].transform("nunique") == len(YEARS),
    }
    return pd.concat([df, pd.DataFrame(new, index=df.index)], axis=1)


def quality_report(df: pd.DataFrame) -> str:
    L = ["# Table Parcoursup harmonisée 2020-2025 — contrôle qualité", ""]
    L.append(f"- Lignes : **{len(df):,}** ; formations distinctes : **{df['cod_aff_form'].nunique():,}**")
    dup = df.duplicated(["cod_aff_form", "session"]).sum()
    L.append(f"- Doublons (formation, session) : **{dup}**")
    L.append(f"- Formations présentes les 6 années : **{df.loc[df.flag_formation_presente_6_ans, 'cod_aff_form'].nunique():,}**")
    L += ["", "## Par session", "", "| Session | Formations | Places | Admis | Places vacantes | % formations admis > places | % rang incohérent |", "|---|---|---|---|---|---|---|"]
    for s, g in df.groupby("session"):
        L.append(f"| {s} | {len(g):,} | {g.capa_fin.sum():,.0f} | {g.acc_tot.sum():,.0f} | {g.ind_places_vacantes.sum():,.0f} "
                 f"| {g.flag_admis_sup_capacite.mean():.1%} | {g.flag_rang_incoherent.mean():.1%} |")
    L += ["", "## Corrections appliquées", "",
          "- `list_com` inversé dans les sources 2024-2025 → variable corrigée `liste_commune` (booléen).",
          f"- `list_com` absent en 2020 → imputé depuis 2021 pour {int(df.liste_commune_imputee_2021.sum()):,} formations "
          f"(sur {(df.session == 2020).sum():,}).",
          "- `fili_harmo` : DUT (2020) → BUT.",
          "- `academie` : « Besançon » (2022) → « Besancon » ; `idf` = Paris, Créteil, Versailles.",
          f"- `ind_admis_hors_pp_pc` : admis hors phases PP/PC, non nul pour {(df.ind_admis_hors_pp_pc != 0).mean():.1%} "
          f"des lignes, jamais négatif ({(df.ind_admis_hors_pp_pc < 0).sum()} cas) — `acc_tot` reste la référence.",
          f"- `flag_cned` : {int(df.flag_cned.sum())} lignes CNED (capacités nominales), "
          f"{df.loc[df.flag_cned & (df.session == 2025), 'ind_places_vacantes'].sum():,.0f} places vacantes en 2025 — à exclure des analyses de tension.",
          "- IFSI 2024 (518 formations au lieu de ~340) : 9 diplômes paramédicaux classés « IFSI » cette année-là seulement "
          "(« Autre formation » les autres années) -> réalignés dans `fili_harmo`.",
          "- `capa_fin` : définition officielle « Capacité de l'établissement par formation », sans autre précision (méthodologie 2024 et 2025).",
          "- `nb_voe_pp` / `voe_tot` : la méthodologie précise qu'il s'agit d'effectifs de CANDIDATS par formation (un candidat compte dans chaque formation demandée)."]
    L += ["", "## Stabilité des modalités de `fili` (nb de formations)", "", df.pivot_table(index="fili", columns="session", values="cod_aff_form", aggfunc="count").fillna(0).astype(int).to_markdown()]
    L += ["", "## Indicateurs dérivés — session 2025", "", df[df.session == 2025].filter(like="ind_").describe().T.round(3).to_markdown()]
    return "\n".join(L)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = derive(load())
    to_csv_gz(df, OUT / "parcoursup_panel_2020_2025.csv.gz", sep=";", index=False)  # octets identiques à chaque exécution
    (REP / "parcoursup_panel_qualite.md").write_text(quality_report(df), encoding="utf-8")
    print(f"{len(df):,} lignes -> {OUT / 'parcoursup_panel_2020_2025.csv.gz'}")


if __name__ == "__main__":
    main()
