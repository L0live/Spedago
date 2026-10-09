"""Spédago — géographie."""
from __future__ import annotations

import numpy as np

EARTH_KM = 6371.0


def haversine_matrix(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    la, lo = np.radians(lat)[:, None], np.radians(lon)[:, None]
    dlat, dlon = la - la.T, lo - lo.T
    h = np.sin(dlat / 2) ** 2 + np.cos(la) * np.cos(la.T) * np.sin(dlon / 2) ** 2
    return 2 * EARTH_KM * np.arcsin(np.sqrt(np.clip(h, 0, 1)))
