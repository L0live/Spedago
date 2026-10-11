import '../styles/commun.css';
import '../styles/simulateur-parcoursup.css';
import { Spedago } from '../lib/commun';
import { loadData } from '../lib/data';
import { el, input, select, table, tbody, esc, fmtInt, fmtPct, options, selectedText } from '../lib/dom';
import { SimCalc as C, type ParamsSim, type LigneGroupe } from '../calc/simulateur';
import type { DonneesSimulateur } from '../types/donnees';

function main(D: DonneesSimulateur): void {
  const E = {
    controls: el<HTMLFormElement>('controls'), s1: input('regle-s1'), s2: input('regle-s2'),
    pct: input('pct'), q: input('q'), sat: input('sat'), sous: input('sous'),
    pctOut: el('pct-out'), pctLabel: el('pct-label'), qOut: el('q-out'), satOut: el('sat-out'), sousOut: el('sous-out'),
    acad: select('acad'), filiere: select('filiere'), reset: el('reset'), exportAcad: el('export-acad'),
    summary: el('summary'), lecture: el('lecture'), demande: el('demande'), hFil: el('h-fil'),
    tAcad: table('t-acad'), tFil: table('t-fil'), tSpe: table('t-spe'),
  };
  const DEF = { pct: '10', q: '75', sat: '95', sous: '80', filiere: '' };
  const FIL = (i: number): string => (D.libelles_filieres || {})[D.filieres[i]] || D.filieres[i];
  options(E.filiere, D.filieres.map((_, i): [number, string] => [i, FIL(i)]));

  const params = (): Required<ParamsSim> => ({
    regle: E.s2.checked ? 's2' : 's1', pct: +E.pct.value / 100, q: +E.q.value / 100, sat: +E.sat.value / 100, sous: +E.sous.value / 100,
  });

  function remplir(t: HTMLTableElement, rows: LigneGroupe[], cells: (r: LigneGroupe) => string): void {
    const tb = tbody(t); tb.innerHTML = '';
    const moi = E.acad.value;  // académie choisie (adresse, profil ou menu) -> ligne surlignée
    rows.forEach((r) => {
      const tr = document.createElement('tr');
      if (t === E.tAcad) { if (r.idf) tr.classList.add('idf'); if (moi !== '' && r.key === +moi) tr.classList.add('moi'); }
      tr.innerHTML = cells(r); tb.appendChild(tr);
    });
    Spedago.sortable(t);
  }

  function render(): void {
    const p = params(), fil = E.filiere.value;
    E.pctOut.textContent = `${E.pct.value} %`;
    E.pctLabel.textContent = p.regle === 's1' ? 'Places ajoutées' : 'Plafond par formation';
    E.qOut.textContent = `${E.q.value} %`; E.satOut.textContent = `${E.sat.value} %`; E.sousOut.textContent = `${E.sous.value} %`;
    const res = C.simulate(D, p);
    const acad = C.groupBy(D, res, C.COL.A, fil).sort((a, b) => b.ajout / b.places - a.ajout / a.places);
    const tot = acad.reduce((s, r) => s + r.ajout, 0), pl = acad.reduce((s, r) => s + r.places, 0);
    const idf = acad.filter((r) => r.idf).reduce((s, r) => s + r.ajout, 0);
    const couv = fil === '' ? res.couvert : (res.couvertFil.get(+fil) || 0);
    const visees = acad.reduce((s, r) => s + r.visees, 0);
    E.summary.innerHTML = ([
      [fmtInt(tot), 'places ajoutées'],
      [pl ? fmtPct(tot / pl) : '–', 'des places de la sélection'],
      [tot ? fmtPct(idf / tot, 0) : '–', 'en Île-de-France'],
      [tot ? fmtPct(couv / tot, 0) : '–', 'récupérables sur des places vides'],
    ] as const).map(([v, l]) => `<div class="stat"><b>${v}</b><span>${l}</span></div>`).join('');
    Spedago.announce(E.summary.innerText);
    E.lecture.innerHTML = tot
      ? `${fmtInt(visees)} formations recevraient des places. Sur ces <strong>${fmtInt(tot)}</strong> places, au plus <strong>${fmtInt(couv)}</strong> pourraient venir de places restées vides dans une formation de même spécialité de la même académie ; le reste (${fmtInt(tot - couv)}) demanderait des moyens nouveaux.`
      : 'Aucune formation ne remplit les conditions avec ces réglages.';
    const dm = C.demande(D, res.add, fil);
    E.demande.innerHTML = tot && dm.formationsRang
      ? `<strong>Ces places trouveraient-elles preneur ?</strong> Dans <strong>${fmtPct(dm.couvertes / dm.formationsRang, 0)}</strong> des ${fmtInt(dm.formationsRang)} formations visées à liste d'appel propre, il restait au moins autant de candidats classés jamais appelés que de places ajoutées (médiane : ${fmtInt(dm.medianeRatio)} classés non appelés par place ajoutée). Ces chiffres comptent des candidatures, pas des personnes : un même candidat est classé dans plusieurs formations, et beaucoup ont été admis ailleurs. Ils disent que les places seraient remplies, pas combien d'élèves sans proposition en profiteraient.${dm.sansRang ? ` Pour ${fmtInt(dm.sansRang)} formations à liste commune (${fmtInt(dm.ajoutSansRang)} places), ce n'est pas mesurable.` : ''}`
      : '';
    const maxA = Math.max(...acad.map((r) => r.ajout / (r.places || 1)), 1e-9);
    remplir(E.tAcad, acad.filter((r) => r.places > 0), (r) => `<td data-v="${esc(D.academies[r.key])}">${esc(D.academies[r.key])}</td><td class="r" data-v="${r.places}">${fmtInt(r.places)}</td><td class="r" data-v="${r.ajout}">${fmtInt(r.ajout)}</td>
      <td class="barcell" data-v="${r.ajout / r.places}"><span class="sr-only">${fmtPct(r.ajout / r.places)}</span><div class="hbar" title="${fmtPct(r.ajout / r.places)}" aria-hidden="true"><span style="width:${(r.ajout / r.places) / maxA * 100}%"></span></div></td>`);
    const ac = E.acad.value, nomA = ac === '' ? '' : D.academies[+ac];
    E.hFil.textContent = nomA ? `Par filière · ${nomA}` : 'Par filière';
    const fils = C.groupBy(D, res, C.COL.FIL, fil, ac).filter((r) => r.places > 0).sort((a, b) => b.ajout - a.ajout);
    const cv = (k: number): number => (ac === '' ? res.couvertFil.get(k) : res.couvertAF.get(ac + '|' + k)) || 0;
    remplir(E.tFil, fils, (r) => `<td data-v="${esc(FIL(r.key))}">${esc(FIL(r.key))}</td><td class="r" data-v="${r.visees}">${fmtInt(r.visees)}</td><td class="r" data-v="${r.ajout}">${fmtInt(r.ajout)}</td><td class="r" data-v="${r.nonServis}">${fmtInt(r.nonServis)}</td><td class="r" data-v="${cv(r.key)}">${fmtInt(cv(r.key))}</td>`);
    const spe = C.groupBy(D, res, C.COL.SPE, fil, ac).filter((r) => r.ajout > 0).sort((a, b) => b.ajout - a.ajout).slice(0, 15);
    remplir(E.tSpe, spe, (r) => `<td data-v="${esc(D.specialites[r.key])}">${esc(D.specialites[r.key])}</td><td class="r" data-v="${r.ajout}">${fmtInt(r.ajout)}</td>`);
  }

  // Académie : adresse, sinon profil ; tous les réglages vont dans l'adresse (lien partageable)
  options(E.acad, D.academies.flatMap((a, i): [number, string][] => (a ? [[i, a]] : [])));
  Spedago.pick(E.acad);
  const saveState = Spedago.bind({ regle: E.s1, pct: E.pct, q: E.q, sat: E.sat, sous: E.sous, filiere: E.filiere });

  function reset(): void {
    E.pct.value = DEF.pct; E.q.value = DEF.q; E.sat.value = DEF.sat; E.sous.value = DEF.sous;
    E.s1.checked = true; E.filiere.value = DEF.filiere; saveState(); render();
  }
  // export du classement par académie (ordre affiché)
  E.exportAcad.addEventListener('click', () => Spedago.download('spedago-simulation-academies.csv', Spedago.csv(Spedago.tableRows(E.tAcad))));
  E.controls.addEventListener('input', render);
  E.controls.addEventListener('change', render);
  E.controls.addEventListener('submit', (e) => e.preventDefault());
  E.reset.addEventListener('click', reset);
  E.acad.addEventListener('change', () => Spedago.setHash(E.acad.value === '' ? '' : selectedText(E.acad)));
  window.addEventListener('hashchange', () => { if (!Spedago.pick(E.acad)) E.acad.value = ''; render(); });
  document.addEventListener('spedago:profil', () => { if (!Spedago.hashSlug() && Spedago.pick(E.acad)) render(); });
  render();
}

loadData<DonneesSimulateur>('simulateur').then(main);
