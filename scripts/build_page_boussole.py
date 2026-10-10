"""Spédago — piste C : données de la page « Boussole des masters ».

Usage : python3 scripts/build_page_boussole.py
Entrées : data/processed/monmaster_simulateur.json (build_monmaster.py)
Sortie  : web/public/data/boussole.json (données de la page « Boussole des masters »)
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # paquet spedago
from spedago.pages import export_web  # noqa: E402

DATA = ROOT / "data" / "processed" / "monmaster_simulateur.json"

INSERTION = ROOT / "data" / "processed" / "insertion_master.json"


def avec_insertion(D: dict) -> dict:
    """Ajoute l'insertion InserSup (scripts/build_insertion.py) : par formation (ifc) et repère par mention (indice)."""
    if not INSERTION.exists():
        return D
    I = json.loads(INSERTION.read_text(encoding="utf-8"))
    idx = {m: i for i, m in enumerate(D["mentions"])}
    D["insertion"] = {"mois": I["mois"], "formations": I["formations"],
                      "mentions": {str(idx[m]): v for m, v in I["mentions"].items() if m in idx}}
    return D


if __name__ == "__main__":
    print(f"-> {export_web('boussole', avec_insertion(json.loads(DATA.read_text(encoding='utf-8'))))}")
