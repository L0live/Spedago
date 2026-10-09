"""Tests Spédago — piste B.  Lancer : python3 -m pytest tests/ -q"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_indice_specialites as b  # noqa: E402

OUT = ROOT / "data" / "processed" / "specialites_lycees.csv"
needs_data = pytest.mark.skipif(not OUT.exists(), reason="table piste B absente")


# ---------- unitaires ----------

def test_appariement_par_position_malgre_troncature():
    cols = ["0613_mathematiques_filles", "0613_mathematiques_garcons",
            "02_nom_tres_long_tronque_et_so", "02_nom_tres_long_tronque_et_s0",
            "autres_combinaisons_filles", "autres_combinaisons_garcons"]
    spe, combo = b.column_groups(cols, "1re")
    assert spe == [("0613_mathematiques_filles", "0613_mathematiques_garcons")]
    assert combo[0] == ("02_nom_tres_long_tronque_et_so", "02_nom_tres_long_tronque_et_s0")
    assert b.check_pairs(spe + combo) == []


def test_doublettes_terminale_separees_des_specialites():
    cols = ["0613_maths_filles", "0613_maths_garcons", "0001_maths_pc_filles", "0001_maths_pc_garcons"]
    spe, combo = b.column_groups(cols, "tle")
    assert [p[0] for p in spe] == ["0613_maths_filles"] and [p[0] for p in combo] == ["0001_maths_pc_filles"]


def test_colonnes_impaires_refusees():
    with pytest.raises(ValueError):
        b.column_groups(["0613_maths_filles"], "1re")


def _toy():
    return pd.DataFrame({
        "rentree_scolaire": [2025], "numero_etablissement": ["0160001A"], "denomination_principale": ["X"],
        "academie": ["POITIERS"], "secteur": ["PUBLIC"], "effectif_total": [100],
        "effectif_total_filles": [50], "effectif_total_garcons": [50],
        "0613_m_filles": [40], "0613_m_garcons": [np.nan], "0623_pc_filles": [0], "0623_pc_garcons": [0],
        "01_a_filles": [30], "01_a_garcons": [30], "02_b_filles": [np.nan], "02_b_garcons": [10],
        "autres_combinaisons_filles": [5], "autres_combinaisons_garcons": [np.nan]})


def test_indicateurs_sur_cas_construit():
    r = b.indicators(_toy(), "1re").iloc[0]
    assert r.nb_spe_visibles == 1 and r.nb_spe_max == 1   # PC à 0 explicite : non ouverte
    assert r.somme_publiee_combos == 75 and r.part_non_publiee == pytest.approx(0.25)
    assert r.part_autres_min == pytest.approx(0.05)
    assert r.nb_cases_masquees_combos == 2


def test_ajustement_taille_centre_chaque_decile():
    rng = np.random.default_rng(0)
    df = pd.DataFrame({"niveau": "1re", "rentree_scolaire": 2025, "effectif_total": rng.integers(20, 400, 500),
                       "part_non_publiee": rng.random(500)})
    adj = b.size_adjust(df)
    dec = pd.qcut(df.effectif_total.rank(method="first"), 10, labels=False)
    assert adj.groupby(dec).median().abs().max() < 1e-9


def test_ols_retrouve_coefficients_connus():
    rng = np.random.default_rng(1)
    X = pd.DataFrame({"a": rng.normal(size=2000), "b": rng.normal(size=2000)})
    y = 2 + 3 * X.a - 1 * X.b + rng.normal(scale=0.1, size=2000)
    r = b.ols(y, X)
    assert r.loc["a", "coef"] == pytest.approx(3, abs=0.02) and r.loc["b", "coef"] == pytest.approx(-1, abs=0.02)


# ---------- validation sur les vraies données ----------

@pytest.fixture(scope="module")
def tab():
    return pd.read_csv(OUT, sep=";", low_memory=False)


@needs_data
def test_partition_jamais_violee(tab):
    assert (tab.somme_publiee_combos <= tab.effectif_total).all()


@needs_data
def test_bornes(tab):
    assert tab.part_non_publiee.between(0, 1).all() and tab.part_autres_min.between(0, 1).all()
    assert (tab.nb_spe_visibles <= tab.nb_spe_max).all()


@needs_data
def test_pas_de_doublon(tab):
    assert not tab.duplicated(["niveau", "rentree", "numero_etablissement"]).any()


@needs_data
@pytest.mark.parametrize("niveau", ["1re", "tle"])
def test_paires_coherentes_sur_sources(niveau):
    fname = b.SOURCES[niveau][0]
    cols = list(pd.read_csv(b.RAW / fname, sep=";", nrows=0).columns)
    spe, combo = b.column_groups(cols, niveau)
    assert b.check_pairs(spe + combo) == []
    assert all("fille" in f for f, _ in spe)  # noms de spécialités non tronqués : ordre filles puis garçons


@needs_data
def test_jointure_ips_2025_suffisante(tab):
    assert tab[tab.rentree == 2025].ips_voie_gt.notna().mean() > 0.95


def test_simulation_neutre_masque_seulement_1_a_4():
    t = pd.DataFrame({"01_a_filles": [1000], "01_a_garcons": [1000], "02_b_filles": [10], "02_b_garcons": [10],
                      "autres_combinaisons_filles": [0], "autres_combinaisons_garcons": [0]})
    obs = pd.DataFrame({"effectif_total": [200, 20], "effectif_total_filles": [100, 10], "part_non_publiee": [0.1, 0.5]})
    sim = b.simulate_neutral(t, "1re", obs, n=2, seed=0)
    assert len(sim) == 2 and sim.sim_neutre.between(0, 1).all()
    # 200 élèves, 99 % dans la combinaison 01 : seule la petite combinaison 02 peut être masquée
    assert sim.loc[sim.effectif_total == 200, "sim_neutre"].iloc[0] <= 8 / 200


# ---------- robustesse ----------
import robustesse_piste_b as rb  # noqa: E402


def test_ols_cluster_retrouve_coefficient_et_se_plus_grande_si_correlation_intra_grappe():
    rng = np.random.default_rng(2)
    g = np.repeat(np.arange(40), 50)
    x = rng.normal(size=2000) + rng.normal(size=40)[g]
    y = 1 + 0.5 * x + rng.normal(size=40)[g] + rng.normal(scale=0.5, size=2000)
    r = rb.ols_cluster(pd.Series(y), pd.DataFrame({"x": x}), pd.Series(g))
    assert r.loc["x", "coef"] == pytest.approx(0.5, abs=0.15)
    naive = b.ols(pd.Series(y), pd.DataFrame({"x": x}))
    assert r.loc["x", "se"] > naive.loc["x", "se"]


def test_parts_corrigees_redonnent_du_poids_aux_cases_masquees():
    t = pd.DataFrame({"effectif_total_filles": [20], "effectif_total_garcons": [20],
                      "01_a_filles": [17], "01_a_garcons": [20], "02_b_filles": [np.nan], "02_b_garcons": [0],
                      "autres_combinaisons_filles": [0], "autres_combinaisons_garcons": [0]})
    pf_naif, _ = rb.national_shares(t, "1re", corrige=False)
    pf_corr, pg_corr = rb.national_shares(t, "1re", corrige=True)
    assert pf_naif[1] == 0 and pf_corr[1] == pytest.approx(3 / 20)
    assert pf_corr.sum() == pytest.approx(1) and pg_corr.sum() == pytest.approx(1)
