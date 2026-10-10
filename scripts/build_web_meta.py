"""Spédago — éléments communs de l'application web : navigation, pied de page, accueil, page « Méthodes ».

Usage : python3 scripts/build_web_meta.py   (après les scripts build_* ; puis `npm run build` dans web/)
Sorties : web/generated/nav.json, web/generated/pied.html, web/public/data/index.json, web/public/data/methodes.json
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.indicateurs import INDICATEURS, par_id  # noqa: E402
from spedago.pages import PAGES, export_nav, export_web  # noqa: E402
from spedago.paths import PROCESSED  # noqa: E402

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def sources() -> dict[str, dict]:
    """Fichiers bruts du MANIFEST : jeu, producteur, lien vers la fiche du jeu, date de téléchargement, empreinte."""
    out: dict[str, dict] = {}
    with open(RAW / "MANIFEST.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            producteur = ("Ministère de l'Enseignement supérieur (MESR-SIES)" if "enseignementsup" in r["portail"]
                          else "Ministère de l'Éducation nationale (DEPP)")
            out[r["fichier"]] = {"jeu": r["jeu"], "producteur": producteur, "url": f"https://{r['portail']}/explore/dataset/{r['jeu']}/",
                                 "telecharge_le": r["telecharge_le"], "sha256": r["sha256"], "lignes": int(r["lignes"])}
    with open(RAW / "MANIFEST_eurostat.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            code = r["requete"].split("?")[0]
            out[r["fichier"]] = {"jeu": code, "producteur": "Eurostat", "url": f"https://ec.europa.eu/eurostat/databrowser/view/{code}/default/table",
                                 "requete": r["requete"], "maj_producteur": r["maj_eurostat"][:10],
                                 "telecharge_le": r["telecharge_le"], "sha256": r["sha256"]}
    return out


def methodes() -> dict:
    src = sources()
    manquants = sorted({s for i in INDICATEURS for s in i.sources} - set(src))
    if manquants:
        raise SystemExit(f"sources absentes du MANIFEST : {manquants}")
    utiles = sorted({s for i in INDICATEURS for s in i.sources})
    return {"indicateurs": [i.to_json() for i in INDICATEURS], "sources": {s: src[s] for s in utiles},
            "pages": {f: lib for f, lib, _ in PAGES}}


def main() -> None:
    M = json.loads((PROCESSED / "mon_academie.json").read_text(encoding="utf-8"))
    fr = M["france"]
    ind = par_id()
    # [valeur, libellé, champ, fiche méthodologique] : chaque chiffre de l'accueil dit d'où il vient
    chiffres = [[fr["ps"]["total"][0], f"formations Parcoursup {M['session']}", "hors CNED et capacités nulles", "ps-pression"],
                [fr["spe"]["lycees"], f"lycées avec une 1re générale (rentrée {M['rentree']})", "géolocalisés dans l'annuaire", "spe-offre"],
                [fr["mm"]["total"][0], f"masters sur Mon Master {M['session']}", "toutes mentions", "mm-proposition"]]
    assert all(c[3] in ind for c in chiffres)
    export_web("index", {"academies": [[a["nom"], a["slug"]] for a in M["academies"]], "chiffres": chiffres})
    print(f"-> {export_web('methodes', methodes())}")
    print(f"-> {export_nav()}")


if __name__ == "__main__":
    main()
