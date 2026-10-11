import '../styles/commun.css';
import '../styles/mon-academie.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { el, select, esc, fmtInt, options } from '../lib/dom';
import { AcadCalc as C } from '../calc/mon-academie';
import type { AcademieFiche, DonneesAcademie, OffrePrivee, PoursuiteAcad } from '../types/donnees';

/** Fiche de comparaison : une académie ou la France entière (sans slug ni zone). */
type Fiche = Omit<AcademieFiche, 'slug' | 'zone'>;

function main(D: DonneesAcademie): void {
  fillMeta({ rentree_po: D.rentree_poursuite, session: D.session });
  const fmtPct = (x: number, d = 0): string => (isFinite(x) ? (x * 100).toFixed(d).replace('.', ',') + ' %' : '–');
  const fmtDec = (x: number, d = 1): string => (isFinite(x) ? x.toFixed(d).replace('.', ',') : '–');
  const FIL = (i: number): string => (D.libelles_filieres || {})[D.filieres[i]] || D.filieres[i];
  const SPE = (i: number): string => (D.libelles_specialites || {})[D.specialites[i]] || D.specialites[i];
  const link = (page: string, a: AcademieFiche, txt: string): string => `<a class="more" href="${page}#${a.slug}">${txt} →</a>`;
  const plural = (n: number, w: string): string => `${fmtInt(n)} ${w}${n > 1 ? 's' : ''}`;
  const E = { acad: select('acad'), cmp: select('cmp'), stats: el('stats'), zone: el('zone'),
              ps: el('ps'), prive: el('prive'), po: el('po'), spe: el('spe'), mm: el('mm') };

  // ---- sélecteurs : académie (adresse, sinon profil, sinon exemple) et point de comparaison
  for (const s of [E.acad, E.cmp]) options(s, D.academies.map((a, i): [number, string] => [i, a.nom]));
  if (!Spedago.pick(E.acad)) E.acad.value = String(Math.max(0, C.indexOf(D, 'poitiers')));
  const cmpParam = Spedago.param('cmp');
  if (cmpParam && cmpParam !== 'fr') { const i = C.indexOf(D, cmpParam); if (i >= 0) E.cmp.value = String(i); }
  const cmpObj = (): Fiche => (E.cmp.value === 'fr' ? D.france : D.academies[+E.cmp.value]);
  const cmpNom = (): string => (E.cmp.value === 'fr' ? 'France' : D.academies[+E.cmp.value].nom);

  function stats(a: AcademieFiche): void {
    const r = a.ref || [0, 0, 0, 0, 0, 0], p = a.ps ? C.ps(a.ps.total) : null, m = a.mm ? C.mm(a.mm.total) : null;
    const k = cmpObj(), kp = k.ps ? C.ps(k.ps.total) : null;
    const cards: [string, string][] = [
      [fmtInt(r[0]), `lycées, dont ${fmtInt(r[1])} avec une 1re générale`],
      [p ? fmtInt(p.places) : '–', p ? `places Parcoursup ${D.session} dans ${plural(p.formations, 'formation')}` : 'pas de formation Parcoursup'],
      [p ? fmtDec(p.vpp) : '–', p && kp ? `vœux par place (${cmpNom()} : ${fmtDec(kp.vpp)})` : 'vœux par place'],
      [m ? fmtInt(m.places) : '–', m ? `places en master ${D.session} dans ${plural(m.formations, 'formation')}` : 'pas de master sur la plateforme'],
    ];
    E.stats.innerHTML = cards.map(([b, t]) => `<div class="stat"><b>${b}</b><span>${t}</span></div>`).join('');
  }

  const toolbar = (id: string, label: string): string => `<div class="toolbar"><span class="note">Cliquez un en-tête pour trier.</span><button type="button" class="btn-ghost" data-export="${id}">Exporter ${label} (CSV)</button></div>`;
  const trier = (id: string): void => Spedago.sortable(el(id));

  function blocPs(a: AcademieFiche): void {
    if (!a.ps) { E.ps.innerHTML = '<p class="empty">Pas de formation Parcoursup recensée dans cette académie.</p>'; return; }
    const k = cmpObj(), nom = cmpNom();
    if (!k.ps || !D.france.ps) { E.ps.innerHTML = "<p class=\"empty\">Pas de formation Parcoursup dans l'académie de comparaison.</p>"; return; }
    const t = C.ps(a.ps.total), f = C.ps(k.ps.total), ref = new Map(k.ps.filieres.map((r) => [r[0], C.ps(r.slice(1))]));
    const [ajout, couvert, visees] = a.ps.sim, [ajFr, coFr] = D.france.ps.sim;
    const rows = a.ps.filieres.map((r) => {
      const x = C.ps(r.slice(1)), n = ref.get(r[0]);
      const chaud = !!n && x.partSat > n.partSat + 0.1, hot = chaud ? ' class="r hot"' : ' class="r"';
      const meter = n ? `<div class="meter${chaud ? ' hot' : ''}" aria-hidden="true"><span style="width:${(x.partSat * 100).toFixed(1)}%"></span><i style="left:calc(${(n.partSat * 100).toFixed(1)}% - 1px)"></i></div>` : '';
      const vs = (v: number | undefined, fmt: (x: number) => string): string => (n && v !== undefined ? `<small>${esc(nom)} ${fmt(v)}</small>` : `<small>absent de ${esc(nom)}</small>`);
      return `<tr><td data-v="${esc(FIL(r[0]))}">${esc(FIL(r[0]))}<small>${plural(x.formations, 'formation')}</small></td>
        <td class="r" data-l="Places" data-v="${x.places}">${fmtInt(x.places)}</td>
        <td class="r" data-l="Vœux par place" data-v="${x.vpp}">${fmtDec(x.vpp)}${vs(n?.vpp, (v) => fmtDec(v))}</td>
        <td class="r" data-l="Places pourvues" data-v="${x.remp}">${fmtPct(x.remp)}${vs(n?.remp, (v) => fmtPct(v))}</td>
        <td${hot} data-l="Dans des formations pleines" data-v="${x.partSat}">${chaud ? '<span aria-hidden="true">▲ </span><span class="sr-only">nettement au-dessus : </span>' : ''}${fmtPct(x.partSat)}${meter}${vs(n?.partSat, (v) => fmtPct(v))}</td></tr>`;
    }).join('');
    E.ps.innerHTML = `
      <p>${fmtInt(t.places)} places et ${fmtInt(t.voeux)} vœux confirmés, soit <strong>${fmtDec(t.vpp)} vœux par place</strong> (${esc(nom)} : ${fmtDec(f.vpp)}).
      ${fmtPct(t.partSat)} des places sont dans des formations pleines à 95 % ou plus (${esc(nom)} : ${fmtPct(f.partSat)}) ; ${fmtInt(t.vac)} places sont restées vacantes.</p>
      ${toolbar('ps', 'la tension par filière')}
      <div class="tablewrap"><table id="t-ps"><caption class="sr-only">Tension Parcoursup par filière, comparée à ${esc(nom)}</caption><thead><tr><th>Filière</th><th class="r">Places</th><th class="r">Vœux par place</th><th class="r">Places pourvues</th><th class="r">Places dans des formations pleines</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note"><span class="hot">▲ en orange</span> : au moins 10 points au-dessus de ${esc(nom)} pour la même filière. Barre : ${esc(a.nom)} ; trait : ${esc(nom)}.</p>
      <div class="simbox"><span class="tag">Simulation ·</span>
      Avec la règle de départ du simulateur (+${fmtPct(D.alpha)} de places aux formations pleines et parmi les plus demandées de leur filière),
      l'académie recevrait <strong>+${fmtInt(ajout)} places</strong> dans ${plural(visees, 'formation')}, soit ${fmtPct(ajout / ajFr, 1)} des places ajoutées en France.
      ${ajout ? `Au plus ${fmtInt(couvert)} (${fmtPct(couvert / ajout)}) pourraient venir de places restées vides dans une formation de même spécialité de l'académie (France : ${fmtPct(coFr / ajFr)}).` : ''}
      ${link('simulateur-parcoursup.html', a, 'Changer la règle dans le simulateur')}</div>`;
    trier('t-ps');
  }

  // ---- offre publique / privée sur Parcoursup, hors apprentissage et en apprentissage (fiche « ps-prive »)
  function blocPrive(a: AcademieFiche): void {
    const p = a.prive;
    if (!p || (!p.hors_app && !p.app)) { E.prive.innerHTML = '<p class="empty">Pas de formation Parcoursup recensée dans cette académie.</p>'; return; }
    const k = cmpObj().prive, nom = cmpNom();
    const lignes: [string, OffrePrivee | undefined, OffrePrivee | undefined][] = [
      ['Hors apprentissage', p.hors_app, k?.hors_app], ['En apprentissage', p.app, k?.app],
      ['Ensemble', C.somme(p.hors_app, p.app), k ? C.somme(k.hors_app, k.app) : undefined]];
    const rows = lignes.map(([lib, t, tk]) => {
      const x = C.prive(t), y = tk ? C.prive(tk) : null;
      const cmp = (v: number | undefined): string => (y && v !== undefined ? `<small>${esc(nom)} ${fmtPct(v)}</small>` : '');
      return `<tr${lib === 'Ensemble' ? ' class="total"' : ''}><td data-v="${lib}">${lib}</td>
        <td class="r" data-l="Formations" data-v="${x.formations}">${fmtInt(x.formations)}</td>
        <td class="r" data-l="Privées" data-v="${x.part}"><strong>${fmtPct(x.part)}</strong>${cmp(y?.part)}</td>
        <td class="r" data-l="Dont hors contrat" data-v="${x.partHorsContrat}">${fmtPct(x.partHorsContrat)}${cmp(y?.partHorsContrat)}</td>
        <td class="r" data-l="Places" data-v="${x.places}">${fmtInt(x.places)}</td>
        <td class="r" data-l="Places dans le privé" data-v="${x.partPlaces}">${fmtPct(x.partPlaces)}${cmp(y?.partPlaces)}</td></tr>`;
    }).join('');
    const h = C.prive(p.hors_app), ap = C.prive(p.app);
    E.prive.innerHTML = `
      <p>Hors apprentissage, <strong>${fmtPct(h.part)}</strong> des formations proposées sur Parcoursup dans l'académie sont privées ;
      en apprentissage, <strong>${fmtPct(ap.part)}</strong>. La part du privé dépend donc d'abord du périmètre : un chiffre cité sans dire lequel est trompeur.</p>
      ${toolbar('prive', "l'offre publique et privée")}
      <div class="tablewrap"><table id="t-prive"><caption class="sr-only">Formations et places Parcoursup portées par le privé, comparées à ${esc(nom)}</caption><thead><tr><th>Périmètre</th><th class="r">Formations</th><th class="r">Formations privées</th><th class="r">dont hors contrat</th><th class="r">Places</th><th class="r">Places dans le privé</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note">Privé : sous contrat, enseignement supérieur privé et hors contrat. Les formations privées qui recrutent hors Parcoursup ne sont pas comptées. <a href="methodes.html#ps-prive">Méthode</a></p>`;
    trier('t-prive');
  }

  function blocSpe(a: AcademieFiche): void {
    if (!a.spe) { E.spe.innerHTML = '<p class="empty">Pas de lycée de cette académie sur la carte des spécialités (effectifs ou coordonnées absents).</p>'; return; }
    const spe = a.spe, k = cmpObj(), nom = cmpNom(), kr = k.spe ? k.spe.spe : null, kl = k.spe ? k.spe.lycees : 0;
    const rows = C.speRows(spe.spe).map((r) => {
      const part = r.isole / spe.lycees, kp = kr ? kr[r.sp][4] / kl : NaN;
      return `<tr><td data-v="${esc(SPE(r.sp))}">${esc(SPE(r.sp))}</td>
      <td class="r" data-l="La proposent" data-v="${r.propose}">${fmtInt(r.propose)}${r.incertain ? `<small>+ ${fmtInt(r.incertain)} incertain${r.incertain > 1 ? 's' : ''}</small>` : ''}</td>
      <td class="r" data-l="Voisin à moins de 20 km" data-v="${r.voisin}">${fmtInt(r.voisin)}</td>
      <td class="r" data-l="Ouverture commune" data-v="${r.commune}">${fmtInt(r.commune)}<small>${plural(r.groupes, 'groupe')}</small></td>
      <td class="r${r.isole ? ' hot' : ''}" data-l="Sans solution proche" data-v="${r.isole}">${fmtInt(r.isole)}<small>${fmtInt(r.eIsole)} élèves de 1re</small></td>
      <td class="r" data-l="Part sans solution" data-v="${part}">${fmtPct(part)}<small>${esc(nom)} ${fmtPct(kp)}</small></td></tr>`;
    }).join('');
    const tot = spe.spe.reduce((s, r) => s + r[4], 0);
    E.spe.innerHTML = `
      <p>${fmtInt(spe.lycees)} lycées avec une 1re générale (rentrée ${D.rentree}). Pour chaque spécialité, combien la proposent, et pour les autres :
      un lycée voisin à moins de 20 km, une ouverture commune possible avec d'autres lycées, ou aucune solution proche.
      ${tot ? '' : '<strong>Aucun cas « sans solution proche » dans l\'académie.</strong>'}</p>
      ${toolbar('spe', "l'accès aux spécialités")}
      <div class="tablewrap"><table id="t-spe"><caption class="sr-only">Accès aux spécialités de 1re générale</caption><thead><tr><th>Spécialité</th><th class="r">La proposent</th><th class="r">Voisin à moins de 20 km</th><th class="r">Ouverture commune possible</th><th class="r">Sans solution proche</th><th class="r">Part des lycées sans solution</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note">« Incertain » : effectif masqué par le secret statistique, la spécialité est probablement proposée.</p>
      ${link('mutualisation.html', a, 'Voir les lycées sur la carte')}`;
    trier('t-spe');
  }

  function blocMm(a: AcademieFiche): void {
    if (!a.mm) { E.mm.innerHTML = '<p class="empty">Pas de master de cette académie sur la plateforme nationale.</p>'; return; }
    const k = cmpObj(), nom = cmpNom(), t = C.mm(a.mm.total), f = k.mm ? C.mm(k.mm.total) : null;
    const rows = a.mm.mentions.map(([m, nf, pl, n, kk, nN, kN]) => {
      const [lo, hi] = C.wilson(kk, n);
      return `<tr><td class="mention" data-v="${esc(m)}">${esc(m)}<small>${plural(nf, 'formation')}</small></td><td class="r" data-l="Places" data-v="${pl}">${fmtInt(pl)}</td>
        <td class="r" data-l="Proposition, L3 générale" data-v="${n ? kk / n : ''}">${n ? fmtPct(kk / n) : '–'}<small>${n ? `entre ${fmtPct(lo)} et ${fmtPct(hi)} · ${fmtInt(n)} cand.` : 'aucun candidat'}</small></td>
        <td class="r" data-l="Même mention, France" data-v="${kN / nN}">${fmtPct(kN / nN)}</td></tr>`;
    }).join('');
    E.mm.innerHTML = `
      <p>${fmtInt(t.formations)} formations, ${fmtInt(t.places)} places, ${fmtInt(t.cand)} candidatures : <strong>${fmtPct(t.taux)}</strong> ont reçu une proposition d'admission${f ? ` (${esc(nom)} : ${fmtPct(f.taux)})` : ''}.
      Pour les candidatures venant d'une 3e année de licence générale : ${fmtPct(t.tauxL3)}${f ? ` (${esc(nom)} : ${fmtPct(f.tauxL3)})` : ''}.</p>
      ${toolbar('mm', 'les mentions')}
      <div class="tablewrap"><table id="t-mm"><caption class="sr-only">Masters : mentions qui offrent le plus de places</caption><thead><tr><th>Mentions qui offrent le plus de places</th><th class="r">Places</th><th class="r">Proposition, L3 générale</th><th class="r">Même mention, France</th></tr></thead><tbody>${rows}</tbody></table></div>
      ${link('boussole-des-masters.html', a, 'Comparer les masters avec la Boussole')}`;
    trier('t-mm');
  }

  function blocPo(a: AcademieFiche): void {
    if (!a.pours) { E.po.innerHTML = '<p class="empty">Académie hors du champ de ce jeu de données (France métropolitaine et DROM, hors COM).</p>'; return; }
    const k = cmpObj(), nom = cmpNom(), ref = new Map((k.pours || []).map((r) => [r[0], r]));
    const pc = (r: PoursuiteAcad | undefined, i: number): number => (r && r[1] ? (r[i] as number) / r[1] : NaN);
    const tot = (r: PoursuiteAcad | undefined): number => (r ? r.slice(2).reduce<number>((s, x) => s + (x as number), 0) : 0);
    const cols: [string, number][] = [['Université (hors IUT)', 2], ['IUT', 3], ['Classes prépa', 4], ['BTS', 5], ['Autres écoles et formations', 6]];
    const rows = a.pours.map((r) => {
      const c = ref.get(r[0]), t = r[1] ? tot(r) / r[1] : NaN, tc = c && c[1] ? tot(c) / c[1] : NaN;
      return `<tr><td data-v="${esc(r[0])}">${esc(r[0])}<small>${fmtInt(r[1])} bacheliers</small></td>
        <td class="r" data-l="Poursuivent" data-v="${t}"><strong>${fmtPct(t)}</strong><small>${esc(nom)} ${fmtPct(tc)}</small></td>
        ${cols.map(([l, i]) => `<td class="r" data-l="${l}" data-v="${pc(r, i)}">${fmtPct(pc(r, i))}<small>${esc(nom)} ${fmtPct(pc(c, i))}</small></td>`).join('')}</tr>`;
    }).join('');
    E.po.innerHTML = `<p>Part des bacheliers de la session ${D.rentree_poursuite}, ayant passé le bac dans l'académie, inscrits dans le supérieur à la rentrée suivante, où qu'ils étudient.</p>
      ${toolbar('po', "la poursuite d'études")}
      <div class="tablewrap"><table id="t-po"><caption class="sr-only">Poursuite d'études des bacheliers par voie et par filière</caption><thead><tr><th>Voie du bac</th><th class="r">Poursuivent</th>${cols.map(([l]) => `<th class="r">${l}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note">Source : SIES, taux de poursuite des néo-bacheliers par académie d'obtention du bac. Apprentissage en BTS compris ; formations hors du champ du ministère non comptées.</p>`;
    trier('t-po');
  }

  // ---- export : les lignes affichées (ordre de tri compris), valeurs brutes
  document.addEventListener('click', (e) => {
    const b = e.target instanceof Element ? e.target.closest<HTMLElement>('[data-export]') : null; if (!b) return;
    const a = D.academies[+E.acad.value], t = el('t-' + b.dataset.export);
    Spedago.download(`spedago-${a.slug}-${b.dataset.export}.csv`, Spedago.csv(Spedago.tableRows(t)));
  });

  function render(): void {
    const a = D.academies[+E.acad.value];
    E.zone.textContent = a.zone;
    stats(a); blocPs(a); blocPrive(a); blocPo(a); blocSpe(a); blocMm(a);
    Spedago.announce(`Fiche de l'académie ${a.nom}, comparée à ${cmpNom()}`);
  }
  E.acad.addEventListener('change', () => { Spedago.setHash(D.academies[+E.acad.value].nom); render(); });
  E.cmp.addEventListener('change', () => { Spedago.setParams({ cmp: E.cmp.value === 'fr' ? '' : D.academies[+E.cmp.value].slug }); render(); });
  el<HTMLFormElement>('pick').addEventListener('submit', (e) => e.preventDefault());
  window.addEventListener('hashchange', () => { if (Spedago.pick(E.acad)) render(); });
  document.addEventListener('spedago:profil', () => { if (!Spedago.hashSlug() && Spedago.pick(E.acad)) render(); });
  render();
}

loadData<DonneesAcademie>('mon_academie').then(main);
