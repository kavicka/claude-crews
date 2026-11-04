Online ordering with pickup time slots is built to the numbers from Jana's quote, and nothing is committed yet. All 323 tests pass, typecheck is clean, and the reviewer approved with two small follow-ups. Nobody has tried the forms in a real browser or run a live server.

**What customers get**
- A new order section on the page: pick quantities, choose a 30-minute pickup slot and enter contact details. Payment is at pickup.
- The shop gets an email in Slovak with Reply-To set to the customer, and the customer gets a confirmation in their language. The page then shows the order number.
- Orders are saved to `data/orders.json` (or the path in `ORDERS_FILE`), so slot counts survive restarts. That folder is excluded from git.

**Your rules, as implemented**
- 8 orders per slot.
- No same-day orders. Orders for a day close at 14:00 the day before, and Tuesday's close on Sunday at 12:00.
- Orders up to 14 days ahead.
- Closed on 25 and 26 Dec, 1 and 6 Jan.
- Medovník needs 2 days' notice, at most 3 per order.
- At most 20 of each item, and at most 3 open orders per email address.
- Prices always come from the server's menu.

**Fixes from testing and review**
- **Contact form crash (bug that was already there):** a crafted request to the contact form left the request hanging and could crash the server. Fixed.
- **Spam:** both forms have a hidden trap field for bots.
- **Double-clicks:** a double-click or resubmit no longer creates two orders. A changed form resubmitted after pressing Back still counts as a new order.
- **Error pages:** if an order can't be placed, the customer sees a translated "your order was NOT placed" page instead of an error dump. `npm start` now runs in production mode.
- **Contact subject:** the name in the contact form can no longer break the email subject.

**Files changed:** `src/app.ts`, `src/render.ts`, `src/hours.ts`, `src/i18n.ts`, `src/menu.ts`, `src/index.ts`, `src/locales/sk.json`, `src/locales/en.json`, `public/style.css`, `package.json`, `.gitignore`, `CLAUDE.md`.
**New files:** `src/slots.ts` and `src/orders.ts`, plus 9 test files in `test/` (the new tests and a shared helper).

**Assumptions I made (please check with Jana)**
- **Cut-off after a closed day:** orders close on the last open day before pickup, at 14:00 or at closing time if earlier. That is how Tuesday ends up at Sunday 12:00, and it also applies after holidays: orders for 27 Dec close on 24 Dec at 14:00.
- **Cake notice:** "2 days' notice" means the pickup date is at least 2 calendar days after the order date.
- **Email limit:** "open orders" means orders not cancelled and with a pickup still in the future.
- **Edits on resubmit:** if a customer goes Back and changes only their name, phone or note, they're sent to the original order and the edit is dropped.

**Decisions and follow-ups for you**
1. **Per-IP rate limit (still open from review).** Someone can still fill every slot using throwaway email addresses; the trap field only stops simple bots. A per-IP limit needs to know whether the site runs behind a proxy. If set up wrong, every customer looks like the same visitor and the whole site gets capped. Tell me how it's deployed and I'll add it.
2. **Real email.** `src/index.ts` still uses `ConsoleMailer`, so the shop receives nothing in production. This must be wired before go-live.
3. **Freeing slots by hand.** Stop the server, set `"status": "cancelled"` on the order in `data/orders.json`, then start it again. The file only supports one server process.
4. **Data retention.** Orders, with personal data, are never deleted. Worth agreeing a retention period with Jana for GDPR.
5. **Two rare double-failure cases (reviewer follow-ups).** A reload after both the shop mail and the cancel fail, or a double-click while the shop mail is failing, can show "Thank you" for an order the shop never got.
6. **Phase 2 (already in the quote).** Cancel link in the shop email and an order list.

**Proposed commit.** The repo's only commit uses a plain-sentence style, so I matched it instead of a Conventional Commit prefix. The contact-form fix is mixed into the same `src/app.ts` changes, so one commit is cleanest. Leave the untracked `.claude/` folder out; it's agent memory, not project code.
```
Online ordering with pickup time slots

30-minute pickup slots, 8 orders each, up to 14 days ahead. No same-day
orders: a day closes at min(14:00, closing time) on the last open day
before it. Holiday closures, medovník with 2 days' notice (max 3),
max 20 per item, max 3 open orders per email, pay at pickup. Orders are
saved to data/orders.json.

Harden both forms: honeypot field, resubmission token, translated 500
page with no stack traces, no CR/LF in the contact name, and no hang
when a contact field is repeated.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

Should I commit it like this (on a new branch, or on `master`)?
