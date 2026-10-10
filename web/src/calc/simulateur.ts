// Fonctions de calcul pures (aucun accès au DOM) : exécutées par la page ET par les tests (Node.js).
// Reproduisent scripts/simulate_ppl_art2.py (prepare, scenario_s1/s2/s3).
import type { DonneesSimulateur, FormationSim } from '../types/donnees';

export interface ParamsSim { regle?: 's1' | 's2'; pct?: number; q?: number; sat?: number; sous?: number }
export interface ResultatSim { add: number[]; elig: boolean[]; total: number; places: number; idf: number; nElig: number; couvert: number;
  couvertFil: Map<number, number>; couvertA: Map<number, number>; couvertAF: Map<string, number>;
  nonServis: number; ajoutRang: number; sansRang: number; ajoutSansRang: number; formationsRang: number; couvertes: number; medianeRatio: number }
export interface LigneGroupe { key: number; places: number; ajout: number; visees: number; nonServis: number; idf: number }

export const SimCalc = (() => {
  const A = 0, FIL = 1, SPE = 2, IDF = 3, MOB = 4, CAP = 5, ACC = 6, VOE = 7, NA = 8, LC = 9;
  // Quantile à interpolation linéaire (identique à pandas.Series.quantile par défaut).
  function quantile(sorted: number[], q: number): number {
    const n = sorted.length; if (!n) return NaN;
    const pos = (n - 1) * q, lo = Math.floor(pos), hi = Math.ceil(pos);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
  }
  // Plafond sûr : 100 × 0,07 = 7,000000000000001 en flottant ; on arrondit à 1e-9 avant le plafond.
  const ceilSafe = (x: number): number => Math.ceil(Math.round(x * 1e9) / 1e9);

  function eligible(D: DonneesSimulateur, q: number, sat: number): boolean[] {
    const F = D.formations, byFil = new Map<number, number[]>();
    F.forEach((f) => { const p = f[VOE] / f[CAP]; (byFil.get(f[FIL]) || byFil.set(f[FIL], []).get(f[FIL])!).push(p); });
    const seuils = new Map<number, number>(); byFil.forEach((v, k) => seuils.set(k, quantile(v.sort((a, b) => a - b), q)));
    return F.map((f) => f[VOE] / f[CAP] >= seuils.get(f[FIL])! && f[ACC] / f[CAP] >= sat && (f[LC] === 1 || f[NA] > 0));
  }

  // params : { regle: "s1"|"s2", pct (0-1), q (0-1), sat (0-1), sous (0-1) }
  function simulate(D: DonneesSimulateur, params: ParamsSim): ResultatSim {
    const { regle = "s1", pct = 0.1, q = 0.75, sat = 0.95, sous = 0.8 } = params;
    const F = D.formations, elig = eligible(D, q, sat);
    const add = F.map((f, i) => {
      if (!elig[i]) return 0;
      if (regle === "s1") return ceilSafe(f[CAP] * pct);
      return f[NA] >= 0 && f[LC] !== 1 ? Math.min(f[NA], ceilSafe(f[CAP] * pct)) : 0;
    });
    // Redéploiement : même académie × filière × spécialité ; gisement = vacantes des formations mobilisables sous-remplies.
    const cells = new Map<string, { besoin: number; gisement: number; fil: number; a: number; idf: number }>();
    F.forEach((f, i) => {
      const key = f[A] + "|" + f[FIL] + "|" + f[SPE] + "|" + f[IDF];
      let c = cells.get(key); if (!c) { c = { besoin: 0, gisement: 0, fil: f[FIL], a: f[A], idf: f[IDF] }; cells.set(key, c); }
      c.besoin += add[i];
      if (f[MOB] === 1 && f[ACC] / f[CAP] < sous) c.gisement += Math.max(0, f[CAP] - f[ACC]);
    });
    let couvert = 0; const couvertFil = new Map<number, number>(), couvertA = new Map<number, number>(), couvertAF = new Map<string, number>();
    cells.forEach((c) => {
      const x = Math.min(c.besoin, c.gisement); couvert += x;
      couvertFil.set(c.fil, (couvertFil.get(c.fil) || 0) + x); couvertA.set(c.a, (couvertA.get(c.a) || 0) + x);
      couvertAF.set(c.a + "|" + c.fil, (couvertAF.get(c.a + "|" + c.fil) || 0) + x);
    });
    let total = 0, places = 0, idf = 0, nElig = 0;
    F.forEach((f, i) => { total += add[i]; places += f[CAP]; if (f[IDF]) idf += add[i]; if (elig[i]) nElig += 1; });
    return { add, elig, total, places, idf, nElig, couvert, couvertFil, couvertA, couvertAF, ...demande(D, add) };
  }

  // Demande non servie dans les formations qui reçoivent des places : candidats classés jamais appelés
  // (listes d'appel propres seulement ; borne HAUTE, ces candidats ont pu être admis ailleurs).
  // Attention : ce sont des CANDIDATURES, pas des personnes (un candidat compte dans chaque formation où il est classé).
  // L'indicateur utile est donc local : les places ajoutées trouveraient-elles preneur dans la formation ?
  function demande(D: DonneesSimulateur, add: number[], filtre: string = "") {
    let nonServis = 0, ajoutRang = 0, sansRang = 0, ajoutSansRang = 0, couvertes = 0;
    const ratios: number[] = [];
    D.formations.forEach((f, i) => {
      if (add[i] <= 0 || (filtre !== "" && f[FIL] !== +filtre)) return;
      if (f[NA] >= 0 && f[LC] !== 1) {
        nonServis += f[NA]; ajoutRang += add[i]; ratios.push(f[NA] / add[i]); if (f[NA] >= add[i]) couvertes += 1;
      } else { sansRang += 1; ajoutSansRang += add[i]; }
    });
    ratios.sort((a, b) => a - b);
    const m = ratios.length, medianeRatio = !m ? NaN : m % 2 ? ratios[(m - 1) / 2] : (ratios[m / 2 - 1] + ratios[m / 2]) / 2;
    return { nonServis, ajoutRang, sansRang, ajoutSansRang, formationsRang: m, couvertes, medianeRatio };
  }

  function groupBy(D: DonneesSimulateur, res: { add: number[] }, col: number, filtre: string = "", acad: string = ""): LigneGroupe[] {
    const g = new Map<number, LigneGroupe>();
    D.formations.forEach((f: FormationSim, i) => {
      if ((filtre !== "" && f[FIL] !== +filtre) || (acad !== "" && f[A] !== +acad)) return;
      let r = g.get(f[col]); if (!r) { r = { key: f[col], places: 0, ajout: 0, visees: 0, nonServis: 0, idf: f[IDF] }; g.set(f[col], r); }
      r.places += f[CAP]; r.ajout += res.add[i]; r.visees += res.add[i] > 0 ? 1 : 0;
      if (res.add[i] > 0 && f[NA] >= 0 && f[LC] !== 1) r.nonServis += f[NA];
    });
    return [...g.values()];
  }
  return { quantile, ceilSafe, eligible, simulate, demande, groupBy, COL: { A, FIL, SPE } };
})();
