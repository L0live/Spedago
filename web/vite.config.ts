// Spédago — application multipage (une page HTML par outil), données JSON chargées à la demande depuis public/data.
// La barre de navigation (avec le panneau « Mon profil ») est produite par le pipeline Python (spedago/pages.py → generated/nav.json)
// et insérée dans chaque page au build : une seule source pour la navigation, aucun JavaScript nécessaire pour l'afficher.
import { readFileSync, readdirSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { defineConfig, type Plugin } from 'vite';

const root = import.meta.dirname;
const pages = readdirSync(root).filter((f) => f.endsWith('.html'));

function navigation(): Plugin {
  return {
    name: 'spedago-nav',
    transformIndexHtml(html, ctx) {
      const nav: Record<string, string> = JSON.parse(readFileSync(resolve(root, 'generated/nav.json'), 'utf8'));
      const page = basename(ctx.filename);
      if (!nav[page]) throw new Error(`navigation absente pour ${page} (relancer scripts/build_web_meta.py)`);
      if (!html.includes('<!--PIED-->')) throw new Error(`pied de page commun absent de ${page} (<!--PIED--> dans <footer>)`);
      const pied = readFileSync(resolve(root, 'generated/pied.html'), 'utf8');
      return html.replace('<!--NAV-->', nav[page]).replace('<!--PIED-->', pied);
    },
  };
}

export default defineConfig({
  base: './',  // chemins relatifs : fonctionne sur GitHub Pages (sous-dossier du dépôt) comme sur un domaine propre
  plugins: [navigation()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: { input: Object.fromEntries(pages.map((f) => [f.replace('.html', ''), resolve(root, f)])) },
  },
});
