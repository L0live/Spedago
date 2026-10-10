"""Registre des indicateurs (page « Méthodes ») : les fiches ne doivent pas dériver des calculs."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

from spedago.indicateurs import INDICATEURS
from spedago.pages import PAGES, WEB_DATA

ROOT = Path(__file__).resolve().parent.parent


def _module(nom: str):
    spec = importlib.util.spec_from_file_location(f"_script_{nom}", ROOT / "scripts" / f"{nom}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)  # les scripts n'exécutent rien hors de main()
    return m


def test_identifiants_uniques():
    ids = [i.id for i in INDICATEURS]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("i,s", [(i, s) for i in INDICATEURS for s in i.seuils if s.module],
                         ids=lambda x: getattr(x, "id", getattr(x, "constante", "")))
def test_seuil_identique_au_script(i, s):
    assert getattr(_module(s.module), s.constante) == s.valeur, f"{i.id} : {s.libelle}"


def test_sources_dans_le_manifest():
    with open(ROOT / "data/raw/MANIFEST.csv", encoding="utf-8") as f:
        connus = {r["fichier"] for r in csv.DictReader(f)}
    with open(ROOT / "data/raw/MANIFEST_eurostat.csv", encoding="utf-8") as f:
        connus |= {r["fichier"] for r in csv.DictReader(f, delimiter=";")}
    for i in INDICATEURS:
        assert set(i.sources) <= connus, i.id


def test_pages_et_rapports_existent():
    pages = {f for f, _, _ in PAGES}
    for i in INDICATEURS:
        assert i.pages and set(i.pages) <= pages, i.id
        assert not i.rapport or (ROOT / "reports" / i.rapport).exists(), i.id
        assert i.definition and i.formule and i.champ and i.limites, i.id


def test_publication_a_jour():
    """methodes.json reflète le registre ; chaque chiffre de l'accueil renvoie à une fiche."""
    d = json.loads((WEB_DATA / "methodes.json").read_text(encoding="utf-8"))
    assert d["indicateurs"] == [i.to_json() for i in INDICATEURS]
    ids = {i.id for i in INDICATEURS}
    for c in json.loads((WEB_DATA / "index.json").read_text(encoding="utf-8"))["chiffres"]:
        assert c[3] in ids and c[2]
