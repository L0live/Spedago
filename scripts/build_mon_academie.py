"""Spédago — niveau 3 : page « Mon académie » (porte d'entrée des décideurs).

Usage : python3 scripts/build_mon_academie.py
Entrées : panel Parcoursup, data/processed/mutualisation.json, monmaster_formations.csv, referentiel_uai.csv
Sorties : data/processed/mon_academie.json, web/public/data/mon_academie.json

Une fiche par académie qui réunit les trois pistes, avec les mêmes règles que les autres outils :
  - Parcoursup 2025 : tension par filière (définitions de analyse_tension.py) et règle de départ du simulateur
    (+10 % aux formations sous pression, redéploiement par spécialité : simulate_ppl_art2.py) ;
  - spécialités de 1re : catégories de la carte des mutualisations (build_mutualisation.py) ;
  - masters : effectifs Mon Master 2025 (build_monmaster.py).
Les nombres sont recalculés ici puis comparés, par les tests, à ceux des autres pages (même source, même résultat).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyse_tension as at  # noqa: E402
import simulate_ppl_art2 as sim  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.pages import export_web  # noqa: E402
from spedago.paths import PROCESSED, RAW  # noqa: E402
from spedago.libelles import FILIERES, SPECIALITES  # noqa: E402
from spedago.referentiel import IDF, OUTRE_MER, academie_canonique, cle, slug  # noqa: E402

SESSION = 2025
ALPHA = 0.10  # règle de départ du simulateur
PROFILS_PARTITION = ["lg3", "lp3", "but3", "master", "autre", "noninscri"]  # somme = tous les candidats
N_MENTIONS = 6
OUT_JSON = PROCESSED / "mon_academie.json"
PS_COLS = ["formations", "places", "admis", "voeux_pp", "places_saturees", "vacantes"]


def _ints(row, cols) -> list[int]:
    return [int(round(float(row[c]))) for c in cols]


def parcoursup(raw: pd.DataFrame) -> tuple[dict, dict, list[str]]:
    df = at.load_panel()
    d = df[df.session == SESSION].assign(academie=lambda x: x.academie.map(academie_canonique))
    filieres = sorted(d.fili_harmo.unique().tolist())
    fi = {f: i for i, f in enumerate(filieres)}
    par_fil = at.aggregate(d, ["academie", "fili_harmo"])
    tot = at.aggregate(d, ["academie"]).set_index("academie")
    nat_fil = at.aggregate(d, ["fili_harmo"])
    nat = at.aggregate(d.assign(tout=1), ["tout"]).iloc[0]

    prev = sim.prepare(raw)
    prev = prev[prev.session == SESSION].assign(academie=lambda x: x.academie.map(academie_canonique))
    add = sim.scenario_s1(prev, ALPHA)
    s3 = sim.scenario_s3(prev, ALPHA)
    ajout = add.groupby(prev.academie).sum()
    visees = (add > 0).groupby(prev.academie).sum()
    couvert = s3.groupby("academie").couvert.sum()

    out = {}
    for a, r in tot.iterrows():
        rows = par_fil[par_fil.academie == a].sort_values("places", ascending=False)
        out[a] = {"total": _ints(r, PS_COLS),
                  "filieres": [[fi[x.fili_harmo]] + _ints(x, PS_COLS) for _, x in rows.iterrows()],
                  "sim": [int(ajout.get(a, 0)), int(couvert.get(a, 0)), int(visees.get(a, 0))]}
    france = {"total": _ints(nat, PS_COLS),
              "filieres": [[fi[x.fili_harmo]] + _ints(x, PS_COLS) for _, x in nat_fil.sort_values("places", ascending=False).iterrows()],
              "sim": [int(add.sum()), int(s3.couvert.sum()), int((add > 0).sum())]}
    return out, france, filieres


def specialites(M: dict) -> tuple[dict, dict]:
    """Par académie et spécialité : [proposée, incertaine, accès voisin, ouverture commune, isolé,
    élèves accès voisin, élèves ouverture commune, élèves isolés, groupes d'ouverture commune]."""
    n_sp = len(M["specialites"])

    def vide() -> list[list[int]]:
        return [[0] * 9 for _ in range(n_sp)]
    out: dict[str, list] = {}
    france = vide()
    pos = {0: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    for l in M["lycees"]:
        a = l[4]
        t = out.setdefault(a, vide())
        for sp, c in enumerate(l[9]):
            for tab in (t, france):
                tab[sp][pos[c]] += 1
                if c in (3, 4, 5):
                    tab[sp][5 + c - 3] += l[8]
    for g in M["groupes"]:
        acads = {M["lycees"][m][4] for m in g[1]}
        for a in acads:
            out[a][g[0]][8] += 1
        france[g[0]][8] += 1
    lycees = {a: sum(1 for l in M["lycees"] if l[4] == a) for a in out}
    return ({a: {"lycees": lycees[a], "spe": v} for a, v in out.items()},
            {"lycees": len(M["lycees"]), "spe": france})


def masters(m: pd.DataFrame) -> tuple[dict, dict]:
    m = m[m.session == SESSION].assign(academie=lambda x: x.lieu_acad_lib.map(academie_canonique))
    part = m[m.profil.isin(PROFILS_PARTITION)]
    lg3 = m[m.profil == "lg3"]

    def bloc(sel_part: pd.DataFrame, sel_lg3: pd.DataFrame) -> dict:
        f = sel_lg3.drop_duplicates("ifc")
        return {"total": [int(f.ifc.nunique()), int(f.col.sum()), int(sel_part.candidats.sum()), int(sel_part.propositions.sum()),
                          int(sel_lg3.candidats.sum()), int(sel_lg3.propositions.sum())]}

    nat_mention = lg3.groupby("mention")[["candidats", "propositions"]].sum()
    out = {}
    for a, g in lg3.groupby("academie"):
        b = bloc(part[part.academie == a], g)
        mt = g.groupby("mention").agg(formations=("ifc", "nunique"), places=("col", "sum"),
                                      cand=("candidats", "sum"), prop=("propositions", "sum"))
        mt = mt.sort_values(["places", "formations"], ascending=False).head(N_MENTIONS)
        b["mentions"] = [[k, int(r.formations), int(r.places), int(r.cand), int(r.prop),
                          int(nat_mention.at[k, "candidats"]), int(nat_mention.at[k, "propositions"])] for k, r in mt.iterrows()]
        out[a] = b
    return out, bloc(part, lg3)


def referentiel(r: pd.DataFrame) -> tuple[dict, dict]:
    """[lycées (annuaire), dont 1re générale, établissements Parcoursup, lycées avec BTS, lycées avec CPGE, établissements Mon Master]"""
    def ligne(x: pd.DataFrame) -> list[int]:
        lyc = x.dans_annuaire_lycees
        return [int(lyc.sum()), int((lyc & x.lycee_1re_generale).sum()), int((x.ps_formations > 0).sum()),
                int((lyc & (x.ps_bts > 0)).sum()), int((lyc & (x.ps_cpge > 0)).sum()), int((x.mm_formations > 0).sum())]
    return {a: ligne(g) for a, g in r.groupby("academie")}, ligne(r)


VOIES = ["Bac général", "Bac technologique", "Bac professionnel"]
POURSUITE_COLS = {"univ": ["univ"], "iut": ["iut"], "cpge": ["cpge_prive", "cpge_public"], "sts": ["sts_nr", "sts_prive", "sts_public"],
                  "autre": ["autre_nr", "autre_prive", "autre_public"]}


def poursuite(p: pd.DataFrame) -> tuple[dict, list, int]:
    """Néo-bacheliers de la dernière session qui poursuivent dans le supérieur, par voie et filière (SIES).
    Les colonnes « _flux » et « _stable » s'additionnent (leur somme redonne le taux de poursuite publié) ;
    on ne commente pas leur partage, non documenté dans la fiche du jeu."""
    an = int(p.rentree_session.max())
    p = p[p.rentree_session == an].assign(academie=lambda x: x.aca_lib.map(academie_canonique))
    for k, cs in POURSUITE_COLS.items():
        p[k] = sum(p[f"{c}_flux"] + p[f"{c}_stable"] for c in cs)
    cols = ["bacheliers", *POURSUITE_COLS]
    ligne = lambda g: [[v, *[int(round(float(g.loc[g.voie_du_baccalaureat == v, c].sum()))) for c in cols]] for v in VOIES]  # noqa: E731
    return {a: ligne(g) for a, g in p.groupby("academie")}, ligne(p), an


def zone(a: str) -> str:
    return "Île-de-France" if a in IDF else "Outre-mer" if a in OUTRE_MER else "Métropole hors Île-de-France"


def build() -> dict:
    raw = pd.read_csv(sim.PANEL, sep=";", low_memory=False)
    ps, ps_fr, filieres = parcoursup(raw)
    M = json.loads((PROCESSED / "mutualisation.json").read_text(encoding="utf-8"))
    sp, sp_fr = specialites(M)
    mm, mm_fr = masters(pd.read_csv(PROCESSED / "monmaster_formations.csv", sep=";", low_memory=False))
    ref, ref_fr = referentiel(pd.read_csv(PROCESSED / "referentiel_uai.csv", sep=";", dtype={"uai": str}))
    po, po_fr, an_po = poursuite(pd.read_csv(RAW / "poursuite_academie.csv", sep=";"))
    noms = sorted((set(ps) | set(sp) | set(mm)) - {"Étranger"}, key=cle)
    assert all(academie_canonique(a) == a for a in noms)
    acads = [{"nom": a, "slug": slug(a), "zone": zone(a), "ref": ref.get(a), "ps": ps.get(a), "spe": sp.get(a), "mm": mm.get(a),
              "pours": po.get(a)} for a in noms]
    return {"session": SESSION, "rentree": M["rentree"], "alpha": ALPHA, "filieres": filieres, "specialites": M["specialites"],
            "libelles_filieres": FILIERES, "libelles_specialites": SPECIALITES, "rentree_poursuite": an_po,
            "france": {"nom": "France entière", "ref": ref_fr, "ps": ps_fr, "spe": sp_fr, "mm": mm_fr, "pours": po_fr},
            "academies": acads}


def main() -> None:
    D = build()
    OUT_JSON.write_text(json.dumps(D, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    export_web("mon_academie", D)
    print(f"{len(D['academies'])} académies -> web/public/data/mon_academie.json")


if __name__ == "__main__":
    main()
