// Spédago — captures pleine page des pages construites (contrôle visuel d'une refonte, design.md).
// Usage : node tools/captures.mjs <dossier-sortie> [base] [page…]   (CHROMIUM=chemin d'un Chrome local, facultatif)
// Écrit <page>-<largeur>.png pour 1440, 375 et 320 px et signale tout défilement horizontal.
import fs from 'fs';
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const [out, base = 'http://localhost:4173/', ...pages] = process.argv.slice(2);
const liste = pages.length ? pages : ['index.html'];
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
let debord = 0;
for (const w of [1440, 375, 320]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 } });
  for (const f of liste) {
    await p.goto(new URL(f, base).href); await p.waitForSelector('[aria-busy="true"]', { state: 'detached', timeout: 10000 }).catch(() => {}); await p.waitForTimeout(400);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    if (sw > w) { debord += 1; console.log(`débordement ${f} à ${w} px : ${sw} px`); }
    await p.screenshot({ path: `${out}/${f.replace('.html', '')}-${w}.png`, fullPage: true });
  }
  await p.close();
}
await b.close();
console.log(debord ? `${debord} page(s) avec défilement horizontal` : 'Aucun défilement horizontal.');
process.exit(debord ? 1 : 0);
