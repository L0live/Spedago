// Fonctions de calcul pures (aucun accès au DOM) : exécutées par la page ET par les tests (Node.js).
// Codes de statut : 0 proposée, 2 incertaine, 3 accès voisin, 4 ouverture commune, 5 isolé.
import type { DonneesCarte, GroupeCarte, LyceeCarte } from '../types/donnees';

export const MutCalc = (() => {
  const STAT = 3, ACAD = 4, EFF = 8, ST = 9;
  const visible = (l: LyceeCarte, statut: string, acad: string): boolean => (statut === "" || l[STAT] === statut) && (acad === "" || l[ACAD] === acad);
  // Nombre de lycées par code et élèves de 1re concernés (codes 3, 4, 5), pour une spécialité et un filtre.
  function summary(D: DonneesCarte, sp: number, statut: string = "", acad: string = "") {
    const n: Record<number, number> = { 0: 0, 2: 0, 3: 0, 4: 0, 5: 0 }, eleves: Record<number, number> = { 3: 0, 4: 0, 5: 0 };
    for (const l of D.lycees) {
      if (!visible(l, statut, acad)) continue;
      const c = l[ST][sp]; n[c] += 1; if (c in eleves) eleves[c] += l[EFF];
    }
    return { n, eleves };
  }
  // Groupes d'ouverture commune de la spécialité dont au moins un membre est visible, par demande décroissante.
  function groups(D: DonneesCarte, sp: number, statut: string = "", acad: string = ""): GroupeCarte[] {
    return D.groupes.filter((g) => g[0] === sp && g[1].some((m) => visible(D.lycees[m], statut, acad)))
      .sort((a, b) => b[2] - a[2] || a[1][0] - b[1][0]);
  }
  return { visible, summary, groups };
})();
