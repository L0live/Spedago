"""Spédago — page « France et voisins » : étudiants français à l'étranger, et régions de part et d'autre des frontières.

Usage : python3 scripts/download_eurostat.py && python3 scripts/build_voisins.py
Entrées : data/raw/eurostat_*.json (JSON-stat, API Eurostat)
Sorties : data/processed/voisins.json, web/public/data/voisins.json, reports/voisins.md

Choix :
- Mobilité : étudiants en mobilité DIPLÔMANTE (inscrits pour un diplôme entier, pas Erasmus), CITE 5 à 8, comptés par le
  pays d'accueil (educ_uoe_mobs02). Les drapeaux Eurostat (rupture de série, définition différente) sont gardés et affichés.
- Régions : académie -> région NUTS 2 qui la contient (anciennes régions, découpage proche des académies) ; voisines =
  régions frontalières (terrestres, et la Sardaigne pour la Corse). Indicateurs de l'enquête Forces de travail, petits
  échantillons régionaux : moyenne des 3 dernières années disponibles, drapeau « peu fiable » repris s'il touche une année.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.jsonstat import DRAPEAUX, lire  # noqa: E402
from spedago.pages import export_web  # noqa: E402
from spedago.paths import PROCESSED, RAW, REPORTS  # noqa: E402
from spedago.referentiel import ACADEMIES, cle, slug  # noqa: E402

OUT_JSON = PROCESSED / "voisins.json"
OUT_MD = REPORTS / "voisins.md"

PAYS = ["BE", "CH", "ES", "DE", "IT", "PT", "LU"]  # Pays-Bas : pas de valeur publiée
NOMS_PAYS = {"BE": "Belgique", "CH": "Suisse", "ES": "Espagne", "DE": "Allemagne", "IT": "Italie", "PT": "Portugal", "LU": "Luxembourg",
             "NL": "Pays-Bas", "FR": "France", "EU27_2020": "Union européenne (27)"}
NUTS = {"Paris": ["FR10"], "Créteil": ["FR10"], "Versailles": ["FR10"], "Orléans-Tours": ["FRB0"], "Dijon": ["FRC1"], "Besançon": ["FRC2"],
        "Normandie": ["FRD1", "FRD2"], "Lille": ["FRE1"], "Amiens": ["FRE2"], "Strasbourg": ["FRF1"], "Reims": ["FRF2"], "Nancy-Metz": ["FRF3"],
        "Nantes": ["FRG0"], "Rennes": ["FRH0"], "Bordeaux": ["FRI1"], "Limoges": ["FRI2"], "Poitiers": ["FRI3"], "Montpellier": ["FRJ1"],
        "Toulouse": ["FRJ2"], "Clermont-Ferrand": ["FRK1"], "Lyon": ["FRK2"], "Grenoble": ["FRK2"], "Aix-Marseille": ["FRL0"], "Nice": ["FRL0"],
        "Corse": ["FRM0"], "Guadeloupe": ["FRY1"], "Martinique": ["FRY2"], "Guyane": ["FRY3"], "La Réunion": ["FRY4"], "Mayotte": ["FRY5"]}
VOISINES = {"Lille": ["BE25", "BE32"], "Amiens": ["BE32", "BE35"], "Reims": ["BE34", "BE35"],
            "Nancy-Metz": ["BE34", "LU00", "DEC0", "DEB3"], "Strasbourg": ["DEB3", "DE12", "DE13", "CH03"],
            "Besançon": ["CH01", "CH02", "CH03"], "Lyon": ["CH01"], "Grenoble": ["CH01", "ITC2", "ITC1"], "Aix-Marseille": ["ITC1"],
            "Nice": ["ITC1", "ITC3"], "Toulouse": ["ES24", "ES51"], "Montpellier": ["ES51"], "Bordeaux": ["ES21", "ES22"], "Corse": ["ITG2"]}
INDICATEURS = [("diplomes_sup_25_34", "Diplômés du supérieur parmi les 25-34 ans", "haut"),
               ("sorties_precoces_18_24", "Sorties précoces du système éducatif (18-24 ans)", "bas"),
               ("neet_15_29", "Jeunes ni en emploi, ni en études, ni en formation (15-29 ans)", "bas")]
REFS = ["FR", "BE", "DE", "CH", "IT", "ES", "LU", "EU27_2020"]


def mobilite() -> dict:
    out_ = lire(RAW / "eurostat_mobilite_francais_etranger.json")
    in_ = lire(RAW / "eurostat_mobilite_etrangers_france.json")
    annees = sorted(out_.time.unique())
    def serie(df, col, code):
        x = df[(df[col] == code) & (df.isced11 == "ED5-8")].set_index("time")
        return [[None if pd.isna(x.valeur.get(a)) else int(x.valeur[a]), x.statut.get(a, "")] if a in x.index else [None, ""] for a in annees]
    niveaux = {}
    der = annees[-1]
    for c in PAYS:
        x = out_[(out_.geo == c) & (out_.time == der)].set_index("isced11").valeur
        niveaux[c] = [None if pd.isna(x.get(k)) else int(x[k]) for k in ("ED5", "ED6", "ED7", "ED8")]
    ue = out_[(out_.geo == "EU27_2020") & (out_.isced11 == "ED5-8")].set_index("time").valeur
    return {"annees": annees, "pays": [[c, NOMS_PAYS[c]] for c in PAYS],
            "sortants": {c: serie(out_, "geo", c) for c in PAYS}, "entrants": {c: serie(in_, "partner", c) for c in PAYS},
            "niveaux": niveaux, "ue": [[a, None if pd.isna(ue.get(a)) else int(ue[a])] for a in annees]}


def regions() -> tuple[dict, dict]:
    vals, libs = {}, {}
    for key, _, _ in INDICATEURS:
        d = lire(RAW / f"eurostat_{key}.json")
        d = d[d.valeur.notna()]
        for geo, g in d.groupby("geo"):
            g = g.sort_values("time").tail(3)
            vals.setdefault(geo, {})[key] = [round(float(g.valeur.mean()), 1), round(float(g.valeur.iloc[-1]), 1), g.time.iloc[0], g.time.iloc[-1],
                                             "u" if g.statut.str.contains("u").any() else ""]
            libs[geo] = g.geo_lib.iloc[0]
    return vals, libs


def build() -> dict:
    vals, libs = regions()
    codes = sorted({c for v in NUTS.values() for c in v} | {c for v in VOISINES.values() for c in v} | set(REFS))
    manquants = [c for c in codes if c not in vals]
    assert not manquants, f"régions absentes d'Eurostat : {manquants}"
    noms = sorted((set(NUTS)), key=cle)
    assert set(noms) <= set(ACADEMIES.values())
    return {"mobilite": mobilite(),
            "indicateurs": [[k, lib, sens] for k, lib, sens in INDICATEURS],
            "regions": {c: {"nom": NOMS_PAYS.get(c) or libs[c], "pays": c[:2] if c not in ("EU27_2020",) else "UE", "v": vals[c]} for c in codes},
            "academies": [[a, slug(a), NUTS[a], VOISINES.get(a, [])] for a in noms], "refs": REFS,
            "drapeaux": DRAPEAUX, "noms_pays": NOMS_PAYS}


def report(D: dict) -> str:
    m = D["mobilite"]; a = m["annees"]
    L = ["# France et voisins (Eurostat)", "", f"## Étudiants français en mobilité diplômante, par pays d'accueil ({a[0]}-{a[-1]})", "",
         "| Pays | " + " | ".join(a[-5:]) + " |", "|---|" + "---:|" * 5]
    for c, nom in m["pays"]:
        s = m["sortants"][c][-5:]
        L.append(f"| {nom} | " + " | ".join("–" if v is None else f"{v:,}{' (' + f + ')' if f else ''}" for v, f in s) + " |")
    L += ["", "Drapeaux : " + ", ".join(f"{k} = {v}" for k, v in DRAPEAUX.items()), ""]
    return "\n".join(L)


def main() -> None:
    D = build()
    OUT_JSON.write_text(json.dumps(D, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    OUT_MD.write_text(report(D), encoding="utf-8")
    export_web("voisins", D)
    print(f"{len(D['regions'])} régions, {len(D['mobilite']['pays'])} pays -> {OUT_JSON}")


if __name__ == "__main__":
    main()
