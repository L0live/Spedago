// @ts-nocheck — portage de l'interface ; types à resserrer progressivement
import '../styles/commun.css';
import '../styles/mes-specialites.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { SpeCalc } from '../calc/mes-specialites';

async function main(D0: any) {
  fillMeta({ annee: D0.annee, rentree: D0.rentree_carte });

  const C = SpeCalc, D = D0;
  const $ = (id) => document.getElementById(id);
  const fmtInt = (x) => Math.round(x).toLocaleString("fr-FR");
  const fmtPct = (x, d = 0) => (isFinite(x) ? (x * 100).toFixed(d).replace(".", ",") + " %" : "–");
  const fmtPts = (x) => (isFinite(x) ? (x > 0 ? "+" : x < 0 ? "−" : "") + Math.abs(Math.round(x * 100)) + " pt" + (Math.abs(Math.round(x * 100)) > 1 ? "s" : "") : "–");
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const norm = (s) => String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  const EDS = D.eds, IDS = EDS.map((e) => e[0]);
  const byUai = new Map(D.lycees.map((l, i) => [l[0], i]));

  // ---- options
  EDS.forEach((e, i) => { for (const id of ["s1", "s2"]) { const o = document.createElement("option"); o.value = e[0]; o.textContent = e[1]; $(id).appendChild(o); } });
  [...new Set(D.groupes.map((g) => g[2]))].forEach((f) => { const o = document.createElement("option"); o.value = f; o.textContent = f; $("fam").appendChild(o); });
  D.lycees.forEach((l) => { const o = document.createElement("option"); o.value = `${l[1]} — ${l[2]}`; $("lycees").appendChild(o); });
  const byLabel = new Map(D.lycees.map((l, i) => [`${l[1]} — ${l[2]}`, i]));
  // valeurs de départ : profil, sinon exemple (la doublette la plus suivie)
  const pr = Spedago.profil().specialites || [];
  $("s1").value = IDS.includes(pr[0]) ? pr[0] : "maths"; $("s2").value = IDS.includes(pr[1]) ? pr[1] : "pc";
  const save = Spedago.bind({ s1: $("s1"), s2: $("s2"), fam: $("fam"), tri: $("tri"), q: $("q") });
  const lp = Spedago.param("lyc"); if (lp && byUai.has(lp)) { const l = D.lycees[byUai.get(lp)]; $("lyc").value = `${l[1]} — ${l[2]}`; }

  let all = false, ouvert = null;
  const dIdx = () => C.doublette(D, IDS.indexOf($("s1").value), IDS.indexOf($("s2").value));
  const nomD = () => `${EDS[IDS.indexOf($("s1").value)][1]} + ${EDS[IDS.indexOf($("s2").value)][1]}`;

  function lignes() {
    const d = dIdx(); if (d < 0) return [];
    const fam = $("fam").value, q = norm($("q").value.trim()), tri = $("tri").value;
    let rows = C.groupes(D, d).filter((r) => r.n > 0 && (!fam || D.groupes[r.key][2] === fam)
      && (!q || norm(D.groupes[r.key][1]).includes(q) || D.formations.some((f) => f[0] === r.key && norm(f[1]).includes(q))));
    const key = { demande: (r) => -r.n, chances: (r) => -(isNaN(r.lo) ? -1 : r.lo), ecart: (r) => -(isNaN(r.lo) || isNaN(r.pO) ? -9 : r.lo - r.pO), nom: () => 0 }[tri];  // écart prudent : bas de l'intervalle
    rows.sort((a, b) => key(a) - key(b) || D.groupes[a.key][1].localeCompare(D.groupes[b.key][1], "fr"));
    return rows;
  }

  function cells(r, nom, sous) {
    const ec = isFinite(r.ecart) && Math.abs(r.ecart) >= 0.05 ? (r.ecart > 0 ? "pos" : "neg") : "";
    const meter = isFinite(r.p) ? `<div class="meter" aria-hidden="true"><span style="width:${(r.p * 100).toFixed(1)}%"></span>${isFinite(r.pO) ? `<i style="left:calc(${(r.pO * 100).toFixed(1)}% - 1px)"></i>` : ""}</div>` : "";
    return `<td data-v="${esc(nom)}">${sous}</td>
      <td class="r" data-l="Élèves comme vous" data-v="${r.n}">${fmtInt(r.n)}<small>${fmtPct(r.part, 1)} de votre doublette</small></td>
      <td class="r" data-l="Ont reçu une proposition" data-v="${isFinite(r.p) ? r.p : ""}">${fmtPct(r.p)}${meter}<small>${r.n >= 30 ? `${fmtPct(r.lo)} – ${fmtPct(r.hi)}` : "peu de candidats"}</small></td>
      <td class="r" data-l="Autres bacheliers" data-v="${isFinite(r.pO) ? r.pO : ""}">${fmtPct(r.pO)}<small>${fmtInt(r.nO)} cand.</small></td>
      <td class="r ${ec}" data-l="Écart" data-v="${isFinite(r.ecart) ? r.ecart : ""}">${fmtPts(r.ecart)}</td>`;
  }

  function render() {
    const d = dIdx(), tb = $("t-g").tBodies[0]; tb.innerHTML = "";
    if (d < 0) {
      $("stats").innerHTML = ""; $("count").textContent = "";
      tb.innerHTML = `<tr><td colspan="5" class="empty">Pas de données pour cette combinaison : choisissez deux spécialités différentes qui peuvent être suivies ensemble.</td></tr>`;
      $("b-detail").hidden = true; renderLycee(); return;
    }
    const s = C.resume(D, d);
    $("stats").innerHTML = [
      [fmtInt(s.n), `bacheliers généraux avec ${esc(nomD())} en ${D.annee} (${fmtPct(s.part, 1)}, ${s.rang === 1 ? "1re" : s.rang + "e"} doublette sur ${s.nb})`],
      [fmtPct(s.k / s.n, 1), `ont reçu au moins une proposition (tous bacheliers généraux : ${fmtPct(s.pTous, 1)})`],
      [fmtInt(C.groupes(D, d).filter((r) => r.n > 0).length), "types de formation demandés au moins une fois"],
    ].map(([b, t]) => `<div class="stat"><b>${b}</b><span>${t}</span></div>`).join("");
    const rows = lignes(), shown = all ? rows : rows.slice(0, 25);
    shown.forEach((r) => {
      const g = D.groupes[r.key], tr = document.createElement("tr"); if (ouvert === r.key) tr.className = "cur";
      tr.innerHTML = cells(r, g[1], `<button type="button" class="linklike" data-g="${r.key}" aria-expanded="${ouvert === r.key}" aria-controls="b-detail">${esc(g[1])}</button><small>${esc(g[2])}</small>`);
      tb.appendChild(tr);
    });
    if (!rows.length) tb.innerHTML = `<tr><td colspan="5" class="empty">Aucune formation ne correspond à ces filtres.</td></tr>`;
    Spedago.sortable($("t-g"));
    $("more").hidden = all || rows.length <= 25;
    $("count").textContent = `${fmtInt(rows.length)} type${rows.length > 1 ? "s" : ""} de formation · ${nomD()} · cliquez un nom pour le détail par formation`;
    Spedago.announce(`${fmtInt(rows.length)} types de formation pour ${nomD()}`);
    renderDetail(); renderLycee();
  }

  function renderDetail() {
    const d = dIdx(), box = $("b-detail");
    if (ouvert === null || d < 0) { box.hidden = true; return; }
    const g = D.groupes[ouvert], rows = C.fines(D, d, ouvert).filter((r) => r.n > 0).sort((a, b) => b.n - a.n);
    $("h-detail").textContent = g[1];
    const t = D.tendance[`${d}|${ouvert}`] || [];
    const trend = t.length > 1 ? `<p class="note">Part ayant reçu une proposition, élèves comme vous, par année du bac :</p><div class="trend">${t.map(([y, v, p]) => `<span>${y} : ${v ? fmtPct(p / v) : "–"} <small>(${fmtInt(v)})</small></span>`).join("")}</div>` : "";
    $("detail").innerHTML = `${trend}
      <div class="tablewrap" tabindex="0" role="region" aria-label="Formations du regroupement (défilant)"><table id="t-f"><caption class="sr-only">Formations de ${esc(g[1])}</caption>
      <thead><tr><th>Formation</th><th class="r">Élèves comme vous</th><th class="r">Ont reçu une proposition</th><th class="r">Autres bacheliers</th><th class="r">Écart</th></tr></thead>
      <tbody>${rows.map((r) => `<tr>${cells(r, D.formations[r.key][1], esc(D.formations[r.key][1]))}</tr>`).join("") || '<tr><td colspan="5" class="empty">Pas de détail.</td></tr>'}</tbody></table></div>`;
    Spedago.sortable($("t-f"));
    box.hidden = false;
  }

  function renderLycee() {
    const li = byLabel.get($("lyc").value), box = $("b-lycee");
    if (li === undefined) { box.hidden = true; return; }
    const l = D.lycees[li], res = C.lycee(D, li, [IDS.indexOf($("s1").value), IDS.indexOf($("s2").value)]);
    $("h-lycee").textContent = `${l[1]} (${l[2]})`;
    $("lycee").innerHTML = `<ul>${res.map((r) => {
      const nom = esc(EDS[r.eds][1]);
      if (r.etat === "propose") return `<li><span class="ok">✓ Proposée</span> ${nom}</li>`;
      if (r.etat === "incertain") return `<li><span class="unk">? Incertain</span> ${nom} <small class="note">(effectif masqué par le secret statistique)</small></li>`;
      if (r.etat === "hors_carte") return `<li><span class="unk">– Non couverte</span> ${nom} <small class="note">(pas dans les données de la carte)</small></li>`;
      const near = r.uai && byUai.has(r.uai) ? D.lycees[byUai.get(r.uai)] : null;
      return `<li><span class="ko">✗ Pas proposée</span> ${nom}${near ? ` — la plus proche : <strong>${esc(near[1])}</strong> (${esc(near[2])}), ${String(r.km).replace(".", ",")} km à vol d'oiseau` : ""}</li>`;
    }).join("")}</ul><p class="note">Offre de 1re (rentrée ${D.rentree_carte}), même statut public/privé pour le lycée le plus proche. <a href="mutualisation.html#${Spedago.slug(l[3])}">Voir la carte des spécialités →</a></p>
      ${l[6] ? `<h3 class="h3">Résultats du lycée au bac ${D.annee_ival}</h3><div class="ival">${[
        ["Réussite au bac", l[6][0], l[6][1]], ["Élèves de 2de qui obtiennent le bac dans le lycée", l[6][2], l[6][3]], ["Mentions", l[6][4], l[6][5]],
      ].map(([t, v, va]) => `<div><b>${v == null ? "–" : Math.round(v) + " %"}</b><span>${t}</span><small>${va == null ? "valeur ajoutée non publiée" : `valeur ajoutée ${va > 0 ? "+" : va < 0 ? "−" : ""}${Math.abs(va)} pt${Math.abs(va) > 1 ? "s" : ""}`}</small></div>`).join("")}</div>
      <p class="note">Valeur ajoutée : écart entre le résultat du lycée et celui attendu compte tenu de ses élèves (âge, origine sociale, résultats au brevet). Positive : le lycée fait mieux que prévu.</p>` : ""}`;
    box.hidden = false;
  }

  $("t-g").addEventListener("click", (e) => {
    const b = e.target.closest("[data-g]"); if (!b) return;
    const g = +b.dataset.g; ouvert = ouvert === g ? null : g; render();
    if (ouvert !== null) { $("b-detail").scrollIntoView({ block: "start" }); $("h-detail").setAttribute("tabindex", "-1"); $("h-detail").focus(); }
  });
  $("more").addEventListener("click", () => { all = true; render(); });
  $("filters").addEventListener("submit", (e) => e.preventDefault());
  ["s1", "s2", "fam", "tri"].forEach((id) => $(id).addEventListener("change", () => { ouvert = null; render(); }));
  $("q").addEventListener("input", () => { render(); });
  $("lyc").addEventListener("input", () => { const li = byLabel.get($("lyc").value); if (li !== undefined) Spedago.setParams({ lyc: D.lycees[li][0] }); renderLycee(); });
  $("export").addEventListener("click", () => {
    const d = dIdx(); if (d < 0) return;
    const out = [["Doublette", "Type de formation", "Famille", "Élèves comme moi ayant demandé", "Part de la doublette", "Ont reçu une proposition", "Bas", "Haut", "Autres bacheliers : part", "Écart (points)"]];
    lignes().forEach((r) => out.push([nomD(), D.groupes[r.key][1], D.groupes[r.key][2], r.n, r.part, r.p, r.lo, r.hi, r.pO, r.ecart * 100]));
    Spedago.download(`spedago-${$("s1").value}-${$("s2").value}-formations.csv`, Spedago.csv(out));
  });
  document.addEventListener("spedago:profil", (e) => {
    const s = e.detail.specialites || [];
    if (s.length === 2 && !Spedago.param("s1")) { $("s1").value = s[0]; $("s2").value = s[1]; save(); render(); }
  });
  render();
}

loadData('mes_specialites').then(main);
