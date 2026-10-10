// Fonctions de calcul pures (aucun accès au DOM) : exécutées par la page ET par les tests (Node.js).
import type { DonneesBoussole, FormationMaster, Prior } from '../types/donnees';

export interface LigneMention { mention: number; formations: number; places: number; n: number; k: number;
  best: { ifc: string; etab: number; parcours: string; p: number; lo: number } | null; p: number; lo: number; hi: number }
export interface OptionsClassement { academie?: string; modalite?: string; secteur?: string; minCandidats?: number }

export const BoussoleCalc = (() => {
  const Z = 1.96;
  // Candidats et propositions d'un profil, cumulés sur les sessions (−1 = formation absente cette session).
  function counts(f: FormationMaster, profil: string, P: string[], S: number[]): [number, number] {
    const pi = P.indexOf(profil); let n = 0, k = 0;
    for (let j = 0; j < S.length; j++) {
      const at = (pi * S.length + j) * 2, nn = f[9][at], kk = f[9][at + 1];
      if (nn > 0) { n += nn; k += kk; }
    }
    return [n, k];
  }
  function wilson(k: number, n: number): [number, number, number] {
    if (n <= 0) return [NaN, NaN, NaN];
    const p = k / n, den = 1 + Z * Z / n;
    const c = (p + Z * Z / (2 * n)) / den, h = Z * Math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den;
    return [p, Math.max(0, c - h), Math.min(1, c + h)];
  }
  // Estimation bayésienne empirique : a priori Bêta(m, κ) de la mention × profil,
  // a posteriori Bêta(k + κm, n − k + κ(1 − m)) ; intervalle à 95 % par approximation normale.
  function posterior(k: number, n: number, prior?: Prior): [number, number, number] {
    if (n <= 0) return [NaN, NaN, NaN];
    if (!prior) return wilson(k, n);
    const [m, kap] = prior, a = k + kap * m, b = n - k + kap * (1 - m);
    const mean = a / (a + b), sd = Math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)));
    return [mean, Math.max(0, mean - Z * sd), Math.min(1, mean + Z * sd)];
  }
  function estimate(D: DonneesBoussole, f: FormationMaster, profil: string): [number, number, number, number, number] {
    const [n, k] = counts(f, profil, D.profils, D.sessions);
    const prior = (D.priors[String(f[3])] || {})[profil];
    return [n, k, ...posterior(k, n, prior)];
  }
  // Vue inversée : une ligne par mention, chances poolées du profil (Wilson sur Σk/Σn)
  // + formation la plus accessible (meilleure borne basse de l'estimation corrigée).
  function rankMentions(D: DonneesBoussole, profil: string, opts: OptionsClassement = {}): LigneMention[] {
    const { academie = "", modalite = "", secteur = "", minCandidats = 30 } = opts;
    const last = D.sessions.length - 1;
    const by = new Map<number, Omit<LigneMention, 'p' | 'lo' | 'hi'>>();
    for (const f of D.formations) {
      if ((academie !== "" && f[2] !== +academie) || (modalite !== "" && f[5] !== +modalite) || (secteur !== "" && f[6] !== +secteur)) continue;
      const [n, k, p, lo] = estimate(D, f, profil);
      let g = by.get(f[3]);
      if (!g) { g = { mention: f[3], formations: 0, places: 0, n: 0, k: 0, best: null }; by.set(f[3], g); }
      g.formations += 1; g.places += f[7][last] || 0; g.n += n; g.k += k;
      if (n > 0 && f[7][last] != null && (!g.best || lo > g.best.lo)) g.best = { ifc: f[0], etab: f[1], parcours: f[4], p, lo };
    }
    const out: LigneMention[] = [];
    for (const g of by.values()) {
      if (g.n < minCandidats) continue;
      const [p, lo, hi] = wilson(g.k, g.n);
      out.push({ ...g, p, lo, hi });
    }
    return out.sort((a, b) => b.lo - a.lo || b.n - a.n);
  }
  return { counts, wilson, posterior, estimate, rankMentions };
})();
