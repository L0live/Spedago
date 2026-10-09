"""Tests Spédago — piste A.  Lancer : python3 -m pytest tests/ -q

Deux familles :
  - tests unitaires sur données synthétiques (logique des scripts) ;
  - tests de validation sur les vraies données (ignorés si les fichiers n'existent pas).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_parcoursup_panel as bp  # noqa: E402
import simulate_ppl_art2 as sim  # noqa: E402

RAW = ROOT / "data" / "raw"
PANEL = ROOT / "data" / "processed" / "parcoursup_panel_2020_2025.csv.gz"
needs_data = pytest.mark.skipif(not PANEL.exists(), reason="table harmonisée absente")


# ---------- unitaires ----------

def test_ratio_gere_zero_et_nan():
    r = bp.ratio(pd.Series([10, 5, np.nan]), pd.Series([2, 0, 4]))
    assert r.iloc[0] == 5 and np.isnan(r.iloc[1]) and np.isnan(r.iloc[2])


def _mini(session, list_com, code="F1"):
    return pd.DataFrame({"session": [session], "cod_aff_form": [code], "list_com": [list_com],
                         "fili": ["DUT"], "fil_lib_voe_acc": ["Génie électrique"], "acad_mies": ["Besançon"]})


def test_inversion_list_com_2024_2025():
    df = pd.concat([_mini(2023, "Liste d'appel commune à plusieurs formations", "A"),
                    _mini(2024, "Liste d'appel propre à cette formation", "A"),
                    _mini(2025, "Liste d'appel propre à cette formation", "A")], ignore_index=True)
    out = bp.harmonize(df)
    assert out.liste_commune.tolist() == [True, True, True]


def test_imputation_2020_depuis_2021():
    df = pd.concat([_mini(2020, np.nan, "A"), _mini(2021, "Liste d'appel commune à plusieurs formations", "A"),
                    _mini(2020, np.nan, "B")], ignore_index=True)
    out = bp.harmonize(df)
    assert out.loc[0, "liste_commune"] == True  # noqa: E712
    assert pd.isna(out.loc[2, "liste_commune"])  # B absent en 2021 : pas d'imputation
    assert out.liste_commune_imputee_2021.tolist() == [True, False, False]


def test_ifsi_paramedical_2024_realigne():
    df = _mini(2024, "Liste d'appel propre à cette formation").assign(fili="IFSI", fil_lib_voe_acc="D.E Ergothérapeute")
    df = pd.concat([df, _mini(2024, "Liste d'appel propre à cette formation", "B").assign(fili="IFSI", fil_lib_voe_acc="D.E Infirmier")])
    assert bp.harmonize(df.reset_index(drop=True)).fili_harmo.tolist() == ["Autre formation", "IFSI"]


def test_harmonisation_libelles():
    out = bp.harmonize(_mini(2021, "Liste d'appel propre à cette formation"))
    assert out.fili_harmo.iloc[0] == "BUT" and out.academie.iloc[0] == "Besancon"


def _toy_sim():
    """Deux formations d'une même cellule : A saturée sous pression, B sous-remplie."""
    return pd.DataFrame({
        "session": [2024, 2024], "cod_aff_form": ["A", "B"], "fili_harmo": ["BTS", "BTS"],
        "academie": ["Poitiers"] * 2, "idf": [False, False], "liste_commune": [False, False],
        "fil_lib_voe_acc": ["Comptabilité", "Comptabilité"], "contrat_etab": ["Public", "Public"],
        "capa_fin": [100, 100], "acc_tot": [100, 50], "nb_voe_pp": [3000, 200],
        "nb_cla_pp": [2000, 200], "ran_grp1": [300, 200], "ran_grp2": [np.nan] * 2, "ran_grp3": [np.nan] * 2})


def test_eligibilite_et_s1():
    p = sim.prepare(_toy_sim())
    assert p.eligible.tolist() == [True, False]
    assert sim.scenario_s1(p, 0.10).tolist() == [10, 0]


def test_s2_plafonne_par_non_appeles():
    p = sim.prepare(_toy_sim())
    assert p.non_appeles.tolist() == [1700, 0]
    assert sim.scenario_s2(p, 0.20).tolist() == [20, 0]  # min(1700, 20 % de 100)


