"""Spédago — téléchargements robustes des données ouvertes.

Les portails servent parfois un fichier compressé en gzip (octets 1f 8b) sans le dire : il est décompressé.
Un fichier reçu est contrôlé avant de remplacer la copie locale (CSV : UTF-8 et séparateur « ; » ; JSON : lisible).
En cas d'échec réseau ou de contenu invalide, trois essais espacés ; l'erreur finale nomme le fichier et l'adresse.
"""
from __future__ import annotations

import codecs
import gzip
import http.client
import json
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

GZIP = b"\x1f\x8b"
ESSAIS = 3
PAUSES = (5, 20)  # secondes avant le 2e et le 3e essai


class ContenuInvalide(Exception):
    """Fichier reçu inutilisable (encodage, séparateur, vide…) ; le message dit pourquoi."""


def est_gzip(path: Path) -> bool:
    with open(path, "rb") as f:
        return f.read(2) == GZIP


def decompresser_si_gzip(path: Path) -> bool:
    """Remplace le fichier par sa version décompressée s'il est en gzip. Retourne True s'il l'était."""
    if not est_gzip(path):
        return False
    tmp = path.with_name(path.name + ".gunzip")
    try:
        with gzip.open(path, "rb") as src, open(tmp, "wb") as dst:
            shutil.copyfileobj(src, dst, 1 << 20)
    except (OSError, EOFError) as e:
        tmp.unlink(missing_ok=True)
        raise ContenuInvalide(f"gzip illisible ({e})") from e
    tmp.replace(path)
    return True


def verifier_csv(path: Path, sep: str = ";") -> None:
    """Contrôle un CSV d'export : non vide, entièrement en UTF-8, en-tête découpé par `sep`. Lève ContenuInvalide."""
    dec = codecs.getincrementaldecoder("utf-8")()
    tete = ""
    with open(path, "rb") as f:
        try:
            while chunk := f.read(1 << 20):
                texte = dec.decode(chunk)
                if len(tete) < 4096:
                    tete += texte[:4096]
            dec.decode(b"", final=True)
        except UnicodeDecodeError as e:
            raise ContenuInvalide(f"pas en UTF-8 (octet {e.object[e.start:e.start + 1].hex()} à la position {e.start} d'un bloc)") from e
    entete = tete.lstrip("﻿").split("\n", 1)[0]
    if not entete.strip():
        raise ContenuInvalide("fichier vide")
    if sep not in entete:
        raise ContenuInvalide(f"séparateur « {sep} » absent de l'en-tête : {entete[:80]!r}")


def verifier_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ContenuInvalide(f"JSON illisible ({e})") from e


def telecharger(url: str, path: Path, verifier, *, timeout: int = 600, essais: int = ESSAIS, pauses=PAUSES) -> Path:
    """Télécharge `url` vers `path` : décompresse un gzip, contrôle le contenu avec `verifier(fichier)`,
    puis remplace la copie locale. Réessaie ; après le dernier échec, SystemExit qui nomme le fichier."""
    tmp = path.with_name(path.name + ".part")
    raison = ""
    for k in range(1, essais + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r, open(tmp, "wb") as f:
                shutil.copyfileobj(r, f, 1 << 20)
            if decompresser_si_gzip(tmp):
                print(f"   {path.name} : reçu compressé en gzip, décompressé")
            verifier(tmp)
            tmp.replace(path)
            return path
        except (urllib.error.URLError, http.client.HTTPException, TimeoutError, OSError, ContenuInvalide) as e:
            raison = str(e) or e.__class__.__name__
            tmp.unlink(missing_ok=True)
            if k < essais:
                pause = pauses[min(k - 1, len(pauses) - 1)]
                print(f"   {path.name} : essai {k}/{essais} échoué ({raison}) ; nouvel essai dans {pause} s")
                time.sleep(pause)
    raise SystemExit(f"{path.name} : téléchargement inutilisable après {essais} essais — {raison}\n   adresse : {url}")


def reparer_copie_locale(path: Path, verifier) -> bool:
    """Copie locale déjà présente : décompresse un gzip laissé par une version antérieure du script, puis contrôle.
    Retourne False si le fichier reste invalide (il faut le retélécharger)."""
    try:
        if decompresser_si_gzip(path):
            print(f"   {path.name} : copie locale en gzip, décompressée")
        verifier(path)
        return True
    except ContenuInvalide as e:
        print(f"   {path.name} : copie locale invalide ({e}) ; retéléchargement")
        return False
