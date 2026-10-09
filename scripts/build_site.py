"""Spédago — niveau 3 : le site (accueil + 4 outils, deux portes d'entrée).

Usage : python3 scripts/build_site.py   (après les scripts build_* des pages)
Sorties : app/index.html (fragment, format de publication de la page principale)
          site/*.html    (documents complets, à ouvrir localement ou à publier comme pages annexes)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.pages import PAGES, build_page, document  # noqa: E402
from spedago.paths import APP, PROCESSED, ROOT  # noqa: E402

SITE = ROOT / "site"


def main() -> None:
    acad = json.loads((PROCESSED / "mon_academie.json").read_text(encoding="utf-8"))["academies"]
    build_page(APP / "index_template.html", APP / "index.html", [[a["nom"], a["slug"]] for a in acad])
    SITE.mkdir(exist_ok=True)
    for f, _, _ in PAGES:
        src = APP / f
        if not src.exists():
            raise SystemExit(f"page manquante : {src} (lancer d'abord les scripts build_*)")
        (SITE / f).write_text(document(src.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{len(PAGES)} pages -> {SITE}")


if __name__ == "__main__":
    main()
