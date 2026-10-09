"""Spédago — assemblage des pages autonomes (gabarit + données JSON intégrées)."""
from __future__ import annotations

import json
from pathlib import Path


def embed_json(data) -> str:
    """JSON compact sûr dans une balise <script> (pas de « </ » littéral)."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def build_page(template: Path, out: Path, data, replacements: dict[str, str] | None = None) -> Path:
    """Remplace __DATA__ (et les jetons __X__ fournis) dans le gabarit, écrit la page, la renvoie."""
    page = template.read_text(encoding="utf-8")
    for k, v in (replacements or {}).items():
        page = page.replace(k, v)
    out.write_text(page.replace("__DATA__", embed_json(data)), encoding="utf-8")
    return out
