// Fonctions de calcul pures (aucun accès au DOM) : exécutées par la page ET par les tests (Node.js).
import type { DonneesAcademie } from '../types/donnees';

export const AcadCalc = (() => {
  const Z = 1.96;
  // Intervalle de Wilson à 95 % (identique à spedago.stats.wilson).
  function wilson(k: number, n: number): [number, number] {
    if (!n) return [NaN, NaN];
    const p = k / n, d = 1 + Z * Z / n, c = (p + Z * Z / (2 * n)) / d, h = (Z * Math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))) / d;
    return [c - h, c + h];
  }
  const ratio = (a: number, b: number): number => (b ? a / b : NaN);
  // [formations, places, admis, vœux, places des formations pleines, vacantes] -> indicateurs
  function ps(t: number[]) {
    const [formations, places, admis, voeux, sat, vac] = t;
    return { formations, places, admis, voeux, sat, vac, vpp: ratio(voeux, places), remp: ratio(admis, places), partSat: ratio(sat, places) };
  }
  // Spécialités : une ligne par spécialité, les plus difficiles d'accès d'abord.
  function speRows(spe: number[][]) {
    return spe.map((r, sp) => ({ sp, propose: r[0], incertain: r[1], voisin: r[2], commune: r[3], isole: r[4],
                                 eVoisin: r[5], eCommune: r[6], eIsole: r[7], groupes: r[8] }))
      .sort((a, b) => b.isole - a.isole || b.eIsole - a.eIsole || a.sp - b.sp);
  }
  // [formations, places, candidatures, propositions, candidatures L3 générale, propositions L3 générale]
  function mm(t: number[]) {
    const [formations, places, cand, prop, candL3, propL3] = t;
    return { formations, places, cand, prop, candL3, propL3, taux: ratio(prop, cand), tauxL3: ratio(propL3, candL3) };
  }
  const indexOf = (D: DonneesAcademie, slug: string): number => D.academies.findIndex((a) => a.slug === slug);
  return { wilson, ps, speRows, mm, indexOf };
})();
