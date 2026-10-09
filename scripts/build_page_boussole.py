"""Spédago — piste C : assemble la page « Boussole des masters » (HTML autonome, données intégrées).

Usage : python3 scripts/build_page_boussole.py
Entrées : app/boussole_template.html, data/processed/monmaster_simulateur.json (build_monmaster.py)
Sortie  : app/boussole-des-masters.html  (contenu de page sans <html>/<head>/<body> : format de publication Artifact)
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "app" / "boussole_template.html"
DATA = ROOT / "data" / "processed" / "monmaster_simulateur.json"
OUT = ROOT / "app" / "boussole-des-masters.html"

if __name__ == "__main__":
    d = json.loads(DATA.read_text(encoding="utf-8"))
    raw = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")  # pas de </script> dans les données
    OUT.write_text(TPL.read_text(encoding="utf-8").replace("__DATA__", raw), encoding="utf-8")
    print(f"-> {OUT} ({OUT.stat().st_size / 1e6:.1f} Mo)")
