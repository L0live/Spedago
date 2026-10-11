import '../styles/commun.css';
import '../styles/boussole-des-masters.css';
import { Spedago, type Profil } from '../lib/commun';
import { loadData } from '../lib/data';
import { el, input, select, table, tbody, esc, options, selectedText } from '../lib/dom';
import { BoussoleCalc as C } from '../calc/boussole';
import type { DonneesBoussole, FormationMaster } from '../types/donnees';

type Vue = 'mention' | 'inverse';
/** Insertion InserSup d'une formation : [taux, diplômés, promotion, salaire médian | null] */
type Insertion = [number, number, string, number | null];
interface LigneFormation { f: FormationMaster; n: number; k: number; p: number; lo: number; hi: number; brut: number; ni: number; ki: number; ne: number; ke: number }

function main(D: DonneesBoussole): void {
  const S = D.sessions, MIN = D.min_candidats;
  const fmtPct = (x: number): string => (x * 100).toFixed(x < 0.1 ? 1 : 0).replace('.', ',') + ' %';
  const fmtInt = (x: number): string => x.toLocaleString('fr-FR');
  const PROFILS_CHOIX = ['lg3', 'but3', 'lp3', 'master', 'autre', 'noninscri'];
  const level = (p: number): string => (p >= 0.3 ? 'hi' : p >= 0.1 ? 'mid' : 'lo');
  const LAST = S.length - 1, ANNEE = S[LAST];
  const ouverte = (f: FormationMaster): boolean => f[7][LAST] != null;
  const counts = (f: FormationMaster, profil: string): [number, number] => C.counts(f, profil, D.profils, S);
  const E = { mention: input('mention'), academie: select('academie'), secteur: select('secteur'), profil: select('profil'),
              modalite: select('modalite'), tri: select('tri'), list: el('list'), summary: el('summary'), insider: el('insider'),
              count: el('count'), more: el('more'), countInv: el('count-inv'), rank: table('rank'), moreInv: el('more-inv'),
              tabMention: el('tab-mention'), tabInverse: el('tab-inverse'), vueMention: el('vue-mention'), vueInverse: el('vue-inverse'),
              labMention: el('lab-mention'), labSecteur: el('lab-secteur'), mysel: el('mysel'), tSel: table('t-sel') };

  // ---- options
  const dl = el('mentions');
  D.mentions.forEach((m) => { if (m) { const o = document.createElement('option'); o.value = m; dl.appendChild(o); } });
  options(E.academie, D.academies.flatMap((a, i): [number, string][] => (a ? [[i, a]] : [])));
  Spedago.pick(E.academie);  // #poitiers dans l'adresse -> académie présélectionnée
  options(E.secteur, D.secteurs.flatMap((a, i): [number, string][] => (a ? [[i, a]] : [])));
  options(E.profil, PROFILS_CHOIX.map((p): [string, string] => [p, D.libelles_profils[p]]));
  const mentionIndex = new Map(D.mentions.map((m, i) => [m.toUpperCase(), i]));

  // ---- insertion (InserSup) : taux de la mention dans l'établissement, repère national de la mention
  const INS = D.insertion || { formations: {}, mentions: {}, mois: 18 };
  const insOf = (f: FormationMaster): Insertion | null => INS.formations[String(f[0])] || null;
  function insertion(f: FormationMaster): string {
    const x = insOf(f), nat = INS.mentions[String(f[3])];
    if (!x) return '<span>Insertion : <em>non publiée</em></span>';
    return `<span>En emploi salarié ${INS.mois} mois après le diplôme : <em>${fmtPct(x[0])}</em> (promo ${x[2]}, ${fmtInt(x[1])} diplômés${x[3] ? `, salaire net médian ${fmtInt(x[3])} €` : ''})${nat != null ? ` · mention, France : ${fmtPct(nat)}` : ''}</span>`;
  }

  // ---- Ma sélection (ce navigateur)
  const SKEY = 'spedago.selection', byIfc = new Map(D.formations.map((f) => [String(f[0]), f]));
  let selection_ = new Set<string>();
  try {
    const brut: unknown = JSON.parse(localStorage.getItem(SKEY) ?? 'null');
    if (Array.isArray(brut)) selection_ = new Set(brut.map(String).filter((x) => byIfc.has(x)));
  } catch { /* vide */ }
  const saveSel = (): void => { try { localStorage.setItem(SKEY, JSON.stringify([...selection_])); } catch { /* indisponible */ } };

  // ---- vue « par mention »
  let shown = 30, vue: Vue = 'mention', shownInv = 40, started = false;
  function selectionMention(): FormationMaster[] | null {
    const m = mentionIndex.get(E.mention.value.trim().toUpperCase());
    const a = E.academie.value, mod = E.modalite.value;
    if (m === undefined) return null;
    return D.formations.filter((f) => f[3] === m && (a === '' || f[2] === +a) && (mod === '' || f[5] === +mod));
  }

  function renderMention(): void {
    const sel = selectionMention(), profil = E.profil.value;
    E.list.innerHTML = '';
    if (!sel) {
      E.summary.innerHTML = ''; E.insider.hidden = true; E.count.textContent = '';
      E.list.innerHTML = '<p class="empty">Choisissez une mention dans la liste proposée.</p>'; E.more.hidden = true; return;
    }
    const rows: LigneFormation[] = sel.map((f) => {
      const [n, k, p, lo, hi] = C.estimate(D, f, profil);
      const [ni, ki] = counts(f, 'etab'), [ne, ke] = counts(f, 'hors_etab');
      return { f, n, k, p, lo, hi, brut: n > 0 ? k / n : NaN, ni, ki, ne, ke };
    });
    let N = 0, K = 0, places = 0, NI = 0, KI = 0, NE = 0, KE = 0;
    rows.forEach((r) => {
      N += r.n; K += r.k; places += r.f[7][LAST] || 0;
      if (r.ni >= MIN && r.ne >= MIN) { NI += r.ni; KI += r.ki; NE += r.ne; KE += r.ke; }
    });
    const tau = N ? K / N : NaN;
    const valid = rows.filter((r) => !isNaN(r.p)).map((r) => r.p).sort((a, b) => a - b);
    const med = valid.length ? valid[Math.floor(valid.length / 2)] : NaN;
    E.summary.innerHTML = ([
      [fmtInt(rows.length), 'formations'],
      [fmtInt(places), `places en ${ANNEE}`],
      [isNaN(tau) ? '–' : fmtPct(tau), 'taux global pour votre profil'],
      [isNaN(med) ? '–' : fmtPct(med), "estimation médiane d'une formation"],
    ] as [string, string][]).map(([v, l]) => `<div class="stat"><b>${v}</b><span>${l}</span></div>`).join('');
    if (NI && NE) {
      E.insider.hidden = false;
      E.insider.innerHTML = `Dans cette sélection, les candidats déjà inscrits dans l'établissement du master ont reçu une proposition dans <strong>${fmtPct(KI / NI)}</strong> des cas, contre <strong>${fmtPct(KE / NE)}</strong> pour les autres (tous profils confondus, formations où les deux groupes ont au moins ${MIN} candidats).`;
    } else E.insider.hidden = true;

    const tri = E.tri.value;
    const key = (r: LigneFormation): number => (isNaN(r.p) ? -1 : tri === 'prudent' ? r.lo : r.p);
    const insV = (f: FormationMaster): number => insOf(f)?.[0] ?? -1;
    rows.sort((a, b) => (Number(ouverte(b.f)) - Number(ouverte(a.f))) || (tri === 'places' ? (b.f[7][LAST] || 0) - (a.f[7][LAST] || 0)
      : tri === 'insertion' ? insV(b.f) - insV(a.f)
      : tri === 'nom' ? D.etablissements[a.f[1]].localeCompare(D.etablissements[b.f[1]], 'fr')
      : key(b) - key(a)));
    E.count.textContent = `${fmtInt(rows.length)} formation${rows.length > 1 ? 's' : ''} · profil : ${D.libelles_profils[profil]}`;
    Spedago.announce(E.count.textContent);

    const frag = document.createDocumentFragment();
    rows.slice(0, shown).forEach((r) => {
      const f = r.f, art = document.createElement('article'); art.className = 'row';
      const pl = f[7][LAST], rang = f[8][LAST], peu = r.n > 0 && r.n < MIN;
      const rate = isNaN(r.p)
        ? '<div class="na">Aucun candidat de votre profil en 2024-2025</div>'
        : `<div class="rate"><div class="num"><b>${fmtPct(r.p)}</b><span>${fmtPct(r.lo)} – ${fmtPct(r.hi)}</span></div>
           <div class="bar" role="img" aria-label="Estimation ${fmtPct(r.p)}, intervalle ${fmtPct(r.lo)} à ${fmtPct(r.hi)}">
           <span class="ci ${level(r.p)}" style="left:${r.lo * 100}%;width:${(r.hi - r.lo) * 100}%"></span>
           <span class="pt ${level(r.p)}" style="left:calc(${r.p * 100}% - 1px)"></span></div>
           <div class="num"><span>Observé : ${r.k} / ${fmtInt(r.n)} candidats (${fmtPct(r.brut)})${peu ? ' · peu de candidats, estimation proche de la moyenne de la mention' : ''}</span></div></div>`;
      const ins = r.ni >= MIN && r.ne >= MIN
        ? `<span>Internes <em>${fmtPct(r.ki / r.ni)}</em> · autres <em>${fmtPct(r.ke / r.ne)}</em></span>` : '';
      const kept = selection_.has(f[0]);
      art.innerHTML = `<div style="min-width:0"><h3>${esc(D.etablissements[f[1]])}</h3>
        <button type="button" class="star" data-ifc="${esc(f[0])}" aria-pressed="${kept}">${kept ? '★ Gardé' : '☆ Garder'}<span class="sr-only"> : ${esc(D.etablissements[f[1]])}, ${esc(f[4] || 'parcours non précisé')}</span></button>
        <div class="meta"><span>${esc(f[4] || 'Parcours non précisé')}</span><span>${esc(D.academies[f[2]])}</span>${f[5] ? '<span class="tag">Alternance</span>' : ''}${ouverte(f) ? '' : `<span class="tag">Non proposée en ${ANNEE}</span>`}</div></div>
        ${rate}
        <div class="sub"><span>Places ${ANNEE} : <em>${pl ?? '–'}</em></span><span>Dernier appelé ${ANNEE} (phase principale) : <em>${rang != null ? 'rang ' + fmtInt(rang) : '–'}</em></span>${ins}${insertion(f)}</div>`;
      frag.appendChild(art);
    });
    E.list.appendChild(frag);
    E.more.hidden = rows.length <= shown;
  }

  // ---- vue inversée
  function renderInverse(): void {
    const profil = E.profil.value;
    const rows = C.rankMentions(D, profil, { academie: E.academie.value, modalite: E.modalite.value, secteur: E.secteur.value });
    E.countInv.textContent = `${fmtInt(rows.length)} mention${rows.length > 1 ? 's' : ''} classée${rows.length > 1 ? 's' : ''} · profil : ${D.libelles_profils[profil]}`;
    Spedago.announce(E.countInv.textContent);
    const tb = tbody(E.rank);
    tb.innerHTML = rows.length ? '' : '<tr><td colspan="5" class="empty">Aucune mention avec assez de candidats de votre profil pour cette sélection.</td></tr>';
    rows.slice(0, shownInv).forEach((g) => {
      const tr = document.createElement('tr'); tr.dataset.mention = D.mentions[g.mention];
      const best = g.best ? `${esc(D.etablissements[g.best.etab])}<small>${esc(g.best.parcours || 'Parcours non précisé')} · ${fmtPct(g.best.p)}</small>` : '–';
      tr.innerHTML = `<td class="mention"><button type="button" class="linklike">${esc(D.mentions[g.mention])}</button><small>${fmtInt(g.n)} candidats de votre profil</small></td>
        <td class="r">${fmtInt(g.formations)}</td><td class="r">${fmtInt(g.places)}</td>
        <td><div class="mini"><span><b>${fmtPct(g.p)}</b> <small style="display:inline">(${fmtPct(g.lo)} – ${fmtPct(g.hi)})</small></span>
          <div class="bar"><span class="ci ${level(g.p)}" style="left:${g.lo * 100}%;width:${(g.hi - g.lo) * 100}%"></span><span class="pt ${level(g.p)}" style="left:calc(${g.p * 100}% - 1px)"></span></div></div></td>
        <td>${best}</td>`;
      tb.appendChild(tr);
    });
    E.moreInv.hidden = rows.length <= shownInv;
  }

  function renderSel(): void {
    E.mysel.hidden = selection_.size === 0; if (E.mysel.hidden) return;
    const profil = E.profil.value, tb = tbody(E.tSel); tb.innerHTML = '';
    selection_.forEach((ifc) => {
      const f = byIfc.get(ifc); if (!f) return;
      const [n, k, p, lo, hi] = C.estimate(D, f, profil), x = insOf(f), rang = f[8][LAST], tr = document.createElement('tr');
      tr.innerHTML = `<td data-v="${esc(D.etablissements[f[1]])}"><span class="v">${esc(D.etablissements[f[1]])}</span><small>${esc(D.mentions[f[3]])} · ${esc(f[4] || 'parcours non précisé')} · ${esc(D.academies[f[2]])}</small></td>
        <td class="r" data-v="${f[7][LAST] ?? ''}">${f[7][LAST] ?? '–'}</td>
        <td class="r" data-v="${isNaN(p) ? '' : p}">${isNaN(p) ? '–' : fmtPct(p)}<small>${isNaN(p) ? 'aucun candidat de ce profil' : `${fmtPct(lo)} – ${fmtPct(hi)}`}</small></td>
        <td class="r" data-v="${n ? k / n : ''}">${n ? `${k} / ${fmtInt(n)}` : '–'}</td>
        <td class="r" data-v="${rang ?? ''}">${rang != null ? 'rang ' + fmtInt(rang) : '–'}</td>
        <td class="r" data-v="${x ? x[0] : ''}">${x ? fmtPct(x[0]) : '–'}<small>${x ? 'promo ' + x[2] : 'non publiée'}</small></td>
        <td><button type="button" class="btn-ghost" data-remove="${esc(f[0])}">Retirer<span class="sr-only"> ${esc(D.etablissements[f[1]])}</span></button></td>`;
      tb.appendChild(tr);
    });
    Spedago.sortable(E.tSel);
  }

  const render = (): void => { if (vue === 'mention') renderMention(); else renderInverse(); renderSel(); };

  function setVue(v: Vue): void {
    vue = v;
    E.tabMention.setAttribute('aria-selected', String(v === 'mention'));
    E.tabInverse.setAttribute('aria-selected', String(v === 'inverse'));
    E.tabMention.tabIndex = v === 'mention' ? 0 : -1; E.tabInverse.tabIndex = v === 'inverse' ? 0 : -1;
    if (started) Spedago.setParams({ vue: v === 'inverse' ? 'inverse' : '' });
    E.vueMention.hidden = v !== 'mention'; E.vueInverse.hidden = v !== 'inverse';
    E.labMention.hidden = v !== 'mention'; E.labSecteur.hidden = v !== 'inverse';
    render();
  }

  document.addEventListener('click', (e) => {
    if (!(e.target instanceof Element)) return;
    const s = e.target.closest<HTMLElement>('.star'), r = e.target.closest<HTMLElement>('[data-remove]');
    const ifc = s ? s.dataset.ifc : r ? r.dataset.remove : undefined; if (!ifc) return;
    if (selection_.has(ifc)) selection_.delete(ifc); else selection_.add(ifc);
    saveSel(); render(); Spedago.announce(`${selection_.size} master${selection_.size > 1 ? 's' : ''} dans votre sélection`);
  });
  el('sel-clear').addEventListener('click', () => { selection_.clear(); saveSel(); render(); Spedago.announce('Sélection vidée'); });
  el('sel-export').addEventListener('click', () => {
    const profil = E.profil.value;
    const rows: (string | number | null)[][] = [['Établissement', 'Mention', 'Parcours', 'Académie', `Places ${ANNEE}`, 'Estimation', 'Bas', 'Haut', 'Candidats du profil', 'Propositions', `Dernier appelé ${ANNEE}`, `Emploi salarié ${INS.mois} mois`, 'Promotion', 'Diplômés', 'Salaire médian', 'Profil']];
    selection_.forEach((ifc) => {
      const f = byIfc.get(ifc); if (!f) return;
      const [n, k, p, lo, hi] = C.estimate(D, f, profil), x = insOf(f);
      rows.push([D.etablissements[f[1]], D.mentions[f[3]], f[4], D.academies[f[2]], f[7][LAST], p, lo, hi, n, k, f[8][LAST],
                 x ? x[0] : null, x ? x[2] : null, x ? x[1] : null, x ? x[3] : null, D.libelles_profils[profil]]);
    });
    Spedago.download('spedago-ma-selection-masters.csv', Spedago.csv(rows));
  });

  const reinit = (): void => { shown = 30; shownInv = 40; render(); };
  E.mention.addEventListener('input', reinit);
  for (const c of [E.academie, E.profil, E.modalite, E.tri, E.secteur]) c.addEventListener('change', reinit);
  el<HTMLFormElement>('filters').addEventListener('submit', (e) => e.preventDefault());
  E.academie.addEventListener('change', () => Spedago.setHash(E.academie.value === '' ? '' : selectedText(E.academie)));
  window.addEventListener('hashchange', () => { if (!Spedago.pick(E.academie)) E.academie.value = ''; render(); });
  E.more.addEventListener('click', () => { shown += 30; render(); });
  E.moreInv.addEventListener('click', () => { shownInv += 40; render(); });
  E.tabMention.addEventListener('click', () => setVue('mention'));
  E.tabInverse.addEventListener('click', () => setVue('inverse'));
  // Onglets au clavier : flèches gauche/droite, Début/Fin (motif ARIA « tabs »)
  document.querySelector<HTMLElement>('.tabs')?.addEventListener('keydown', (e) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;
    e.preventDefault();
    const next: Vue = e.key === 'Home' ? 'mention' : e.key === 'End' ? 'inverse' : (vue === 'mention' ? 'inverse' : 'mention');
    setVue(next); (next === 'mention' ? E.tabMention : E.tabInverse).focus();
  });
  E.rank.addEventListener('click', (e) => {
    const tr = e.target instanceof Element ? e.target.closest<HTMLTableRowElement>('tr[data-mention]') : null; if (!tr) return;
    E.mention.value = tr.dataset.mention ?? ''; shown = 30; setVue('mention'); window.scrollTo({ top: 0 });
  });

  // État initial : adresse, sinon profil, sinon exemple réel (modifiable)
  E.mention.value = 'INFORMATIQUE';
  const pm = Spedago.profil().profilMaster;
  E.profil.value = pm && [...E.profil.options].some((o) => o.value === pm) ? pm : 'lg3';
  Spedago.bind({ mention: E.mention, profil: E.profil, modalite: E.modalite, tri: E.tri, secteur: E.secteur });
  document.addEventListener('spedago:profil', (e) => {
    const q = (e as CustomEvent<Profil>).detail.profilMaster;
    if (q && !Spedago.param('profil')) { E.profil.value = q; render(); }
  });
  setVue(Spedago.param('vue') === 'inverse' || location.hash === '#inverse' ? 'inverse' : 'mention');
  started = true;
}

loadData<DonneesBoussole>('boussole').then(main);
