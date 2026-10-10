// @ts-nocheck — portage de l'interface ; types à resserrer progressivement
import '../styles/commun.css';
import '../styles/index.css';
import { Spedago } from '../lib/commun';
import { loadData, fillMeta } from '../lib/data';

async function main(D0: any) {
  const D = D0;

  
  const sel = document.getElementById("acad");
  document.getElementById("figures").innerHTML = D.chiffres
    .map(([n, t, champ, id]) => `<li><b>${Math.round(n).toLocaleString("fr-FR")}</b><span>${t}</span>`
      + `<a class="champ" href="methodes.html#${id}">${champ} · méthode</a></li>`).join("");
  D.academies.forEach(([nom, slug]) => { const o = document.createElement("option"); o.value = slug; o.textContent = nom; sel.appendChild(o); });
  if (!Spedago.pick(sel)) sel.value = "poitiers";
  document.getElementById("go").addEventListener("submit", (e) => { e.preventDefault(); location.href = "mon-academie.html#" + sel.value; });
  sel.addEventListener("change", () => Spedago.setHash(sel.selectedOptions[0].textContent));
}

loadData('index').then(main);
