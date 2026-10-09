"""Spédago — piste A : simulation de l'article 2 de la PPL Sénat n° 447 (mars 2026).

Texte : insérer « du taux de pression constaté l'année précédente sur chaque formation » parmi
les critères pris en compte pour modifier les capacités d'accueil (art. L. 612-3 code éducation).
Le texte ne définit ni le taux de pression ni une formule : on simule donc des RÈGLES EXPLICITES,
paramétrables, qui sont autant d'interprétations possibles.

Usage : python3 scripts/simulate_ppl_art2.py
Entrée  : data/processed/parcoursup_panel_2020_2025.csv.gz
Sortie  : reports/simulation_ppl_art2.md

Définitions (année t-1, formation f) :
  pression      = vœux PP / places
  saturée       = admis / places ≥ 0.95
  non_appeles   = classés PP − rang du dernier appelé (listes propres uniquement) : candidats
                  classés jamais appelés = borne HAUTE de la demande non satisfaite de f
                  (ces candidats ont pu être admis ailleurs).
  éligible      = pression ≥ quantile Q de sa filière ET saturée
                  ET (liste commune OU non_appeles > 0)

Scénarios appliqués à l'année t à partir de t-1 :
  S1(α)  : +α % de places dans chaque formation éligible (budget additionnel).
  S2(β)  : + min(non_appeles, β % des places) — n'ajoute que ce que la demande classée peut remplir
           (listes propres seulement).
  S3(α)  : S1 financé à places constantes, par redéploiement des places vacantes des formations
           sous-remplies (< 80 %) de la même académie × filière.

Ce n'est PAS une prévision des admissions : sans données individuelles, on ne peut pas modéliser
les réallocations en chaîne des candidats.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "data" / "processed" / "parcoursup_panel_2020_2025.csv.gz"
OUT_MD = ROOT / "reports" / "simulation_ppl_art2.md"

Q_PRESSION = 0.75
SEUIL_SATURE = 0.95
SEUIL_SOUS_REMPLIE = 0.80
ALPHAS = (0.05, 0.10, 0.20)
BETA = 0.20
REF_CESPM_IDF = 7_300  # propositions manquantes en IdF à taux égal (8e rapport CESPM, session 2025)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    keep = df.capa_fin > 0
    if "flag_cned" in df:  # CNED : capacités nominales d'enseignement à distance
        keep &= ~df.flag_cned.astype(bool)
    df = df[keep].copy()
    df["pression"] = df.nb_voe_pp / df.capa_fin
    df["remplissage"] = df.acc_tot / df.capa_fin
    df["saturee"] = df.remplissage >= SEUIL_SATURE
    df["sous_remplie"] = df.remplissage < SEUIL_SOUS_REMPLIE
    commune = df.liste_commune == True  # noqa: E712
    rang_max = df[["ran_grp1", "ran_grp2", "ran_grp3"]].max(axis=1)
    df["non_appeles"] = (df.nb_cla_pp - rang_max).clip(lower=0).where(~commune & df.liste_commune.notna())
    df["seuil_pression"] = df.groupby(["session", "fili_harmo"]).pression.transform(lambda s: s.quantile(Q_PRESSION))
    df["eligible"] = (df.pression >= df.seuil_pression) & df.saturee & (commune | (df.non_appeles > 0))
    return df


def scenario_s1(prev: pd.DataFrame, alpha: float) -> pd.Series:
    # arrondi à 1e-9 avant le plafond : 100 × 0,07 vaut 7,000000000000001 en flottant -> 8 places au lieu de 7
    return np.ceil(np.round(prev.capa_fin * alpha, 9)).where(prev.eligible, 0)


def scenario_s2(prev: pd.DataFrame, beta: float) -> pd.Series:
    add = np.minimum(prev.non_appeles, np.ceil(np.round(prev.capa_fin * beta, 9)))
    return add.where(prev.eligible & prev.non_appeles.notna(), 0)


PERIMETRE_GISEMENT = {"Public", "Privé sous contrat d'association"}
CELLULE_S3 = ["academie", "fili_harmo", "fil_lib_voe_acc", "idf"]


def scenario_s3(prev: pd.DataFrame, alpha: float) -> pd.DataFrame:
    """Besoin S1 couvert par redéploiement dans la même cellule académie × filière × SPÉCIALITÉ
    (une place de BTS Comptabilité ne remplace pas une place de BTS Électrotechnique).
    Le gisement ne provient que du public et du privé sous contrat (places mobilisables par l'État).
    Retourne par cellule : besoin, gisement (vacantes des sous-remplies), couvert = min(besoin, gisement)."""
    mobilisable = prev.contrat_etab.isin(PERIMETRE_GISEMENT) if "contrat_etab" in prev else True
    p = prev.assign(besoin=scenario_s1(prev, alpha),
                    gisement=(prev.capa_fin - prev.acc_tot).clip(lower=0).where(prev.sous_remplie & mobilisable, 0))
    c = p.groupby(CELLULE_S3, as_index=False, dropna=False)[["besoin", "gisement"]].sum()
    c["couvert"] = np.minimum(c.besoin, c.gisement)
    return c


def backtest(df: pd.DataFrame) -> pd.DataFrame:
    """Une formation éligible en t-1 est-elle encore saturée, avec des classés non appelés, en t ?
    (= la règle « pression de l'année précédente » vise-t-elle les bonnes formations ?)"""
    rows = []
    for t in sorted(df.session.unique())[1:]:
        prev = df[df.session == t - 1].set_index("cod_aff_form")
        cur = df[df.session == t].set_index("cod_aff_form")
        j = prev[["eligible"]].join(cur[["saturee", "non_appeles", "eligible"]], rsuffix="_t", how="inner")
        e = j[j.eligible]
        rows.append({"session_t": t, "eligibles_t-1_suivies": len(e),
                     "encore_saturees_t": e.saturee.mean(),
                     "encore_non_appeles_t": (e.non_appeles > 0).mean() if e.non_appeles.notna().any() else np.nan,
                     "encore_eligibles_t": e.eligible_t.mean(),
                     "base_saturees_non_eligibles": j.loc[~j.eligible, "saturee"].mean()})
    return pd.DataFrame(rows)


def simulate(df: pd.DataFrame, t: int) -> dict:
    prev = df[df.session == t - 1]
    res = {"t": t, "eligibles": int(prev.eligible.sum()), "places_t-1": prev.capa_fin.sum(),
           "places_eligibles": prev.capa_fin.where(prev.eligible, 0).sum()}
    for a in ALPHAS:
        add = scenario_s1(prev, a)
        res[f"S1_{a:.0%}"] = add.sum()
        res[f"S1_{a:.0%}_idf"] = add[prev.idf].sum()
    add2 = scenario_s2(prev, BETA)
    res["S2"] = add2.sum()
    res["S2_idf"] = add2[prev.idf].sum()
    s3 = scenario_s3(prev, 0.10)
    res["S3_besoin"], res["S3_couvert"] = s3.besoin.sum(), s3.couvert.sum()
    res["S3_couvert_idf"] = s3.loc[s3.idf, "couvert"].sum()
    res["S3_besoin_idf"] = s3.loc[s3.idf, "besoin"].sum()
    res["par_filiere"] = (prev.assign(S1=scenario_s1(prev, 0.10), S2=add2)
                          .groupby("fili_harmo")[["S1", "S2"]].sum().sort_values("S1", ascending=False))
    return res


def sensitivity(raw: pd.DataFrame, t: int = 2025) -> pd.DataFrame:
    """Robustesse aux deux seuils arbitraires (quantile de pression, seuil de saturation)."""
    global Q_PRESSION, SEUIL_SATURE
    q0, s0 = Q_PRESSION, SEUIL_SATURE
    rows = []
    try:
        for q in (0.50, 0.75, 0.90):
            for sat in (0.90, 0.95, 1.00):
                Q_PRESSION, SEUIL_SATURE = q, sat
                d = prepare(raw)
                r, b = simulate(d, t), backtest(d)
                rows.append({"quantile_pression": q, "seuil_saturation": sat, "eligibles": r["eligibles"],
                             "S1_10%": r["S1_10%"], "S1_10%_idf": r["S1_10%_idf"], "S2": r["S2"],
                             "S3_part_couverte": r["S3_couvert"] / max(r["S3_besoin"], 1),
                             "retrotest_encore_saturees": b.iloc[-1].encore_saturees_t})
    finally:
        Q_PRESSION, SEUIL_SATURE = q0, s0
    return pd.DataFrame(rows)


def main() -> None:
    raw = pd.read_csv(PANEL, sep=";", low_memory=False)
    sens = sensitivity(raw)
    df = prepare(raw)
    r = simulate(df, 2025)
    bt = backtest(df)

    L = ["# Simulation — article 2 de la PPL Sénat n° 447 (pression de l'année précédente)", "",
         "**Statut : exercice de simulation à règles explicites, pas une prévision.** Le texte de loi ne fixe aucune formule.", "",
         f"Paramètres : pression ≥ quantile {Q_PRESSION:.0%} de la filière, saturation ≥ {SEUIL_SATURE:.0%}, "
         f"redéploiement depuis les formations < {SEUIL_SOUS_REMPLIE:.0%} de remplissage, plafond S2 = {BETA:.0%}.", "",
         "## 1. Session 2025 simulée à partir de 2024", "",
         f"- Formations éligibles en 2024 : **{r['eligibles']:,}** ({r['places_eligibles']:,.0f} places sur {r['places_t-1']:,.0f})", "",
         "| Scénario | Places ajoutées | dont Île-de-France | % des places totales |", "|---|---|---|---|"]
    for a in ALPHAS:
        k = f"S1_{a:.0%}"
        L.append(f"| S1 : +{a:.0%} dans les formations éligibles | {r[k]:,.0f} | {r[k + '_idf']:,.0f} | {r[k] / r['places_t-1']:.2%} |")
    L.append(f"| S2 : classés non appelés, plafond +{BETA:.0%} | {r['S2']:,.0f} | {r['S2_idf']:,.0f} | {r['S2'] / r['places_t-1']:.2%} |")
    L += ["", f"Référence : le CESPM estime à environ **{REF_CESPM_IDF:,}** les propositions manquantes en Île-de-France en 2025 "
          "(à taux égal avec le reste du pays). Ordre de grandeur seulement : les deux chiffres ne mesurent pas la même chose.", "",
          "## 2. S3 — financer S1 (+10 %) à places constantes par redéploiement", "",
          "Redéploiement limité à la même académie × filière × spécialité (`fil_lib_voe_acc`), "
          "depuis les seules formations publiques ou privées sous contrat.", "",
          f"- Besoin national : {r['S3_besoin']:,.0f} places ; couvrable par redéploiement dans la même cellule : "
          f"**{r['S3_couvert']:,.0f}** ({r['S3_couvert'] / max(r['S3_besoin'], 1):.0%})",
          f"- Île-de-France : besoin {r['S3_besoin_idf']:,.0f}, couvrable {r['S3_couvert_idf']:,.0f} "
          f"({r['S3_couvert_idf'] / max(r['S3_besoin_idf'], 1):.0%})",
          "- Hypothèse encore forte : une place vacante d'un établissement devient une place dans un autre établissement de "
          "la même académie et de la même spécialité (locaux et enseignants ne se déplacent pas librement).", "",
          "## 3. Places ajoutées par filière (2025, S1 +10 % et S2)", "", r["par_filiere"].astype(int).reset_index().to_markdown(index=False), "",
          "## 4. Rétro-test : la pression de l'année précédente vise-t-elle les bonnes formations ?", "",
          bt.round(3).to_markdown(index=False), "",
          "Lecture : part des formations éligibles en t-1 qui sont encore saturées (resp. avec des classés non appelés) en t, "
          "comparée au taux de saturation des formations non éligibles.", "",
          "## 5. Sensibilité aux seuils (session 2025)", "",
          sens.assign(S3_part_couverte=lambda x: (x.S3_part_couverte * 100).round(0),
                      retrotest_encore_saturees=lambda x: (x.retrotest_encore_saturees * 100).round(0)).to_markdown(index=False), "",
          "Lecture : le VOLUME de places dépend fortement des seuils (facteur ~10) — il ne faut donc pas en citer un seul chiffre. "
          "La part couvrable par redéploiement et la persistance de la saturation sont, elles, robustes.", "",
          "## Limites", "",
          "- Aucune modélisation du comportement des candidats ni des réallocations en chaîne (il faudrait les vœux individuels, accessibles via le CASD).",
          "- `non_appeles` est une borne haute de la demande non satisfaite : un candidat non appelé ici peut être admis ailleurs.",
          "- Les listes d'appel communes ne permettent pas de calculer `non_appeles` : S2 les ignore.",
          "- Le coût (enseignants, locaux) n'est pas chiffré."]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"-> {OUT_MD}")


if __name__ == "__main__":
    main()
