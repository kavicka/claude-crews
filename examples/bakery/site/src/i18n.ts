import en from "./locales/en.json" with { type: "json" };
import sk from "./locales/sk.json" with { type: "json" };

export type Lang = "sk" | "en";
export type Messages = typeof sk;

const MESSAGES: Record<Lang, Messages> = { sk, en };

export function pickLang(value: unknown): Lang {
  return value === "en" ? "en" : "sk";
}

export function t(lang: Lang): Messages {
  return MESSAGES[lang];
}
