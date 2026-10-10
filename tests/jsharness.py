"""Harnais commun des tests de l'application web (web/) : calculs TypeScript compilés pour Node, données publiées, pages construites.

Les modules de calcul (web/src/calc/*.ts) sont ceux que les pages exécutent. Ils sont compilés ici avec esbuild
en CommonJS dont `module.exports` est l'objet de calcul, pour que les tests les appellent depuis Node.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
DATA = WEB / "public" / "data"
DIST = WEB / "dist"
ESBUILD = WEB / "node_modules" / ".bin" / "esbuild"

# page -> (module de calcul, objet exporté, fichier de données)
CALCS = {
    "boussole-des-masters": ("src/calc/boussole.ts", "BoussoleCalc", "boussole"),
    "simulateur-parcoursup": ("src/calc/simulateur.ts", "SimCalc", "simulateur"),
    "mutualisation": ("src/calc/mutualisation.ts", "MutCalc", "mutualisation"),
    "mon-academie": ("src/calc/mon-academie.ts", "AcadCalc", "mon_academie"),
    "mes-specialites": ("src/calc/mes-specialites.ts", "SpeCalc", "mes_specialites"),
    "france-et-voisins": ("src/calc/voisins.ts", "VoisinsCalc", "voisins"),
    "commun": ("src/lib/commun.ts", "Spedago", None),
}


def disponible() -> bool:
    """Node, esbuild (npm install dans web/) et les données publiées sont présents."""
    return shutil.which("node") is not None and ESBUILD.exists() and DATA.exists()


@lru_cache(maxsize=None)
def compile_calc(page: str) -> str:
    """Code CommonJS du calcul d'une page ; `require()` renvoie directement l'objet de calcul."""
    src, export, _ = CALCS[page]
    r = subprocess.run([str(ESBUILD), src, "--bundle", "--format=cjs", "--platform=node", "--log-level=error"],
                       cwd=WEB, capture_output=True, text=True, check=True)
    return r.stdout + f"\nmodule.exports = module.exports.{export};\n"


def data_text(page: str) -> str:
    return (DATA / f"{CALCS[page][2]}.json").read_text(encoding="utf-8")


def extract_page(page: str) -> tuple[str, str]:
    """(code JS du calcul, texte JSON des données) d'une page de l'application."""
    return compile_calc(page), data_text(page)


def built_html(page: str) -> str:
    p = DIST / f"{page}.html"
    if not p.exists():
        raise FileNotFoundError(f"{p} absent : lancer `npm run build` dans web/")
    return p.read_text(encoding="utf-8")


def data_json(name: str):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))
