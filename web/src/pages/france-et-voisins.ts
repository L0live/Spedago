import '../styles/commun.css';
import '../styles/france-et-voisins.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { el, select, table, esc, options, stat } from '../lib/dom';
import { VoisinsCalc as C, type LigneRegion } from '../calc/voisins';
import type { DonneesVoisins } from '../types/donnees';

type Serie = ReturnType<typeof C.serie>;
type Point = Serie[number];

function main(D: DonneesVoisins): void {
  const M = D.mobilite;
  fillMeta({ an0: M.annees[0], an1: M.annees[M.annees.length - 1] });
  const fmtInt = (x: number | null | undefined): string => (x == null ? '–' : Math.round(x).toLocaleString('fr-FR'));
  const fmt1 = (x: number | null | undefined): string => (x == null ? '–' : x.toFixed(1).replace('.', ','));
  const flagTxt = (f: string): string => (f ? f.split('').filter((x) => D.drapeaux[x]).map((x) => D.drapeaux[x]).join(', ') : '');
  const E = { acad: select('acad'), tMob: table('t-mob'), tReg: table('t-reg') };

  // ---- chiffres clés
  const last = M.annees.length - 1, an = M.annees[last];
  const sortant = (c: string): number => M.sortants[c][last][0] || 0;
  const tot = M.pays.reduce((s, [c]) => s + sortant(c), 0);
  const ue = M.ue.find((x) => x[0] === an)?.[1];
  const top = [...M.pays].sort((a, b) => sortant(b[0]) - sortant(a[0]))[0];
  el('mob-stats').innerHTML = [
    stat('eu-mobilite', fmtInt(ue), `étudiants français en mobilité diplômante dans l’UE en ${an}`, 'comptés par le pays d’accueil'),
    stat('eu-mobilite', fmtInt(tot), `dans les ${M.pays.length} pays ci-dessous en ${an}, dont ${fmtInt(M.sortants.CH[last][0])} en Suisse (hors UE, d’où un total supérieur)`,
         'pays voisins publiant la donnée (pas les Pays-Bas)'),
    stat('eu-mobilite', esc(top[1]), `premier pays d’accueil en ${an} (${fmtInt(M.sortants[top[0]][last][0])})`, 'pays voisins publiant la donnée'),
  ].join('');

  // ---- petits multiples
  const W = 240, H = 120, P = { l: 34, r: 6, t: 8, b: 18 };
  M.pays.forEach(([c, nom]) => {
    const s = C.serie(D, c), vmax = Math.max(1, ...s.flatMap((r) => [r.sortants || 0, r.entrants || 0]));
    const step = Math.pow(10, Math.floor(Math.log10(vmax))), top = Math.ceil(vmax / step) * step;
    const x = (i: number): number => P.l + i * (W - P.l - P.r) / (s.length - 1);
    const y = (v: number): number => H - P.b - v / top * (H - P.t - P.b);
    const path = (k: 'sortants' | 'entrants'): string => {
      let d = '', on = false;
      s.forEach((r, i) => { const v = r[k]; if (v == null) { on = false; return; } d += (on ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); on = true; });
      return d;
    };
    const flags = (k: 'sortants' | 'entrants', fk: 'flagS' | 'flagE'): string =>
      s.map((r, i) => { const v = r[k]; return r[fk] && v != null ? `<circle class="flag" cx="${x(i).toFixed(1)}" cy="${y(v).toFixed(1)}" r="4"/>` : ''; }).join('');
    const lastS: Point | undefined = [...s].reverse().find((r) => r.sortants != null);
    const lastE: Point | undefined = [...s].reverse().find((r) => r.entrants != null);
    const box = document.createElement('div'); box.className = 'panel';
    box.innerHTML = `<h3>${esc(nom)}</h3><p class="last">${lastS ? `${fmtInt(lastS.sortants)} Français (${lastS.annee})` : '–'} · ${lastE ? `${fmtInt(lastE.entrants)} venus en France` : '–'}</p>
      <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(nom)} : Français inscrits de ${fmtInt(s.find((r) => r.sortants != null)?.sortants)} à ${fmtInt(lastS?.sortants)} entre ${s[0].annee} et ${lastS?.annee}">
        <g class="grid">${[0, top / 2, top].map((v) => `<line x1="${P.l}" x2="${W - P.r}" y1="${y(v)}" y2="${y(v)}"/>`).join('')}</g>
        <g class="axis">${[0, top / 2, top].map((v) => `<text x="${P.l - 4}" y="${y(v) + 3}" text-anchor="end">${v >= 1000 ? fmt1(v / 1000).replace(',0', '') + ' k' : v}</text>`).join('')}
          <text x="${P.l}" y="${H - 4}">${s[0].annee}</text><text x="${W - P.r}" y="${H - 4}" text-anchor="end">${s[s.length - 1].annee}</text></g>
        <path d="${path('entrants')}" class="l-in" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="${path('sortants')}" class="l-out" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        ${flags('sortants', 'flagS')}${flags('entrants', 'flagE')}
        <line class="cross" y1="${P.t}" y2="${H - P.b}" x1="-10" x2="-10"/>
        <rect x="${P.l}" y="0" width="${W - P.l - P.r}" height="${H}" fill="transparent"/>
      </svg><div class="tip" hidden></div>`;
    const svg = box.querySelector('svg')!, cross = box.querySelector('.cross')!, tip = box.querySelector<HTMLElement>('.tip')!;
    svg.addEventListener('pointermove', (e) => {
      const r = svg.getBoundingClientRect(), px = (e.clientX - r.left) / r.width * W;
      const i = Math.max(0, Math.min(s.length - 1, Math.round((px - P.l) / ((W - P.l - P.r) / (s.length - 1))))), d = s[i];
      cross.setAttribute('x1', String(x(i))); cross.setAttribute('x2', String(x(i)));
      tip.innerHTML = `<b>${d.annee}</b><br>Français dans ce pays : <b>${fmtInt(d.sortants)}</b>${d.flagS ? ` (${esc(flagTxt(d.flagS))})` : ''}<br>Venus en France : <b>${fmtInt(d.entrants)}</b>${d.flagE ? ` (${esc(flagTxt(d.flagE))})` : ''}`;
      tip.hidden = false; tip.style.left = Math.max(4, Math.min(box.clientWidth - tip.offsetWidth - 4, x(i) / W * r.width + 12)) + 'px'; tip.style.top = '40px';
    });
    svg.addEventListener('pointerleave', () => { tip.hidden = true; cross.setAttribute('x1', '-10'); cross.setAttribute('x2', '-10'); });
    el('multiples').appendChild(box);
  });
  // tableau (alternative accessible et détail des drapeaux)
  const sens = ['sortants', 'entrants'] as const;
  E.tMob.innerHTML = `<caption class="sr-only">Étudiants en mobilité diplômante par année</caption><thead><tr><th>Pays</th><th>Sens</th>${M.annees.map((a) => `<th class="r">${a}</th>`).join('')}</tr></thead><tbody>${
    M.pays.map(([c, nom]) => sens.map((k) => `<tr><td>${esc(nom)}</td><td>${k === 'sortants' ? 'Français dans ce pays' : 'Venus en France'}</td>${
      M[k][c].map(([v, f]) => `<td class="r">${fmtInt(v)}${f ? `<sup title="${esc(flagTxt(f))}"> ${esc(f)}</sup>` : ''}</td>`).join('')}</tr>`).join('')).join('')}</tbody>`;
  el('mob-note').textContent = `Signalements Eurostat : ${Object.entries(D.drapeaux).map(([k, v]) => `${k} = ${v}`).join(' ; ')}. Répartition ${an} des Français par niveau (licence / master / doctorat) : ` +
    M.pays.map(([c, nom]) => { const n = M.niveaux[c]; return n[1] == null ? null : `${nom} ${fmtInt(n[1])} / ${fmtInt(n[2])} / ${fmtInt(n[3])}`; }).filter(Boolean).join(' ; ') + '.';

  // ---- régions
  const ROLES: Record<LigneRegion['role'], string> = { moi: "Région de l’académie", voisine: 'Voisine', ref: 'Référence' };
  options(E.acad, D.academies.map(([nom], i): [number, string] => [i, nom]));
  if (!Spedago.pick(E.acad)) E.acad.value = String(Math.max(0, D.academies.findIndex((a) => a[1] === 'strasbourg')));
  function renderReg(): void {
    const ai = +E.acad.value, a = D.academies[ai], nv = a[3].length;
    el('reg-note').textContent = nv ? `${nv} région${nv > 1 ? 's' : ''} voisine${nv > 1 ? 's' : ''}` : "Pas de frontière terrestre avec un pays couvert : comparaison avec la France et l’Union européenne.";
    el('dots').innerHTML = D.indicateurs.map(([key, lib, sensInd]) => {
      const rows = C.lignes(D, ai, key), vmax = Math.max(...rows.map((r) => r.v)) * 1.1;
      return `<div><h3>${esc(lib)}</h3><p class="sens">${sensInd === 'haut' ? "Plus c’est haut, plus les jeunes adultes sont diplômés du supérieur." : "Plus c’est bas, mieux c’est."} Échelle de 0 à ${fmt1(vmax)} %.</p>
        ${rows.map((r) => `<div class="drow ${r.role}"><span class="nom">${esc(r.nom)}${r.role === 'ref' ? '' : ` <small class="u">${esc(D.noms_pays[r.code.slice(0, 2)] || '')}</small>`}${r.u ? ' <small class="u">(peu fiable)</small>' : ''}</span>
          <span class="track" title="${esc(r.nom)} : ${fmt1(r.v)} % (moyenne ${r.de}-${r.a}, ${fmt1(r.dernier)} % en ${r.a})"><span style="left:${(r.v / vmax * 100).toFixed(1)}%"></span></span>
          <span class="val">${fmt1(r.v)} %</span></div>`).join('')}</div>`;
    }).join('');
    const all = D.indicateurs.map(([k]) => C.lignes(D, ai, k));
    E.tReg.innerHTML = `<caption class="sr-only">Indicateurs des régions</caption><thead><tr><th>Région ou pays</th><th>Rôle</th>${D.indicateurs.map(([, lib]) => `<th class="r">${esc(lib)}</th>`).join('')}</tr></thead><tbody>${
      all[0].map((l0) => `<tr><td>${esc(D.regions[l0.code].nom)} <small class="u">${l0.code}</small></td><td>${ROLES[l0.role]}</td>${
        all.map((rows) => { const r = rows.find((x) => x.code === l0.code); return `<td class="r">${r ? fmt1(r.v) + ' %' + (r.u ? ' *' : '') : '–'}</td>`; }).join('')}</tr>`).join('')}</tbody>`;
    Spedago.announce(`Académie de ${a[0]} : ${nv} régions voisines`);
  }
  E.acad.addEventListener('change', () => { Spedago.setHash(D.academies[+E.acad.value][0]); renderReg(); });
  el<HTMLFormElement>('pick').addEventListener('submit', (e) => e.preventDefault());
  window.addEventListener('hashchange', () => { if (Spedago.pick(E.acad)) renderReg(); });
  document.addEventListener('spedago:profil', () => { if (!Spedago.hashSlug() && Spedago.pick(E.acad)) renderReg(); });
  el('export').addEventListener('click', () => {
    const ai = +E.acad.value;
    const out: (string | number)[][] = [['Académie', 'Code', 'Région ou pays', 'Rôle', 'Indicateur', 'Moyenne 3 ans (%)', 'Dernière valeur (%)', 'Années', 'Peu fiable']];
    D.indicateurs.forEach(([k, lib]) => C.lignes(D, ai, k).forEach((r) => out.push([D.academies[ai][0], r.code, r.nom, r.role, lib, r.v, r.dernier, `${r.de}-${r.a}`, r.u ? 'oui' : ''])));
    Spedago.download(`spedago-voisins-${D.academies[ai][1]}.csv`, Spedago.csv(out));
  });
  renderReg();
}

loadData<DonneesVoisins>('voisins').then(main);
