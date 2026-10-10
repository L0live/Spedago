// Fonctions de calcul pures (aucun accès au DOM) : exécutées par la page ET par les tests (Node.js).
import type { DonneesSpecialites } from '../types/donnees';

export interface LigneSpe { key: number; n: number; k: number; p: number; lo: number; hi: number; part: number; nO: number; pO: number; ecart: number }
export type EtatLycee = { eds: number; etat: 'hors_carte' | 'propose' | 'incertain' } | { eds: number; etat: 'absent'; km: number | null; uai: string | null };
interface Totaux { g: Map<number, [number, number]>; f: Map<number, [number, number]>; n: Map<number, [number, number]>; N: number }

export const SpeCalc = (() => {
  const Z = 1.96;
  function wilson(k: number, n: number): [number, number] {
    if (!n) return [NaN, NaN];
    const p = k / n, d = 1 + Z * Z / n, c = (p + Z * Z / (2 * n)) / d, h = (Z * Math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))) / d;
    return [c - h, c + h];
  }
  // Indice de la doublette (ordre indifférent), -1 si elle n'existe pas dans les données.
  function doublette(D: DonneesSpecialites, a: number, b: number): number {
    const x = Math.min(a, b), y = Math.max(a, b);
    return D.doublettes.findIndex(([i, j]) => i === x && j === y);
  }
  const cache = new WeakMap<DonneesSpecialites, Totaux>();
  function totals(D: DonneesSpecialites): Totaux {
    const deja = cache.get(D); if (deja) return deja;
    const g = new Map<number, [number, number]>(), f = new Map<number, [number, number]>(), n = new Map<number, [number, number]>();
    D.g.forEach(([, gi, v, p]) => { const t: [number, number] = g.get(gi) || [0, 0]; t[0] += v; t[1] += p; g.set(gi, t); });
    D.f.forEach(([, fi, v, p]) => { const t: [number, number] = f.get(fi) || [0, 0]; t[0] += v; t[1] += p; f.set(fi, t); });
    D.n.forEach(([d, v, p]) => n.set(d, [v, p]));
    const out = { g, f, n, N: D.n.reduce((s, r) => s + r[1], 0) };
    cache.set(D, out); return out;
  }
  // Une ligne : n demandeurs de la doublette, k propositions ; comparaison aux AUTRES bacheliers (total moins la doublette).
  function ligne(key: number, v: number, p: number, tot: [number, number], Nd: number): LigneSpe {
    const [lo, hi] = wilson(p, v), nO = tot[0] - v, kO = tot[1] - p, pO = nO ? kO / nO : NaN, pr = v ? p / v : NaN;
    return { key, n: v, k: p, p: pr, lo, hi, part: Nd ? v / Nd : NaN, nO, pO, ecart: pr - pO };
  }
  function groupes(D: DonneesSpecialites, d: number): LigneSpe[] {
    const T = totals(D), Nd = (T.n.get(d) || [0])[0];
    return D.g.filter((r) => r[0] === d).map(([, gi, v, p]) => ligne(gi, v, p, T.g.get(gi)!, Nd));
  }
  function fines(D: DonneesSpecialites, d: number, gi: number): LigneSpe[] {
    const T = totals(D), Nd = (T.n.get(d) || [0])[0];
    return D.f.filter((r) => r[0] === d && D.formations[r[1]][0] === gi).map(([, fi, v, p]) => ligne(fi, v, p, T.f.get(fi)!, Nd));
  }
  // Résumé de la doublette : candidats, rang parmi les doublettes, part avec au moins une proposition.
  function resume(D: DonneesSpecialites, d: number) {
    const T = totals(D), [v, p] = T.n.get(d) || [0, 0];
    const rang = 1 + D.n.filter((r) => r[1] > v).length;
    const tot = D.n.reduce<[number, number]>((s, r) => [s[0] + r[1], s[1] + r[2]], [0, 0]);
    return { n: v, k: p, p: v ? p / v : NaN, part: v / T.N, rang, nb: D.n.length, pTous: tot[1] / tot[0] };
  }
  // Mon lycée : pour chaque spécialité choisie, proposée / incertaine / sinon lycée le plus proche qui la propose.
  function lycee(D: DonneesSpecialites, li: number, eds: number[]): EtatLycee[] {
    const l = D.lycees[li], keys = D.carte_specialites;
    return eds.map((e): EtatLycee => {
      const ks = D.eds[e][2].map((k) => keys.indexOf(k)).filter((x) => x >= 0);
      if (!ks.length) return { eds: e, etat: "hors_carte" };
      const codes = ks.map((x) => l[4][x]);
      if (codes.includes(0)) return { eds: e, etat: "propose" };
      if (codes.includes(2)) return { eds: e, etat: "incertain" };
      let best: [number, string] | null = null as [number, string] | null;
      ks.forEach((x) => { const nr = l[5][String(x)]; if (nr && (!best || nr[0] < best[0])) best = nr; });
      return { eds: e, etat: "absent", km: best ? best[0] : null, uai: best ? best[1] : null };
    });
  }
  return { wilson, doublette, groupes, fines, resume, lycee, totals };
})();
