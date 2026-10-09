"""Spédago — piste C : données du simulateur d'accès Mon Master + analyse des écarts entre profils.

Usage : python3 scripts/build_monmaster.py
Entrée  : data/raw/monmaster_2024_2025.csv (open data MESR, une ligne = formation × session)
Sorties : data/processed/monmaster_formations.csv   (formation × session × profil, long)
          data/processed/monmaster_simulateur.json  (données compactes pour la page interactive)
          reports/piste_C_monmaster.md

Vérifié sur les sources (tests) : pour chaque formation, la somme des 6 profils redonne exactement
candidats (PP et PC), classés, propositions et acceptations ; propositions ≤ candidats.

Définitions (par formation, session, profil) :
  candidats   = candidats confirmés phase principale + phase complémentaire
  taux_prop   = propositions / candidats  — taux HISTORIQUE, pas une probabilité individuelle :
                le dossier (notes, parcours, lettre) n'est pas observé.
  Profil « même établissement » : candidats inscrits dans l'établissement qui porte le master.
Intervalle de Wilson à 95 % ; taux non affiché si candidats < MIN_CANDIDATS.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "monmaster_2024_2025.csv"
OUT_CSV = ROOT / "data" / "processed" / "monmaster_formations.csv"
OUT_JSON = ROOT / "data" / "processed" / "monmaster_simulateur.json"
OUT_MD = ROOT / "reports" / "piste_C_monmaster.md"

PROFILS = {"lg3": "L3 générale", "lp3": "Licence pro", "but3": "BUT 3e année", "master": "Déjà en master",
           "autre": "Autre inscription", "noninscri": "Non inscrit en 2024-25 / reprise d'études"}
MIN_CANDIDATS = 10
Z = 1.96


def wilson(k: np.ndarray, n: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    k, n = np.asarray(k, float), np.asarray(n, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = k / n
        den = 1 + Z**2 / n
        c = (p + Z**2 / (2 * n)) / den
        h = Z * np.sqrt(p * (1 - p) / n + Z**2 / (4 * n**2)) / den
    return np.where(n > 0, c - h, np.nan), np.where(n > 0, c + h, np.nan)


def load(path: Path = RAW) -> pd.DataFrame:
    return pd.read_csv(path, sep=";", low_memory=False)


def to_long(m: pd.DataFrame) -> pd.DataFrame:
    base = ["session", "ifc", "eta_uai", "eta_nom", "lieu_acad_lib", "mention", "parcours", "alternance",
            "modalite_enseignement", "disci_lib", "secteur_disci_lib", "col", "rang_dernier_appele_pp", "rang_dernier_appele_pc"]
    rows = []
    for p in PROFILS:
        d = m[base].copy()
        d["profil"] = p
        d["candidats"] = m[f"n_can_{p}_pp"] + m[f"n_can_{p}_pc"]
        d["classes"] = m[f"n_clas_{p}_total"]
        d["propositions"] = m[f"n_prop_{p}_total"]
        d["acceptations"] = m[f"n_accept_{p}_total"]
        rows.append(d)
    d = m[base].copy()
    d["profil"] = "etab"
    d["candidats"] = m.n_can_etab_pp + m.n_can_etab_pc
    d["classes"], d["propositions"], d["acceptations"] = m.n_clas_etab, m.n_prop_etab, m.n_accept_etab
    rows.append(d)
    d = m[base].copy()
    d["profil"] = "hors_etab"
    d["candidats"] = (m.n_can_pp + m.n_can_pc) - (m.n_can_etab_pp + m.n_can_etab_pc)
    d["classes"] = m.n_clas_total - m.n_clas_etab
    d["propositions"] = m.n_prop_total - m.n_prop_etab
    d["acceptations"] = m.n_accept_total - m.n_accept_etab
    rows.append(d)
    out = pd.concat(rows, ignore_index=True)
    out["taux_prop"] = np.where(out.candidats > 0, out.propositions / out.candidats, np.nan)
    out["ic_bas"], out["ic_haut"] = wilson(out.propositions, out.candidats)
    return out


# ---------- analyse ----------

def within_gap(long: pd.DataFrame, a: str, b: str, min_n: int = MIN_CANDIDATS) -> dict:
    """Écart de taux de proposition a − b À L'INTÉRIEUR des mêmes formations (formations où les deux profils
    ont ≥ min_n candidats), pondéré par le nombre de candidats du profil b. Neutralise l'effet « formation »."""
    w = long.pivot_table(index=["session", "ifc"], columns="profil", values=["candidats", "propositions"], aggfunc="sum")
    na, nb = w["candidats"][a], w["candidats"][b]
    ok = (na >= min_n) & (nb >= min_n)
    ra, rb = w["propositions"][a][ok] / na[ok], w["propositions"][b][ok] / nb[ok]
    wt = nb[ok]
    gap = ((ra - rb) * wt).sum() / wt.sum()
    # intervalle par bootstrap sur les formations
    rng = np.random.default_rng(0)
    idx = np.arange(ok.sum())
    diffs, wts = (ra - rb).to_numpy(), wt.to_numpy()
    boots = [np.average(diffs[s], weights=wts[s]) for s in (rng.choice(idx, len(idx)) for _ in range(500))]
    return {"comparaison": f"{a} − {b}", "formations_x_sessions": int(ok.sum()), "taux_a": float((ra * wt).sum() / wt.sum()),
            "taux_b": float((rb * wt).sum() / wt.sum()), "ecart_points": gap * 100,
            "ic95_bas": np.percentile(boots, 2.5) * 100, "ic95_haut": np.percentile(boots, 97.5) * 100,
            "part_formations_a_superieur": float((ra > rb).mean())}


