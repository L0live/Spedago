// Spédago — scan d'accessibilité automatique (axe-core, WCAG 2.0/2.1/2.2 A-AA) des pages du dossier site/.
// Usage : npm i axe-core playwright  puis  node tools/check_a11y.mjs site node_modules/axe-core/axe.min.js
// Code de sortie 1 si une violation « serious » ou « critical » est trouvée (ordinateur 1280 px et téléphone 390 px).
import fs from 'fs';
import path from 'path';
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const [dir, axePath] = process.argv.slice(2);
const axe = fs.readFileSync(axePath, 'utf8');
const pages = fs.readdirSync(dir).filter((f) => f.endsWith('.html'));
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
let graves = 0;
for (const [w, h, tag] of [[1280, 900, 'ordinateur'], [390, 844, 'téléphone']]) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  for (const f of pages) {
    await p.goto('file://' + path.resolve(dir, f)); await p.waitForTimeout(400);
    await p.addScriptTag({ content: axe });
    const r = await p.evaluate(async () => axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }));
    for (const v of r.violations) {
      if (v.impact === 'serious' || v.impact === 'critical') graves += 1;
      console.log(`${tag} ${f} · ${v.impact} · ${v.id} (${v.nodes.length}) · ${v.help}`);
    }
  }
}
await b.close();
console.log(graves ? `${graves} violation(s) graves` : 'Aucune violation grave.');
process.exit(graves ? 1 : 0);
