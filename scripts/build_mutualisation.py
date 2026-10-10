"""Spédago — piste B : où des lycées voisins pourraient-ils partager une spécialité ?

Usage : python3 scripts/build_mutualisation.py
Entrées : data/raw/specialites_triplettes_1ere.csv (rentrée la plus récente), data/raw/annuaire_lycees.csv
Sorties : data/processed/mutualisation.json, data/processed/mutualisation_lycees.csv,
          reports/piste_B_mutualisation.md, web/public/data/mutualisation.json

Pour chaque spécialité et chaque lycée de 1re générale qui NE la propose PAS (effectifs explicitement à 0) :
  - « accès voisin »       : un lycée du même statut (public / privé) la propose (ou a des effectifs masqués,
                             donc probablement un petit groupe) à moins de R km ;
  - « ouverture commune »  : aucun lycée qui la propose à moins de R km, mais avec d'autres lycées voisins
                             qui ne la proposent pas non plus (≤ R km du lycée pivot), la demande estimée
                             atteint SEUIL élèves : un groupe commun serait envisageable ;
  - « isolé »              : ni l'un ni l'autre.
Demande estimée d'un lycée pour une spécialité = effectif de 1re × taux de choix national de la spécialité
dans les lycées qui la proposent (calculé sur les lycées où ses cases ne sont pas masquées).
Une case masquée (secret statistique) laisse le statut « incertain » : ces lycées ne sont pas comptés absents.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_indice_specialites as b  # noqa: E402  (appariement des colonnes filles / garçons)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # paquet spedago
from spedago.geo import EARTH_KM, haversine_matrix  # noqa: E402,F401
from spedago.pages import export_web  # noqa: E402
from spedago.libelles import SPECIALITES  # noqa: E402
from spedago.referentiel import academie_canonique  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT_JSON = ROOT / "data" / "processed" / "mutualisation.json"
OUT_CSV = ROOT / "data" / "processed" / "mutualisation_lycees.csv"
OUT_MD = ROOT / "reports" / "piste_B_mutualisation.md"

R_KM = 20.0
SEUIL = 12            # élèves : taille minimale d'un groupe de spécialité pour envisager une ouverture commune
MAX_MEMBRES = 4       # au-delà, un groupe commun n'est plus réaliste (horaires, transports)
MIN_LYCEES_OFFRE = 50  # spécialités proposées par moins de lycées (danse, cirque…) : hors champ


def specialty_status(t: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Statut par lycée × spécialité : 'o' proposée (≥ 1 élève visible), 'n' absente (zéros explicites),
    'm' incertaine (case masquée, rien de visible). Retourne aussi les effectifs visibles par spécialité."""
    spe, _ = b.column_groups(list(t.columns), "1re")
    names, status, counts = [], {}, {}
    for f, g in spe:
        name = f.split("_", 1)[1].removesuffix("_filles").rsplit("_filles", 1)[0]
        names.append(name)
        vf, vg = t[f], t[g]
        vis = vf.fillna(0) + vg.fillna(0)
        masked = vf.isna() | vg.isna()
        status[name] = np.where(vis > 0, "o", np.where(masked, "m", "n"))
        counts[name] = vis.where(~masked)  # effectif exact seulement si aucune case masquée
    return pd.DataFrame(status, index=t.index), pd.DataFrame(counts, index=t.index), names


def take_up_rates(status: pd.DataFrame, counts: pd.DataFrame, eff: pd.Series, offered_only: bool) -> pd.Series:
    """Part des élèves de 1re qui suivent la spécialité.
    offered_only=True  : dans les lycées qui la proposent (estimation HAUTE : ces lycées attirent les élèves intéressés,
                         notamment pour les spécialités artistiques à section dédiée).
    offered_only=False : tous lycées confondus, absents compris (estimation BASSE : l'absence d'offre réduit la demande).
    Seuls les lycées où les cases de la spécialité ne sont pas masquées entrent dans le calcul."""
    rates = {}
    for s in status.columns:
        ok = counts[s].notna() & ((status[s] == "o") if offered_only else True)
        rates[s] = counts.loc[ok, s].sum() / eff[ok].sum() if ok.any() else np.nan
    return pd.Series(rates)