def report(m: pd.DataFrame, long: pd.DataFrame) -> str:
    L = ["# Piste C — Mon Master : accès selon le profil (sessions 2024 et 2025)", "",
         "Source : open data MESR (une ligne = formation × session). Taux = propositions / candidats (phases principale + complémentaire).", ""]
    tot = m.groupby("session").agg(formations=("ifc", "size"), places=("col", "sum"), candidatures=("n_can_pp", "sum"),
                                   propositions=("n_prop_total", "sum"), acceptations=("n_accept_total", "sum"))
    L += ["## 1. Vue d'ensemble", "", tot.reset_index().to_markdown(index=False), "",
          "« candidatures » = somme sur les formations des candidats en phase principale (un candidat compte dans chaque formation demandée).", ""]

    nat = long[long.profil.isin(PROFILS)].groupby(["session", "profil"])[["candidats", "propositions"]].sum()
    nat["taux_prop"] = nat.propositions / nat.candidats
    piv = nat.taux_prop.unstack("session").round(3).rename(index=PROFILS)
    L += ["## 2. Taux de proposition national par profil (toutes formations confondues)", "", piv.reset_index().to_markdown(index=False), "",
          "Attention : ces taux mélangent l'effet du profil et celui des formations demandées. La section 3 compare à formation identique.", ""]

    gaps = [within_gap(long, "etab", "hors_etab"), within_gap(long, "etab", "lg3")]
    gaps += [within_gap(long, p, "lg3") for p in ("but3", "lp3", "master", "noninscri")]
    g = pd.DataFrame(gaps)
    L += ["## 3. Écarts à formation identique", "",
          f"Formations où les deux profils ont au moins {MIN_CANDIDATS} candidats ; moyenne pondérée ; IC 95 % par bootstrap sur les formations.", "",
          g.round(3).to_markdown(index=False), "",
          "Biais de composition : les internes sont surtout des L3 générales, les externes comptent plus de LP, BUT et non-inscrits "
          "(taux plus faibles). Les données ne croisent pas établissement × profil. La ligne « etab − lg3 » compare les internes à TOUS "
          "les L3 générales (internes compris) : c'est une borne BASSE de la prime aux internes à profil comparable.", "",
          "Lecture : un écart positif signifie que le premier profil reçoit plus souvent une proposition que le second, dans les mêmes formations. "
          "Ce n'est PAS un effet causal du profil : les candidats internes ou en BUT peuvent différer par leurs résultats, leur projet, "
          "ou ne candidater que là où ils ont de bonnes chances.", ""]

    by = []
    for disc, sub in long.groupby("secteur_disci_lib"):
        try:
            r = within_gap(sub, "etab", "hors_etab")
            by.append({"secteur": disc, **{k: r[k] for k in ("formations_x_sessions", "taux_a", "taux_b", "ecart_points", "ic95_bas", "ic95_haut")}})
        except (ZeroDivisionError, ValueError):
            continue
    L += ["## 4. Prime aux candidats internes par secteur disciplinaire", "",
          pd.DataFrame(by).sort_values("ecart_points", ascending=False).round(3).to_markdown(index=False), ""]

    sel = long[(long.profil == "lg3")].assign(r=lambda x: x.taux_prop)
    tension = long[long.profil.isin(PROFILS)].groupby(["session", "ifc", "mention"]).agg(c=("candidats", "sum"), p=("propositions", "sum")).reset_index()
    tension["taux"] = tension.p / tension.c
    mt = tension.groupby("mention").agg(formations=("ifc", "nunique"), candidats=("c", "sum"), propositions=("p", "sum"))
    mt = mt[mt.formations >= 10]
    mt["taux_prop"] = mt.propositions / mt.candidats
    L += ["## 5. Mentions les plus et les moins accessibles (≥ 10 formations, 2024-2025 cumulés)", "",
          "**Les moins accessibles**", "", mt.nsmallest(15, "taux_prop").round(3).reset_index().to_markdown(index=False), "",
          "**Les plus accessibles**", "", mt.nlargest(10, "taux_prop").round(3).reset_index().to_markdown(index=False), ""]
    del sel
    L += ["## Limites", "",
          "- Taux historiques par profil, pas des probabilités individuelles : dossier, notes et projet ne sont pas observés.",
          "- Un candidat compte dans chaque formation demandée ; les candidats qui se désistent avant toute proposition restent au dénominateur.",
          "- Hors champ de la plateforme : étudiants « Études en France », redoublants, admissions de droit, certains masters internationaux.",
          "- Deux sessions seulement (2024, 2025) : les taux d'une formation peuvent varier fortement d'une année à l'autre.",
          "- Les comparaisons de profils ne sont pas causales (sélection des candidatures)."]
    return "\n".join(L)


