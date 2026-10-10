"""Spédago — assemblage des pages autonomes (gabarit + données JSON intégrées)."""
from __future__ import annotations

import json
from pathlib import Path


def embed_json(data) -> str:
    """JSON compact sûr dans une balise <script> (pas de « </ » littéral)."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# Le site : une page d'accueil, deux portes d'entrée (élèves, décideurs). Nom de fichier, libellé, porte.
PAGES = [
    ("index.html", "Accueil", ""),
    ("boussole-des-masters.html", "Boussole des masters", "Élèves"),
    ("mon-academie.html", "Mon académie", "Décideurs"),
    ("simulateur-parcoursup.html", "Simulateur des places", "Décideurs"),
    ("mutualisation.html", "Carte des spécialités", "Décideurs"),
]
COMMUN = Path(__file__).resolve().parent.parent / "app" / "_commun.html"


def nav(current: str) -> str:
    """Barre de navigation commune ; la page courante porte aria-current. Les liens gardent le #académie (JS)."""
    portes: dict[str, list[str]] = {}
    for f, lib, porte in PAGES:
        if porte:
            cur = ' aria-current="page"' if f == current else ""
            portes.setdefault(porte, []).append(f'<a href="{f}" data-page="{f}"{cur}>{lib}</a>')
    blocs = [f'<div class="door"><span>{p}</span>{"".join(liens)}</div>' for p, liens in portes.items()]
    cur = ' aria-current="page"' if current == "index.html" else ""
    return ('<a class="skip" href="#contenu">Aller au contenu</a>'
            '<div class="sr-only" role="status" aria-live="polite" id="sr-status"></div>'
            f'<nav class="site-nav" aria-label="Spédago"><a class="brand" href="index.html" data-page="index.html"{cur}>Spédago</a>'
            + '<span class="sep"></span>'.join(blocs) + "</nav>")


def document(fragment: str, title_fallback: str = "Spédago") -> str:
    """Document HTML complet autour d'un fragment de page (pour les pages annexes et l'usage local)."""
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body>\n'
            + fragment + "\n</body>\n</html>\n")


def build_page(template: Path, out: Path, data, replacements: dict[str, str] | None = None) -> Path:
    """Remplace __DATA__, __COMMUN__ (styles et script communs), __NAV__ (barre du site) et les jetons
    __X__ fournis dans le gabarit, écrit la page (fragment, format de publication), la renvoie."""
    page = template.read_text(encoding="utf-8")
    page = page.replace("__COMMUN__", COMMUN.read_text(encoding="utf-8").strip()).replace("__NAV__", nav(out.name))
    for k, v in (replacements or {}).items():
        page = page.replace(k, v)
    out.write_text(page.replace("__DATA__", embed_json(data)), encoding="utf-8")
    return out
