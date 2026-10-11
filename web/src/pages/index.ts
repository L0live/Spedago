import '../styles/commun.css';
import '../styles/index.css';
import { Spedago } from '../lib/commun';
import { loadData } from '../lib/data';
import { el, select, esc, fmtInt, options, selectedText } from '../lib/dom';
import type { DonneesAccueil } from '../types/donnees';

function main(D: DonneesAccueil): void {
  const sel = select('acad');
  el('figures').innerHTML = D.chiffres
    .map(([n, t, champ, id]) => `<li><b>${fmtInt(n)}</b><span>${esc(t)}</span>`
      + `<a class="champ" href="methodes.html#${esc(id)}">${esc(champ)} · méthode</a></li>`).join('');
  options(sel, D.academies.map(([nom, slug]): [string, string] => [slug, nom]));
  if (!Spedago.pick(sel)) sel.value = 'poitiers';
  el<HTMLFormElement>('go').addEventListener('submit', (e) => { e.preventDefault(); location.href = 'mon-academie.html#' + sel.value; });
  sel.addEventListener('change', () => Spedago.setHash(selectedText(sel)));
}

loadData<DonneesAccueil>('index').then(main);
