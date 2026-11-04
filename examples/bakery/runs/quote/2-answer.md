The quote is ready for your review: **phase 1 at 3 500 € excl. VAT, exactly Jana's ceiling**. To get there, the builder moved the menu photos out of phase 1, because with honest hours phase 1 came to 3 800 €. Nothing has been sent to Jana.

## Totals (excl. VAT)

| | Hours | Fixed | Hourly (50 €/h) |
|---|---|---|---|
| **Phase 1 (main offer):** order form for the 7 menu products, pickup slots, emails, SK + EN, spam protection, privacy notice | 70 h | **3 500 €** | 64–78 h, 3 200–3 900 € |
| **Phase 2 (optional):** password-protected next-day list, A4 print, totals per product, "cancelled" switch that frees the slot | 10 h | 500 € | 8–12 h, 400–600 € |
| Menu photos (optional) | 5 h | 250 € | |
| **Everything** | | **4 250 €** | |

Going over the upper hourly bound needs written approval.

**Other optional add-ons:**
- Online cake deposit: from 700 €, no earlier than January, after her accountant has checked eKasa.
- Hosting setup: 120 €. The quote now marks this as likely.
- Maintenance: 60 € per month.

**Cakes:** only medovník (38 €) can be ordered online. Made-to-order cakes and cakes over 50 € stay by phone or in the shop with the 30 % deposit, as today.

## Payment
- **Phase 1:** 1 400 € at signing, 1 400 € when Jana reviews the test version of the site, 700 € at handover.
- **Phase 2:** 500 €, invoiced on handover.
- Invoices are due in 14 days. If Jana sends no comments within 2 working days of review, the test version counts as approved.

## Timeline
- **9 Nov:** signing.
- **11 Nov:** slot and cut-off settings are fixed. Changes after that are billed at 50 €/h, estimated in writing first.
- **20 Nov:** Jana's texts due.
- **25 Nov:** test version stable for the staff session.
- **30 Nov:** deploy, while the shop is closed.
- **1 Dec:** target launch, confirmed only once her texts arrive.
- **Late texts:** up to 3 working days late, launch moves day for day. Beyond that, the quote offers launching with the existing site's texts.
- **Phase 2:** by 11 Dec.

## Reviews
- **Pricing analyst:** "NEEDS INFO" on the first draft (3 600 €). It called the hours slightly short against the florist project's actual hours and the deposit add-on underpriced. Both are fixed now.
- **Skeptic's top objection:** cancelled orders and unpaid big cakes would still get baked. That is covered now: deposit cakes are off the online form, and phase 2 has the "cancelled" switch.

## Left for you to decide
1. **Email in production.** In the `kvasok-site` repo the contact form only prints to the console. Please check how it actually sends email today before signing. The quote includes 7 h for setting up real sending.
2. **Hosting.** Check whether the host runs Node with a disk that keeps data. If not, add the 120 € hosting line.
3. **VAT.** Your pricing file says 20 %, but the analyst found Slovakia's standard rate has been 23 % since 1 January 2025. The quote just says "DPH podľa platnej sadzby" (VAT at the current rate). Should I update `pricing/README.md`?
4. **"Nová cena" labels.** Phase 2 and the photo add-on are marked "nová cena" (new price) in the client-facing text. Keep or remove?
5. **Cancellations without phase 2.** If Jana skips phase 2, there is still no way to cancel an order or free its slot. Cancellations then stay manual, by phone.
6. **Assumptions for Jana to confirm:**
   - 30-minute slots with 8 orders each.
   - Next-day orders close at 14:00.
   - Medovník needs 2 days' notice.
   - Orders up to 14 days ahead.
   - Still open: the Tuesday cut-off after the closed Monday, and the hours from 24 Dec to 6 Jan.
7. **Privacy notice.** It's written from a template and is not legal advice. Jana confirms it as the data owner.

Files are in `~/knowledge`:
- `pricing/quotes/2026-11-04-kvasok-a-syn.md`: the quote, in Slovak.
- `clients/kvasok-a-syn.md`: I added the decisions from your call.

Want me to render the quote as a PDF?
