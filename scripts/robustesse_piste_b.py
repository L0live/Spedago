"""Spédago — piste B : contrôles de robustesse.

Usage : python3 scripts/robustesse_piste_b.py
Entrées : data/processed/specialites_lycees.csv (build_indice_specialites.py) + sources brutes
Sortie  : reports/piste_B_robustesse.md

  1. Simulation « neutre » corrigée : les parts nationales des combinaisons incluent la masse masquée
     (répartie à parts égales entre les cases masquées de chaque lycée × sexe), au lieu des seules cases
     publiées qui sous-représentent les combinaisons rares.
  2. Taille : effets fixes par décile de taille (au lieu du seul log) + erreurs-types regroupées par académie.
  3. Stabilité : rentrées 2021, 2023, 2025.
  4. Résultat IPS contre-intuitif : quelles spécialités sont moins souvent proposées dans les lycées
     favorisés, à taille égale ?
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_indice_specialites as b  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TAB = ROOT / "data" / "processed" / "specialites_lycees.csv"
OUT_MD = ROOT / "reports" / "piste_B_robustesse.md"
ANNEES = (2021, 2023, 2025)


# ---------- 1. parts nationales corrigées ----------

def national_shares(t: pd.DataFrame, niveau: str, corrige: bool) -> tuple[np.ndarray, np.ndarray]:
    _, combo = b.column_groups(list(t.columns), niveau)
    out = []
    for sexe, tot in ((0, "effectif_total_filles"), (1, "effectif_total_garcons")):
        cols = [p[sexe] for p in combo]
        known = t[cols].fillna(0)
        if corrige:
            reste = (t[tot] - known.sum(axis=1)).clip(lower=0).fillna(0)
            nmask = t[cols].isna().sum(axis=1).replace(0, np.nan)
            known = known + t[cols].isna().mul(reste / nmask, axis=0).fillna(0)
        s = known.sum().to_numpy(float)
        out.append(s / s.sum())
    return out[0], out[1]


def simulate(t: pd.DataFrame, niveau: str, obs: pd.DataFrame, pf: np.ndarray, pg: np.ndarray, n: int = 1500, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for _, r in obs.sample(min(n, len(obs)), random_state=seed).iterrows():
        eff = int(r.effectif_total)
        nf = int(r.effectif_total_filles) if pd.notna(r.effectif_total_filles) else eff // 2
        cf, cg = rng.multinomial(nf, pf), rng.multinomial(eff - nf, pg)
        rows.append({"effectif_total": eff, "observe": r.part_non_publiee,
                     "sim": (cf[(cf > 0) & (cf < 5)].sum() + cg[(cg > 0) & (cg < 5)].sum()) / eff})
    return pd.DataFrame(rows)


# ---------- 2. régression à effets fixes, erreurs regroupées ----------

def ols_cluster(y: pd.Series, X: pd.DataFrame, cluster: pd.Series) -> pd.DataFrame:
    """MCO, erreurs-types robustes regroupées (CR1). X contient déjà les indicatrices d'effets fixes."""
    d = pd.concat([y.rename("_y"), X, cluster.rename("_g")], axis=1).dropna()
    yv = d["_y"].to_numpy(float)
    Xv = np.column_stack([np.ones(len(d)), d[X.columns].to_numpy(float)])
    bread = np.linalg.pinv(Xv.T @ Xv)
    beta = bread @ Xv.T @ yv
    e = yv - Xv @ beta
    meat = np.zeros((Xv.shape[1],) * 2)
    for _, idx in d.groupby("_g").indices.items():
        s = Xv[idx].T @ e[idx]
        meat += np.outer(s, s)
    n, k, g = len(d), Xv.shape[1], d["_g"].nunique()
    cov = bread @ meat @ bread * (g / (g - 1)) * ((n - 1) / (n - k))
    se = np.sqrt(np.diag(cov))
    names = ["constante", *X.columns]
    return pd.DataFrame({"coef": beta, "se": se, "t": beta / se}, index=names).assign(n=n, grappes=g)


def size_fe(d: pd.DataFrame) -> pd.DataFrame:
    dec = pd.qcut(d.effectif_total.rank(method="first"), 10, labels=False)
    return pd.get_dummies(dec, prefix="taille_dec", drop_first=True).astype(float)


def regressions(d: pd.DataFrame) -> pd.DataFrame:
    z = lambda s: (s - s.mean()) / s.std()  # noqa: E731
    ctrl = {"ips_z": z(d.ips_voie_gt), "eloignement_z": z(d.indice_eloignement), "prive": d.prive.astype(float)}
    if "type_de_lycee" in d:  # LPO (polyvalent) vs LEGT : confusion possible avec l'IPS
        ctrl["lpo"] = (d.type_de_lycee == "LPO").astype(float)
    X = pd.concat([size_fe(d), pd.DataFrame(ctrl, index=d.index)], axis=1)
    rows = []
    for y in ("nb_spe_visibles", "part_non_publiee"):
        r = ols_cluster(d[y], X, d.academie)
        for v in ctrl:
            rows.append({"variable_expliquee": y, "variable": v, "coef": r.loc[v, "coef"], "se_grappes": r.loc[v, "se"],
                         "t": r.loc[v, "t"], "n": int(r.n.iloc[0]), "academies": int(r.grappes.iloc[0])})
    return pd.DataFrame(rows)


# ---------- 4. offre par spécialité selon l'IPS ----------