# ---------- correction statistique (bayésien empirique) ----------

KAPPA_MIN, KAPPA_MAX, MIN_FORMATIONS_PRIOR = 2.0, 1000.0, 5


def _moments(k: np.ndarray, n: np.ndarray) -> tuple[float, float]:
    """Loi a priori Bêta(m, κ) par la méthode des moments (bêta-binomiale) : m = moyenne poolée,
    variance « vraie » entre formations = variance observée − bruit binomial attendu."""
    m = k.sum() / n.sum()
    p = k / n
    var_obs = np.average((p - m) ** 2, weights=n)
    bruit = np.average(m * (1 - m) / n, weights=n)
    tau2 = max(var_obs - bruit, 1e-6)
    kappa = float(np.clip(m * (1 - m) / tau2 - 1, KAPPA_MIN, KAPPA_MAX))
    return float(m), kappa


def fit_priors(long: pd.DataFrame) -> pd.DataFrame:
    """Une loi a priori par (mention, profil), estimée sur les formations de la mention ; repli sur la loi
    nationale du profil si la mention compte moins de MIN_FORMATIONS_PRIOR formations avec candidats."""
    d = long[long.candidats > 0].groupby(["mention", "profil", "ifc"])[["propositions", "candidats"]].sum().reset_index()
    nat = {p: _moments(g.propositions.to_numpy(float), g.candidats.to_numpy(float)) for p, g in d.groupby("profil")}
    rows = []
    for (men, pro), g in d.groupby(["mention", "profil"]):
        if len(g) >= MIN_FORMATIONS_PRIOR and g.propositions.sum() > 0:
            m, kappa = _moments(g.propositions.to_numpy(float), g.candidats.to_numpy(float))
            src = "mention"
        else:
            (m, kappa), src = nat[pro], "national"
        rows.append({"mention": men, "profil": pro, "m": m, "kappa": kappa, "source": src})
    return pd.DataFrame(rows).set_index(["mention", "profil"])


