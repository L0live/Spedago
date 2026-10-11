// Accès typés au DOM et mise en forme, communs aux pages.
// Un élément absent est une erreur de construction de la page (HTML et TypeScript désaccordés) : on échoue tout de suite, avec son nom.

export function el<T extends HTMLElement = HTMLElement>(id: string, type?: { new (): T }): T {
  const e = document.getElementById(id);
  if (!e) throw new Error(`élément #${id} absent de la page`);
  if (type && !(e instanceof type)) throw new Error(`#${id} n'est pas un ${type.name}`);
  return e as T;
}
export const input = (id: string): HTMLInputElement => el(id, HTMLInputElement);
export const select = (id: string): HTMLSelectElement => el(id, HTMLSelectElement);
export const table = (id: string): HTMLTableElement => el(id, HTMLTableElement);
/** Premier corps d'un tableau (créé s'il manque). */
export const tbody = (t: HTMLTableElement): HTMLTableSectionElement => t.tBodies[0] ?? t.createTBody();

const ENTITES: Record<string, string> = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
export const esc = (t: unknown): string => String(t).replace(/[&<>"']/g, (c) => ENTITES[c] ?? c);
export const fmtInt = (x: number): string => Math.round(x).toLocaleString('fr-FR');
export const fmtPct = (x: number, d = 1): string => (x * 100).toFixed(d).replace('.', ',') + ' %';

/** Ajoute des <option> (valeur, libellé) à un <select>. */
export function options(s: HTMLSelectElement, items: Iterable<[string | number, string]>): void {
  for (const [v, t] of items) { const o = document.createElement('option'); o.value = String(v); o.textContent = t; s.appendChild(o); }
}
/** Libellé de l'option choisie d'un <select> ('' si aucune). */
export const selectedText = (s: HTMLSelectElement): string => s.selectedOptions[0]?.textContent ?? '';

/** Chiffre clé : valeur et libellé (HTML déjà échappé), puis son champ et le lien vers sa fiche de la page Méthodes.
 *  La fiche vient en premier : les tests vérifient qu'elle existe dans spedago/indicateurs.py et qu'elle couvre la page. */
export function stat(fiche: string, valeur: string, libelle: string, champ: string, classe = 'stat', style = ''): string {
  return `<div class="${classe}"${style ? ` style="${style}"` : ''}><b>${valeur}</b><span>${libelle}</span>`
    + `<a class="champ" href="methodes.html#${esc(fiche)}">${esc(champ)} · méthode</a></div>`;
}
/** Texte à annoncer pour une rangée de chiffres clés : valeurs et libellés, sans les liens vers les fiches. */
export const resumeStats = (zone: HTMLElement): string =>
  [...zone.children].map((c) => `${c.querySelector('b')?.textContent ?? ''} ${c.querySelector('span')?.textContent ?? ''}`).join(' ; ');
