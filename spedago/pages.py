"""Spédago — liaison avec l'application web (web/) : navigation commune, export des données des pages."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path


# Le site : une page d'accueil, deux portes d'entrée (élèves, décideurs). Nom de fichier, libellé, porte.
PAGES = [
    ("index.html", "Accueil", ""),
    ("mes-specialites.html", "Mes spécialités", "Élèves"),
    ("boussole-des-masters.html", "Boussole des masters", "Élèves"),
    ("mon-academie.html", "Mon académie", "Décideurs"),
    ("simulateur-parcoursup.html", "Simulateur des places", "Décideurs"),
    ("mutualisation.html", "Carte des spécialités", "Décideurs"),
    ("france-et-voisins.html", "France et voisins", "Décideurs"),
    ("methodes.html", "Méthodes et sources", ""),  # lien en pied de page, hors barre de navigation
]
ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
WEB_DATA = WEB / "public" / "data"


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
    """Barre de navigation commune ; la page courante porte aria-current. Les liens gardent le #académie (JS).
    Sur téléphone, les portes et les outils se replient derrière le bouton « Menu » (commun.ts) ; sans JavaScript, tout reste visible."""
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
            '<button type="button" class="nav-toggle" aria-expanded="true" aria-controls="nav-menu" hidden>Menu</button>'
            '<div class="nav-menu" id="nav-menu">' + '<span class="sep"></span>'.join(blocs) + _profil_panel() + "</div></nav>")


def export_web(name: str, data) -> Path:
    """Écrit les données d'une page de l'application web : web/public/data/<name>.json (compact, déterministe)."""
    WEB_DATA.mkdir(parents=True, exist_ok=True)
    out = WEB_DATA / f"{name}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return out


def pied() -> str:
    """Mentions communes du pied de page : méthodes, licences (code AGPL-3.0, données Licence Ouverte 2.0)."""
    return ('<p class="pied-commun"><a href="methodes.html">Méthodes et sources</a> · '
            '<a href="https://github.com/L0live/Spedago">Code source</a> sous licence <a href="https://www.gnu.org/licenses/agpl-3.0.html" hreflang="en">GNU AGPL-3.0</a> · '
            'Données et textes sous <a href="https://www.etalab.gouv.fr/licence-ouverte-open-licence/">Licence Ouverte 2.0</a>, '
            'mention « Spédago, d\'après [producteur], [date] » · Aucun compte, aucun traceur.</p>')


def export_nav() -> Path:
    """Barre de navigation de chaque page et pied de page commun (insérés au build par vite.config.ts)."""
    out = WEB / "generated" / "nav.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({f: nav(f) for f, _, _ in PAGES}, ensure_ascii=False, indent=1), encoding="utf-8")
    (out.parent / "pied.html").write_text(pied(), encoding="utf-8")
    return out
