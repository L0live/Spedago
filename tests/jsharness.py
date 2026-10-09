"""Harnais commun des tests de pages : extrait le bloc <script id="calc"> et les données d'une page construite."""
from __future__ import annotations

import re


def extract_page(html: str) -> tuple[str, str]:
    """Retourne (code JS de calcul, texte JSON des données) d'une page Spédago."""
    calc = re.search(r'<script id="calc">(.*?)</script>', html, re.S).group(1)
    data = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S).group(1).replace("<\\/", "</")
    return calc, data
