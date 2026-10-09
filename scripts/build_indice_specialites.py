"""Spédago — piste B : offre et dispersion des spécialités par lycée (1re et terminale générales).

Usage : python3 scripts/build_indice_specialites.py
Entrées : data/raw/specialites_triplettes_1ere.csv, specialites_doublettes_tle.csv,
          ips_lycees_2016_2022.csv, ips_lycees_ap2023.csv, eloignement_lycees.csv
Sorties : data/processed/specialites_lycees.csv
          reports/piste_B_specialites.md

Constats sur les sources (vérifiés, voir rapport) :
  - Colonnes par paires filles / garçons, DANS CET ORDRE ; certains noms sont tronqués à 100 caractères
    et perdent leur suffixe -> appariement par POSITION, pas par nom.
  - Zéros explicites ; cases vides = valeurs masquées (secret statistique), pas toujours < 5 :
    secret secondaire probable (reste moyen par case vide > 4, et parfois 0).
  - Les combinaisons publiées (nommées + « autres ») partitionnent les élèves : la somme publiée ne
    dépasse jamais l'effectif. Donc part_non_publiee = (effectif − somme publiée) / effectif est EXACTE.

Indicateurs par lycée × rentrée × niveau :
  nb_spe_visibles      spécialités avec au moins un élève visible (borne basse de l'offre)
  nb_spe_max           idem en comptant les cases masquées comme ouvertes (borne haute)
  part_non_publiee     part des élèves dans des cellules combinaison × sexe masquées
                       = proxy de dispersion des élèves en petits groupes de combinaisons
  part_autres_min      part visible hors des combinaisons nationales dominantes (borne basse)
  indice_dispersion    part_non_publiee − médiane des lycées de même taille (décile), même niveau et année
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT_CSV = ROOT / "data" / "processed" / "specialites_lycees.csv"
OUT_MD = ROOT / "reports" / "piste_B_specialites.md"

SOURCES = {"1re": ("specialites_triplettes_1ere.csv", 3), "tle": ("specialites_doublettes_tle.csv", 2)}
EXCLUS_EFFECTIF_MASQUE = 0
ID_COLS = ["rentree_scolaire", "numero_etablissement", "denomination_principale", "academie", "secteur",
           "effectif_total", "effectif_total_filles", "effectif_total_garcons"]


# ---------- parsing ----------

def column_groups(columns: list[str], niveau: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Retourne (paires spécialités, paires combinaisons) sous forme [(col_filles, col_garcons), ...].
    Spécialité : code à 4 chiffres (en terminale, les codes 0001-0015 sont des doublettes).
    Combinaison : 1re -> code à 2 chiffres ; tle -> 0001-0015 ; + autres_combinaisons."""
    spe, combo = [], []
    for c in columns:
        head = c.split("_")[0]
        if c.startswith("autres_combinaisons"):
            combo.append(c)
        elif niveau == "1re" and len(head) == 2 and head.isdigit():
            combo.append(c)
        elif len(head) == 4 and head.isdigit():
            (combo if niveau == "tle" and int(head) <= 15 else spe).append(c)
    pair = lambda cs: [(cs[i], cs[i + 1]) for i in range(0, len(cs), 2)]  # noqa: E731
    if len(spe) % 2 or len(combo) % 2:
        raise ValueError("nombre impair de colonnes : l'hypothèse filles/garçons par paire est fausse")
    return pair(spe), pair(combo)


