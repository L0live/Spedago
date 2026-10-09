#!/usr/bin/env bash
# Spédago — pipeline complet, des données brutes aux rapports.
# Usage : bash run_all.sh            (télécharge ce qui manque)
#         bash run_all.sh --fresh    (efface data/processed et reports/ générés, puis relance tout)
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--fresh" ]]; then
  mkdir -p _anciens && mv -n data/processed _anciens/processed_$(date +%s) 2>/dev/null || true
fi
mkdir -p data/processed reports/profiling

python3 scripts/download_data.py
python3 scripts/download_data.py --check
python3 scripts/profile_data.py
python3 scripts/build_parcoursup_panel.py
python3 scripts/analyse_tension.py
python3 scripts/analyse_tension_fine.py
python3 scripts/simulate_ppl_art2.py
python3 scripts/build_indice_specialites.py
python3 scripts/robustesse_piste_b.py
python3 scripts/build_monmaster.py
python3 scripts/build_referentiel.py
python3 scripts/build_page_boussole.py
python3 scripts/build_simulateur_parcoursup.py
python3 scripts/build_mutualisation.py
python3 scripts/build_mon_academie.py
python3 scripts/build_site.py
python3 -m pytest tests/ -q -p no:cacheprovider
echo "Pipeline terminé."
