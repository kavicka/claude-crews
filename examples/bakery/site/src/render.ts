import { OPENING_HOURS } from "./hours.js";
import { t, type Lang } from "./i18n.js";
import { formatPrice, MENU } from "./menu.js";

export function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]!);
}

export interface PageState {
  sent?: boolean;
  error?: boolean;
  values?: { name?: string; email?: string; message?: string };
}

export function renderHome(lang: Lang, state: PageState = {}): string {
  const m = t(lang);
  const other: Lang = lang === "sk" ? "en" : "sk";
  const v = state.values ?? {};

  const menu = MENU.map(
    (p) => `<li><span>${escapeHtml(p.name[lang])}</span> <strong>${formatPrice(p.priceCents, lang)}</strong></li>`,
  ).join("");

  const hours = [2, 3, 4, 5, 6, 0, 1]
    .map((day) => {
      const h = OPENING_HOURS[day];
      return `<li>${m.days[day]}: ${h ? `${h.open}–${h.close}` : m.closed}</li>`;
    })
    .join("");

  return `<!doctype html>
<html lang="${lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(m.title)}</title><link rel="stylesheet" href="/style.css"></head>
<body>
<header><h1>Kvások &amp; syn</h1><p>${escapeHtml(m.tagline)}</p><a href="/?lang=${other}">${m.otherLang}</a></header>
<main>
<section><h2>${m.menuHeading}</h2><ul class="menu">${menu}</ul></section>
<section><h2>${m.hoursHeading}</h2><ul>${hours}</ul></section>
<section id="contact"><h2>${m.contactHeading}</h2><p>${escapeHtml(m.contactIntro)}</p>
${state.sent ? `<p role="status">${m.sent}</p>` : ""}
${state.error ? `<p role="alert">${m.invalid}</p>` : ""}
<form method="post" action="/contact?lang=${lang}">
<label>${m.name} <input name="name" required value="${escapeHtml(v.name ?? "")}"></label>
<label>${m.email} <input name="email" type="email" required value="${escapeHtml(v.email ?? "")}"></label>
<label>${m.message} <textarea name="message" required>${escapeHtml(v.message ?? "")}</textarea></label>
<button>${m.send}</button>
</form></section>
</main>
</body></html>`;
}
