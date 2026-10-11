// Spédago — fonctions communes à toutes les pages.
//  - Adresse : #<académie>&cle=valeur… (l'académie d'abord, puis les filtres de la page) ; slug() = spedago.referentiel.slug (testé).
//  - Profil : réglages de la personne (rôle, académie, profil d'études, spécialités), gardés dans ce navigateur seulement.
//  - Annonces pour lecteurs d'écran, tableaux triables, export CSV, copie du lien de la vue.

export interface Profil { role?: string; academie?: string; profilMaster?: string; specialites?: string[] }
export interface EtatAdresse { acad: string; params: Record<string, string> }
type Controle = HTMLInputElement | HTMLSelectElement;
type Cellule = string | number | boolean | null | undefined;
interface TableTriable extends HTMLTableElement { _sortable?: boolean; _sort?: { col: number; dir: 'ascending' | 'descending' } }

export const Spedago = (() => {
  const HAS_DOM = typeof document !== 'undefined';
  function slug(nom: string): string {
    let s = String(nom).normalize('NFKD').replace(/[^\x00-\x7f]/g, '').toUpperCase();
    s = s.replace(/[-'\s]+/g, ' ').trim().replace(/^ST /, 'SAINT ');
    return s.toLowerCase().replace(/ /g, '-');
  }
  // ---- état dans l'adresse
  function parseHash(h: string): EtatAdresse {
    const out: EtatAdresse = { acad: '', params: {} };
    String(h || '').replace(/^#/, '').split('&').forEach((t, i) => {
      if (!t) return;
      let k: string, v: string | undefined;
      try { [k, v] = t.split('=').map(decodeURIComponent); } catch { return; }
      if (v === undefined) { if (i === 0) out.acad = k; } else out.params[k] = v;
    });
    return out;
  }
  function buildHash(st: EtatAdresse): string {
    const parts: string[] = [];
    if (st.acad) parts.push(st.acad);
    Object.entries(st.params).forEach(([k, v]) => { if (v !== '' && v != null) parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v)); });
    return parts.length ? '#' + parts.join('&') : '';
  }
  const current = (): EtatAdresse => parseHash(HAS_DOM ? location.hash : '');
  const hashSlug = (): string => current().acad;
  const param = (k: string): string | undefined => current().params[k];
  function writeHash(st: EtatAdresse): void {
    const h = buildHash(st);
    try { history.replaceState(null, '', h || location.pathname + location.search); } catch { location.hash = h; }
    syncNav();
  }
  function setParams(obj: Record<string, string>): void { const st = current(); Object.assign(st.params, obj); writeHash(st); }
  function setHash(nom: string): void { const st = current(); st.acad = nom ? slug(nom) : ''; writeHash(st); }
  // Page dont l'ancre désigne une section (<body data-ancres="locales">, ex. Méthodes) : l'adresse ne porte pas d'académie.
  const ancresLocales = (): boolean => HAS_DOM && document.body?.dataset.ancres === 'locales';
  // Les liens de la barre gardent l'académie (les filtres propres à une page restent sur cette page).
  function syncNav(): void {
    if (!HAS_DOM) return;
    const a = ancresLocales() ? '' : hashSlug();
    document.querySelectorAll<HTMLAnchorElement>('.site-nav a[data-page]').forEach((x) => { x.href = (x.dataset.page ?? '') + (a ? '#' + a : ''); });
  }
  // ---- profil (ce navigateur seulement)
  const KEY = 'spedago.profil';
  function profil(): Profil { try { return JSON.parse(localStorage.getItem(KEY) ?? 'null') || {}; } catch { return {}; } }
  function saveProfil(p: Profil | null): void {
    try { if (p) localStorage.setItem(KEY, JSON.stringify(p)); else localStorage.removeItem(KEY); } catch { /* stockage indisponible */ }
    if (HAS_DOM) document.dispatchEvent(new CustomEvent('spedago:profil', { detail: p || {} }));
  }
  // Sélectionne l'option du <select> qui correspond à l'académie de l'adresse, sinon à celle du profil.
  function pick(select: HTMLSelectElement | null): boolean {
    if (!select) return false;
    const h = hashSlug() || profil().academie || ''; if (!h) return false;
    const o = [...select.options].find((x) => x.value !== '' && slug(x.textContent ?? '') === h);
    if (o) select.value = o.value;
    return !!o;
  }
  // Restaure / enregistre des contrôles de formulaire dans l'adresse : { cle: element }
  function bind(map: Record<string, Controle | null>, onChange?: () => void): () => void {
    const p = current().params;
    Object.entries(map).forEach(([k, el]) => {
      if (!el || p[k] === undefined) return;
      if (el instanceof HTMLInputElement && el.type === 'radio') {
        const r = document.querySelector<HTMLInputElement>(`input[name="${el.name}"][value="${p[k]}"]`); if (r) r.checked = true;
      } else if (el instanceof HTMLInputElement || [...el.options].length === 0 || [...el.options].some((o) => o.value === p[k])) el.value = p[k];
    });
    const save = (): void => {
      const o: Record<string, string> = {};
      Object.entries(map).forEach(([k, el]) => {
        if (!el) return;
        o[k] = el instanceof HTMLInputElement && el.type === 'radio'
          ? document.querySelector<HTMLInputElement>(`input[name="${el.name}"]:checked`)?.value ?? '' : el.value;
      });
      setParams(o); if (onChange) onChange();
    };
    Object.values(map).forEach((el) => el && el.addEventListener('change', save));
    return save;
  }
  // ---- annonces (WCAG 4.1.3), regroupées
  let tAnn: ReturnType<typeof setTimeout> | undefined;
  function announce(text: string): void {
    if (!HAS_DOM) return;
    const z = document.getElementById('sr-status'); if (!z) return;
    clearTimeout(tAnn); tAnn = setTimeout(() => { z.textContent = ''; setTimeout(() => { z.textContent = String(text).replace(/\s+/g, ' ').trim(); }, 50); }, 700);
  }
  // ---- tableaux triables : en-têtes boutons, aria-sort ; valeur de tri = data-v sinon texte
  function sortValue(td: HTMLTableCellElement): number | string {
    const v = td.dataset.v !== undefined ? td.dataset.v : (td.textContent ?? '').trim();
    const n = Number(String(v).replace(/\s/g, '').replace(',', '.').replace('%', ''));
    return v !== '' && isFinite(n) ? n : String(v).toLowerCase();
  }
  function applySort(table: TableTriable): void {
    const st = table._sort; if (!st) return;
    const tb = table.tBodies[0], rows = [...tb.rows].filter((r) => r.cells.length > st.col);
    rows.sort((a, b) => {
      const x = sortValue(a.cells[st.col]), y = sortValue(b.cells[st.col]);
      const c = typeof x === 'number' && typeof y === 'number' ? x - y : String(x).localeCompare(String(y), 'fr');
      return st.dir === 'ascending' ? c : -c;
    });
    rows.forEach((r) => tb.appendChild(r));
    [...table.tHead!.rows[0].cells].forEach((th, i) => { if (!th.hasAttribute('data-nosort')) th.setAttribute('aria-sort', i === st.col ? st.dir : 'none'); });
  }
  function sortable(el: HTMLElement | null): void {
    const table = el as TableTriable | null;
    if (!table || table._sortable) { if (table) applySort(table); return; }
    table._sortable = true;
    [...table.tHead!.rows[0].cells].forEach((th, i) => {
      if (th.hasAttribute('data-nosort')) return;
      const b = document.createElement('button'); b.type = 'button'; b.className = 'th-sort';
      while (th.firstChild) b.appendChild(th.firstChild);
      th.appendChild(b); th.setAttribute('aria-sort', 'none');
      b.addEventListener('click', () => {
        const st = table._sort;
        table._sort = { col: i, dir: st && st.col === i && st.dir === 'descending' ? 'ascending' : 'descending' };
        applySort(table); announce(`Tri : ${(b.textContent ?? '').trim()}, ${table._sort.dir === 'ascending' ? 'croissant' : 'décroissant'}`);
      });
    });
  }
  // ---- export CSV (séparateur « ; », compatible tableur français)
  function csv(rows: Cellule[][]): string {
    return '﻿' + rows.map((r) => r.map((c) => { const s = c == null ? '' : String(c); return /[;"\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }).join(';')).join('\r\n');
  }
  function tableRows(table: HTMLElement | null): string[][] {
    if (!(table instanceof HTMLTableElement)) return [];
    return [...table.rows].map((tr) => [...tr.cells].map((c) => (c.dataset.v !== undefined ? c.dataset.v : ((c.querySelector('.v') || c).textContent ?? '').replace(/\s+/g, ' ').trim())));
  }
  function download(filename: string, text: string): boolean {
    try {
      const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv;charset=utf-8' }));
      a.download = filename; document.body.appendChild(a); a.click(); a.remove(); return true;
    } catch { announce('Export impossible dans cette vue'); return false; }
  }
  // ---- copie du lien de la vue
  async function copyLink(btn: HTMLElement): Promise<void> {
    const url = location.href;
    try { await navigator.clipboard.writeText(url); btn.textContent = 'Lien copié'; } catch { window.prompt('Copiez ce lien :', url); }
    setTimeout(() => { btn.textContent = 'Copier le lien'; }, 2000);
  }
  // ---- panneau « Mon profil »
  function initProfil(): void {
    const btn = document.getElementById('profil-btn'), panel = document.getElementById('profil-panel'); if (!btn || !panel) return;
    const f = panel.querySelector('form'); if (!f) return;
    const sel = (n: string): HTMLSelectElement => f.elements.namedItem(n) as HTMLSelectElement;
    const fill = (q: Profil): void => {
      sel('role').value = q.role || ''; sel('academie').value = q.academie || ''; sel('profilMaster').value = q.profilMaster || '';
      sel('spe1').value = (q.specialites || [])[0] || ''; sel('spe2').value = (q.specialites || [])[1] || '';
    };
    fill(profil());
    const label = (): void => { const q = profil(), a = sel('academie').selectedOptions[0]; btn.querySelector('span')!.textContent = q.academie && a ? a.textContent : 'Mon profil'; };
    label();
    const close = (): void => { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', () => { const o = panel.hidden; panel.hidden = !o; btn.setAttribute('aria-expanded', String(o)); if (o) sel('role').focus(); });
    panel.addEventListener('keydown', (e) => { if (e.key === 'Escape') { close(); btn.focus(); } });
    f.addEventListener('submit', (e) => {
      e.preventDefault();
      const q: Profil = { role: sel('role').value, academie: sel('academie').value, profilMaster: sel('profilMaster').value,
                          specialites: [sel('spe1').value, sel('spe2').value].filter(Boolean) };
      saveProfil(q); label(); close(); btn.focus(); announce('Profil enregistré dans ce navigateur');
      if (q.academie && !hashSlug() && !ancresLocales()) { const st = current(); st.acad = q.academie; writeHash(st); window.dispatchEvent(new HashChangeEvent('hashchange')); }
    });
    f.querySelector('[data-reset]')?.addEventListener('click', () => { saveProfil(null); fill({}); label(); announce('Profil effacé'); });
    const cp = document.getElementById('copy-link'); if (cp) cp.addEventListener('click', () => copyLink(cp));
  }
  // ---- menu replié sur téléphone (même seuil que commun.css) ; sans JavaScript, le menu reste ouvert
  function initMenu(): void {
    const btn = document.querySelector<HTMLButtonElement>('.nav-toggle'), menu = document.getElementById('nav-menu'); if (!btn || !menu) return;
    const mq = window.matchMedia('(max-width: 640px)');
    const set = (open: boolean): void => { menu.hidden = !open; btn.setAttribute('aria-expanded', String(open)); };
    const apply = (): void => { btn.hidden = !mq.matches; set(!mq.matches); };
    btn.addEventListener('click', () => set(menu.hidden !== false));
    menu.addEventListener('keydown', (e) => { if (e.key === 'Escape' && mq.matches && !(e.target as HTMLElement).closest('#profil-panel')) { set(false); btn.focus(); } });
    mq.addEventListener('change', apply);
    apply();
  }
  function init(): void { syncNav(); initMenu(); initProfil(); }
  if (HAS_DOM) {
    // les modules sont différés : le DOM est déjà analysé quand ce code s'exécute
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
    window.addEventListener('hashchange', syncNav);
  }
  return { slug, parseHash, buildHash, hashSlug, param, setParams, setHash, syncNav, pick, bind, profil, saveProfil,
           announce, sortable, applySort, csv, tableRows, download };
})();