def classify(lyc: pd.DataFrame, status: pd.DataFrame, rates: pd.Series, dist: np.ndarray,
             r_km: float = R_KM, seuil: float = SEUIL, max_membres: int = MAX_MEMBRES) -> tuple[pd.DataFrame, list[dict]]:
    """Catégorie de chaque couple (lycée absent, spécialité) + groupes d'ouverture commune (gloutons, disjoints)."""
    rows, groups = [], []
    same = lyc.statut.to_numpy()[:, None] == lyc.statut.to_numpy()[None, :]
    eff = lyc.effectif.to_numpy(float)
    for s in status.columns:
        st = status[s].to_numpy()
        # Offre pour les voisins : proposée OU masquée. Une case masquée cache presque toujours un petit groupe
        # (1 à 4 élèves par sexe) : ignorer ces lycées inventait des « isolés » à côté d'une offre réelle.
        offer, absent = (st == "o") | (st == "m"), st == "n"
        demand = eff * rates[s]
        d_off = np.where(same & offer[None, :], dist, np.inf)
        nearest = d_off.min(axis=1)
        nearest_idx = d_off.argmin(axis=1)
        voisin = absent & (nearest <= r_km)
        cand = absent & ~voisin
        # groupes : chaque candidat pivot réunit les candidats du même statut à ≤ R km ; on retient les groupes
        # qui atteignent le seuil, par demande décroissante, sans réutiliser un lycée.
        idx = np.flatnonzero(cand)
        options = []
        for i in idx:
            mem = idx[(dist[i, idx] <= r_km) & same[i, idx]]
            mem = mem[np.argsort(dist[i, mem], kind="stable")][:max_membres]   # le pivot (distance 0) et ses plus proches
            options.append((demand[mem].sum(), i, mem))
        used = np.zeros(len(lyc), bool)
        in_group = np.zeros(len(lyc), bool)
        for dem, i, mem in sorted(options, key=lambda x: (-x[0], x[1])):
            mem = mem[~used[mem]]
            if len(mem) < 2 or demand[mem].sum() < seuil:
                continue
            used[mem] = True
            in_group[mem] = True
            groups.append({"specialite": s, "pivot": int(i), "membres": [int(m) for m in mem],
                           "demande": float(demand[mem].sum()), "rayon_km": float(dist[i, mem].max())})
        cat = np.full(len(lyc), "", dtype=object)
        cat[voisin], cat[in_group], cat[cand & ~in_group] = "acces_voisin", "ouverture_commune", "isole"
        for i in np.flatnonzero(absent):
            rows.append({"uai": lyc.uai.iat[i], "specialite": s, "categorie": cat[i], "demande_estimee": demand[i],
                         "km_offre_la_plus_proche": None if np.isinf(nearest[i]) else float(nearest[i]),
                         "lycee_offre_le_plus_proche": None if np.isinf(nearest[i]) else lyc.uai.iat[nearest_idx[i]]})
    return pd.DataFrame(rows), groups


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[str], int]:
    t = pd.read_csv(RAW / "specialites_triplettes_1ere.csv", sep=";", low_memory=False)
    an = int(t.rentree_scolaire.max())
    t = t[(t.rentree_scolaire == an) & t.effectif_total.notna()].reset_index(drop=True)
    a = pd.read_csv(RAW / "annuaire_lycees.csv", sep=";", dtype=str)
    a = a.rename(columns={"identifiant_de_l_etablissement": "uai"}).drop_duplicates("uai")
    t = t.merge(a[["uai", "nom_etablissement", "nom_commune", "statut_public_prive", "libelle_academie",
                   "code_bassin_formation", "libelle_bassin_formation", "latitude", "longitude"]],
                left_on="numero_etablissement", right_on="uai", how="inner")
    t["latitude"], t["longitude"] = pd.to_numeric(t.latitude), pd.to_numeric(t.longitude)
    t = t[t.latitude.notna() & t.longitude.notna()].reset_index(drop=True)
    status, counts, names = specialty_status(t)
    lyc = pd.DataFrame({"uai": t.uai, "nom": t.nom_etablissement, "commune": t.nom_commune,
                        "statut": t.statut_public_prive, "academie": t.libelle_academie.map(academie_canonique),
                        "bassin": t.libelle_bassin_formation.fillna(""), "lat": t.latitude, "lon": t.longitude,
                        "effectif": t.effectif_total.astype(int)})
    return lyc, status, counts, names, an


