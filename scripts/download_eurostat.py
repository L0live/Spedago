"""Spédago — téléchargement des indicateurs Eurostat (API de diffusion, JSON-stat 2.0), pour la page « France et voisins ».

Usage : python3 scripts/download_eurostat.py [--force]
Sorties : data/raw/eurostat_<nom>.json + data/raw/MANIFEST_eurostat.csv (empreintes SHA-256, date de téléchargement)
Licence : réutilisation libre avec mention de la source (politique de droits d'auteur d'Eurostat).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.telechargement import telecharger, verifier_json  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
REQUETES = {
    # étudiants en mobilité diplômante, par pays d'accueil (geo) et pays d'origine (partner)
    "mobilite_francais_etranger": "educ_uoe_mobs02?partner=FR&isced11=ED5-8&isced11=ED5&isced11=ED6&isced11=ED7&isced11=ED8&sex=T&unit=NR&sinceTimePeriod=2013",
    "mobilite_etrangers_france": "educ_uoe_mobs02?geo=FR&isced11=ED5-8&sex=T&unit=NR&sinceTimePeriod=2013",
    # indicateurs régionaux (NUTS 2) et nationaux, enquête Forces de travail
    "diplomes_sup_25_34": "edat_lfse_04?age=Y25-34&isced11=ED5-8&sex=T&unit=PC&sinceTimePeriod=2015",
    "sorties_precoces_18_24": "edat_lfse_16?sex=T&unit=PC&sinceTimePeriod=2015",
    "neet_15_29": "edat_lfse_22?age=Y15-29&sex=T&unit=PC&sinceTimePeriod=2015",
}


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--force", action="store_true"); a = ap.parse_args()
    rows = []
    for nom, q in REQUETES.items():
        p = RAW / f"eurostat_{nom}.json"
        if a.force or not p.exists():
            # gzip décompressé, JSON contrôlé, trois essais ; puis réécriture compacte (forme des empreintes du MANIFEST)
            telecharger(f"{API}/{q}", p, verifier_json, timeout=300)
            p.write_text(json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False), encoding="utf-8")
        d = json.loads(p.read_text(encoding="utf-8"))
        rows.append([p.name, q, hashlib.sha256(p.read_bytes()).hexdigest(), d.get("updated", ""), str(date.today())])
        print(f"{p.name} : {len(d['value'])} valeurs, mis à jour {d.get('updated')}")
    with open(RAW / "MANIFEST_eurostat.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["fichier", "requete", "sha256", "maj_eurostat", "telecharge_le"]); w.writerows(rows)


if __name__ == "__main__":
    main()
