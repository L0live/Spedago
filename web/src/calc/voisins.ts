// Fonctions de calcul pures (aucun accès au DOM) : exécutées par la page ET par les tests (Node.js).
import type { DonneesVoisins } from '../types/donnees';

export interface LigneRegion { code: string; nom: string; role: 'moi' | 'voisine' | 'ref'; v: number; dernier: number; de: string; a: string; u: boolean }

export const VoisinsCalc = (() => {
  // Lignes du graphique en points pour un indicateur : région(s) de l'académie, voisines, puis références nationales.
  function lignes(D: DonneesVoisins, ai: number, key: string): LigneRegion[] {
    const [, , mes, vois] = D.academies[ai];
    const pays = [...new Set(["FR", ...vois.map((c) => c.slice(0, 2)), "EU27_2020"])];
    // un pays qui n'a qu'une région (Luxembourg : LU00) apparaît déjà comme voisine : pas de doublon en référence
    const refs = D.refs.filter((c) => pays.includes(c) && !vois.includes(c + "00"));
    const row = (c: string, role: LigneRegion['role']): LigneRegion | null => { const r = D.regions[c], v = r.v[key]; return v ? { code: c, nom: r.nom, role, v: v[0], dernier: v[1], de: v[2], a: v[3], u: v[4] === "u" } : null; };
    return [...mes.map((c) => row(c, "moi")), ...vois.map((c) => row(c, "voisine")), ...refs.map((c) => row(c, "ref"))].filter((r): r is LigneRegion => r !== null);
  }
  // Série d'un pays : [{annee, sortants, flagS, entrants, flagE}]
  function serie(D: DonneesVoisins, c: string) {
    const M = D.mobilite;
    return M.annees.map((a, i) => ({ annee: a, sortants: M.sortants[c][i][0], flagS: M.sortants[c][i][1], entrants: M.entrants[c][i][0], flagE: M.entrants[c][i][1] }));
  }
  return { lignes, serie };
})();