def main() -> None:
    lyc, status, counts, names, an = load()
    rates = take_up_rates(status, counts, lyc.effectif, offered_only=False)        # estimation basse (par défaut)
    rates_hi = take_up_rates(status, counts, lyc.effectif, offered_only=True)      # estimation haute
    n_offre = (status == "o").sum()
    keep = [s for s in names if n_offre[s] >= MIN_LYCEES_OFFRE]
    status, rates, rates_hi = status[keep], rates[keep], rates_hi[keep]
    dist = haversine_matrix(lyc.lat.to_numpy(), lyc.lon.to_numpy())
    pairs, groups = classify(lyc, status, rates, dist)
    pairs_hi, groups_hi = classify(lyc, status, rates_hi, dist)
    pairs.to_csv(OUT_CSV, sep=";", index=False)

    # ---- rapport
    L = [f"# Piste B — mutualisation possible des spécialités (1re générale, rentrée {an})", "",
         f"{len(lyc):,} lycées géolocalisés (annuaire de l'Éducation nationale). Rayon {R_KM:.0f} km, même statut "
         f"(public avec public, privé avec privé), groupe commun de {MAX_MEMBRES} lycées au plus, envisageable dès {SEUIL} élèves estimés.", "",
         "Demande : estimation BASSE (part des élèves de 1re qui suivent la spécialité, tous lycées confondus) ; "
         "entre parenthèses, le nombre de lycées en ouverture commune avec l'estimation HAUTE (part observée là où elle est proposée).", "",
         "| Spécialité | Lycées qui la proposent | Absente (certain) | Incertaine (masquée) | Taux bas – haut | Accès voisin | Ouverture commune (haute) | Isolés | Élèves de 1re des lycées isolés |",
         "|---|---|---|---|---|---|---|---|---|"]
    for s in keep:
        p = pairs[pairs.specialite == s]
        ph = pairs_hi[pairs_hi.specialite == s]
        iso = p[p.categorie == "isole"].uai
        L.append(f"| {s} | {int((status[s] == 'o').sum())} | {int((status[s] == 'n').sum())} | {int((status[s] == 'm').sum())} | "
                 f"{rates[s]:.1%} – {rates_hi[s]:.1%} | {int((p.categorie == 'acces_voisin').sum())} | "
                 f"{int((p.categorie == 'ouverture_commune').sum())} ({int((ph.categorie == 'ouverture_commune').sum())}) | "
                 f"{len(iso)} | {int(lyc.set_index('uai').loc[iso, 'effectif'].sum()):,} |")
    G = pd.DataFrame(groups)
    if len(G):
        G["nb_lycees"] = G.membres.map(len)
        L += ["", f"## Groupes d'ouverture commune ({len(G)})", "",
              G.groupby("specialite").agg(groupes=("pivot", "size"), lycees=("nb_lycees", "sum"),
                                          eleves_estimes=("demande", "sum")).round(0).sort_values("groupes", ascending=False)
              .reset_index().to_markdown(index=False)]
    L += ["", "## Limites", "",
          "- Absent = zéros explicites ; une case masquée (moins de 5 élèves, ou secret secondaire) laisse le statut incertain "
          "pour le lycée lui-même, mais compte comme offre possible pour ses voisins.",
          "- Demande estimée = effectif × taux national (bas ou haut) : ignore les goûts locaux et l'IPS. Le taux bas sous-estime "
          "(l'absence d'offre supprime la demande), le taux haut surestime (les lycées qui proposent attirent les élèves intéressés).",
          "- Distance à vol d'oiseau, pas temps de transport. Un groupe commun suppose aussi un enseignant et des horaires alignés.",
          "- Un même lycée peut appartenir à des groupes de spécialités différentes ; les groupes sont choisis de façon gloutonne.",
          f"- Bassin de formation inconnu pour {lyc.bassin.eq('').mean():.0%} des lycées (surtout privés) : la distance remplace le bassin."]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")

    # ---- export pour la page
    code = {"o": 0, "n": 1, "m": 2}
    cat_code = {"acces_voisin": 3, "ouverture_commune": 4, "isole": 5}
    st = np.vectorize(code.get)(status.to_numpy()).astype(int)
    pos = {u: i for i, u in enumerate(lyc.uai)}
    for u, s_, c in zip(pairs.uai, pairs.specialite, pairs.categorie):   # remplace « absente » par sa catégorie
        st[pos[u], keep.index(s_)] = cat_code[c]
    near = {}
    for _, r in pairs[pairs.lycee_offre_le_plus_proche.notna()].iterrows():
        near.setdefault(r.uai, {})[keep.index(r.specialite)] = [round(r.km_offre_la_plus_proche, 1), r.lycee_offre_le_plus_proche]
    data = {"rentree": an, "rayon_km": R_KM, "seuil": SEUIL, "specialites": keep, "libelles_specialites": SPECIALITES, "taux": [round(float(x), 4) for x in rates],
            "taux_haut": [round(float(x), 4) for x in rates_hi],
            "lycees": [[r.uai, r.nom, r.commune, r.statut, r.academie, r.bassin, round(r.lat, 5), round(r.lon, 5), int(r.effectif),
                        st[i].tolist(), near.get(r.uai, {})] for i, r in lyc.iterrows()],
            "groupes": [[keep.index(g["specialite"]), g["membres"], round(g["demande"], 1), round(g["rayon_km"], 1)] for g in groups]}
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"-> {export_web('mutualisation', data)}")
    print(f"{len(lyc):,} lycées, {len(pairs):,} couples absents, {len(groups)} groupes -> {OUT_MD}")


if __name__ == "__main__":
    main()
