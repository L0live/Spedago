"""Spédago — porte « lycéens » : Mes spécialités → mes formations.

Usage : python3 scripts/build_mes_specialites.py
Entrées : data/raw/parcoursup_specialites_v3.csv (2025, formations fines), parcoursup_specialites_v2.csv (2021-2024),
          data/processed/mutualisation.json (offre de spécialités par lycée, voisins)
Sorties : data/processed/mes_specialites.json, app/mes-specialites.html, reports/mes_specialites.md

Pour une doublette de spécialités de terminale : quelles formations demandent les bacheliers qui l'ont suivie,
et quelle part de ceux qui ont demandé une formation y ont reçu une proposition, comparée à l'ensemble des
bacheliers généraux. Niveau national seulement (aucune donnée par lycée ou par formation précise d'établissement).
« Vœux » = candidats ayant confirmé au moins un vœu dans la formation (ce sont des personnes, pas des vœux).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.libelles import EDS  # noqa: E402
from spedago.pages import build_page  # noqa: E402
from spedago.paths import APP, PROCESSED, RAW, REPORTS  # noqa: E402

OUT_JSON = PROCESSED / "mes_specialites.json"
TPL = APP / "mes_specialites_template.html"
OUT_PAGE = APP / "mes-specialites.html"
OUT_MD = REPORTS / "mes_specialites.md"
NOMS_PS = {ps: i for i, (_, _, ps, _) in enumerate(EDS)}
V2_VERS_V3 = {"Licence Sciences de l éducation": "Licence Sciences de l'éducation"}


def nettoie(s: str) -> str:
    return " ".join(str(s).replace("\xa0", " ").split())


def doublette(s: str) -> tuple[int, int]:
    """« A,B » où A et B peuvent contenir des virgules : on cherche le découpage en deux noms connus."""
    s = str(s)
    for i in range(len(s)):
        if s[i] == "," and s[:i] in NOMS_PS and s[i + 1:] in NOMS_PS:
            a, b = NOMS_PS[s[:i]], NOMS_PS[s[i + 1:]]
            return (min(a, b), max(a, b))
    raise KeyError(f"doublette inconnue : {s!r}")


def famille(g: str) -> str:
    g = nettoie(g)
    if g.startswith("Licence professionnelle"):
        return "Licences professionnelles"
    if g in ("PASS", "Licence L.AS", "D.E sanitaire"):
        return "Santé"
    if g.startswith("Licence"):
        return "Licences"
    if g.startswith("BUT"):
        return "BUT"
    if g.startswith("BTS"):
        return "BTS"
    if g.startswith(("CPGE", "CUPGE", "CPES", "Classe préparatoire")):
        return "Classes préparatoires"
    if g in ("Ecoles d'ingénieurs", "Ecoles de Commerce", "Sciences po", "Formations des écoles nationales vétérinaires"):
        return "Écoles"
    if g == "D.E social":
        return "Travail social"
    if g == "Formations d'ART":
        return "Art et design"
    return "Autres formations"


LIBELLES = {"Psychlogie": "Psychologie", "l univers": "l'univers", "l ingénieur": "l'ingénieur", "l information": "l'information",
            "D.E social": "Diplômes d'État du social", "D.E sanitaire": "Diplômes d'État sanitaires (IFSI, etc.)",
            "Ecoles de Commerce": "Écoles de commerce", "Ecoles d'ingénieurs": "Écoles d'ingénieurs", "Formations d'ART": "Formations d'art (DN MADE, etc.)"}


def libelle(g: str) -> str:
    g = nettoie(g)
    for a, b in LIBELLES.items():
        g = g.replace(a, b)
    return g


def charge() -> tuple[pd.DataFrame, pd.DataFrame]:
    v3 = pd.read_csv(RAW / "parcoursup_specialites_v3.csv", sep=";")
    v2 = pd.read_csv(RAW / "parcoursup_specialites_v2.csv", sep=";")
    for d in (v3, v2):
        d["d"] = d.doublette.map(doublette)
    v3["groupe"] = v3.regroupement_de_formations.map(nettoie)
    v3["formation"] = v3.formation.map(nettoie)
    v2["groupe"] = v2.formation.map(nettoie).replace(V2_VERS_V3)
    return v3, v2


def build() -> dict:
    v3, v2 = charge()
    doubs = sorted(set(v3.d) | set(v2.d))
    di = {d: i for i, d in enumerate(doubs)}
    l0, l1, l2 = (v3[v3.niveau_d_agregation == k] for k in (0, 1, 2))
    groupes = sorted(set(l1.groupe), key=lambda g: (famille(g), libelle(g)))
    gi = {g: i for i, g in enumerate(groupes)}
    fines = sorted(set(zip(l2.groupe, l2.formation)), key=lambda t: (gi[t[0]], t[1]))
    fi = {t: i for i, t in enumerate(fines)}
    # tendance 2021-2024 (+2025) au niveau du regroupement, quand le libellé existe les deux années
    v2 = v2[v2.groupe.isin(gi) | (v2.groupe == "Ensemble des bacheliers")]
    tend = {}
    for r in v2.itertuples():
        if r.groupe in gi:
            tend.setdefault(f"{di[r.d]}|{gi[r.groupe]}", []).append([int(r.annee_du_bac), int(r.voeux), int(r.propositions_d_admissions)])
    for r in l1.itertuples():
        k = f"{di[r.d]}|{gi[r.groupe]}"
        if k in tend:
            tend[k].append([int(r.annee_du_bac), int(r.voeux), int(r.propositions_d_admissions)])
    for v in tend.values():
        v.sort()
    tot_v2 = v2[v2.groupe == "Ensemble des bacheliers"].groupby("annee_du_bac")[["voeux"]].sum()["voeux"].astype(int).to_dict()
    # offre de spécialités par lycée (carte) : on garde le strict nécessaire
    M = json.loads((PROCESSED / "mutualisation.json").read_text(encoding="utf-8"))
    lyc = [[l[0], l[1], l[2], l[4], l[9], {k: v for k, v in l[10].items()}] for l in M["lycees"]]
    return {
        "annee": int(l0.annee_du_bac.iloc[0]), "rayon_km": M["rayon_km"], "rentree_carte": M["rentree"],
        "eds": [[i, lib, keys] for i, lib, _, keys in EDS], "carte_specialites": M["specialites"],
        "doublettes": [list(d) for d in doubs],
        "n": [[di[r.d], int(r.voeux), int(r.propositions_d_admissions)] for r in l0.itertuples()],
        "groupes": [[g, libelle(g), famille(g)] for g in groupes],
        "g": [[di[r.d], gi[r.groupe], int(r.voeux), int(r.propositions_d_admissions), int(r.acceptations)] for r in l1.itertuples()],
        "formations": [[gi[g], f] for g, f in fines],
        "f": [[di[r.d], fi[(r.groupe, r.formation)], int(r.voeux), int(r.propositions_d_admissions), int(r.acceptations)] for r in l2.itertuples()],
        "tendance": tend, "total_annees": {str(k): v for k, v in tot_v2.items()} | {str(int(l0.annee_du_bac.iloc[0])): int(l0.voeux.sum())},
        "lycees": lyc,
    }


def report(D: dict) -> str:
    n = pd.DataFrame(D["n"], columns=["d", "candidats", "prop"]).sort_values("candidats", ascending=False)
    lib = lambda d: " + ".join(D["eds"][i][1] for i in D["doublettes"][d])  # noqa: E731
    L = ["# Mes spécialités → mes formations (Parcoursup)", "",
         f"{len(D['doublettes'])} doublettes, {len(D['groupes'])} regroupements de formations, {len(D['formations'])} formations fines ; "
         f"{int(n.candidats.sum()):,} bacheliers généraux en {D['annee']}.", "", "## Doublettes les plus suivies", "",
         "| Doublette | Candidats | Au moins une proposition |", "|---|---:|---:|"]
    for r in n.head(10).itertuples():
        L.append(f"| {lib(r.d)} | {r.candidats:,} | {r.prop / r.candidats:.1%} |")
    return "\n".join(L) + "\n"


def main() -> None:
    D = build()
    OUT_JSON.write_text(json.dumps(D, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    OUT_MD.write_text(report(D), encoding="utf-8")
    if TPL.exists():
        build_page(TPL, OUT_PAGE, D, {"__ANNEE__": str(D["annee"]), "__RENTREE__": str(D["rentree_carte"])})
    print(f"{len(D['doublettes'])} doublettes, {len(D['groupes'])} regroupements -> {OUT_JSON} ({OUT_JSON.stat().st_size / 1e6:.2f} Mo)")


if __name__ == "__main__":
    main()
