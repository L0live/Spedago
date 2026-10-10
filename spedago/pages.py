"""Spédago — assemblage des pages autonomes (gabarit + données JSON intégrées)."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path


def embed_json(data) -> str:
    """JSON compact sûr dans une balise <script> (pas de « </ » littéral)."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# Le site : une page d'accueil, deux portes d'entrée (élèves, décideurs). Nom de fichier, libellé, porte.
PAGES = [
    ("index.html", "Accueil", ""),
    ("mes-specialites.html", "Mes spécialités", "Élèves"),
    ("boussole-des-masters.html", "Boussole des masters", "Élèves"),
    ("mon-academie.html", "Mon académie", "Décideurs"),
    ("simulateur-parcoursup.html", "Simulateur des places", "Décideurs"),
    ("mutualisation.html", "Carte des spécialités", "Décideurs"),
]
COMMUN = Path(__file__).resolve().parent.parent / "app" / "_commun.html"


def _profil_panel() -> str:
    """Panneau « Mon profil » : réglages gardés dans le navigateur, lus par toutes les pages."""
    from .libelles import EDS, PROFILS_MASTER
    from .referentiel import ACADEMIES, cle, slug
    acads = sorted({v for v in ACADEMIES.values() if v != "Étranger"}, key=cle)
    opt = lambda v, t: f'<option value="{escape(v)}">{escape(t)}</option>'  # noqa: E731
    spe_opts = opt("", "—") + "".join(opt(i, lib) for i, lib, _, _ in EDS)
    return ('<div class="site-tools"><button type="button" id="copy-link">Copier le lien</button>'
            '<button type="button" id="profil-btn" aria-expanded="false" aria-controls="profil-panel"><span>Mon profil</span></button>'
            '<div id="profil-panel" hidden><form autocomplete="off">'
            '<label>Je suis<select name="role">' + opt("", "—") + opt("lyceen", "Lycéen·ne") + opt("etudiant", "Étudiant·e")
            + opt("decideur", "Décideur, élu, journaliste…") + '</select></label>'
            '<label>Mon académie<select name="academie">' + opt("", "—") + "".join(opt(slug(a), a) for a in acads) + '</select></label>'
            '<label>Mes études (masters)<select name="profilMaster">' + opt("", "—")
            + "".join(opt(k, v) for k, v in PROFILS_MASTER.items()) + '</select></label>'
            '<div class="row2"><label>Spécialité 1<select name="spe1">' + spe_opts + '</select></label>'
            '<label>Spécialité 2<select name="spe2">' + spe_opts + '</select></label></div>'
            '<p>Gardé dans ce navigateur seulement ; rien n\'est envoyé. Chaque page s\'ouvre sur ces réglages.</p>'
            '<div class="acts"><button type="button" data-reset>Effacer</button><button type="submit">Enregistrer</button></div>'
            '</form></div></div>')


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
            + '<span class="sep"></span>'.join(blocs) + _profil_panel() + "</nav>")


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
