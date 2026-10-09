"""Spédago — écritures déterministes (mêmes octets à chaque exécution)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def to_csv_gz(df: pd.DataFrame, path: Path, **kw) -> None:
    """CSV compressé gzip SANS horodatage dans l'en-tête (mtime=0) : le fichier ne change que si les données changent."""
    df.to_csv(path, compression={"method": "gzip", "mtime": 0}, **kw)
