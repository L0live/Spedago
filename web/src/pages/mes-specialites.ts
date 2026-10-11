import '../styles/commun.css';
import '../styles/mes-specialites.css';
import { Spedago, type Profil } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { el, input, select, table, tbody, esc, fmtInt, options, stat } from '../lib/dom';
import { SpeCalc as C, type LigneSpe } from '../calc/mes-specialites';
import type { DonneesSpecialites } from '../types/donnees';

type Tri = 'demande' | 'chances' | 'ecart' | 'nom';

function main(D: DonneesSpecialites): void {
  fillMeta({ annee: D.annee, rentree: D.rentree_carte });
  const fmtPct = (x: number, d = 0): string => (isFinite(x) ? (x * 100).toFixed(d).replace('.', ',') + ' %' : '–');
  const fmtPts = (x: number): string => {
    if (!isFinite(x)) return '–';
    const p = Math.abs(Math.round(x * 100));
    return (x > 0 ? '+' : x < 0 ? '−' : '') + p + ' pt' + (p > 1 ? 's' : '');
  };
  const norm = (s: string): string => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const EDS = D.eds, IDS = EDS.map((e) => e[0]);
  const byUai = new Map(D.lycees.map((l, i) => [l[0], i]));
  const E = { s1: select('s1'), s2: select('s2'), fam: select('fam'), tri: select('tri'), q: input('q'), lyc: input('lyc'),
              stats: el('stats'), count: el('count'), tG: table('t-g'), bDetail: el('b-detail'), hDetail: el('h-detail'), detail: el('detail'),
              more: el('more'), bLycee: el('b-lycee'), hLycee: el('h-lycee'), lycee: el('lycee') };

  // ---- options
  for (const s of [E.s1, E.s2]) options(s, EDS.map((e): [string, string] => [e[0], e[1]]));
  options(E.fam, [...new Set(D.groupes.map((g) => g[2]))].map((f): [string, string] => [f, f]));
  const datalist = el('lycees');
  D.lycees.forEach((l) => { const o = document.createElement('option'); o.value = `${l[1]} — ${l[2]}`; datalist.appendChild(o); });
  const byLabel = new Map(D.lycees.map((l, i) => [`${l[1]} — ${l[2]}`, i]));
  // valeurs de départ : profil, sinon exemple (la doublette la plus suivie)
  const pr = Spedago.profil().specialites || [];
  E.s1.value = IDS.includes(pr[0]) ? pr[0] : 'maths'; E.s2.value = IDS.includes(pr[1]) ? pr[1] : 'pc';
  const save = Spedago.bind({ s1: E.s1, s2: E.s2, fam: E.fam, tri: E.tri, q: E.q });
  const lp = Spedago.param('lyc'), lpi = lp ? byUai.get(lp) : undefined;
  if (lpi !== undefined) { const l = D.lycees[lpi]; E.lyc.value = `${l[1]} — ${l[2]}`; }

  let all = false, ouvert: number | null = null;
  const dIdx = (): number => C.doublette(D, IDS.indexOf(E.s1.value), IDS.indexOf(E.s2.value));
  const nomD = (): string => `${EDS[IDS.indexOf(E.s1.value)][1]} + ${EDS[IDS.indexOf(E.s2.value)][1]}`;

  function lignes(): LigneSpe[] {
    const d = dIdx(); if (d < 0) return [];
    const fam = E.fam.value, q = norm(E.q.value.trim()), tri = E.tri.value as Tri;
    const rows = C.groupes(D, d).filter((r) => r.n > 0 && (!fam || D.groupes[r.key][2] === fam)
      && (!q || norm(D.groupes[r.key][1]).includes(q) || D.formations.some((f) => f[0] === r.key && norm(f[1]).includes(q))));
    const CLES: Record<Tri, (r: LigneSpe) => number> = {
      demande: (r) => -r.n, chances: (r) => -(isNaN(r.lo) ? -1 : r.lo),
      ecart: (r) => -(isNaN(r.lo) || isNaN(r.pO) ? -9 : r.lo - r.pO),  // écart prudent : bas de l'intervalle
      nom: () => 0 };
    const key = CLES[tri] ?? CLES.demande;
    rows.sort((a, b) => key(a) - key(b) || D.groupes[a.key][1].localeCompare(D.groupes[b.key][1], 'fr'));
    return rows;
  }

  function cells(r: LigneSpe, nom: string, sous: string): string {
    const ec = isFinite(r.ecart) && Math.abs(r.ecart) >= 0.05 ? (r.ecart > 0 ? 'pos' : 'neg') : '';
    const meter = isFinite(r.p) ? `<div class="meter" aria-hidden="true"><span style="width:${(r.p * 100).toFixed(1)}%"></span>${isFinite(r.pO) ? `<i style="left:calc(${(r.pO * 100).toFixed(1)}% - 1px)"></i>` : ''}</div>` : '';
    return `<td data-v="${esc(nom)}">${sous}</td>
      <td class="r" data-l="Élèves comme vous" data-v="${r.n}">${fmtInt(r.n)}<small>${fmtPct(r.part, 1)} de votre doublette</small></td>
      <td class="r" data-l="Ont reçu une proposition" data-v="${isFinite(r.p) ? r.p : ''}">${fmtPct(r.p)}${meter}<small>${r.n >= 30 ? `${fmtPct(r.lo)} – ${fmtPct(r.hi)}` : 'peu de candidats'}</small></td>
      <td class="r" data-l="Autres bacheliers" data-v="${isFinite(r.pO) ? r.pO : ''}">${fmtPct(r.pO)}<small>${fmtInt(r.nO)} cand.</small></td>
      <td class="r ${ec}" data-l="Écart" data-v="${isFinite(r.ecart) ? r.ecart : ''}">${fmtPts(r.ecart)}</td>`;
  }

  function render(): void {
    const d = dIdx(), tb = tbody(E.tG); tb.innerHTML = '';
    if (d < 0) {
      E.stats.innerHTML = ''; E.count.textContent = '';
      tb.innerHTML = '<tr><td colspan="5" class="empty">Pas de données pour cette combinaison : choisissez deux spécialités différentes qui peuvent être suivies ensemble.</td></tr>';
      E.bDetail.hidden = true; renderLycee(); return;
    }
    const s = C.resume(D, d);
    E.stats.innerHTML = [
      stat('spe-propositions', fmtInt(s.n), `bacheliers généraux avec ${esc(nomD())} en ${D.annee} (${fmtPct(s.part, 1)}, ${s.rang === 1 ? '1re' : s.rang + 'e'} doublette sur ${s.nb})`,
           'bacheliers généraux, niveau national'),
      stat('spe-propositions', fmtPct(s.k / s.n, 1), `ont reçu au moins une proposition (tous bacheliers généraux : ${fmtPct(s.pTous, 1)})`, 'candidats ayant confirmé un vœu'),
      stat('spe-propositions', fmtInt(C.groupes(D, d).filter((r) => r.n > 0).length), 'types de formation demandés au moins une fois', 'doublette choisie, niveau national'),
    ].join('');
    const rows = lignes(), shown = all ? rows : rows.slice(0, 25);
    shown.forEach((r) => {
      const g = D.groupes[r.key], tr = document.createElement('tr'); if (ouvert === r.key) tr.className = 'cur';
      tr.innerHTML = cells(r, g[1], `<button type="button" class="linklike" data-g="${r.key}" aria-expanded="${ouvert === r.key}" aria-controls="b-detail">${esc(g[1])}</button><small>${esc(g[2])}</small>`);
      tb.appendChild(tr);
    });
    if (!rows.length) tb.innerHTML = '<tr><td colspan="5" class="empty">Aucune formation ne correspond à ces filtres.</td></tr>';
    Spedago.sortable(E.tG);
    E.more.hidden = all || rows.length <= 25;
    E.count.textContent = `${fmtInt(rows.length)} type${rows.length > 1 ? 's' : ''} de formation · ${nomD()} · cliquez un nom pour le détail par formation`;
    Spedago.announce(`${fmtInt(rows.length)} types de formation pour ${nomD()}`);
    renderDetail(); renderLycee();
  }

  function renderDetail(): void {
    const d = dIdx();
    if (ouvert === null || d < 0) { E.bDetail.hidden = true; return; }
    const g = D.groupes[ouvert], rows = C.fines(D, d, ouvert).filter((r) => r.n > 0).sort((a, b) => b.n - a.n);
    E.hDetail.textContent = g[1];
    const t = D.tendance[`${d}|${ouvert}`] || [];
    const trend = t.length > 1 ? `<p class="note">Part ayant reçu une proposition, élèves comme vous, par année du bac :</p><div class="trend">${t.map(([y, v, p]) => `<span>${y} : ${v ? fmtPct(p / v) : '–'} <small>(${fmtInt(v)})</small></span>`).join('')}</div>` : '';
    E.detail.innerHTML = `${trend}
      <div class="tablewrap" tabindex="0" role="region" aria-label="Formations du regroupement (défilant)"><table id="t-f"><caption class="sr-only">Formations de ${esc(g[1])}</caption>
      <thead><tr><th>Formation</th><th class="r">Élèves comme vous</th><th class="r">Ont reçu une proposition</th><th class="r">Autres bacheliers</th><th class="r">Écart</th></tr></thead>
      <tbody>${rows.map((r) => `<tr>${cells(r, D.formations[r.key][1], esc(D.formations[r.key][1]))}</tr>`).join('') || '<tr><td colspan="5" class="empty">Pas de détail.</td></tr>'}</tbody></table></div>`;
    Spedago.sortable(table('t-f'));
    E.bDetail.hidden = false;
  }

  function renderLycee(): void {
    const li = byLabel.get(E.lyc.value);
    if (li === undefined) { E.bLycee.hidden = true; return; }
    const l = D.lycees[li], res = C.lycee(D, li, [IDS.indexOf(E.s1.value), IDS.indexOf(E.s2.value)]), ival = l[6];
    E.hLycee.textContent = `${l[1]} (${l[2]})`;
    const pts = (va: number): string => `${va > 0 ? '+' : va < 0 ? '−' : ''}${Math.abs(va)} pt${Math.abs(va) > 1 ? 's' : ''}`;
    E.lycee.innerHTML = `<ul>${res.map((r) => {
      const nom = esc(EDS[r.eds][1]);
      if (r.etat === 'propose') return `<li><span class="ok">✓ Proposée</span> ${nom}</li>`;
      if (r.etat === 'incertain') return `<li><span class="unk">? Incertain</span> ${nom} <small class="note">(effectif masqué par le secret statistique)</small></li>`;
      if (r.etat !== 'absent') return `<li><span class="unk">– Non couverte</span> ${nom} <small class="note">(pas dans les données de la carte)</small></li>`;
      const ni = r.uai ? byUai.get(r.uai) : undefined, near = ni !== undefined ? D.lycees[ni] : null;
      return `<li><span class="ko">✗ Pas proposée</span> ${nom}${near ? ` — la plus proche : <strong>${esc(near[1])}</strong> (${esc(near[2])}), ${String(r.km).replace('.', ',')} km à vol d’oiseau` : ''}</li>`;
    }).join('')}</ul><p class="note">Offre de 1re (rentrée ${D.rentree_carte}), même statut public/privé pour le lycée le plus proche. <a href="mutualisation.html#${Spedago.slug(l[3])}">Voir la carte des spécialités →</a></p>
      ${ival ? `<h3 class="h3">Résultats du lycée au bac ${D.annee_ival}</h3><div class="ival">${([
        ['Réussite au bac', ival[0], ival[1]], ['Élèves de 2de qui obtiennent le bac dans le lycée', ival[2], ival[3]], ['Mentions', ival[4], ival[5]],
      ] as [string, number | null, number | null][]).map(([t, v, va]) => `<div><b>${v == null ? '–' : Math.round(v) + ' %'}</b><span>${t}</span><small>${va == null ? 'valeur ajoutée non publiée' : `valeur ajoutée ${pts(va)}`}</small></div>`).join('')}</div>
      <p class="note">Valeur ajoutée : écart entre le résultat du lycée et celui attendu compte tenu de ses élèves (âge, origine sociale, résultats au brevet). Positive : le lycée fait mieux que prévu.</p>` : ''}`;
    E.bLycee.hidden = false;
  }

  E.tG.addEventListener('click', (e) => {
    const b = e.target instanceof Element ? e.target.closest<HTMLElement>('[data-g]') : null; if (!b) return;
    const g = +(b.dataset.g ?? -1); ouvert = ouvert === g ? null : g; render();
    if (ouvert !== null) { E.bDetail.scrollIntoView({ block: 'start' }); E.hDetail.setAttribute('tabindex', '-1'); E.hDetail.focus(); }
  });
  E.more.addEventListener('click', () => { all = true; render(); });
  el<HTMLFormElement>('filters').addEventListener('submit', (e) => e.preventDefault());
  for (const s of [E.s1, E.s2, E.fam, E.tri]) s.addEventListener('change', () => { ouvert = null; render(); });
  E.q.addEventListener('input', () => { render(); });
  E.lyc.addEventListener('input', () => { const li = byLabel.get(E.lyc.value); if (li !== undefined) Spedago.setParams({ lyc: D.lycees[li][0] }); renderLycee(); });
  el('export').addEventListener('click', () => {
    const d = dIdx(); if (d < 0) return;
    const out: (string | number)[][] = [['Doublette', 'Type de formation', 'Famille', 'Élèves comme moi ayant demandé', 'Part de la doublette', 'Ont reçu une proposition', 'Bas', 'Haut', 'Autres bacheliers : part', 'Écart (points)']];
    lignes().forEach((r) => out.push([nomD(), D.groupes[r.key][1], D.groupes[r.key][2], r.n, r.part, r.p, r.lo, r.hi, r.pO, r.ecart * 100]));
    Spedago.download(`spedago-${E.s1.value}-${E.s2.value}-formations.csv`, Spedago.csv(out));
  });
  document.addEventListener('spedago:profil', (e) => {
    const s = ((e as CustomEvent<Profil>).detail.specialites) || [];
    if (s.length === 2 && !Spedago.param('s1')) { E.s1.value = s[0]; E.s2.value = s[1]; save(); render(); }
  });
  render();
}

loadData<DonneesSpecialites>('mes_specialites').then(main);
