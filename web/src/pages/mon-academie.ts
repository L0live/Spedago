// @ts-nocheck — portage de l'interface ; types à resserrer progressivement
import '../styles/commun.css';
import '../styles/mon-academie.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { AcadCalc } from '../calc/mon-academie';

async function main(D0: any) {
  fillMeta({ rentree_po: D0.rentree_poursuite });

  const C = AcadCalc, D = D0;
  const $ = (id) => document.getElementById(id);
  const fmtInt = (x) => Math.round(x).toLocaleString("fr-FR");
  const fmtPct = (x, d = 0) => (isFinite(x) ? (x * 100).toFixed(d).replace(".", ",") + " %" : "–");
  const fmtDec = (x, d = 1) => (isFinite(x) ? x.toFixed(d).replace(".", ",") : "–");
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const FIL = (i) => (D.libelles_filieres || {})[D.filieres[i]] || D.filieres[i];
  const SPE = (i) => (D.libelles_specialites || {})[D.specialites[i]] || D.specialites[i];
  const link = (page, a, txt) => `<a class="more" href="${page}#${a.slug}">${txt} →</a>`;
  const plural = (n, w) => `${fmtInt(n)} ${w}${n > 1 ? "s" : ""}`;

  // ---- sélecteurs : académie (adresse, sinon profil, sinon exemple) et point de comparaison
  D.academies.forEach((a, i) => {
    for (const id of ["acad", "cmp"]) { const o = document.createElement("option"); o.value = i; o.textContent = a.nom; $(id).appendChild(o); }
  });
  if (!Spedago.pick($("acad"))) $("acad").value = Math.max(0, C.indexOf(D, "poitiers"));
  const cmpParam = Spedago.param("cmp");
  if (cmpParam && cmpParam !== "fr") { const i = C.indexOf(D, cmpParam); if (i >= 0) $("cmp").value = i; }
  const cmpObj = () => ($("cmp").value === "fr" ? D.france : D.academies[+$("cmp").value]);
  const cmpNom = () => ($("cmp").value === "fr" ? "France" : D.academies[+$("cmp").value].nom);

  function stats(a) {
    const r = a.ref || [0, 0, 0, 0, 0, 0], p = a.ps ? C.ps(a.ps.total) : null, m = a.mm ? C.mm(a.mm.total) : null;
    const k = cmpObj(), kp = k.ps ? C.ps(k.ps.total) : null;
    const cards = [
      [fmtInt(r[0]), `lycées, dont ${fmtInt(r[1])} avec une 1re générale`],
      [p ? fmtInt(p.places) : "–", p ? `places Parcoursup 2025 dans ${plural(p.formations, "formation")}` : "pas de formation Parcoursup"],
      [p ? fmtDec(p.vpp) : "–", p && kp ? `vœux par place (${cmpNom()} : ${fmtDec(kp.vpp)})` : "vœux par place"],
      [m ? fmtInt(m.places) : "–", m ? `places en master 2025 dans ${plural(m.formations, "formation")}` : "pas de master sur la plateforme"],
    ];
    $("stats").innerHTML = cards.map(([b, t]) => `<div class="stat"><b>${b}</b><span>${t}</span></div>`).join("");
  }

  const toolbar = (id, label) => `<div class="toolbar"><span class="note">Cliquez un en-tête pour trier.</span><button type="button" class="btn-ghost" data-export="${id}">Exporter ${label} (CSV)</button></div>`;

  function blocPs(a) {
    if (!a.ps) { $("ps").innerHTML = `<p class="empty">Pas de formation Parcoursup recensée dans cette académie.</p>`; return; }
    const k = cmpObj(), nom = cmpNom();
    if (!k.ps) { $("ps").innerHTML = `<p class="empty">Pas de formation Parcoursup dans l'académie de comparaison.</p>`; return; }
    const t = C.ps(a.ps.total), f = C.ps(k.ps.total), ref = new Map(k.ps.filieres.map((r) => [r[0], C.ps(r.slice(1))]));
    const [ajout, couvert, visees] = a.ps.sim, [ajFr, coFr] = D.france.ps.sim;
    const rows = a.ps.filieres.map((r) => {
      const x = C.ps(r.slice(1)), n = ref.get(r[0]);
      const chaud = n && x.partSat > n.partSat + 0.1, hot = chaud ? ' class="r hot"' : ' class="r"';
      const meter = n ? `<div class="meter${chaud ? " hot" : ""}" aria-hidden="true"><span style="width:${(x.partSat * 100).toFixed(1)}%"></span><i style="left:calc(${(n.partSat * 100).toFixed(1)}% - 1px)"></i></div>` : "";
      const vs = (v, fmt) => (n ? `<small>${esc(nom)} ${fmt(v)}</small>` : `<small>absent de ${esc(nom)}</small>`);
      return `<tr><td data-v="${esc(FIL(r[0]))}">${esc(FIL(r[0]))}<small>${plural(x.formations, "formation")}</small></td>
        <td class="r" data-l="Places" data-v="${x.places}">${fmtInt(x.places)}</td>
        <td class="r" data-l="Vœux par place" data-v="${x.vpp}">${fmtDec(x.vpp)}${vs(n && n.vpp, fmtDec)}</td>
        <td class="r" data-l="Places pourvues" data-v="${x.remp}">${fmtPct(x.remp)}${vs(n && n.remp, fmtPct)}</td>
        <td${hot} data-l="Dans des formations pleines" data-v="${x.partSat}">${chaud ? '<span aria-hidden="true">▲ </span><span class="sr-only">nettement au-dessus : </span>' : ""}${fmtPct(x.partSat)}${meter}${vs(n && n.partSat, fmtPct)}</td></tr>`;
    }).join("");
    $("ps").innerHTML = `
      <p>${fmtInt(t.places)} places et ${fmtInt(t.voeux)} vœux confirmés, soit <strong>${fmtDec(t.vpp)} vœux par place</strong> (${esc(nom)} : ${fmtDec(f.vpp)}).
      ${fmtPct(t.partSat)} des places sont dans des formations pleines à 95 % ou plus (${esc(nom)} : ${fmtPct(f.partSat)}) ; ${fmtInt(t.vac)} places sont restées vacantes.</p>
      ${toolbar("ps", "la tension par filière")}
      <div class="tablewrap"><table id="t-ps"><caption class="sr-only">Tension Parcoursup par filière, comparée à ${esc(nom)}</caption><thead><tr><th>Filière</th><th class="r">Places</th><th class="r">Vœux par place</th><th class="r">Places pourvues</th><th class="r">Places dans des formations pleines</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note"><span class="hot">▲ en orange</span> : au moins 10 points au-dessus de ${esc(nom)} pour la même filière. Barre : ${esc(a.nom)} ; trait : ${esc(nom)}.</p>
      <div class="simbox"><span class="tag">Simulation</span>
      Avec la règle de départ du simulateur (+${fmtPct(D.alpha)} de places aux formations pleines et parmi les plus demandées de leur filière),
      l'académie recevrait <strong>+${fmtInt(ajout)} places</strong> dans ${plural(visees, "formation")}, soit ${fmtPct(ajout / ajFr, 1)} des places ajoutées en France.
      ${ajout ? `Au plus ${fmtInt(couvert)} (${fmtPct(couvert / ajout)}) pourraient venir de places restées vides dans une formation de même spécialité de l'académie (France : ${fmtPct(coFr / ajFr)}).` : ""}
      ${link("simulateur-parcoursup.html", a, "Changer la règle dans le simulateur")}</div>`;
    Spedago.sortable($("t-ps"));
  }

  function blocSpe(a) {
    if (!a.spe) { $("spe").innerHTML = `<p class="empty">Pas de lycée de cette académie sur la carte des spécialités (effectifs ou coordonnées absents).</p>`; return; }
    const k = cmpObj(), nom = cmpNom(), kr = k.spe ? k.spe.spe : null, kl = k.spe ? k.spe.lycees : 0;
    const rows = C.speRows(a.spe.spe).map((r) => {
      const part = r.isole / a.spe.lycees, kp = kr ? kr[r.sp][4] / kl : NaN;
      return `<tr><td data-v="${esc(SPE(r.sp))}">${esc(SPE(r.sp))}</td>
      <td class="r" data-l="La proposent" data-v="${r.propose}">${fmtInt(r.propose)}${r.incertain ? `<small>+ ${fmtInt(r.incertain)} incertain${r.incertain > 1 ? "s" : ""}</small>` : ""}</td>
      <td class="r" data-l="Voisin à moins de 20 km" data-v="${r.voisin}">${fmtInt(r.voisin)}</td>
      <td class="r" data-l="Ouverture commune" data-v="${r.commune}">${fmtInt(r.commune)}<small>${plural(r.groupes, "groupe")}</small></td>
      <td class="r${r.isole ? " hot" : ""}" data-l="Sans solution proche" data-v="${r.isole}">${fmtInt(r.isole)}<small>${fmtInt(r.eIsole)} élèves de 1re</small></td>
      <td class="r" data-l="Part sans solution" data-v="${part}">${fmtPct(part)}<small>${esc(nom)} ${fmtPct(kp)}</small></td></tr>`;
    }).join("");
    const tot = a.spe.spe.reduce((s, r) => s + r[4], 0);
    $("spe").innerHTML = `
      <p>${fmtInt(a.spe.lycees)} lycées avec une 1re générale (rentrée ${D.rentree}). Pour chaque spécialité, combien la proposent, et pour les autres :
      un lycée voisin à moins de 20 km, une ouverture commune possible avec d'autres lycées, ou aucune solution proche.
      ${tot ? "" : "<strong>Aucun cas « sans solution proche » dans l'académie.</strong>"}</p>
      ${toolbar("spe", "l'accès aux spécialités")}
      <div class="tablewrap"><table id="t-spe"><caption class="sr-only">Accès aux spécialités de 1re générale</caption><thead><tr><th>Spécialité</th><th class="r">La proposent</th><th class="r">Voisin à moins de 20 km</th><th class="r">Ouverture commune possible</th><th class="r">Sans solution proche</th><th class="r">Part des lycées sans solution</th></tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note">« Incertain » : effectif masqué par le secret statistique, la spécialité est probablement proposée.</p>
      ${link("mutualisation.html", a, "Voir les lycées sur la carte")}`;
    Spedago.sortable($("t-spe"));
  }

  function blocMm(a) {
    if (!a.mm) { $("mm").innerHTML = `<p class="empty">Pas de master de cette académie sur la plateforme nationale.</p>`; return; }
    const k = cmpObj(), nom = cmpNom(), t = C.mm(a.mm.total), f = k.mm ? C.mm(k.mm.total) : null;
    const rows = a.mm.mentions.map(([m, nf, pl, n, kk, nN, kN]) => {
      const [lo, hi] = C.wilson(kk, n);
      return `<tr><td class="mention" data-v="${esc(m)}">${esc(m)}<small>${plural(nf, "formation")}</small></td><td class="r" data-l="Places" data-v="${pl}">${fmtInt(pl)}</td>
        <td class="r" data-l="Proposition, L3 générale" data-v="${n ? kk / n : ""}">${n ? fmtPct(kk / n) : "–"}<small>${n ? `entre ${fmtPct(lo)} et ${fmtPct(hi)} · ${fmtInt(n)} cand.` : "aucun candidat"}</small></td>
        <td class="r" data-l="Même mention, France" data-v="${kN / nN}">${fmtPct(kN / nN)}</td></tr>`;
    }).join("");
    $("mm").innerHTML = `
      <p>${fmtInt(t.formations)} formations, ${fmtInt(t.places)} places, ${fmtInt(t.cand)} candidatures : <strong>${fmtPct(t.taux)}</strong> ont reçu une proposition d'admission${f ? ` (${esc(nom)} : ${fmtPct(f.taux)})` : ""}.
      Pour les candidatures venant d'une 3e année de licence générale : ${fmtPct(t.tauxL3)}${f ? ` (${esc(nom)} : ${fmtPct(f.tauxL3)})` : ""}.</p>
      ${toolbar("mm", "les mentions")}
      <div class="tablewrap"><table id="t-mm"><caption class="sr-only">Masters : mentions qui offrent le plus de places</caption><thead><tr><th>Mentions qui offrent le plus de places</th><th class="r">Places</th><th class="r">Proposition, L3 générale</th><th class="r">Même mention, France</th></tr></thead><tbody>${rows}</tbody></table></div>
      ${link("boussole-des-masters.html", a, "Comparer les masters avec la Boussole")}`;
    Spedago.sortable($("t-mm"));
  }

  function blocPo(a) {
    if (!a.pours) { $("po").innerHTML = `<p class="empty">Académie hors du champ de ce jeu de données (France métropolitaine et DROM, hors COM).</p>`; return; }
    const k = cmpObj(), nom = cmpNom(), ref = new Map((k.pours || []).map((r) => [r[0], r]));
    const pc = (r, i) => (r && r[1] ? r[i] / r[1] : NaN), tot = (r) => (r ? r.slice(2).reduce((s, x) => s + x, 0) : 0);
    const cols = [["Université (hors IUT)", 2], ["IUT", 3], ["Classes prépa", 4], ["BTS", 5], ["Autres écoles et formations", 6]];
    const rows = a.pours.map((r) => {
      const c = ref.get(r[0]), t = r[1] ? tot(r) / r[1] : NaN, tc = c && c[1] ? tot(c) / c[1] : NaN;
      return `<tr><td data-v="${esc(r[0])}">${esc(r[0])}<small>${fmtInt(r[1])} bacheliers</small></td>
        <td class="r" data-l="Poursuivent" data-v="${t}"><strong>${fmtPct(t)}</strong><small>${esc(nom)} ${fmtPct(tc)}</small></td>
        ${cols.map(([l, i]) => `<td class="r" data-l="${l}" data-v="${pc(r, i)}">${fmtPct(pc(r, i))}<small>${esc(nom)} ${fmtPct(pc(c, i))}</small></td>`).join("")}</tr>`;
    }).join("");
    $("po").innerHTML = `<p>Part des bacheliers de la session ${D.rentree_poursuite}, ayant passé le bac dans l'académie, inscrits dans le supérieur à la rentrée suivante, où qu'ils étudient.</p>
      ${toolbar("po", "la poursuite d'études")}
      <div class="tablewrap"><table id="t-po"><caption class="sr-only">Poursuite d'études des bacheliers par voie et par filière</caption><thead><tr><th>Voie du bac</th><th class="r">Poursuivent</th>${cols.map(([l]) => `<th class="r">${l}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table></div>
      <p class="note">Source : SIES, taux de poursuite des néo-bacheliers par académie d'obtention du bac. Apprentissage en BTS compris ; formations hors du champ du ministère non comptées.</p>`;
    Spedago.sortable($("t-po"));
  }

  // ---- export : les lignes affichées (ordre de tri compris), valeurs brutes
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-export]"); if (!b) return;
    const a = D.academies[+$("acad").value], t = $("t-" + b.dataset.export);
    Spedago.download(`spedago-${a.slug}-${b.dataset.export}.csv`, Spedago.csv(Spedago.tableRows(t)));
  });

  function render() {
    const a = D.academies[+$("acad").value];
    $("zone").textContent = a.zone;
    stats(a); blocPs(a); blocPo(a); blocSpe(a); blocMm(a);
    Spedago.announce(`Fiche de l'académie ${a.nom}, comparée à ${cmpNom()}`);
  }
  $("acad").addEventListener("change", () => { Spedago.setHash(D.academies[+$("acad").value].nom); render(); });
  $("cmp").addEventListener("change", () => { Spedago.setParams({ cmp: $("cmp").value === "fr" ? "" : D.academies[+$("cmp").value].slug }); render(); });
  $("pick").addEventListener("submit", (e) => e.preventDefault());
  window.addEventListener("hashchange", () => { if (Spedago.pick($("acad"))) render(); });
  document.addEventListener("spedago:profil", () => { if (!Spedago.hashSlug() && Spedago.pick($("acad"))) render(); });
  render();
}

loadData('mon_academie').then(main);
