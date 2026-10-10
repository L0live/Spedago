// @ts-nocheck — portage de l'interface ; types à resserrer progressivement
import '../styles/commun.css';
import '../styles/simulateur-parcoursup.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';
import { SimCalc } from '../calc/simulateur';

async function main(D0: any) {

  const C = SimCalc, D = D0;
  const $ = (id) => document.getElementById(id);
  const fmtInt = (x) => Math.round(x).toLocaleString("fr-FR");
  const fmtPct = (x, d = 1) => (x * 100).toFixed(d).replace(".", ",") + " %";
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const DEF = { pct: 10, q: 75, sat: 95, sous: 80, regle: "s1", filiere: "" };
  const FIL = (i) => (D.libelles_filieres || {})[D.filieres[i]] || D.filieres[i];
  D.filieres.forEach((f, i) => { const o = document.createElement("option"); o.value = i; o.textContent = FIL(i); $("filiere").appendChild(o); });

  function params() {
    return { regle: $("regle-s2").checked ? "s2" : "s1", pct: +$("pct").value / 100, q: +$("q").value / 100,
             sat: +$("sat").value / 100, sous: +$("sous").value / 100 };
  }

  function table(id, rows, cells) {
    const tb = $(id).tBodies[0]; tb.innerHTML = "";
    const moi = $("acad").value;  // académie choisie (adresse, profil ou menu) -> ligne surlignée
    rows.forEach((r) => {
      const tr = document.createElement("tr");
      if (id === "t-acad") { if (r.idf) tr.classList.add("idf"); if (moi !== "" && r.key === +moi) tr.classList.add("moi"); }
      tr.innerHTML = cells(r); tb.appendChild(tr);
    });
    Spedago.sortable($(id));
  }

  function render() {
    const p = params(), fil = $("filiere").value;
    $("pct-out").textContent = `${$("pct").value} %`;
    $("pct-label").textContent = p.regle === "s1" ? "Places ajoutées" : "Plafond par formation";
    $("q-out").textContent = `${$("q").value} %`; $("sat-out").textContent = `${$("sat").value} %`; $("sous-out").textContent = `${$("sous").value} %`;
    const res = C.simulate(D, p);
    const acad = C.groupBy(D, res, C.COL.A, fil).sort((a, b) => b.ajout / b.places - a.ajout / a.places);
    const tot = acad.reduce((s, r) => s + r.ajout, 0), pl = acad.reduce((s, r) => s + r.places, 0);
    const idf = acad.filter((r) => r.idf).reduce((s, r) => s + r.ajout, 0);
    const couv = fil === "" ? res.couvert : (res.couvertFil.get(+fil) || 0);
    const visees = acad.reduce((s, r) => s + r.visees, 0);
    $("summary").innerHTML = [
      [fmtInt(tot), "places ajoutées"],
      [pl ? fmtPct(tot / pl) : "–", "des places de la sélection"],
      [tot ? fmtPct(idf / tot, 0) : "–", "en Île-de-France"],
      [tot ? fmtPct(couv / tot, 0) : "–", "récupérables sur des places vides"],
    ].map(([v, l]) => `<div class="stat"><b>${v}</b><span>${l}</span></div>`).join("");
    Spedago.announce($("summary").innerText);
    $("lecture").innerHTML = tot
      ? `${fmtInt(visees)} formations recevraient des places. Sur ces <strong>${fmtInt(tot)}</strong> places, au plus <strong>${fmtInt(couv)}</strong> pourraient venir de places restées vides dans une formation de même spécialité de la même académie ; le reste (${fmtInt(tot - couv)}) demanderait des moyens nouveaux.`
      : "Aucune formation ne remplit les conditions avec ces réglages.";
    const dm = C.demande(D, res.add, fil);
    $("demande").innerHTML = tot && dm.formationsRang
      ? `<strong>Ces places trouveraient-elles preneur ?</strong> Dans <strong>${fmtPct(dm.couvertes / dm.formationsRang, 0)}</strong> des ${fmtInt(dm.formationsRang)} formations visées à liste d'appel propre, il restait au moins autant de candidats classés jamais appelés que de places ajoutées (médiane : ${fmtInt(dm.medianeRatio)} classés non appelés par place ajoutée). Ces chiffres comptent des candidatures, pas des personnes : un même candidat est classé dans plusieurs formations, et beaucoup ont été admis ailleurs. Ils disent que les places seraient remplies, pas combien d'élèves sans proposition en profiteraient.${dm.sansRang ? ` Pour ${fmtInt(dm.sansRang)} formations à liste commune (${fmtInt(dm.ajoutSansRang)} places), ce n'est pas mesurable.` : ""}`
      : "";
    const maxA = Math.max(...acad.map((r) => r.ajout / (r.places || 1)), 1e-9);
    table("t-acad", acad.filter((r) => r.places > 0), (r) => `<td data-v="${esc(D.academies[r.key])}">${esc(D.academies[r.key])}</td><td class="r" data-v="${r.places}">${fmtInt(r.places)}</td><td class="r" data-v="${r.ajout}">${fmtInt(r.ajout)}</td>
      <td class="barcell" data-v="${r.ajout / r.places}"><span class="sr-only">${fmtPct(r.ajout / r.places)}</span><div class="hbar" title="${fmtPct(r.ajout / r.places)}" aria-hidden="true"><span style="width:${(r.ajout / r.places) / maxA * 100}%"></span></div></td>`);
    const ac = $("acad").value, nomA = ac === "" ? "" : D.academies[+ac];
    $("h-fil").textContent = nomA ? `Par filière · ${nomA}` : "Par filière";
    const fils = C.groupBy(D, res, C.COL.FIL, fil, ac).filter((r) => r.places > 0).sort((a, b) => b.ajout - a.ajout);
    const cv = (k) => (ac === "" ? res.couvertFil.get(k) : res.couvertAF.get(ac + "|" + k)) || 0;
    table("t-fil", fils, (r) => `<td data-v="${esc(FIL(r.key))}">${esc(FIL(r.key))}</td><td class="r" data-v="${r.visees}">${fmtInt(r.visees)}</td><td class="r" data-v="${r.ajout}">${fmtInt(r.ajout)}</td><td class="r" data-v="${r.nonServis}">${fmtInt(r.nonServis)}</td><td class="r" data-v="${cv(r.key)}">${fmtInt(cv(r.key))}</td>`);
    const spe = C.groupBy(D, res, C.COL.SPE, fil, ac).filter((r) => r.ajout > 0).sort((a, b) => b.ajout - a.ajout).slice(0, 15);
    table("t-spe", spe, (r) => `<td data-v="${esc(D.specialites[r.key])}">${esc(D.specialites[r.key])}</td><td class="r" data-v="${r.ajout}">${fmtInt(r.ajout)}</td>`);
  }

  function reset() {
    $("pct").value = DEF.pct; $("q").value = DEF.q; $("sat").value = DEF.sat; $("sous").value = DEF.sous;
    $("regle-s1").checked = true; $("filiere").value = DEF.filiere; saveState(); render();
  }
  // export du classement par académie (ordre affiché)
  $("export-acad").addEventListener("click", () => Spedago.download("spedago-simulation-academies.csv", Spedago.csv(Spedago.tableRows($("t-acad")))));
  $("controls").addEventListener("input", render);
  $("controls").addEventListener("change", render);
  $("controls").addEventListener("submit", (e) => e.preventDefault());
  $("reset").addEventListener("click", reset);
  // Académie : adresse, sinon profil ; tous les réglages vont dans l'adresse (lien partageable)
  D.academies.forEach((a, i) => { if (a) { const o = document.createElement("option"); o.value = i; o.textContent = a; $("acad").appendChild(o); } });
  Spedago.pick($("acad"));
  $("acad").addEventListener("change", () => Spedago.setHash($("acad").value === "" ? "" : $("acad").selectedOptions[0].textContent));
  const saveState = Spedago.bind({ regle: $("regle-s1"), pct: $("pct"), q: $("q"), sat: $("sat"), sous: $("sous"), filiere: $("filiere") });
  window.addEventListener("hashchange", () => { if (!Spedago.pick($("acad"))) $("acad").value = ""; render(); });
  document.addEventListener("spedago:profil", () => { if (!Spedago.hashSlug() && Spedago.pick($("acad"))) render(); });
  render();
}

loadData('simulateur').then(main);
