"""Spédago — niveau 2 : référentiel commun des académies et des établissements (UAI).

Usage : python3 scripts/build_referentiel.py
Sorties : data/processed/academies.csv        (source, graphie d'origine -> académie canonique)
          data/processed/referentiel_uai.csv  (un établissement par ligne, présence dans chaque source)
          reports/referentiel.md

Relie les trois pistes : un lycée de la carte (B) peut porter des BTS et des prépas (A) ;
une université porte des licences (A) et des masters (C). L'UAI est la clé commune ; l'académie
canonique, la clé territoriale.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.paths import PROCESSED, RAW, REPORTS  # noqa: E402
from spedago.referentiel import academie_canonique  # noqa: E402

SESSION = 2025
OUT_ACAD = PROCESSED / "academies.csv"
OUT_UAI = PROCESSED / "referentiel_uai.csv"
OUT_MD = REPORTS / "referentiel.md"


def sources() -> dict[str, pd.DataFrame]:
    p = pd.read_csv(PROCESSED / "parcoursup_panel_2020_2025.csv.gz", sep=";", low_memory=False)
    p = p[p.session == SESSION]
    m = pd.read_csv(RAW / "monmaster_2024_2025.csv", sep=";", low_memory=False)
    m = m[m.session == SESSION]
    a = pd.read_csv(RAW / "annuaire_lycees.csv", sep=";", dtype=str)
    t = pd.read_csv(RAW / "specialites_triplettes_1ere.csv", sep=";", low_memory=False)
    t = t[t.rentree_scolaire == t.rentree_scolaire.max()]
    ips = pd.read_csv(RAW / "ips_lycees_ap2023.csv", sep=";", low_memory=False)
    return {"parcoursup": p, "monmaster": m, "annuaire": a, "triplettes": t, "ips": ips}


def academies(src: dict[str, pd.DataFrame]) -> pd.DataFrame:
    cols = {"parcoursup": ["academie"], "monmaster": ["acad_lib", "lieu_acad_lib"], "annuaire": ["libelle_academie"],
            "triplettes": ["academie"], "ips": ["academie"]}
    rows = [{"source": f"{s}.{c}", "graphie": g, "academie": academie_canonique(g)}
            for s, cs in cols.items() for c in cs for g in sorted(src[s][c].dropna().astype(str).unique())]
    return pd.DataFrame(rows)


def referentiel(src: dict[str, pd.DataFrame]) -> pd.DataFrame:
    a = src["annuaire"].rename(columns={"identifiant_de_l_etablissement": "uai"}).drop_duplicates("uai")
    base = pd.DataFrame({"uai": a.uai, "nom": a.nom_etablissement, "commune": a.nom_commune,
                         "statut": a.statut_public_prive, "academie": a.libelle_academie.map(academie_canonique),
                         "bassin": a.libelle_bassin_formation, "lat": pd.to_numeric(a.latitude),
                         "lon": pd.to_numeric(a.longitude), "dans_annuaire_lycees": True})
    p = src["parcoursup"]
    ps = p.groupby("cod_uai").agg(nom_ps=("g_ea_lib_vx", "first"), acad_ps=("academie", "first"),
                                  ps_formations=("cod_aff_form", "size"), ps_places=("capa_fin", "sum"),
                                  ps_bts=("fili_harmo", lambda s: int((s == "BTS").sum())),
                                  ps_cpge=("fili_harmo", lambda s: int((s == "CPGE").sum())),
                                  ps_licences=("fili_harmo", lambda s: int(s.isin(["Licence", "Licence_Las", "PASS"]).sum())))
    m = src["monmaster"]
    mm = m.groupby("eta_uai").agg(nom_mm=("eta_nom", "first"), acad_mm=("acad_lib", "first"),
                                  mm_formations=("ifc", "size"), mm_places=("col", "sum"))
    t = src["triplettes"]
    # quelques lycées de la carte des spécialités manquent à l'annuaire (pas de coordonnées) : on les garde quand même
    tri = pd.DataFrame({"nom_tri": t.denomination_principale.values, "acad_tri": t.academie.values},
                       index=t.numero_etablissement.values)
    r = (base.set_index("uai").join(ps, how="outer").join(mm, how="outer").join(tri, how="outer"))
    r.index.name = "uai"
    r["nom"] = r.nom.fillna(r.nom_ps).fillna(r.nom_mm).fillna(r.nom_tri)
    r["academie"] = r.academie.fillna(r.acad_ps.map(academie_canonique, na_action="ignore")) \
                              .fillna(r.acad_mm.map(academie_canonique, na_action="ignore")) \
                              .fillna(r.acad_tri.map(academie_canonique, na_action="ignore"))
    r["dans_annuaire_lycees"] = r.dans_annuaire_lycees.eq(True)
    r["lycee_1re_generale"] = r.index.isin(tri.index)
    for c in ("ps_formations", "ps_places", "ps_bts", "ps_cpge", "ps_licences", "mm_formations", "mm_places"):
        r[c] = r[c].fillna(0).astype(int)
    return r.drop(columns=["nom_ps", "nom_mm", "nom_tri", "acad_ps", "acad_mm", "acad_tri"]).reset_index()


def report(acad: pd.DataFrame, r: pd.DataFrame) -> str:
    n = len(r)
    L = ["# Référentiel commun (académies, établissements)", "",
         "## Académies", "",
         f"{acad.graphie.nunique()} graphies d'origine dans {acad.source.nunique()} colonnes sources → "
         f"**{acad.academie.nunique()} académies canoniques**. Aucune graphie inconnue (sinon le script s'arrête).", "",
         acad[acad.graphie != acad.academie].drop_duplicates(["graphie", "academie"]).sort_values("academie")
         .to_markdown(index=False), "",
         "## Établissements (UAI)", "",
         f"- {n:,} établissements au total.",
         f"- Lycées de l'annuaire : {int(r.dans_annuaire_lycees.sum()):,}, dont {int((r.lycee_1re_generale & r.dans_annuaire_lycees).sum()):,} avec une 1re générale (carte, piste B).",
         f"- Lycées avec une 1re générale absents de l'annuaire (pas de coordonnées, donc hors carte) : "
         f"{int((r.lycee_1re_generale & ~r.dans_annuaire_lycees).sum())}.",
         f"- Établissements Parcoursup {SESSION} : {int((r.ps_formations > 0).sum()):,} ; dont lycées de l'annuaire : "
         f"{int(((r.ps_formations > 0) & r.dans_annuaire_lycees).sum()):,} (BTS, prépas portés par un lycée).",
         f"- Lycées de la carte qui portent aussi des formations Parcoursup : {int(((r.ps_formations > 0) & r.lycee_1re_generale).sum()):,}.",
         f"- Établissements Mon Master {SESSION} : {int((r.mm_formations > 0).sum()):,} ; présents aussi dans Parcoursup : "
         f"{int(((r.mm_formations > 0) & (r.ps_formations > 0)).sum()):,}.",
         f"- Académie inconnue : {int(r.academie.isna().sum() + (r.academie == '').sum())} établissements."]
    return "\n".join(L)


def main() -> None:
    src = sources()
    acad = academies(src)
    r = referentiel(src)
    acad.to_csv(OUT_ACAD, sep=";", index=False)
    r.to_csv(OUT_UAI, sep=";", index=False)
    OUT_MD.write_text(report(acad, r), encoding="utf-8")
    print(f"{len(r):,} établissements, {acad.academie.nunique()} académies -> {OUT_UAI}")


if __name__ == "__main__":
    main()