def test_s3_redeploiement_borne_par_gisement():
    c = sim.scenario_s3(sim.prepare(_toy_sim()), 0.10)
    assert c.besoin.sum() == 10 and c.gisement.sum() == 50 and c.couvert.sum() == 10
    c = sim.scenario_s3(sim.prepare(_toy_sim()), 0.80)
    assert c.couvert.sum() == 50  # on ne redéploie pas plus que les vacantes


# ---------- validation sur les vraies données ----------

@pytest.fixture(scope="module")
def panel():
    return pd.read_csv(PANEL, sep=";", low_memory=False)


@needs_data
def test_pas_de_doublon(panel):
    assert not panel.duplicated(["cod_aff_form", "session"]).any()


@needs_data
@pytest.mark.parametrize("year", range(2020, 2026))
def test_totaux_identiques_aux_sources(panel, year):
    raw = pd.read_csv(RAW / f"parcoursup_{year}.csv", sep=";", low_memory=False)
    p = panel[panel.session == year]
    assert len(p) == len(raw)
    for c in ("capa_fin", "acc_tot", "nb_voe_pp", "acc_brs"):
        assert p[c].sum() == pytest.approx(pd.to_numeric(raw[c], errors="coerce").sum())


@needs_data
def test_identites_comptables(panel):
    assert (panel.acc_neobac <= panel.acc_tot).all()
    assert (panel.acc_brs <= panel.acc_neobac).all()
    assert (panel.ind_admis_hors_pp_pc >= 0).all()


@needs_data
def test_parts_entre_0_et_1(panel):
    for c in panel.filter(like="ind_pct_brs").columns.tolist() + ["ind_part_classes_appeles"]:
        s = panel[c].dropna()
        assert ((s >= 0) & (s <= 1)).all(), c


@needs_data
def test_garde_fou_inversion_list_com(panel):
    """Après correction, la part de listes communes doit être stable (~13 %) chaque année."""
    part = panel[panel.session >= 2021].groupby("session").liste_commune.apply(lambda s: (s == True).mean())  # noqa: E712
    assert part.between(0.08, 0.20).all(), part.to_dict()


@needs_data
def test_rang_coherent_apres_correction(panel):
    taux = panel[panel.session >= 2021].groupby("session").flag_rang_incoherent.mean()
    assert (taux < 0.02).all(), taux.to_dict()


@needs_data
def test_cned_isole(panel):
    """Les capacités nominales CNED ne doivent plus peser sur les places vacantes analysées."""
    p = panel[panel.session == 2025]
    assert p.flag_cned.sum() >= 15
    assert p.loc[p.flag_cned, "ind_taux_remplissage"].median() < 0.3
    hors = p[~p.flag_cned & (p.capa_fin > 0)]
    assert hors.ind_places_vacantes.max() < 2000


def test_s3_ne_redeploie_pas_entre_specialites_ni_depuis_hors_contrat():
    t = _toy_sim().assign(fil_lib_voe_acc=["Comptabilité", "Électrotechnique"])
    assert sim.scenario_s3(sim.prepare(t), 0.10).couvert.sum() == 0
    t = _toy_sim().assign(contrat_etab=["Public", "Privé hors contrat"])
    assert sim.scenario_s3(sim.prepare(t), 0.10).couvert.sum() == 0


def test_sensibilite_restaure_les_parametres():
    q0, s0 = sim.Q_PRESSION, sim.SEUIL_SATURE
    sens = sim.sensitivity(pd.concat([_toy_sim(), _toy_sim().assign(session=2025)], ignore_index=True))
    assert len(sens) == 9 and (sim.Q_PRESSION, sim.SEUIL_SATURE) == (q0, s0)


def test_simulation_exclut_cned():
    t = _toy_sim().assign(flag_cned=[False, True])
    assert sim.prepare(t).cod_aff_form.tolist() == ["A"]


@needs_data
def test_ifsi_reserve_aux_infirmiers(panel):
    i = panel[panel.fili_harmo == "IFSI"]
    assert (i.fil_lib_voe_acc == "D.E Infirmier").all()
    n = i.groupby("session").size()
    assert n.max() / n.min() < 1.15, n.to_dict()


@needs_data
def test_academies_normalisees(panel):
    assert "Besançon" not in set(panel.academie)
