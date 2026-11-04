# A bakery goes online: one story through all three crews

**Kvások & syn** is a family bakery in Bratislava. It takes about 70 pre-orders a week by phone and Instagram, misses calls in the morning rush, and wants customers to order online and pick a time to collect. **Lucia** built its website two years ago and is asked to do this too. She uses claude-crews in the order a real project goes:

| | Command | Question it answers |
|---|---|---|
| 1 | `/council:vote Should the bakery launch with online payments or start with pay-at-pickup?` | What should we build? |
| 2 | `/office:quote one-page online ordering site for a bakery, Slovak + English, contact form to email` | What does it cost, and on what terms? |
| 3 | `/crew:ship add online ordering with pickup time slots to the bakery website` | Build it, tested and reviewed. |

> **What is real and what isn't.** The bakery, its owner Jana, Lucia and every number about them are invented: see [knowledge/](knowledge) (Lucia's knowledge base) and [site/](site) (the bakery's website before the change). The runs are real: Claude Code with the plugins from this repository, recorded on 2026-11-04 by [record.py](record.py). When an agent asked a question, the answer was written by the person recording the example, playing Lucia; every question and answer is shown below as it was. The client persona in the council is an agent too, not Jana.

Each step has a full, readable log of the conversation: what Lucia typed, every brief the main session sent to an agent, and every agent's answer. Briefs are folded.

---

## 1 · Decide: online payments or pay at pickup?

<p align="center"><img src="../../assets/bakery-council.svg" width="760" alt="Council debate as a chat"></p>

**How they decided.** Five members answered independently, then each read the others and answered the strongest opposing argument by name. All five voted **NO** to card payments at launch in both rounds. The interesting part is *why* the verdict came out the way it did:

- In round 1 everyone, the skeptic included, argued that big cakes "already carry a 30 % deposit". In round 2 the skeptic pointed at line 18 of the client file: that deposit is taken **in the shop**. Cakes ordered online would skip it, right before Christmas. That turned "payments later" into "pay at pickup, plus a stopgap for cakes".
- The client persona first asked for a launch date that didn't depend on Jana's texts arriving, then dropped it after the others pointed to Lucia's own rule against promising dates before content arrives.
- The moderator didn't vote. It checked the claims the decision rests on and threw out six, including a card fee off by half (0.46 €, not 0.30 €), a date the simulated client made up, and a project cited as a "payments delay" that had no payments.

**What it asked you.** It ended with six questions to put to the client before quoting:

> 1. Is the 3 000 € including or excluding VAT?
> 2. On what date will texts and photos arrive? Please confirm in writing.
> 3. Last December, how many cakes were never picked up, split into over and under 50 €?
> 4. Can she ask her accountant whether online deposits have to be recorded in eKasa, and how?
> 5. Does she want English at launch?
> 6. Until online deposits exist, is it OK that big cakes are confirmed only once the deposit is paid?

**What you got:** the verdict (REJECTED, 0 of 5 for payments at launch), a recommendation with an optional cake-deposit line of 400–500 €, and the debate logged to Lucia's knowledge base.

Files: [verdict as shown in chat](runs/council/1-answer.md) · [full debate log](runs/council/2026-11-04-bakery-online-payments-vs-pickup.md) · [whole conversation](runs/council/conversation.md) · 8 min · $2.53

---

## 2 · Quote: what does it cost?

<p align="center"><img src="../../assets/bakery-quote.svg" width="760" alt="Quote workflow as a chat"></p>

**What it asked you, before doing anything.** The quote workflow stops when missing facts would move the price by more than 20 %. It asked six questions and offered defaults ([1-answer.md](runs/quote/1-answer.md)):

> 1. **Scope.** (a) A one-page site where orders arrive through the contact form as emails, roughly 1 650–1 800 €. (b) An order form with pickup slots on the existing site, roughly 3 000–3 600 €. (c) A different bakery.
> 2. **Payments.** Online, at pickup, or a deposit online only for cakes over 50 €?
> 3. **Admin.** An order list with a daily export (+400 €), or are emails enough?
> 4. **Content.** Will Jana supply the texts and photos?
> 5. **Deadline.** A reduced phase 1 by 1 December, or a later date?
> 6. **Language** of the quote?

**Lucia's answers** ([2-prompt.md](runs/quote/2-prompt.md)), after asking Jana the council's questions:

> (b) pickup slots; pay at pickup, as the council decided; email notifications plus a printable list for the morning shift; Jana sends texts and photos by 20 November; phase 1 live by 1 December; quote in Slovak. Jana: the 3 000 € is excluding VAT and she can go to 3 500 €; last December 9 cakes were never picked up, 6 of them over 50 €.

**How they decided.**

1. **quote-builder** priced it from the hours of the most similar past project: 72 h, **3 600 €**, 100 € over Jana's ceiling. It did not squeeze the price to fit; it listed what could be cut.
2. **pricing-analyst** and **skeptic** reviewed it in parallel.
   - The analyst returned **NEEDS INFO**. The florist project the hours came from ran 19 % over its net estimate, so the slots were underestimated. It also found that Lucia's own pricing file uses 20 % VAT, while Slovakia's standard rate has been 23 % since January 2025.
   - The skeptic, playing Jana's procurement person, found that nobody could cancel an order or mark a deposit as paid, so cancelled orders and unpaid cakes would still be baked: exactly last December's 9 lost cakes. It also noticed that the "cakes over 50 €" rule couldn't trigger, because the only cake on the online menu costs 38 € (`site/src/menu.ts:18`).
3. **quote-builder** revised once with both lists: phase 1 at **3 500 €** by moving menu photos to an add-on instead of discounting, big cakes stay by phone, and an optional phase 2 (500 €) adds a "cancelled" switch that frees the slot.

**What it asked you at the end.** Two things only Lucia can check: how the existing site actually sends email in production (in the repository the contact form only prints to the console), and whether to fix the VAT rate in her pricing file.

**What the client gets:** [the quote, in Slovak](runs/quote/2026-11-04-kvasok-a-syn.md), with phases, line items and hours, payment terms, timeline and assumptions to confirm. Nothing was sent; Lucia sends it.

Files: [whole conversation](runs/quote/conversation.md) · [client file after the run](runs/quote/client-file-after.md) (the main session recorded the decisions from Lucia's call) · 13 min · $3.01

---

## 3 · Build: online ordering with pickup slots

<p align="center"><img src="../../assets/bakery-crew.svg" width="760" alt="Crew workflow as a chat"></p>

**How they decided, before any code.** The **planner** read the site and planned an order form, 30-minute slots with 4 orders each, and orders kept in memory. The **skeptic** answered **GO WITH CHANGES** with evidence from the code: a slot count kept in memory resets on every restart (`npm run dev` restarts on every edit), anyone could fill every slot with fake orders, and an async page route can crash Express 4 (`package.json:12`). It also caught that the planned order number was lowercase while the check for it expected uppercase, so the confirmation would never show.

**What it asked you: the checkpoint.** The crew stops once, before any code ([1-answer.md](runs/crew/1-answer.md)):

> **One decision I need from you:**
> - **A — no per-slot limit in v1 (recommended):** a slot is only a checked pickup time. The shop email is the record of the order, and the shop phones the customer if a slot gets too busy.
> - **B — 4 orders per slot:** orders are saved to a local file so the counts survive restarts. The shop email gets a cancel link that frees the slot, and there's a limit on open orders per email address.
>
> Reply **A** or **B**, plus any changes to the defaults, and I'll start the coder.

**Lucia's answer** ([2-prompt.md](runs/crew/2-prompt.md)), matching the quote Jana is signing:

> B, with 8 orders per slot saved to a file; no same-day orders, orders for a day close at 14:00 the day before (for Tuesday, on Sunday at 12:00); cakes with 2 days' notice, at most 3; orders up to 14 days ahead; at most 3 open orders per email; no cancel link yet, that's phase 2; closed on 25 and 26 Dec, 1 and 6 Jan.

**How they built and checked it.**

| Round | Agent | What happened |
|---|---|---|
| 1 | web-coder | Built slots, the order store (a JSON file), the form in both languages and the emails. |
| 1 | tester | Wrote edge-case tests (time zones, DST, cut-offs, capacity, escaping). Four failed on an **old bug**: a repeated field in the existing contact form hangs the request, because Express 4 doesn't catch a rejected promise (`src/app.ts:135`). |
| 1 | web-coder | Fixed it. |
| 1 | reviewer | **CHANGES REQUIRED.** A short script could book out all 1 920 places of the next two weeks: no per-IP limit, no honeypot. Error pages leaked stack traces, and a double click created two orders. |
| 2 | web-coder → tester → reviewer | Added a honeypot, a translated error page, `NODE_ENV=production` and a resubmission token. **CHANGES REQUIRED** again: the token fix matched on the token alone, so a customer who went Back, changed the day and resubmitted would silently get the first order. |
| 3 | web-coder → tester → reviewer | Compared the order content too. **APPROVE WITH NITS**: two rare double-failure cases logged as follow-ups. |
| — | docs-writer | Updated the site's `CLAUDE.md`. |

**What you get.** Nothing is committed. The crew handed back the [diff](runs/crew/changes.patch), 323 passing tests (235 written plus parameterised cases), clean typecheck, a proposed commit message, the assumptions it made, and the open decisions: a per-IP limit needs to know how the site is deployed, the production mailer is still a console stub, and nobody has agreed how long orders with personal data are kept.

<p align="center"><img src="../../assets/bakery-order-form.png" width="320" alt="The order form the crew built, English version"></p>

**Was it worth it?** It was the most expensive step by far: 45 minutes and $15 for the build alone, most of it in the review loops, and 323 tests is more than a feature this size needs. In exchange it found an old crash nobody had asked about, a way to book out the shop, and a regression introduced by its own fix. Whether that is worth $15 depends on what a bad December weekend would cost the bakery.

Files: [whole conversation](runs/crew/conversation.md) · [final summary](runs/crew/2-answer.md) · [diff](runs/crew/changes.patch) · 53 min · $16.54

---

## Totals

| Step | Agents that ran | Questions to you | Time | Cost |
|---|---|---|---|---|
| Council | optimist, skeptic, engineer, business, client ×2 rounds, moderator | 6 (for the client) | 8 min | $2.53 |
| Quote | quote-builder ×2, pricing-analyst, skeptic | 6 before, 2 after | 13 min | $3.01 |
| Crew | planner, skeptic, web-coder ×4, tester ×3, reviewer ×3, docs-writer | 1 at the checkpoint, 1 before go-live | 53 min | $16.54 |
| **All three** | | | **74 min** | **$22.08** |

Costs are what Claude Code reports at list price, subagents included.

## Re-run it

```bash
cd examples/bakery
python3 record.py setup           # a fresh home with Lucia's knowledge base and the site, outside the repo
python3 record.py run council
python3 record.py run quote       # stops with questions
python3 record.py answer quote my-answers.md
python3 record.py run crew        # stops at the checkpoint
python3 record.py answer crew my-answers.md
python3 extract.py                # readable conversation logs
```

Your runs will differ: the agents are not deterministic, and your answers steer them.
