// Chargement des données d'une page (public/data/<nom>.json), avec état visible et message d'erreur accessible.
export async function loadData<T = any>(name: string): Promise<T> {
  const main = document.getElementById('contenu');
  const status = document.createElement('p');
  status.className = 'chargement';
  status.setAttribute('role', 'status');
  status.textContent = 'Chargement des données…';
  main?.prepend(status);
  main?.setAttribute('aria-busy', 'true');
  try {
    const r = await fetch(`${import.meta.env.BASE_URL}data/${name}.json`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const d = (await r.json()) as T;
    status.remove();
    return d;
  } catch (e) {
    status.className = 'chargement erreur';
    status.setAttribute('role', 'alert');
    status.textContent = `Les données de cette page n’ont pas pu être chargées (${(e as Error).message}). Rechargez la page ; si le problème persiste, la publication est peut-être en cours.`;
    throw e;
  } finally {
    main?.removeAttribute('aria-busy');
  }
}

// Remplit les <span data-meta="…"> (année, rayon, seuil…) à partir des données.
export function fillMeta(values: Record<string, string | number>): void {
  document.querySelectorAll<HTMLElement>('[data-meta]').forEach((el) => {
    const k = el.dataset.meta ?? '';
    if (k in values) el.textContent = String(values[k]);
  });
}
