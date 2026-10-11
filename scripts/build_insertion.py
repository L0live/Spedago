"""Spédago — insertion professionnelle des diplômés de master (InserSup), rattachée aux formations de Mon Master.

Usage : python3 scripts/build_insertion.py
Entrées : data/raw/insersup_master.csv (masters LMD, diplômés, tous publics), data/processed/monmaster_formations.csv
Sorties : data/processed/insertion_master.json, reports/insertion_master.md

Indicateur : part des diplômés sortants en emploi salarié en France 18 mois après le diplôme
(« tx_sortants_en_emploi_sal_fr_18 », InserSup). Pour chaque établissement × mention, on garde la promotion la
plus récente où l'indicateur est publié (une promotion seule ou le cumul de deux, quand l'effectif est petit).
Rattachement à Mon Master par (UAI de l'établissement, mention) ; InserSup donne deux UAI (établissement
et UAI FRESQ) : les deux sont essayés. Repère national par mention : moyenne pondérée par les sortants.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.paths import PROCESSED, RAW, REPORTS  # noqa: E402

OUT_JSON = PROCESSED / "insertion_master.json"
OUT_MD = REPORTS / "insertion_master.md"
MOIS = 18


def charge() -> pd.DataFrame:
    i = pd.read_csv(RAW / "insersup_master.csv", sep=";", low_memory=False, dtype={"promo": str})
    num = lambda s: pd.to_numeric(s.replace("nd", np.nan), errors="coerce")  # noqa: E731
    i["tx"] = num(i[f"tx_sortants_en_emploi_sal_fr_{MOIS}"]) / 100
    i["n"] = num(i[f"nb_sortants_{MOIS}"])
    i["sal"] = num(i[f"salaire_q2_{MOIS}"])
    i["fin"] = i.promo.str.split(",").map(lambda x: max(int(y) for y in x))
    i["cumul"] = i.promo.str.contains(",")
    return i[i.tx.notna() & (i.n > 0)]


def par_formation(i: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par (UAI, mention) : promotion la plus récente publiée ; à égalité, la promotion seule plutôt que le cumul."""
    rows = []
    for col in ("etablissement", "uai_fresq"):
        rows.append(i.assign(uai=i[col]))
    j = pd.concat(rows).drop_duplicates(["uai", "libelle_diplome", "promo"])
    j = j.sort_values(["uai", "libelle_diplome", "fin", "cumul"], ascending=[True, True, False, True])
    return j.groupby(["uai", "libelle_diplome"], as_index=False).first()


def build() -> dict:
    i = charge()
    f = par_formation(i)
    m = pd.read_csv(PROCESSED / "monmaster_formations.csv", sep=";", low_memory=False)
    m = m[m.profil == "lg3"].sort_values(["session", "ifc"], kind="mergesort").drop_duplicates("ifc", keep="last")[["ifc", "eta_uai", "mention"]]
    j = m.merge(f, left_on=["eta_uai", "mention"], right_on=["uai", "libelle_diplome"], how="left")
    # repère national par mention : diplômés en emploi / diplômés sortants, sur les lignes retenues (une par établissement)
    f["emploi"] = f.tx * f.n
    nat = f.drop_duplicates(["etablissement", "libelle_diplome"]).groupby("libelle_diplome")[["emploi", "n"]].sum()
    nat = (nat.emploi / nat.n).round(4)
    form = {str(r.ifc): [round(float(r.tx), 4), int(r.n), str(r.promo).replace(",", "-"), None if pd.isna(r.sal) else int(r.sal)]
            for r in j[j.tx.notna()].sort_values("ifc", kind="mergesort").itertuples()}  # ordre fixe : fichier identique d'une construction à l'autre
    return {"mois": MOIS, "formations": form, "mentions": {k: float(v) for k, v in sorted(nat.items())},
            "couverture": [int(j.tx.notna().sum()), int(len(j))]}


def main() -> None:
    D = build()
    OUT_JSON.write_text(json.dumps(D, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ok, tot = D["couverture"]
    OUT_MD.write_text(f"# Insertion des diplômés de master (InserSup)\n\nFormations Mon Master rattachées à un taux d'emploi salarié "
                      f"en France à {MOIS} mois : **{ok:,} sur {tot:,}** ({ok / tot:.0%}). Mentions avec un repère national : "
                      f"{len(D['mentions']):,}.\n", encoding="utf-8")
    print(f"{ok:,}/{tot:,} formations avec insertion -> {OUT_JSON}")


if __name__ == "__main__":
    main()
