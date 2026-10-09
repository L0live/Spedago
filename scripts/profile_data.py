"""Spédago — profilage des jeux de données ouverts (pistes A, B, C).

Usage : python3 scripts/profile_data.py
Lit tous les CSV de data/raw/, écrit un rapport par fichier dans reports/profiling/
et un rapport de synthèse reports/profiling/_synthese.md (clés de jointure UAI, années).
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "reports" / "profiling"

UAI_RE = re.compile(r"^\d{7}[A-Z]$")
YEAR_HINTS = ("session", "annee", "année", "rentree", "rentrée", "year")


def read_any(path: Path) -> pd.DataFrame:
    """Lecture robuste : détecte séparateur et encodage."""
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(path, encoding=enc, newline="") as f:
                sample = f.read(50_000)
            sep = csv.Sniffer().sniff(sample, delimiters=";,\t|").delimiter
            return pd.read_csv(path, sep=sep, encoding=enc, low_memory=False)
        except (UnicodeDecodeError, csv.Error):
            continue
    raise ValueError(f"Lecture impossible : {path.name}")


def uai_columns(df: pd.DataFrame) -> list[str]:
    cols = []
    for c in df.columns:
        s = df[c].dropna().astype(str).str.strip().str.upper()
        if len(s) and s.head(500).map(lambda v: bool(UAI_RE.match(v))).mean() > 0.9:
            cols.append(c)
    return cols


def year_columns(df: pd.DataFrame) -> dict[str, list]:
    out = {}
    for c in df.columns:
        if any(h in c.lower() for h in YEAR_HINTS):
            vals = sorted(df[c].dropna().astype(str).unique().tolist())
            out[c] = vals[:30]
    return out


def profile(path: Path) -> dict:
    df = read_any(path)
    n = len(df)
    lines = [f"# {path.name}", "", f"- Lignes : **{n:,}**", f"- Colonnes : **{df.shape[1]}**"]

    uais = uai_columns(df)
    years = year_columns(df)
    lines.append(f"- Colonnes UAI détectées : {uais or 'aucune'}")
    for c, v in years.items():
        lines.append(f"- Valeurs de `{c}` : {v}")
    dup = df.duplicated().sum()
    lines.append(f"- Lignes dupliquées : {dup}")
    for c in uais:
        lines.append(f"- Doublons sur `{c}` : {df[c].duplicated().sum()} (attendu > 0 si plusieurs années/formations par UAI)")

    lines += ["", "| Colonne | Type | % manquant | Nb distincts | Min | Max | Exemples |", "|---|---|---|---|---|---|---|"]
    for c in df.columns:
        s = df[c]
        miss = s.isna().mean() * 100
        nun = s.nunique(dropna=True)
        num = pd.to_numeric(s, errors="coerce")
        is_num = num.notna().sum() >= 0.9 * s.notna().sum() and s.notna().any()
        mn = f"{num.min():.4g}" if is_num else ""
        mx = f"{num.max():.4g}" if is_num else ""
        ex = ", ".join(map(str, s.dropna().astype(str).unique()[:3]))[:80].replace("|", "/")
        lines.append(f"| `{c}` | {'num' if is_num else 'txt'} | {miss:.1f} | {nun} | {mn} | {mx} | {ex} |")

    # Alertes de qualité
    alerts = []
    for c in df.columns:
        num = pd.to_numeric(df[c], errors="coerce")
        if num.notna().any() and (num < 0).any():
            alerts.append(f"valeurs négatives dans `{c}`")
        if df[c].isna().mean() > 0.5:
            alerts.append(f"`{c}` manquant à plus de 50 %")
    lines += ["", "## Alertes", *(f"- {a}" for a in alerts or ["aucune"])]

    (OUT / f"{path.stem}.md").write_text("\n".join(lines), encoding="utf-8")
    return {"file": path.name, "rows": n, "cols": df.shape[1], "uai": uais,
            "uai_sets": {c: set(df[c].dropna().astype(str).str.upper()) for c in uais},
            "years": years}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(RAW.glob("*.csv"))
    if not files:
        sys.exit(f"Aucun CSV dans {RAW}")
    results = []
    for f in files:
        try:
            results.append(profile(f))
            print(f"OK  {f.name}")
        except Exception as e:  # noqa: BLE001
            print(f"ERR {f.name}: {e}")

    syn = ["# Synthèse du profilage", "", "| Fichier | Lignes | Colonnes | Colonnes UAI | Années |", "|---|---|---|---|---|"]
    for r in results:
        yrs = "; ".join(f"{k}: {v[0]}…{v[-1]}" for k, v in r["years"].items() if v)
        syn.append(f"| {r['file']} | {r['rows']:,} | {r['cols']} | {', '.join(r['uai']) or '—'} | {yrs or '—'} |")

    # Recouvrement des UAI entre fichiers (faisabilité des jointures)
    keyed = [(r["file"], s) for r in results for s in r["uai_sets"].values()]
    if len(keyed) > 1:
        syn += ["", "## Recouvrement des UAI (jointures)", "", "| A | B | UAI communs | % de A | % de B |", "|---|---|---|---|---|"]
        for i in range(len(keyed)):
            for j in range(i + 1, len(keyed)):
                (fa, a), (fb, b) = keyed[i], keyed[j]
                inter = len(a & b)
                syn.append(f"| {fa} | {fb} | {inter} | {inter / max(len(a), 1):.0%} | {inter / max(len(b), 1):.0%} |")
    (OUT / "_synthese.md").write_text("\n".join(syn), encoding="utf-8")
    print(f"Rapports : {OUT}")


if __name__ == "__main__":
    main()
