"""Spédago — téléchargement reproductible des données ouvertes.

Usage :
  python3 scripts/download_data.py            # télécharge ce qui manque, puis écrit data/raw/MANIFEST.csv
  python3 scripts/download_data.py --force    # retélécharge tout
  python3 scripts/download_data.py --check    # vérifie les fichiers locaux contre MANIFEST.csv (empreintes SHA-256)

Source : API Explore v2.1 (OpenDataSoft) des portails ESR et Éducation nationale, export CSV « ; »,
noms de champs bruts (use_labels=false). Licence Ouverte 2.0.

Attention : `fr-esr-parcoursup` et `fr-esr-mon_master` sont des jeux « courants » qui seront
remplacés par la session suivante. Le MANIFEST garde l'empreinte de la version utilisée, et
`EXPECTED` contrôle que la session téléchargée est bien celle attendue.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "MANIFEST.csv"
ESR = "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets"
EDU = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets"

# fichier local -> (portail, identifiant du jeu)
DATASETS = {
    **{f"parcoursup_{y}": (ESR, f"fr-esr-parcoursup-{y}") for y in (2018, 2019)},
    **{f"parcoursup_{y}": (ESR, f"fr-esr-parcoursup_{y}") for y in range(2020, 2025)},
    "parcoursup_2025": (ESR, "fr-esr-parcoursup"),
    "parcoursup_apprentissage": (ESR, "fr-esr-parcoursup-apprentissage"),
    "parcoursup_specialites_v2": (ESR, "fr-esr-parcoursup-enseignements-de-specialite-bacheliers-generaux-2"),  # 2021-2024
    "parcoursup_specialites_v3": (ESR, "fr-esr-parcoursup-enseignements-de-specialite-bacheliers-generaux-3"),  # 2025
    "monmaster_2023": (ESR, "fr-esr-mon_master_2023"),
    "monmaster_2024_2025": (ESR, "fr-esr-mon_master"),
    "specialites_triplettes_1ere": (EDU, "fr-en-effectifs-specialites-triplettes-1ere-generale"),
    "specialites_doublettes_tle": (EDU, "fr-en-effectifs-specialites-doublettes-terminale-generale"),
    "ips_lycees_2016_2022": (EDU, "fr-en-ips_lycees"),
    "ips_lycees_ap2023": (EDU, "fr-en-ips-lycees-ap2023"),
    "eloignement_lycees": (EDU, "fr-en-indice_eloignement_lycee_ap2020"),
    "remplacement_2nd_degre": (EDU, "fr-en-remplacement-second-degre"),
    # InserSup : masters LMD, diplômés, tous publics confondus (une ligne par établissement × mention × promotion)
    "insersup_master": (ESR, "fr-esr-insersup",
                        "select=uo_lib,etablissement,uai_fresq,aca_nom,libelle_diplome,discipli_lib,promo,source,"
                        "nb_sortants_12,nb_sortants_18,nb_sortants_30,nb_sortants_en_emploi_sal_fr_12,nb_sortants_en_emploi_sal_fr_18,"
                        "nb_sortants_en_emploi_sal_fr_30,tx_sortants_en_emploi_sal_fr_12,tx_sortants_en_emploi_sal_fr_18,"
                        "tx_sortants_en_emploi_sal_fr_30,tx_sortants_en_emploi_stable_18,salaire_q2_18,salaire_q2_30,diplome"
                        "&where=type_diplome_long%3D%22Master%20LMD%22%20and%20genre%3D%22ensemble%22%20and%20nationalite%3D%22ensemble%22"
                        "%20and%20regime_inscription%3D%22ensemble%22%20and%20obtention_diplome%3D%22dipl%C3%B4m%C3%A9%22"),
    # Poursuite d'études des bacheliers par académie (SIES) ; résultats des lycées GT (IVAL)
    "poursuite_academie": (ESR, "fr-esr-taux-poursuite-enseignement-superieur-par-academie"),
    "ival_lycees_gt": (EDU, "fr-en-indicateurs-de-resultat-des-lycees-gt_v2"),
    # Annuaire : lycées seulement, colonnes utiles (coordonnées, bassin de formation, statut)
    "annuaire_lycees": (EDU, "fr-en-annuaire-education",
                        "select=identifiant_de_l_etablissement,nom_etablissement,statut_public_prive,nom_commune,"
                        "code_departement,libelle_academie,code_bassin_formation,libelle_bassin_formation,"
                        "latitude,longitude,etat,voie_generale,code_nature,libelle_nature"
                        "&where=type_etablissement%3D%22Lyc%C3%A9e%22"),
}
# Contrôles de contenu pour les jeux « courants » (colonne, valeurs attendues)
EXPECTED = {"parcoursup_2025": ("session", {"2025"}), "monmaster_2024_2025": ("session", {"2024", "2025"})}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(name: str, force: bool) -> Path:
    base, ds, *extra = DATASETS[name]
    path = RAW / f"{name}.csv"
    if path.exists() and path.stat().st_size > 0 and not force:
        return path
    url = f"{base}/{ds}/exports/csv?delimiter=%3B&use_labels=false" + (f"&{extra[0]}" if extra else "")
    tmp = path.with_suffix(".part")
    with urllib.request.urlopen(url, timeout=600) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    tmp.replace(path)
    return path


def check_content(name: str, path: Path) -> None:
    if name in EXPECTED:
        col, vals = EXPECTED[name]
        got = set(pd.read_csv(path, sep=";", usecols=[col], dtype=str)[col].dropna().unique())
        if got != vals:
            raise SystemExit(f"{name} : {col} = {sorted(got)} au lieu de {sorted(vals)} — le jeu courant a changé de session.")


def write_manifest() -> None:
    rows = []
    for name, (base, ds, *_) in DATASETS.items():
        p = RAW / f"{name}.csv"
        n = len(pd.read_csv(p, sep=";", low_memory=False, dtype=str))  # lignes de données (champs multilignes gérés)
        rows.append({"fichier": p.name, "jeu": ds, "portail": base.split("/")[2], "lignes": n,
                     "sha256": sha256(p), "telecharge_le": date.fromtimestamp(p.stat().st_mtime).isoformat()})
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def check_manifest() -> int:
    bad = 0
    for r in csv.DictReader(open(MANIFEST, encoding="utf-8")):
        p = RAW / r["fichier"]
        ok = p.exists() and sha256(p) == r["sha256"]
        bad += not ok
        print(("OK " if ok else "DIFFÉRENT ") + r["fichier"])
    return bad


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        sys.exit(1 if check_manifest() else 0)
    RAW.mkdir(parents=True, exist_ok=True)
    for name in DATASETS:
        p = download(name, a.force)
        check_content(name, p)
        print(f"OK {p.name}")
    write_manifest()
    print(f"-> {MANIFEST}")


if __name__ == "__main__":
    main()
