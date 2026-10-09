"""Spédago — écritures déterministes (mêmes octets à chaque exécution)."""
from __future__ import annotations

import gzip
import io as _io
from pathlib import Path

import pandas as pd


def to_csv_gz(df: pd.DataFrame, path: Path, **kw) -> None:
    """CSV compressé gzip déterministe : en-tête sans date (mtime=0) ni nom de fichier.
    Le fichier ne change que si les données changent."""
    buf = _io.StringIO()
    df.to_csv(buf, **kw)
    with open(path, "wb") as raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
        gz.write(buf.getvalue().encode("utf-8"))
