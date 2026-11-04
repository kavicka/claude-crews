import type { Lang } from "./i18n.js";

export interface Product {
  id: string;
  name: Record<Lang, string>;
  priceCents: number;
  /** Cakes are made to order and need notice. */
  kind: "bread" | "pastry" | "cake";
}

export const MENU: Product[] = [
  { id: "kvaskovy-chlieb", name: { sk: "Kváskový chlieb 1 kg", en: "Sourdough loaf 1 kg" }, priceCents: 520, kind: "bread" },
  { id: "rascovy-chlieb", name: { sk: "Rascový chlieb 750 g", en: "Caraway rye 750 g" }, priceCents: 460, kind: "bread" },
  { id: "bageta", name: { sk: "Bageta", en: "Baguette" }, priceCents: 190, kind: "bread" },
  { id: "croissant", name: { sk: "Maslový croissant", en: "Butter croissant" }, priceCents: 180, kind: "pastry" },
  { id: "makovy-zavin", name: { sk: "Makový závin", en: "Poppy seed roll" }, priceCents: 350, kind: "pastry" },
  { id: "ranajkovy-box", name: { sk: "Raňajkový box pre 4", en: "Breakfast box for 4" }, priceCents: 1890, kind: "pastry" },
  { id: "medovnik", name: { sk: "Medovník (celá torta)", en: "Honey cake (whole)" }, priceCents: 3800, kind: "cake" },
];

export function formatPrice(cents: number, lang: Lang): string {
  return new Intl.NumberFormat(lang === "sk" ? "sk-SK" : "en-GB", { style: "currency", currency: "EUR" }).format(
    cents / 100,
  );
}