def offer_by_specialty(t: pd.DataFrame, niveau: str, ctx: pd.DataFrame) -> pd.DataFrame:
    spe, _ = b.column_groups(list(t.columns), niveau)
    d = t[["numero_etablissement", "effectif_total", "academie"]].merge(ctx, left_on="numero_etablissement", right_on="uai", how="left")
    z = (d.ips_voie_gt - d.ips_voie_gt.mean()) / d.ips_voie_gt.std()
    X = pd.concat([size_fe(d), z.rename("ips_z")], axis=1)
    rows = []
    for f, g in spe:
        offered = ((t[f].fillna(0) + t[g].fillna(0)) > 0).astype(float).reset_index(drop=True)
        if offered.mean() < 0.02:
            continue
        r = ols_cluster(offered, X.reset_index(drop=True), d.academie.reset_index(drop=True))
        rows.append({"specialite": f.split("_", 1)[1].removesuffix("_filles").rsplit("_filles", 1)[0],
                     "part_lycees_proposant": offered.mean(), "effet_ips_1_ecart_type": r.loc["ips_z", "coef"],
                     "t": r.loc["ips_z", "t"]})
    return pd.DataFrame(rows).sort_values("effet_ips_1_ecart_type")


def main() -> None:
    tab = pd.read_csv(TAB, sep=";", low_memory=False)
    L = ["# Piste B — contrôles de robustesse", ""]

    # 1
    L += ["## 1. Simulation neutre : parts nationales naïves vs corrigées (rentrée 2025)", "",
          "Naïf : parts calculées sur les cases publiées (sous-représente les combinaisons rares). "
          "Corrigé : masse masquée de chaque lycée × sexe répartie entre ses cases masquées.", ""]
    for niveau, (fname, _) in b.SOURCES.items():
        t = pd.read_csv(b.RAW / fname, sep=";", low_memory=False)
        t = t[t.rentree_scolaire == 2025]
        obs = tab[(tab.niveau == niveau) & (tab.rentree == 2025)]
        res = []
        for lab, corr in (("naif", False), ("corrige", True)):
            pf, pg = national_shares(t, niveau, corr)
            s = simulate(t, niveau, obs, pf, pg)
            s["taille"] = pd.cut(s.effectif_total, [0, 60, 120, 200, 300, 10_000], labels=["<60", "60-119", "120-199", "200-299", "300+"])
            res.append(s.groupby("taille", observed=True).agg(**{f"sim_{lab}": ("sim", "median"), "observe": ("observe", "median")}))
        r = res[0].join(res[1].drop(columns="observe"))
        r["ratio_naif"], r["ratio_corrige"] = r.observe / r.sim_naif, r.observe / r.sim_corrige
        L += [f"**{niveau}**", "", r.round(3).reset_index().to_markdown(index=False), ""]

    # 2-3
    L += ["## 2-3. Régressions à effets fixes de taille (déciles), erreurs regroupées par académie, 3 rentrées", "",
          "Coefficients pour un écart-type d'IPS ou d'éloignement ; `prive` = privé sous contrat vs public ; "
          "`lpo` = lycée polyvalent vs LEGT (contrôle du type de lycée).", ""]
    ips_a = pd.read_csv(b.RAW / "ips_lycees_2016_2022.csv", sep=";", low_memory=False)
    ips_b = pd.read_csv(b.RAW / "ips_lycees_ap2023.csv", sep=";", low_memory=False)
    types = pd.concat([ips_a[["rentree_scolaire", "uai", "type_de_lycee"]], ips_b[["rentree_scolaire", "uai", "type_de_lycee"]]])
    types["rentree"] = types.rentree_scolaire.str[:4].astype(int)
    tab = tab.merge(types[["rentree", "uai", "type_de_lycee"]], left_on=["rentree", "numero_etablissement"],
                    right_on=["rentree", "uai"], how="left")
    allr = []
    for niveau in ("1re", "tle"):
        for an in ANNEES:
            d = tab[(tab.niveau == niveau) & (tab.rentree == an)].reset_index(drop=True)
            if d.ips_voie_gt.notna().mean() < 0.5:
                continue
            allr.append(regressions(d).assign(niveau=niveau, rentree=an))
    R = pd.concat(allr)
    piv = R.pivot_table(index=["niveau", "variable_expliquee", "variable"], columns="rentree", values=["coef", "t"]).round(3)
    piv.columns = [f"{a}_{c}" for a, c in piv.columns]
    L += [piv.reset_index().to_markdown(index=False), "",
          "Lecture : |t| > 2 ≈ significatif à 5 %. Un signe stable sur les 3 rentrées renforce la conclusion.", ""]

    # 4
    a = pd.read_csv(b.RAW / "ips_lycees_ap2023.csv", sep=";", low_memory=False)
    ctx = a[a.rentree_scolaire.str.startswith("2025")][["uai", "ips_voie_gt"]]
    for niveau, (fname, _) in b.SOURCES.items():
        t = pd.read_csv(b.RAW / fname, sep=";", low_memory=False)
        t = t[(t.rentree_scolaire == 2025) & t.effectif_total.notna()].reset_index(drop=True)
        o = offer_by_specialty(t, niveau, ctx)
        L += [f"## 4. Offre de chaque spécialité selon l'IPS, à taille égale — {niveau} 2025", "",
              "Effet d'un écart-type d'IPS sur la probabilité qu'un lycée propose la spécialité (points de probabilité), "
              "effets fixes de taille, erreurs regroupées par académie.", "",
              o.round(3).to_markdown(index=False), ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"-> {OUT_MD}")


if __name__ == "__main__":
    main()
