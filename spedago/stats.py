"""Spédago — statistiques partagées (intervalles, bêta-binomiale, régressions).

Extraites telles quelles des scripts d'origine : le comportement est garanti identique par les tests.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

Z = 1.96
KAPPA_MIN, KAPPA_MAX = 2.0, 1000.0


def wilson(k: np.ndarray, n: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    k, n = np.asarray(k, float), np.asarray(n, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = k / n
        den = 1 + Z**2 / n
        c = (p + Z**2 / (2 * n)) / den
        h = Z * np.sqrt(p * (1 - p) / n + Z**2 / (4 * n**2)) / den
    return np.where(n > 0, c - h, np.nan), np.where(n > 0, c + h, np.nan)


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


def shrink(k, n, m, kappa):
    """Moyenne a posteriori : (k + κ·m) / (n + κ). Peu de candidats → proche de m ; beaucoup → proche de k/n."""
    return (np.asarray(k, float) + kappa * m) / (np.asarray(n, float) + kappa)


def ratio(num: pd.Series, den: pd.Series) -> pd.Series:
    return num.where(den > 0) / den.where(den > 0)


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


beta_binomial_moments = _moments  # nom public
