// @ts-nocheck — portage de l'interface ; types à resserrer progressivement
import '../styles/commun.css';
import '../styles/mutualisation.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { MutCalc } from '../calc/mutualisation';

async function main(D0: any) {
  const D = D0;
  fillMeta({ rentree: D0.rentree, rayon: Math.round(D0.rayon_km), seuil: D0.seuil });

  
  const $ = (id) => document.getElementById(id);
  const NS = "http://www.w3.org/2000/svg";
  const fmtInt = (x) => Math.round(x).toLocaleString("fr-FR");
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const LIB = (s) => (D.libelles_specialites || {})[s] || s.replace(/_/g, " ").replace(/\bsc\b/g, "sciences").replace(/^./, (c) => c.toUpperCase());
  // codes : 0 proposée, 2 incertaine, 3 accès voisin, 4 ouverture commune, 5 isolé
  const CAT = { 0: ["Proposée", "--offre"], 3: ["Accès voisin", "--voisin"], 4: ["Ouverture commune", "--commun"], 5: ["Sans solution proche", "--isole"], 2: ["Incertain", "--incertain"] };
  const L = D.lycees, I = { uai: 0, nom: 1, com: 2, stat: 3, acad: 4, bassin: 5, lat: 6, lon: 7, eff: 8, st: 9, near: 10 };
  const idx = new Map(L.map((l, i) => [l[I.uai], i]));

  // ---- projection (métropole) : équirectangulaire corrigée de la latitude moyenne
  const LAT0 = 46.5, K = Math.cos(LAT0 * Math.PI / 180), BOX = { lon: [-5.3, 9.7], lat: [41.2, 51.2] };
  const W = 600, H = 620, PAD = 10;
  const sx = (W - 2 * PAD) / ((BOX.lon[1] - BOX.lon[0]) * K), sy = (H - 2 * PAD) / (BOX.lat[1] - BOX.lat[0]), s = Math.min(sx, sy);
  const px = (lon) => PAD + (lon - BOX.lon[0]) * K * s, py = (lat) => H - PAD - (lat - BOX.lat[0]) * s;
  const inMetro = (l) => l[I.lat] > 41 && l[I.lat] < 51.5 && l[I.lon] > -5.5 && l[I.lon] < 10;

  // ---- options
  D.specialites.forEach((sp, i) => { const o = document.createElement("option"); o.value = i; o.textContent = LIB(sp); $("spe").appendChild(o); });
  [...new Set(L.map((l) => l[I.acad]))].sort((a, b) => a.localeCompare(b, "fr")).forEach((a) => { const o = document.createElement("option"); o.value = a; o.textContent = a; $("acad").appendChild(o); });
  Spedago.pick($("acad"));  // #poitiers dans l'adresse -> académie présélectionnée
  L.forEach((l) => { const o = document.createElement("option"); o.value = `${l[I.nom]} — ${l[I.com]}`; $("lycees").appendChild(o); });
  const byLabel = new Map(L.map((l, i) => [`${l[I.nom]} — ${l[I.com]}`, i]));
  $("legend").innerHTML = [0, 3, 4, 5, 2].map((c) => `<span><i style="--c:var(${CAT[c][1]})${c === 2 ? ";background:none;border:1.5px solid var(--incertain)" : ""}"></i>${CAT[c][0]}</span>`).join("");

  // ---- carte
  const svg = $("map"), gLines = document.createElementNS(NS, "g"), gDots = document.createElementNS(NS, "g");
  svg.append(gLines, gDots);
  const dots = L.map((l, i) => {
    if (!inMetro(l)) return null;
    const c = document.createElementNS(NS, "circle");
    c.setAttribute("cx", px(l[I.lon]).toFixed(1)); c.setAttribute("cy", py(l[I.lat]).toFixed(1));
    c.dataset.i = i; const t = document.createElementNS(NS, "title"); c.appendChild(t); gDots.appendChild(c); return c;
  });
  let selected = null;

  const visible = (l) => MutCalc.visible(l, $("statut").value, $("acad").value);

  function render() {
    const sp = +$("spe").value, { n, eleves: el } = MutCalc.summary(D, sp, $("statut").value, $("acad").value);
    L.forEach((l, i) => {
      const code = l[I.st][sp], vis = visible(l), d = dots[i];
      if (!d) return;
      d.hidden = !vis;
      // Hiérarchie : « sans solution » et « ouverture commune » ressortent ; « incertain » = anneau vide (forme, pas seulement couleur)
      d.setAttribute("r", ({ 0: 2, 2: 1.8, 3: 2.4, 4: 3.6, 5: 3.8 }[code] * zf).toFixed(2));
      d.style.fill = code === 2 ? "none" : `var(${CAT[code][1]})`;
      d.style.stroke = code === 2 ? "var(--incertain)" : code >= 4 ? "#fff" : "none";
      d.style.strokeWidth = code === 2 ? 1 : code >= 4 ? 0.8 : 0;
      d.style.opacity = { 0: 0.45, 2: 0.9, 3: 0.65, 4: 1, 5: 1 }[code];
      d.firstChild.textContent = `${l[I.nom]} (${l[I.com]}) — ${CAT[code][0]}`;
      d.classList.toggle("sel", selected === i);
    });
    // les points « problème » au-dessus
    [3, 4, 5].forEach((c) => L.forEach((l, i) => { if (dots[i] && l[I.st][sp] === c) gDots.appendChild(dots[i]); }));
    if (selected !== null && dots[selected]) gDots.appendChild(dots[selected]);
    $("counts").innerHTML = [[0, n[0], "lycées la proposent"], [3, n[3], `sans elle · voisin à moins de ${D.rayon_km} km`],
      [4, n[4], "sans elle · ouverture commune possible"], [5, n[5], `sans elle · rien à moins de ${D.rayon_km} km (${fmtInt(el[5])} élèves de 1re)`]]
      .map(([c, v, t]) => `<div class="count" style="--c:var(${CAT[c][1]})"><b>${fmtInt(v)}</b><span>${t}</span></div>`).join("");
    Spedago.announce($("counts").innerText);
    renderListe();
    // groupes
    gLines.innerHTML = "";
    const grs = MutCalc.groups(D, sp, $("statut").value, $("acad").value);
    $("g-title").textContent = `Ouvertures communes possibles (${grs.length})`;
    $("groups").innerHTML = grs.length ? "" : '<p class="empty">Aucune pour cette spécialité et cette sélection.</p>';
    grs.forEach((g) => {
      const pts = g[1].filter((m) => dots[m]).map((m) => [px(L[m][I.lon]), py(L[m][I.lat])]);
      for (let k = 1; k < pts.length; k++) {
        const ln = document.createElementNS(NS, "line"); ln.setAttribute("class", "grp");
        ln.setAttribute("x1", pts[0][0]); ln.setAttribute("y1", pts[0][1]); ln.setAttribute("x2", pts[k][0]); ln.setAttribute("y2", pts[k][1]); gLines.appendChild(ln);
      }
      const b = document.createElement("button"); b.type = "button"; b.className = "group";
      b.innerHTML = `<b>${fmtInt(g[2])} élèves estimés</b> · ${g[1].length} lycées · ${String(g[3]).replace(".", ",")} km au plus<small>${g[1].map((m) => esc(`${L[m][I.nom]} (${L[m][I.com]})`)).join(" · ")}</small>`;
      b.addEventListener("click", () => select(g[1][0]));
      $("groups").appendChild(b);
    });
    renderFiche();
  }

  function renderFiche() {
    const f = $("fiche");
    if (selected === null) { f.innerHTML = '<h2>Fiche lycée</h2><p class="empty">Cliquez un point sur la carte ou cherchez un lycée.</p>'; return; }
    const l = L[selected];
    const rows = D.specialites.map((sp, j) => {
      const c = l[I.st][j], nr = l[I.near][j];
      const extra = nr ? `${String(nr[0]).replace(".", ",")} km · ${esc(L[idx.get(nr[1])][I.nom])}` : "";
      return `<div><span>${esc(LIB(sp))}</span><small><span class="pill" style="--c:var(${CAT[c][1]})">${CAT[c][0]}</span>${extra ? "<br>Plus proche : " + extra : ""}</small></div>`;
    }).join("");
    f.innerHTML = `<h2>${esc(l[I.nom])}</h2><dl><dt>Commune</dt><dd>${esc(l[I.com])}</dd><dt>Académie</dt><dd>${esc(l[I.acad])}</dd>
      <dt>Statut</dt><dd>${esc(l[I.stat])}</dd>${l[I.bassin] ? `<dt>Bassin</dt><dd>${esc(l[I.bassin])}</dd>` : ""}<dt>Élèves de 1re</dt><dd>${fmtInt(l[I.eff])}</dd></dl>
      <div class="spes">${rows}</div>`;
  }

  // ---- zoom sur l'académie choisie (cadre des lycées de métropole visibles)
  let zf = 1;
  function zoom() {
    const ac = $("acad").value, pts = ac ? L.filter((l) => l[I.acad] === ac && inMetro(l)) : [];
    if (!pts.length) { svg.setAttribute("viewBox", `0 0 ${W} ${H}`); zf = 1; return; }
    const xs = pts.map((l) => px(l[I.lon])), ys = pts.map((l) => py(l[I.lat]));
    let x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const w = Math.max(x1 - x0, 40) * 1.4 + 12, h = Math.max(y1 - y0, 40) * 1.4 + 12, side = Math.max(w, h * W / H);
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    svg.setAttribute("viewBox", `${(cx - side / 2).toFixed(1)} ${(cy - side * H / W / 2).toFixed(1)} ${side.toFixed(1)} ${(side * H / W).toFixed(1)}`);
    zf = Math.max(0.25, Math.pow(side / W, 0.75));
  }
  // ---- liste des lycées de la sélection
  let shownLyc = 100;
  const SIT = { 0: "La propose", 2: "Incertain (effectif masqué)", 3: "Voisin à moins de " + D.rayon_km + " km", 4: "Ouverture commune possible", 5: "Sans solution proche" };
  function lycRows() {
    const sp = +$("spe").value, m = $("montrer").value;
    return L.map((l, i) => [l, i]).filter(([l]) => visible(l) && (m === "tous" || (m === "isole" ? l[I.st][sp] === 5 : [3, 4, 5].includes(l[I.st][sp]))))
      .sort((a, b) => b[0][I.st][sp] - a[0][I.st][sp] || b[0][I.eff] - a[0][I.eff]);
  }
  function renderListe() {
    const sp = +$("spe").value, rows = lycRows(), tb = $("t-lyc").tBodies[0]; tb.innerHTML = "";
    rows.slice(0, shownLyc).forEach(([l, i]) => {
      const c = l[I.st][sp], nr = l[I.near][sp], near = nr ? L[idx.get(nr[1])] : null, tr = document.createElement("tr");
      tr.innerHTML = `<td data-v="${esc(l[I.nom])}"><button type="button" class="linklike" data-lyc="${i}">${esc(l[I.nom])}</button><small>${esc(l[I.com])}</small></td>
        <td data-v="${esc(l[I.acad])}">${esc(l[I.acad])}</td><td data-v="${esc(l[I.stat])}">${esc(l[I.stat])}</td>
        <td class="r" data-v="${l[I.eff]}">${fmtInt(l[I.eff])}</td>
        <td data-v="${c}"><span class="pill" style="--c:var(${CAT[c][1]})">${SIT[c]}</span></td>
        <td class="r" data-v="${nr ? nr[0] : ""}">${nr ? `${String(nr[0]).replace(".", ",")} km` : "–"}${near ? `<small>${esc(near[I.nom])}</small>` : ""}</td>`;
      tb.appendChild(tr);
    });
    Spedago.sortable($("t-lyc"));
    $("more-lyc").hidden = rows.length <= shownLyc;
    $("liste-note").textContent = `${fmtInt(rows.length)} lycée${rows.length > 1 ? "s" : ""}${rows.length > shownLyc ? `, ${fmtInt(shownLyc)} affichés (l'export les contient tous)` : ""} · ${LIB(D.specialites[sp])}`;
  }
  $("t-lyc").addEventListener("click", (e) => { const b = e.target.closest("[data-lyc]"); if (b) { select(+b.dataset.lyc); $("fiche").scrollIntoView({ block: "nearest" }); } });
  $("more-lyc").addEventListener("click", () => { shownLyc += 200; renderListe(); });
  $("montrer").addEventListener("change", () => { shownLyc = 100; renderListe(); });
  $("export-lyc").addEventListener("click", () => {
    const sp = +$("spe").value, out = [["UAI", "Lycée", "Commune", "Académie", "Statut", "Élèves de 1re", "Spécialité", "Situation", "Offre la plus proche (km)", "Lycée le plus proche"]];
    lycRows().forEach(([l]) => { const nr = l[I.near][sp], near = nr ? L[idx.get(nr[1])] : null;
      out.push([l[I.uai], l[I.nom], l[I.com], l[I.acad], l[I.stat], l[I.eff], LIB(D.specialites[sp]), SIT[l[I.st][sp]], nr ? nr[0] : "", near ? near[I.nom] : ""]); });
    Spedago.download(`spedago-lycees-${D.specialites[sp]}.csv`, Spedago.csv(out));
  });

  function select(i) { selected = i; render(); }
  gDots.addEventListener("click", (e) => { const c = e.target.closest("circle"); if (c) select(+c.dataset.i); });
  $("filters").addEventListener("change", render);
  $("filters").addEventListener("submit", (e) => e.preventDefault());
  $("acad").addEventListener("change", () => { Spedago.setHash($("acad").value); zoom(); shownLyc = 100; render(); });
  window.addEventListener("hashchange", () => { if (!Spedago.pick($("acad"))) $("acad").value = ""; zoom(); render(); });
  document.addEventListener("spedago:profil", () => { if (!Spedago.hashSlug() && Spedago.pick($("acad"))) { zoom(); render(); } });
  $("cherche").addEventListener("input", () => { const i = byLabel.get($("cherche").value); if (i !== undefined) select(i); });

  // État initial : spécialité NSI, premier groupe sélectionné (exemple réel)
  const nsi = D.specialites.indexOf("numerique_et_sciences_informatiques");
  $("spe").value = nsi >= 0 ? nsi : 0;
  Spedago.bind({ spe: $("spe"), statut: $("statut"), montrer: $("montrer") });
  zoom();
  const g0 = MutCalc.groups(D, +$("spe").value, "", $("acad").value)[0];  // premier groupe (de l'académie choisie, s'il y en a une)
  selected = g0 ? g0[1][0] : null;
  render();
}

loadData('mutualisation').then(main);