def shrink(k, n, m, kappa):
    """Moyenne a posteriori : (k + κ·m) / (n + κ). Peu de candidats → proche de m ; beaucoup → proche de k/n."""
    return (np.asarray(k, float) + kappa * m) / (np.asarray(n, float) + kappa)


def backtest(long: pd.DataFrame, n_eval: int = 30) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Prévoir 2025 à partir de 2024 seul : taux brut vs taux corrigé. Évaluation sur les couples
    formation × profil avec ≥ n_eval candidats en 2025 et ≥ 1 en 2024."""
    a, b = long[long.session == 2024], long[long.session == 2025]
    pri = fit_priors(a)
    k = ["ifc", "profil"]
    j = a[k + ["mention", "candidats", "propositions"]].merge(b[k + ["candidats", "propositions"]], on=k, suffixes=("_24", "_25"))
    j = j[(j.candidats_24 > 0) & (j.candidats_25 >= n_eval)].join(pri, on=["mention", "profil"])
    j["brut"] = j.propositions_24 / j.candidats_24
    j["corrige"] = shrink(j.propositions_24, j.candidats_24, j.m, j.kappa)
    j["obs"] = j.propositions_25 / j.candidats_25
    w = j.candidats_25
    rows = []
    for lab, sub in (("tous", j), ("moins de 30 candidats en 2024", j[j.candidats_24 < 30]), ("30 candidats ou plus en 2024", j[j.candidats_24 >= 30])):
        ww = w.loc[sub.index]
        rows.append({"couples": lab, "n": len(sub),
                     "erreur_abs_brut_pts": np.average((sub.brut - sub.obs).abs(), weights=ww) * 100,
                     "erreur_abs_corrige_pts": np.average((sub.corrige - sub.obs).abs(), weights=ww) * 100,
                     "spearman_brut": sub.brut.rank().corr(sub.obs.rank()),
                     "spearman_corrige": sub.corrige.rank().corr(sub.obs.rank())})
    bins = [0, .05, .1, .2, .3, .5, 1.01]
    cal = pd.concat([j.groupby(pd.cut(j[c], bins, include_lowest=True), observed=True)
                     .agg(**{f"n_{c}": ("obs", "size"), f"prevu_{c}": (c, "mean"), f"observe_{c}": ("obs", "mean")}) for c in ("brut", "corrige")], axis=1)
    return pd.DataFrame(rows), cal


# ---------- export pour la page ----------

def export_json(long: pd.DataFrame, priors: pd.DataFrame | None = None) -> dict:
    """Une entrée par formation (ifc) : métadonnées + par profil et session [candidats, propositions]."""
    meta_cols = ["eta_nom", "lieu_acad_lib", "mention", "parcours", "alternance", "secteur_disci_lib"]
    last = long.sort_values("session").groupby("ifc").last()
    sessions = sorted(long.session.unique().tolist())
    profils = list(PROFILS) + ["etab", "hors_etab"]
    cube = long.pivot_table(index="ifc", columns=["profil", "session"], values=["candidats", "propositions"], aggfunc="sum").fillna(-1)
    caps = long[long.profil == "lg3"].pivot_table(index="ifc", columns="session", values=["col", "rang_dernier_appele_pp"], aggfunc="first")

    def strings(col: str) -> tuple[list[str], dict]:
        vals = sorted(last[col].fillna("").astype(str).unique().tolist())
        return vals, {v: i for i, v in enumerate(vals)}

    dicts = {c: strings(c) for c in ("eta_nom", "lieu_acad_lib", "mention", "secteur_disci_lib")}
    ifcs = last.index
    cols = [(v, p, s) for p in profils for s in sessions for v in ("candidats", "propositions")]
    stats = cube.reindex(columns=pd.MultiIndex.from_tuples(cols)).reindex(ifcs).fillna(-1).astype(int).to_numpy()
    capa = caps.reindex(ifcs)

    def opt(col: str, s: int) -> list:
        v = capa[(col, s)] if (col, s) in capa else pd.Series(np.nan, index=ifcs)
        return [None if pd.isna(x) else int(x) for x in v]

    cap_s = [opt("col", s) for s in sessions]
    rang_s = [opt("rang_dernier_appele_pp", s) for s in sessions]
    rows = []
    for i, (ifc, r) in enumerate(last.iterrows()):
        rows.append([str(ifc), dicts["eta_nom"][1][str(r.eta_nom or "")], dicts["lieu_acad_lib"][1][str(r.lieu_acad_lib or "")],
                     dicts["mention"][1][str(r.mention or "")], str(r.parcours) if pd.notna(r.parcours) else "",
                     int(r.alternance), dicts["secteur_disci_lib"][1][str(r.secteur_disci_lib or "")],
                     [c[i] for c in cap_s], [c[i] for c in rang_s], stats[i].tolist()])
    return {"sessions": sessions, "profils": profils, "libelles_profils": {**PROFILS, "etab": "Même établissement", "hors_etab": "Autre établissement"},
            "etablissements": dicts["eta_nom"][0], "academies": dicts["lieu_acad_lib"][0], "mentions": dicts["mention"][0],
            "secteurs": dicts["secteur_disci_lib"][0], "min_candidats": MIN_CANDIDATS,
            "colonnes": ["ifc", "etab", "academie", "mention", "parcours", "alternance", "secteur", "places[session]",
                         "rang_dernier_appele_pp[session]", "stats[profil][session][candidats, propositions] aplati ; -1 = absent"],
            "formations": rows,
            # loi a priori par mention × profil, estimée sur 2024+2025 : {mention_index: {profil: [m, kappa]}}
            "priors": {} if priors is None else {
                str(dicts["mention"][1][men]): {pro: [round(r.m, 5), round(r.kappa, 2)] for (_, pro), r in g.iterrows()}
                for men, g in priors.groupby(level=0) if men in dicts["mention"][1]}}


def main() -> None:
    m = load()
    long = to_long(m)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    long.to_csv(OUT_CSV, sep=";", index=False)
    priors = fit_priors(long)
    OUT_JSON.write_text(json.dumps(export_json(long, priors), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    bt, cal = backtest(long)
    extra = ["", "## 6. Prévision : le taux d'une année annonce-t-il celui de l'année suivante ?", "",
             "Taux 2024 utilisés pour prévoir 2025. « Corrigé » = moyenne a posteriori bayésienne empirique "
             "(k + κ·m)/(n + κ), avec une loi a priori Bêta par mention × profil estimée sur 2024 seulement (pas de fuite vers 2025). "
             "Erreurs pondérées par le nombre de candidats 2025.", "",
             bt.round(3).to_markdown(index=False), "",
             "**Calibration** (moyenne prévue vs moyenne observée en 2025, par tranche de prévision)", "",
             cal.round(3).reset_index(names="tranche").to_markdown(index=False), "",
             "Part restante de l'écart : hausse générale des candidatures en 2025 (+17 % en phase principale), qui fait baisser tous les taux."]
    OUT_MD.write_text(report(m, long) + "\n".join(extra), encoding="utf-8")
    print(f"{len(long):,} lignes -> {OUT_CSV}\n-> {OUT_JSON} ({OUT_JSON.stat().st_size / 1e6:.1f} Mo)\n-> {OUT_MD}")


if __name__ == "__main__":
    main()
