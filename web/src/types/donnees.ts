// Formes des données publiées par le pipeline Python (web/public/data/*.json).
// Les lignes sont des tuples compacts : l'ordre des colonnes est documenté dans chaque script build_* et ci-dessous.

/** Simulateur : [académie, filière, spécialité, idf 0/1, mobilisable 0/1, places, admis, candidats PP, non appelés (-1 = inconnu), liste commune (1/0/-1)] */
export type FormationSim = [number, number, number, number, number, number, number, number, number, number];
export interface DonneesSimulateur {
  session: number; academies: string[]; filieres: string[]; libelles_filieres?: Record<string, string>; specialites: string[];
  perimetre_mobilisable: string[]; colonnes: string[]; formations: FormationSim[];
}

/** Boussole : [ifc, étab, académie, mention, parcours, alternance, secteur, places[session], rang dernier appelé[session], stats aplaties] */
export type FormationMaster = [string, number, number, number, string, number, number, (number | null)[], (number | null)[], number[]];
export type Prior = [number, number];
export interface DonneesBoussole {
  sessions: number[]; profils: string[]; libelles_profils: Record<string, string>; etablissements: string[]; academies: string[];
  mentions: string[]; secteurs: string[]; min_candidats: number; formations: FormationMaster[];
  priors: Record<string, Record<string, Prior>>;
  insertion?: { mois: number; formations: Record<string, [number, number, string, number | null]>; mentions: Record<string, number> };
}

/** Carte : [uai, nom, commune, statut, académie, bassin, lat, lon, effectif, codes par spécialité, plus proche {indice: [km, uai]}] */
export type LyceeCarte = [string, string, string, string, string, string, number, number, number, number[], Record<string, [number, string]>];
/** Groupe d'ouverture commune : [spécialité, membres (indices de lycées), demande estimée, distance max km] */
export type GroupeCarte = [number, number[], number, number];
export interface DonneesCarte {
  rentree: number; rayon_km: number; seuil: number; specialites: string[]; libelles_specialites?: Record<string, string>;
  taux: number[]; taux_haut: number[]; lycees: LyceeCarte[]; groupes: GroupeCarte[];
}

/** Mention de master : [mention, formations, places, candidats L3, propositions L3, candidats L3 France, propositions L3 France] */
export type MentionAcad = [string, number, number, number, number, number, number];
/** Poursuite : [voie du bac, bacheliers, université, IUT, CPGE, STS, autres] */
export type PoursuiteAcad = [string, number, number, number, number, number, number];
/** Offre Parcoursup : [formations, privées, dont hors contrat, places, places privées] */
export type OffrePrivee = [number, number, number, number, number];
export interface AcademieFiche {
  nom: string; slug: string; zone: string; ref: number[] | null;
  ps: { total: number[]; filieres: number[][]; sim: number[] } | null;
  spe: { lycees: number; spe: number[][] } | null;
  mm: { total: number[]; mentions: MentionAcad[] } | null;
  pours: PoursuiteAcad[] | null;
  prive: { hors_app?: OffrePrivee; app?: OffrePrivee } | null;
}
export interface DonneesAcademie {
  session: number; rentree: number; rentree_poursuite: number; alpha: number; filieres: string[]; specialites: string[]; prive_colonnes: string[];
  libelles_filieres?: Record<string, string>; libelles_specialites?: Record<string, string>;
  france: Omit<AcademieFiche, 'slug' | 'zone'>; academies: AcademieFiche[];
}

/** Mes spécialités : lycée [uai, nom, commune, académie, codes carte, plus proche, IVAL | null] */
export type LyceeSpe = [string, string, string, string, number[], Record<string, [number, string]>, (number | null)[] | null];
export interface DonneesSpecialites {
  annee: number; rayon_km: number; rentree_carte: number; annee_ival: number;
  eds: [string, string, string[]][]; carte_specialites: string[]; doublettes: [number, number][];
  n: [number, number, number][]; groupes: [string, string, string][];
  g: [number, number, number, number, number][]; formations: [number, string][]; f: [number, number, number, number, number][];
  tendance: Record<string, [number, number, number][]>; total_annees: Record<string, number>; lycees: LyceeSpe[];
}

/** France et voisins : valeur d'indicateur [moyenne 3 ans, dernière, première année, dernière année, drapeau] */
export type ValeurRegion = [number, number, string, string, string];
export interface DonneesVoisins {
  mobilite: { annees: string[]; pays: [string, string][]; sortants: Record<string, [number | null, string][]>;
    entrants: Record<string, [number | null, string][]>; niveaux: Record<string, (number | null)[]>; ue: [string, number | null][] };
  indicateurs: [string, string, string][]; regions: Record<string, { nom: string; pays: string; v: Record<string, ValeurRegion> }>;
  academies: [string, string, string[], string[]][]; refs: string[]; drapeaux: Record<string, string>; noms_pays: Record<string, string>;
}

/** Méthodes : registre des indicateurs (spedago/indicateurs.py) et sources du MANIFEST */
export interface SeuilIndicateur { libelle: string; valeur: number | string; module: string; constante: string }
export interface Indicateur {
  id: string; nom: string; theme: string; definition: string; formule: string; champ: string;
  sources: string[]; pages: string[]; rapport: string; limites: string[]; seuils: SeuilIndicateur[];
}
export interface SourceDonnee {
  jeu: string; producteur: string; url: string; telecharge_le: string; sha256: string;
  lignes?: number; requete?: string; maj_producteur?: string;
}
export interface DonneesMethodes { indicateurs: Indicateur[]; sources: Record<string, SourceDonnee>; pages: Record<string, string> }

/** Accueil : académies [nom, slug] ; chiffres [valeur, libellé, champ, fiche méthodologique] */
export interface DonneesAccueil { academies: [string, string][]; chiffres: [number, string, string, string][] }
