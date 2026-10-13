"""Téléchargement robuste (spedago/telechargement.py) : gzip servi sans le dire, contenu invalide, essais répétés."""
from __future__ import annotations

import gzip
import io
import urllib.error
import urllib.request

import pytest

from spedago import telechargement as T

CSV = "﻿session;cod_uai;lib\n2025;0860001A;Lycée Camille-Guérin\n".encode("utf-8")


def reponses(monkeypatch, *contenus):
    """urlopen renvoie successivement ces contenus (bytes) ou lève ces exceptions ; retourne la liste des appels."""
    appels, file = [], list(contenus)

    def urlopen(url, timeout=0):
        appels.append(url)
        x = file.pop(0)
        if isinstance(x, Exception):
            raise x
        return io.BytesIO(x)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(T.time, "sleep", lambda s: None)
    return appels


def test_csv_en_gzip_decompresse(tmp_path, monkeypatch):
    reponses(monkeypatch, gzip.compress(CSV))
    p = T.telecharger("https://exemple/x.csv", tmp_path / "x.csv", T.verifier_csv)
    assert p.read_bytes() == CSV  # mêmes octets que si le portail l'avait servi en clair (empreinte inchangée)
    assert not (tmp_path / "x.csv.part").exists()


@pytest.mark.parametrize("contenu,motif", [
    ("session,cod_uai\n2025,0860001A\n".encode("utf-8"), "séparateur"),
    ("session;lib\n2025;Lyc\xe9e\n".encode("latin-1"), "UTF-8"),
    (b"", "vide"),
])
def test_contenu_invalide_refuse(tmp_path, contenu, motif):
    p = tmp_path / "x.csv"
    p.write_bytes(contenu)
    with pytest.raises(T.ContenuInvalide, match=motif):
        T.verifier_csv(p)


def test_trois_essais_puis_succes(tmp_path, monkeypatch):
    appels = reponses(monkeypatch, urllib.error.URLError("délai dépassé"), b"\x1f\x8bpas du gzip", CSV)
    T.telecharger("https://exemple/x.csv", tmp_path / "x.csv", T.verifier_csv)
    assert len(appels) == 3 and (tmp_path / "x.csv").read_bytes() == CSV


def test_echec_final_nomme_le_fichier_et_garde_la_copie(tmp_path, monkeypatch):
    p = tmp_path / "parcoursup_2025.csv"
    p.write_bytes(CSV)  # copie précédente valide : jamais écrasée par un contenu invalide
    reponses(monkeypatch, b"<html>erreur</html>", b"<html>erreur</html>", b"<html>erreur</html>")
    with pytest.raises(SystemExit, match=r"parcoursup_2025\.csv .*3 essais.*séparateur"):
        T.telecharger("https://exemple/x.csv", p, T.verifier_csv, essais=3)
    assert p.read_bytes() == CSV and not (tmp_path / "parcoursup_2025.csv.part").exists()


def test_copie_locale_en_gzip_reparee(tmp_path):
    p = tmp_path / "x.csv"
    p.write_bytes(gzip.compress(CSV))
    assert T.reparer_copie_locale(p, T.verifier_csv) and p.read_bytes() == CSV
    p.write_bytes(b"pas;un\xff csv")
    assert not T.reparer_copie_locale(p, T.verifier_csv)


def test_json(tmp_path, monkeypatch):
    reponses(monkeypatch, gzip.compress(b'{"value": {"0": 1}}'))
    p = T.telecharger("https://exemple/x.json", tmp_path / "x.json", T.verifier_json)
    assert p.read_text(encoding="utf-8") == '{"value": {"0": 1}}'
