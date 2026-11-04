# kvasok-site

One-page website of Kvások & syn, a fictional family bakery (claude-crews example). Express + TypeScript, server-rendered HTML, no database yet.

## Commands

- `npm test`: vitest + supertest (`test/`)
- `npm run typecheck`: `tsc --noEmit`
- `npm run dev`: dev server on :3000 (stop it when done)

## Map

- `src/app.ts`: routes (`GET /`, `POST /contact`); `createApp({ mailer })` so tests inject a fake mailer
- `src/render.ts`: the page as a template string; always pass user input through `escapeHtml`
- `src/menu.ts`: products and prices in cents; `src/hours.ts`: opening hours and time zone
- `src/i18n.ts` + `src/locales/{sk,en}.json`: every visible string exists in both locales
- `src/mailer.ts`: `Mailer` interface; `ConsoleMailer` in development

## Rules

- Validate every form with zod; on error re-render the page with status 400 and the escaped values.
- Times are local to `Europe/Bratislava`.
- Prices are integers in cents.
