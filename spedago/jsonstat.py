"""Spédago — lecture d'un jeu JSON-stat 2.0 (API Eurostat) en tableau : une ligne par cellule, valeur et statut (drapeau)."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import pandas as pd

# Drapeaux Eurostat les plus courants (liste officielle : « Eurostat flags »)
DRAPEAUX = {"b": "rupture de série", "d": "définition différente", "e": "estimé", "p": "provisoire", "u": "peu fiable",
            "c": "confidentiel", "m": "manquant", "z": "sans objet", "n": "non significatif", "r": "révisé", "s": "estimation Eurostat"}


def lire(path: Path) -> pd.DataFrame:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    ids, sizes = d["id"], d["size"]
    cats = []
    for k in ids:
        idx = d["dimension"][k]["category"]["index"]
        cats.append([c for c, _ in sorted(idx.items(), key=lambda t: t[1])] if isinstance(idx, dict) else list(idx))
    val, st = d.get("value", {}), d.get("status", {})
    rows = []
    for flat, combo in enumerate(itertools.product(*cats)):
        v, s = val.get(str(flat)), st.get(str(flat), "")
        if v is None and not s:
            continue
        rows.append((*combo, v, s))
    out = pd.DataFrame(rows, columns=[*ids, "valeur", "statut"])
    labels = d["dimension"].get("geo", {}).get("category", {}).get("label", {})
    if "geo" in out:
        out["geo_lib"] = out.geo.map(labels)
    return out
