"""Tests du paquet commun spedago/ : les scripts utilisent bien les mêmes fonctions, écritures déterministes."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from spedago import geo, io, pages, stats  # noqa: E402


def test_une_seule_implementation_partagee():
    import build_indice_specialites as b
    import build_monmaster as mm
    import build_mutualisation as mu
    import build_parcoursup_panel as bp
    import robustesse_piste_b as rb
    assert mm.wilson is stats.wilson and mm.shrink is stats.shrink and mm._moments is stats._moments
    assert b.ols is stats.ols and rb.ols_cluster is stats.ols_cluster and bp.ratio is stats.ratio
    assert mu.haversine_matrix is geo.haversine_matrix


def test_csv_gz_deterministe(tmp_path):
    df = pd.DataFrame({"a": range(100), "b": ["x"] * 100})
    io.to_csv_gz(df, tmp_path / "1.csv.gz", index=False)
    io.to_csv_gz(df, tmp_path / "2.csv.gz", index=False)
    h = [hashlib.sha256((tmp_path / f).read_bytes()).hexdigest() for f in ("1.csv.gz", "2.csv.gz")]
    assert h[0] == h[1]
    assert pd.read_csv(tmp_path / "1.csv.gz").equals(df)


def test_export_web_deterministe(tmp_path, monkeypatch):
    monkeypatch.setattr(pages, "WEB_DATA", tmp_path)
    a = pages.export_web("t", {"txt": "</script><b>", "x": [1, 2.5, None]}).read_bytes()
    b = pages.export_web("t", {"txt": "</script><b>", "x": [1, 2.5, None]}).read_bytes()
    assert a == b and a == '{"txt":"</script><b>","x":[1,2.5,null]}'.encode()
