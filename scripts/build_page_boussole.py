"""Spédago — piste C : assemble la page « Boussole des masters » (HTML autonome, données intégrées).

Usage : python3 scripts/build_page_boussole.py
Entrées : app/boussole_template.html, data/processed/monmaster_simulateur.json (build_monmaster.py)
Sortie  : app/boussole-des-masters.html  (contenu de page sans <html>/<head>/<body> : format de publication Artifact)
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # paquet spedago
from spedago.pages import build_page  # noqa: E402

TPL = ROOT / "app" / "boussole_template.html"
DATA = ROOT / "data" / "processed" / "monmaster_simulateur.json"
OUT = ROOT / "app" / "boussole-des-masters.html"

if __name__ == "__main__":
    build_page(TPL, OUT, json.loads(DATA.read_text(encoding="utf-8")))
    print(f"-> {OUT} ({OUT.stat().st_size / 1e6:.1f} Mo)")
