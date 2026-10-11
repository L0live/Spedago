import '../styles/commun.css';
import '../styles/mutualisation.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { el, input, select, table, tbody, esc, fmtInt, options, stat, resumeStats } from '../lib/dom';
import { MutCalc } from '../calc/mutualisation';
import type { DonneesCarte, LyceeCarte } from '../types/donnees';

/** Codes de situation : 0 proposée, 2 incertaine, 3 accès voisin, 4 ouverture commune, 5 isolé. */
type Code = 0 | 2 | 3 | 4 | 5;

function main(D: DonneesCarte): void {
  fillMeta({ rentree: D.rentree, rayon: Math.round(D.rayon_km), seuil: D.seuil });
  const NS = 'http://www.w3.org/2000/svg';
  const LIB = (s: string): string => (D.libelles_specialites || {})[s] || s.replace(/_/g, ' ').replace(/\bsc\b/g, 'sciences').replace(/^./, (c) => c.toUpperCase());
  const CAT: Record<Code, [string, string]> = { 0: ['Proposée', '--offre'], 3: ['Accès voisin', '--voisin'], 4: ['Ouverture commune', '--commun'], 5: ['Sans solution proche', '--isole'], 2: ['Incertain', '--incertain'] };
  const R: Record<Code, number> = { 0: 2, 2: 1.8, 3: 2.4, 4: 3.6, 5: 3.8 };
  const OPA: Record<Code, number> = { 0: 0.45, 2: 0.9, 3: 0.65, 4: 1, 5: 1 };
  const L = D.lycees, I = { uai: 0, nom: 1, com: 2, stat: 3, acad: 4, bassin: 5, lat: 6, lon: 7, eff: 8, st: 9, near: 10 } as const;
  const code = (l: LyceeCarte, sp: number): Code => l[I.st][sp] as Code;
  const idx = new Map(L.map((l, i) => [l[I.uai], i]));
  const lyceeUai = (uai: string): LyceeCarte | null => { const i = idx.get(uai); return i === undefined ? null : L[i]; };
  const E = { spe: select('spe'), statut: select('statut'), acad: select('acad'), montrer: select('montrer'), cherche: input('cherche'),
              map: el('map') as unknown as SVGSVGElement, counts: el('counts'), groups: el('groups'), gTitle: el('g-title'), fiche: el('fiche'),
              tLyc: table('t-lyc'), moreLyc: el('more-lyc'), listeNote: el('liste-note') };

  // ---- projection (métropole) : équirectangulaire corrigée de la latitude moyenne
  const LAT0 = 46.5, K = Math.cos(LAT0 * Math.PI / 180), BOX = { lon: [-5.3, 9.7], lat: [41.2, 51.2] };
  const W = 600, H = 620, PAD = 10;
  const sx = (W - 2 * PAD) / ((BOX.lon[1] - BOX.lon[0]) * K), sy = (H - 2 * PAD) / (BOX.lat[1] - BOX.lat[0]), s = Math.min(sx, sy);
  const px = (lon: number): number => PAD + (lon - BOX.lon[0]) * K * s, py = (lat: number): number => H - PAD - (lat - BOX.lat[0]) * s;
  const inMetro = (l: LyceeCarte): boolean => l[I.lat] > 41 && l[I.lat] < 51.5 && l[I.lon] > -5.5 && l[I.lon] < 10;

  // ---- options
  options(E.spe, D.specialites.map((sp, i): [number, string] => [i, LIB(sp)]));
  options(E.acad, [...new Set(L.map((l) => l[I.acad]))].sort((a, b) => a.localeCompare(b, 'fr')).map((a): [string, string] => [a, a]));
  Spedago.pick(E.acad);  // #poitiers dans l'adresse -> académie présélectionnée
  const datalist = el('lycees');
  L.forEach((l) => { const o = document.createElement('option'); o.value = `${l[I.nom]} — ${l[I.com]}`; datalist.appendChild(o); });
  const byLabel = new Map(L.map((l, i) => [`${l[I.nom]} — ${l[I.com]}`, i]));
  el('legend').innerHTML = ([0, 3, 4, 5, 2] as const).map((c) => `<span><i style="--c:var(${CAT[c][1]})${c === 2 ? ';background:none;border:1.5px solid var(--incertain)' : ''}"></i>${CAT[c][0]}</span>`).join('');

  // ---- carte
  const svg = E.map, gLines = document.createElementNS(NS, 'g'), gDots = document.createElementNS(NS, 'g');
  svg.append(gLines, gDots);
  const dots: (SVGCircleElement | null)[] = L.map((l, i) => {
    if (!inMetro(l)) return null;
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', px(l[I.lon]).toFixed(1)); c.setAttribute('cy', py(l[I.lat]).toFixed(1));
    c.dataset.i = String(i); c.appendChild(document.createElementNS(NS, 'title')); gDots.appendChild(c); return c;
  });
  let selected: number | null = null;
  let zf = 1;

  const visible = (l: LyceeCarte): boolean => MutCalc.visible(l, E.statut.value, E.acad.value);

  function render(): void {
    const sp = +E.spe.value, { n, eleves } = MutCalc.summary(D, sp, E.statut.value, E.acad.value);
    L.forEach((l, i) => {
      const c = code(l, sp), d = dots[i];
      if (!d) return;
      d.style.display = visible(l) ? '' : 'none';
      // Hiérarchie : « sans solution » et « ouverture commune » ressortent ; « incertain » = anneau vide (forme, pas seulement couleur)
      d.setAttribute('r', (R[c] * zf).toFixed(2));
      d.style.fill = c === 2 ? 'none' : `var(${CAT[c][1]})`;
      d.style.stroke = c === 2 ? 'var(--incertain)' : c >= 4 ? 'var(--surface)' : 'none';
      d.style.strokeWidth = String(c === 2 ? 1 : c >= 4 ? 0.8 : 0);
      d.style.opacity = String(OPA[c]);
      if (d.firstChild) d.firstChild.textContent = `${l[I.nom]} (${l[I.com]}) — ${CAT[c][0]}`;
      d.classList.toggle('sel', selected === i);
    });
    // les points « problème » au-dessus
    [3, 4, 5].forEach((c) => L.forEach((l, i) => { const d = dots[i]; if (d && code(l, sp) === c) gDots.appendChild(d); }));
    const ds = selected !== null ? dots[selected] : null; if (ds) gDots.appendChild(ds);
    E.counts.innerHTML = ([[0, n[0], 'lycées la proposent'], [3, n[3], `sans elle · voisin à moins de ${D.rayon_km} km`],
      [4, n[4], 'sans elle · ouverture commune possible'], [5, n[5], `sans elle · rien à moins de ${D.rayon_km} km (${fmtInt(eleves[5])} élèves de 1re)`]] as [Code, number, string][])
      .map(([c, v, t]) => stat(c === 0 ? 'spe-offre' : 'spe-mutualisation', fmtInt(v), t,
                               c === 0 ? 'lycées de 1re générale, filtres choisis' : "même statut, distance à vol d’oiseau", 'stat count', `--c:var(${CAT[c][1]})`)).join('');
    Spedago.announce(resumeStats(E.counts));
    renderListe();
    // groupes
    gLines.innerHTML = '';
    const grs = MutCalc.groups(D, sp, E.statut.value, E.acad.value);
    E.gTitle.textContent = `Ouvertures communes possibles (${grs.length})`;
    E.groups.innerHTML = grs.length ? '' : '<p class="empty">Aucune pour cette spécialité et cette sélection.</p>';
    grs.forEach((g) => {
      const pts = g[1].filter((m) => dots[m]).map((m) => [px(L[m][I.lon]), py(L[m][I.lat])]);
      for (let k = 1; k < pts.length; k++) {
        const ln = document.createElementNS(NS, 'line'); ln.setAttribute('class', 'grp');
        ln.setAttribute('x1', String(pts[0][0])); ln.setAttribute('y1', String(pts[0][1])); ln.setAttribute('x2', String(pts[k][0])); ln.setAttribute('y2', String(pts[k][1])); gLines.appendChild(ln);
      }
      const b = document.createElement('button'); b.type = 'button'; b.className = 'group';
      b.innerHTML = `<b>${fmtInt(g[2])} élèves estimés</b> · ${g[1].length} lycées · ${String(g[3]).replace('.', ',')} km au plus<small>${g[1].map((m) => esc(`${L[m][I.nom]} (${L[m][I.com]})`)).join(' · ')}</small>`;
      b.addEventListener('click', () => choisir(g[1][0]));
      E.groups.appendChild(b);
    });
    renderFiche();
  }

  function renderFiche(): void {
    if (selected === null) { E.fiche.innerHTML = '<h2>Fiche lycée</h2><p class="empty">Cliquez un point sur la carte ou cherchez un lycée.</p>'; return; }
    const l = L[selected];
    const rows = D.specialites.map((sp, j) => {
      const c = code(l, j), nr = l[I.near][j], proche = nr ? lyceeUai(nr[1]) : null;
      const extra = nr ? `${String(nr[0]).replace('.', ',')} km · ${esc(proche ? proche[I.nom] : nr[1])}` : '';
      return `<div><span>${esc(LIB(sp))}</span><small><span class="pill" style="--c:var(${CAT[c][1]})">${CAT[c][0]}</span>${extra ? '<br>Plus proche : ' + extra : ''}</small></div>`;
    }).join('');
    E.fiche.innerHTML = `<h2>${esc(l[I.nom])}</h2><dl><dt>Commune</dt><dd>${esc(l[I.com])}</dd><dt>Académie</dt><dd>${esc(l[I.acad])}</dd>
      <dt>Statut</dt><dd>${esc(l[I.stat])}</dd>${l[I.bassin] ? `<dt>Bassin</dt><dd>${esc(l[I.bassin])}</dd>` : ''}<dt>Élèves de 1re</dt><dd>${fmtInt(l[I.eff])}</dd></dl>
      <div class="spes">${rows}</div>`;
  }

  // ---- zoom sur l'académie choisie (cadre des lycées de métropole visibles)
  function zoom(): void {
    const ac = E.acad.value, pts = ac ? L.filter((l) => l[I.acad] === ac && inMetro(l)) : [];
    if (!pts.length) { svg.setAttribute('viewBox', `0 0 ${W} ${H}`); zf = 1; return; }
    const xs = pts.map((l) => px(l[I.lon])), ys = pts.map((l) => py(l[I.lat]));
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const w = Math.max(x1 - x0, 40) * 1.4 + 12, h = Math.max(y1 - y0, 40) * 1.4 + 12, side = Math.max(w, h * W / H);
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    svg.setAttribute('viewBox', `${(cx - side / 2).toFixed(1)} ${(cy - side * H / W / 2).toFixed(1)} ${side.toFixed(1)} ${(side * H / W).toFixed(1)}`);
    zf = Math.max(0.25, Math.pow(side / W, 0.75));
  }
  // ---- liste des lycées de la sélection
  let shownLyc = 100;
  const SIT: Record<Code, string> = { 0: 'La propose', 2: 'Incertain (effectif masqué)', 3: 'Voisin à moins de ' + D.rayon_km + ' km', 4: 'Ouverture commune possible', 5: 'Sans solution proche' };
  function lycRows(): [LyceeCarte, number][] {
    const sp = +E.spe.value, m = E.montrer.value;
    return L.map((l, i): [LyceeCarte, number] => [l, i])
      .filter(([l]) => visible(l) && (m === 'tous' || (m === 'isole' ? code(l, sp) === 5 : [3, 4, 5].includes(code(l, sp)))))
      .sort((a, b) => code(b[0], sp) - code(a[0], sp) || b[0][I.eff] - a[0][I.eff]);
  }
  function renderListe(): void {
    const sp = +E.spe.value, rows = lycRows(), tb = tbody(E.tLyc); tb.innerHTML = '';
    rows.slice(0, shownLyc).forEach(([l, i]) => {
      const c = code(l, sp), nr = l[I.near][sp], near = nr ? lyceeUai(nr[1]) : null, tr = document.createElement('tr');
      tr.innerHTML = `<td data-v="${esc(l[I.nom])}"><button type="button" class="linklike" data-lyc="${i}">${esc(l[I.nom])}</button><small>${esc(l[I.com])}</small></td>
        <td data-v="${esc(l[I.acad])}">${esc(l[I.acad])}</td><td data-v="${esc(l[I.stat])}">${esc(l[I.stat])}</td>
        <td class="r" data-v="${l[I.eff]}">${fmtInt(l[I.eff])}</td>
        <td data-v="${c}"><span class="pill" style="--c:var(${CAT[c][1]})">${SIT[c]}</span></td>
        <td class="r" data-v="${nr ? nr[0] : ''}">${nr ? `${String(nr[0]).replace('.', ',')} km` : '–'}${near ? `<small>${esc(near[I.nom])}</small>` : ''}</td>`;
      tb.appendChild(tr);
    });
    Spedago.sortable(E.tLyc);
    E.moreLyc.hidden = rows.length <= shownLyc;
    E.listeNote.textContent = `${fmtInt(rows.length)} lycée${rows.length > 1 ? 's' : ''}${rows.length > shownLyc ? `, ${fmtInt(shownLyc)} affichés (l’export les contient tous)` : ''} · ${LIB(D.specialites[sp])}`;
  }
  E.tLyc.addEventListener('click', (e) => {
    const b = e.target instanceof Element ? e.target.closest<HTMLElement>('[data-lyc]') : null;
    if (b) { choisir(+(b.dataset.lyc ?? 0)); E.fiche.scrollIntoView({ block: 'nearest' }); }
  });
  E.moreLyc.addEventListener('click', () => { shownLyc += 200; renderListe(); });
  E.montrer.addEventListener('change', () => { shownLyc = 100; renderListe(); });
  el('export-lyc').addEventListener('click', () => {
    const sp = +E.spe.value;
    const out: (string | number)[][] = [['UAI', 'Lycée', 'Commune', 'Académie', 'Statut', 'Élèves de 1re', 'Spécialité', 'Situation', 'Offre la plus proche (km)', 'Lycée le plus proche']];
    lycRows().forEach(([l]) => {
      const nr = l[I.near][sp], near = nr ? lyceeUai(nr[1]) : null;
      out.push([l[I.uai], l[I.nom], l[I.com], l[I.acad], l[I.stat], l[I.eff], LIB(D.specialites[sp]), SIT[code(l, sp)], nr ? nr[0] : '', near ? near[I.nom] : '']);
    });
    Spedago.download(`spedago-lycees-${D.specialites[sp]}.csv`, Spedago.csv(out));
  });

  function choisir(i: number): void { selected = i; render(); }
  gDots.addEventListener('click', (e) => {
    const c = e.target instanceof Element ? e.target.closest<SVGCircleElement>('circle') : null;
    if (c) choisir(+(c.dataset.i ?? 0));
  });
  const filtres = el<HTMLFormElement>('filters');
  filtres.addEventListener('change', render);
  filtres.addEventListener('submit', (e) => e.preventDefault());
  E.acad.addEventListener('change', () => { Spedago.setHash(E.acad.value); zoom(); shownLyc = 100; render(); });
  window.addEventListener('hashchange', () => { if (!Spedago.pick(E.acad)) E.acad.value = ''; zoom(); render(); });
  document.addEventListener('spedago:profil', () => { if (!Spedago.hashSlug() && Spedago.pick(E.acad)) { zoom(); render(); } });
  E.cherche.addEventListener('input', () => { const i = byLabel.get(E.cherche.value); if (i !== undefined) choisir(i); });

  // État initial : spécialité NSI, premier groupe sélectionné (exemple réel)
  const nsi = D.specialites.indexOf('numerique_et_sciences_informatiques');
  E.spe.value = String(nsi >= 0 ? nsi : 0);
  Spedago.bind({ spe: E.spe, statut: E.statut, montrer: E.montrer });
  zoom();
  const g0 = MutCalc.groups(D, +E.spe.value, '', E.acad.value)[0];  // premier groupe (de l'académie choisie, s'il y en a une)
  selected = g0 ? g0[1][0] : null;
  render();
}

loadData<DonneesCarte>('mutualisation').then(main);