def check_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Paires dont le code (préfixe) diffère : doit être vide."""
    return [(f, g) for f, g in pairs if f.split("_")[0] != g.split("_")[0]]


def indicators(t: pd.DataFrame, niveau: str) -> pd.DataFrame:
    spe, combo = column_groups(list(t.columns), niveau)
    eff = t.effectif_total.astype(float)
    combo_cols = [c for p in combo for c in p]
    published = t[combo_cols].fillna(0).sum(axis=1)
    autres = [c for c in combo_cols if c.startswith("autres_combinaisons")]

    vis = np.column_stack([(t[f].fillna(0) + t[g].fillna(0)) > 0 for f, g in spe])
    any_masked = np.column_stack([t[f].isna() | t[g].isna() for f, g in spe])
    out = t[ID_COLS].copy()
    out["niveau"] = niveau
    out["nb_spe_visibles"] = vis.sum(axis=1)
    out["nb_spe_max"] = (vis | any_masked).sum(axis=1)
    out["somme_publiee_combos"] = published
    out["part_non_publiee"] = (eff - published) / eff
    out["part_autres_min"] = t[autres].fillna(0).sum(axis=1) / eff
    out["nb_cases_masquees_combos"] = t[combo_cols].isna().sum(axis=1)
    return out


def size_adjust(df: pd.DataFrame) -> pd.Series:
    """part_non_publiee nette de l'effet mécanique de la taille (plus un lycée est petit, plus ses cellules
    sont petites donc masquées) : écart à la médiane du décile de taille, par niveau et rentrée."""
    dec = df.groupby(["niveau", "rentree_scolaire"]).effectif_total.transform(
        lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    med = df.groupby([df.niveau, df.rentree_scolaire, dec]).part_non_publiee.transform("median")
    return df.part_non_publiee - med


def load_context() -> pd.DataFrame:
    a = pd.read_csv(RAW / "ips_lycees_2016_2022.csv", sep=";", low_memory=False)
    b = pd.read_csv(RAW / "ips_lycees_ap2023.csv", sep=";", low_memory=False)
    ips = pd.concat([a[["rentree_scolaire", "uai", "ips_voie_gt"]], b[["rentree_scolaire", "uai", "ips_voie_gt"]]])
    ips["rentree"] = ips.rentree_scolaire.str[:4].astype(int)
    elo = pd.read_csv(RAW / "eloignement_lycees.csv", sep=";", low_memory=False)
    elo["rentree"] = elo.rentree_scolaire.astype(int)
    elo["indice_eloignement"] = pd.to_numeric(elo.indice_eloignement, errors="coerce")
    return (ips[["rentree", "uai", "ips_voie_gt"]]
            .merge(elo[["rentree", "uai", "indice_eloignement"]], on=["rentree", "uai"], how="outer"))


def build() -> pd.DataFrame:
    parts = []
    for niveau, (fname, _) in SOURCES.items():
        t = pd.read_csv(RAW / fname, sep=";", low_memory=False)
        parts.append(indicators(t, niveau))
    df = pd.concat(parts, ignore_index=True)
    # Effectif total lui-même masqué (très petits lycées) : indicateurs non calculables
    global EXCLUS_EFFECTIF_MASQUE
    EXCLUS_EFFECTIF_MASQUE = int(df.effectif_total.isna().sum())
    df = df[df.effectif_total.notna()].reset_index(drop=True)
    df["rentree"] = df.rentree_scolaire.astype(int)
    df["indice_dispersion"] = size_adjust(df)
    ctx = load_context()
    df = df.merge(ctx, left_on=["rentree", "numero_etablissement"], right_on=["rentree", "uai"], how="left").drop(columns="uai")
    df["prive"] = df.secteur.str.contains("PRIVE", na=False)
    return df


# ---------- validation du proxy ----------

def simulate_neutral(t: pd.DataFrame, niveau: str, obs: pd.DataFrame, n: int = 1000, seed: int = 0) -> pd.DataFrame:
    """Lycées fictifs de même taille et même sexe-ratio que des lycées réels, dont les élèves tirent leur
    combinaison selon la répartition NATIONALE, soumis au seul secret primaire (cellule sexe × combinaison
    entre 1 et 4 masquée). Donne la part non publiée « mécanique » attendue sans dispersion locale
    ni secret secondaire. Approximation : parts nationales calculées sur les cellules publiées."""
    _, combo = column_groups(list(t.columns), niveau)
    pf = np.array([t[f].fillna(0).sum() for f, _ in combo]); pf = pf / pf.sum()
    pg = np.array([t[g].fillna(0).sum() for _, g in combo]); pg = pg / pg.sum()
    rng = np.random.default_rng(seed)
    rows = []
    for _, r in obs.sample(min(n, len(obs)), random_state=seed).iterrows():
        eff = int(r.effectif_total)
        nf = int(r.effectif_total_filles) if pd.notna(r.effectif_total_filles) else eff // 2
        cf, cg = rng.multinomial(nf, pf), rng.multinomial(eff - nf, pg)
        masked = cf[(cf > 0) & (cf < 5)].sum() + cg[(cg > 0) & (cg < 5)].sum()
        rows.append({"effectif_total": eff, "sim_neutre": masked / eff, "observe": r.part_non_publiee})
    return pd.DataFrame(rows)


# ---------- analyse ----------

def ols(y: pd.Series, X: pd.DataFrame) -> pd.DataFrame:
    """MCO avec erreurs-types robustes (HC1). Variables explicatives standardisées en amont."""
    d = pd.concat([y, X], axis=1).dropna()
    yv, Xv = d.iloc[:, 0].to_numpy(float), np.column_stack([np.ones(len(d)), d.iloc[:, 1:].to_numpy(float)])
    beta, *_ = np.linalg.lstsq(Xv, yv, rcond=None)
    e = yv - Xv @ beta
    n, k = Xv.shape
    bread = np.linalg.inv(Xv.T @ Xv)
    cov = bread @ (Xv.T * e**2) @ Xv @ bread * n / (n - k)
    se = np.sqrt(np.diag(cov))
    r2 = 1 - (e @ e) / ((yv - yv.mean()) @ (yv - yv.mean()))
    return pd.DataFrame({"coef": beta, "se": se, "t": beta / se}, index=["constante", *X.columns]).round(3).assign(n=n, r2=round(r2, 3))


def by_quartile(d: pd.DataFrame, col: str, label: str) -> pd.DataFrame:
    q = pd.qcut(d[col], 4, labels=[f"Q1 ({label} faible)", "Q2", "Q3", f"Q4 ({label} fort)"])
    return d.groupby(q, observed=True).agg(lycees=("effectif_total", "size"), effectif_median=("effectif_total", "median"),
                                           nb_spe_moyen=("nb_spe_visibles", "mean"),
                                           part_lycees_moins_6_spe=("nb_spe_visibles", lambda x: (x < 6).mean()),
                                           part_non_publiee=("part_non_publiee", "median"),
                                           indice_dispersion=("indice_dispersion", "median")).round(3).reset_index()


def report(df: pd.DataFrame) -> str:
    L = ["# Piste B — offre et dispersion des spécialités par lycée", "",
         "Sources DEPP (1re : triplettes 2021-2025 ; terminale : doublettes 2020-2025), IPS voie GT, indice d'éloignement.", ""]

    L += ["## 1. Contrôles sur les sources", ""]
    for niveau, (fname, _) in SOURCES.items():
        t = pd.read_csv(RAW / fname, sep=";", nrows=0)
        spe, combo = column_groups(list(t.columns), niveau)
        L.append(f"- {niveau} : {len(spe)} spécialités, {len(combo)} combinaisons (dont « autres ») ; "
                 f"paires filles/garçons incohérentes : {len(check_pairs(spe + combo))}")
    d = df
    L += [f"- Lignes exclues car effectif total masqué : {EXCLUS_EFFECTIF_MASQUE}",
          f"- Somme publiée > effectif : {(d.somme_publiee_combos > d.effectif_total).sum()} lignes (attendu 0 : partition)",
          f"- Jointure IPS (2025) : {d[(d.rentree == 2025)].ips_voie_gt.notna().mean():.1%} des lycées ; "
          f"éloignement (2025) : {d[(d.rentree == 2025)].indice_eloignement.notna().mean():.1%}",
          "- IPS absent pour la rentrée 2022 (trou entre les deux séries DEPP) et rupture de série en 2023 : pas de comparaison de niveaux d'IPS dans le temps.", ""]

    L += ["## 1bis. Validation du proxy : lycées « neutres » simulés (rentrée 2025)", "",
          "Même taille et sexe-ratio que 1 000 lycées réels tirés au hasard, combinaisons tirées selon la répartition nationale, "
          "secret primaire seul. Si l'observé ≈ simulé, la part non publiée ne serait qu'un artefact de taille.", ""]
    for niveau, (fname, _) in SOURCES.items():
        t = pd.read_csv(RAW / fname, sep=";", low_memory=False)
        t = t[t.rentree_scolaire == 2025]
        sim = simulate_neutral(t, niveau, df[(df.niveau == niveau) & (df.rentree == 2025)])
        sim["taille"] = pd.cut(sim.effectif_total, [0, 60, 120, 200, 300, 10_000], labels=["<60", "60-119", "120-199", "200-299", "300+"])
        tab = sim.groupby("taille", observed=True)[["sim_neutre", "observe"]].median()
        tab["ratio"] = tab.observe / tab.sim_neutre
        L += [f"**{niveau}** (corrélation de rang observé/simulé : {sim.sim_neutre.rank().corr(sim.observe.rank()):.2f})", "",
              tab.round(3).reset_index().to_markdown(index=False), ""]
    L += ["**Attention : cette simulation est biaisée** (parts nationales calculées sur les seules cases publiées, ce qui "
          "sous-représente les combinaisons rares et sous-estime le masquage mécanique). Version corrigée dans "
          "`reports/piste_B_robustesse.md` : l'observé y est proche du mécanique dans les petits et moyens lycées (ratio ≈ 1 à 1,4) "
          "et ne le dépasse nettement que dans les grands (≈ 1,5 à 2,3). La part non publiée est donc SURTOUT un effet de taille ; "
          "l'indice ajusté sert à comparer des lycées de taille voisine, avec un signal faible.", ""]

    ev = df.groupby(["niveau", "rentree"]).agg(lycees=("effectif_total", "size"), eleves=("effectif_total", "sum"),
                                              nb_spe_visibles=("nb_spe_visibles", "median"), nb_spe_max=("nb_spe_max", "median"),
                                              part_non_publiee=("part_non_publiee", "median"),
                                              part_autres_min=("part_autres_min", "median")).round(3).reset_index()
    L += ["## 2. Évolution nationale (médianes par lycée)", "", ev.to_markdown(index=False), ""]

    for niveau in ("1re", "tle"):
        d = df[(df.niveau == niveau) & (df.rentree == 2025)].copy()
        d["taille"] = pd.cut(d.effectif_total, [0, 60, 120, 200, 300, 10_000], labels=["<60", "60-119", "120-199", "200-299", "300+"])
        L += [f"## 3.{niveau} Rentrée 2025 — par taille et secteur", "",
              d.groupby(["taille", "secteur"], observed=True).agg(lycees=("effectif_total", "size"),
                                                                  nb_spe_visibles=("nb_spe_visibles", "median"),
                                                                  part_non_publiee=("part_non_publiee", "median")).round(3).reset_index().to_markdown(index=False), "",
              f"### Par quartile d'IPS (voie GT) — {niveau} 2025", "", by_quartile(d, "ips_voie_gt", "IPS").to_markdown(index=False), "",
              f"### Par quartile d'éloignement — {niveau} 2025", "", by_quartile(d, "indice_eloignement", "éloignement").to_markdown(index=False), ""]
        z = lambda s: (s - s.mean()) / s.std()  # noqa: E731
        X = pd.DataFrame({"log_effectif_z": z(np.log(d.effectif_total)), "ips_z": z(d.ips_voie_gt),
                          "eloignement_z": z(d.indice_eloignement), "prive": d.prive.astype(float)})
        L += [f"### Régressions (MCO, erreurs robustes) — {niveau} 2025", "",
              "Variables standardisées (z) : un coefficient = effet d'un écart-type, toutes choses égales par ailleurs.", "",
              "**nb_spe_visibles**", "", ols(d.nb_spe_visibles, X).to_markdown(), "",
              "**indice_dispersion** (déjà net de la taille)", "", ols(d.indice_dispersion, X.drop(columns="log_effectif_z")).to_markdown(), ""]

    L += ["## Limites", "",
          "- `part_non_publiee` mélange secret primaire (petites cellules) et secondaire : c'est un PROXY de dispersion, monotone mais non linéaire.",
          "- Le masquage est par sexe : une combinaison suivie par 3 filles et 3 garçons est entièrement masquée alors qu'elle forme un groupe de 6.",
          "- Les combinaisons sont nationales (les 18 ou 15 plus fréquentes) : « autres » n'est pas détaillé.",
          "- Aucune donnée d'emploi du temps : l'indice mesure une CONTRAINTE potentielle (élèves éclatés entre combinaisons), pas le morcellement réel.",
          "- Corrélations descriptives, pas d'effet causal."]
    return "\n".join(L)


def main() -> None:
    df = build()
    df.to_csv(OUT_CSV, sep=";", index=False)
    OUT_MD.write_text(report(df), encoding="utf-8")
    print(f"{len(df):,} lignes -> {OUT_CSV}\n-> {OUT_MD}")


if __name__ == "__main__":
    main()
