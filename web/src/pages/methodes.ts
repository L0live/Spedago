// Méthodes et sources : rend le registre des indicateurs (spedago/indicateurs.py) publié dans data/methodes.json.
import '../styles/commun.css';
import '../styles/methodes.css';
import '../lib/commun';  // barre de navigation et panneau « Mon profil »
import { loadData, fillMeta } from '../lib/data';
import type { DonneesMethodes, Indicateur } from '../types/donnees';

const DEPOT = 'https://github.com/L0live/Spedago';
const esc = (s: string): string => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c] ?? c);
const pct = (v: number | string): string => (typeof v === 'number' && v > 0 && v < 1 ? `${Math.round(v * 100)} %` : String(v).replace('.', ','));

function fiche(i: Indicateur, D: DonneesMethodes): string {
  const sources = i.sources.map((f) => {
    const s = D.sources[f];
    return `<li><a href="${esc(s.url)}">${esc(s.jeu)}</a> (${esc(s.producteur)})</li>`;
  }).join('');
  const seuils = i.seuils.length
    ? `<dt>Seuils</dt><dd><ul>${i.seuils.map((s) => `<li>${esc(s.libelle)} : <strong>${esc(pct(s.valeur))}</strong></li>`).join('')}</ul></dd>` : '';
  const pages = i.pages.map((p) => `<a href="${esc(p)}">${esc(D.pages[p] ?? p)}</a>`).join(', ');
  return `<article class="fiche" id="${esc(i.id)}" aria-labelledby="t-${esc(i.id)}">
    <h3 id="t-${esc(i.id)}">${esc(i.nom)}</h3><p class="theme">${esc(i.theme)}</p>
    <p>${esc(i.definition)}</p>
    <dl>
      <dt>Calcul</dt><dd>${esc(i.formule)}</dd>
      <dt>Champ</dt><dd>${esc(i.champ)}</dd>
      ${seuils}
      <dt>Limites</dt><dd><ul>${i.limites.map((l) => `<li>${esc(l)}</li>`).join('')}</ul></dd>
      <dt>Sources</dt><dd><ul>${sources}</ul></dd>
      <dt>Pages</dt><dd>${pages}</dd>
      ${i.rapport ? `<dt>Rapport</dt><dd><a href="${DEPOT}/blob/main/reports/${esc(i.rapport)}"><code>reports/${esc(i.rapport)}</code></a></dd>` : ''}
    </dl></article>`;
}

function main(D: DonneesMethodes): void {
  fillMeta({ n: D.indicateurs.length });
  const themes = new Map<string, Indicateur[]>();
  D.indicateurs.forEach((i) => themes.set(i.theme, [...(themes.get(i.theme) ?? []), i]));
  document.getElementById('sommaire')!.innerHTML = [...themes].map(([t, l], k) =>
    `<div><h2 id="som-${k}">${esc(t)}</h2><ul aria-labelledby="som-${k}">${l.map((i) => `<li><a href="#${esc(i.id)}">${esc(i.nom)}</a></li>`).join('')}</ul></div>`).join('');
  document.getElementById('fiches')!.innerHTML = D.indicateurs.map((i) => fiche(i, D)).join('');
  document.querySelector('#sources tbody')!.innerHTML = Object.entries(D.sources).map(([f, s]) =>
    `<tr><td><code>${esc(f)}</code></td><td><a href="${esc(s.url)}">${esc(s.jeu)}</a></td><td>${esc(s.producteur)}</td>`
    + `<td>${esc(s.telecharge_le)}</td><td><code title="${esc(s.sha256)}">${esc(s.sha256.slice(0, 12))}…</code></td></tr>`).join('');
  // l'ancre visée (#ps-pression…) n'existait pas avant le rendu : on y va maintenant
  const cible = location.hash.slice(1) && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (cible) { cible.classList.add("visee"); cible.scrollIntoView(); }
}

loadData<DonneesMethodes>('methodes').then(main);
