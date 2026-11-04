# Council: Should Lucia recommend that Kvások & syn launch online pre-orders with online card payments from day one (vs. pay-at-pickup)?

Date: 2026-11-04 · Members: optimist, skeptic, engineer, business, client (Jana Kováčová) · Rounds: 2 · Threshold: 60 %

## Context

- Question asked: "Should the bakery launch with online payments or start with pay-at-pickup?" Framed as YES = online card payments (Stripe/GoPay) at launch, NO = pay-at-pickup, payments later.
- Client: Kvások & syn, family bakery in Bratislava–Ružinov, 1 shop, 7 staff, owner Jana Kováčová (`clients/kvasok-a-syn.md`).
- ~70 pre-orders/week (avg 14 €) + ~15 cakes/week (avg 38 €); 5–10 missed calls/day in the 7–9 rush.
- No-shows ~6 %, worst on cakes; 30 % deposit taken in the shop for cakes over 50 €. Card terminal at the counter, no online payments.
- Budget "around 3 000 €, a bit more if it clearly pays off"; deadline early December. Worries: fees, refunds, staff training. English "would be nice".
- Pricing (`pricing/README.md`): 50 €/h; payments add-on incl. refunds 700–900 €; extra language 300–450 €; prices excl. 20 % VAT.
- Reference: florist (`pricing/quotes/2026-03-12-kvetinarstvo-ruza.md`), no payments, 3 400 €, 68→74 h, 5→6 weeks. Café with Stripe, 3 locations, SK+EN: 120 h, 6 000 €, 8 weeks.
- Hard rule (`profile.md`): never promise a launch date before the client has delivered texts and photos.

## Round 1

### 🟢 optimist — NO 72
**Position:** Launch with pay-at-pickup, and build the order model so a cake-deposit payment can be added within weeks of launch. The upside of launching on time is larger than the upside of payments on day one.

**Arguments:**
- **Budget:** The base is about 3 400 € (florist reference), before payments. Adding English (300–450 €) and payments (700–900 €, `pricing/README.md`) gives roughly 4 400–4 750 €. That is well over Jana's "around 3 000 €". A pay-at-pickup base with a slimmer scope can land near her budget, which wins her trust.
- **Schedule:** The florist project slipped from 5 to 6 weeks and from 68 to 74 h. We have 4 weeks, and your rule says no date is promised before texts and photos arrive. Payments, refunds and webhook testing are the likeliest cause of missing early December. The café project with Stripe took 8 weeks.
- **Size of the prize:** The main gain is catching missed calls (5–10 a day) and giving customers pickup slots. Payments barely add to that. No-shows cost about 6 % of roughly 980 €/week in pre-orders, or about 59 €/week. Cakes are the real pain, and they already carry a 30 % deposit.
- **Jana's worries:** Fees, refunds and staff training are exactly what payments add. Launching without them removes all three, and a quick win builds the case for phase 2.

**Would change my mind:** Jana accepts about 4 500 € and a launch date that depends on her texts and photos, or she shows that cake no-shows cost far more than the 59 €/week estimate.

### 🔴 skeptic — NO 75
**Position:** Adding online payments within 4 weeks puts Jana's budget, the December deadline and the Christmas rush at risk, all to fix a problem worth about 93 €/week. Launch with pay-at-pickup and add cake deposits in January.

**Objections:**
- 🔴 Deadline: the florist job had the same shape and no payments, and still slipped from 5 to 6 weeks (74 h instead of 68 h, texts arrived a week late). The café job with Stripe took 8 weeks. Here we have about 4, and payments add 14–18 h plus merchant account setup.
- 🔴 Budget: the 3,400 € base plus 700–900 € for payments comes to 4,100–4,300 € excl. VAT. Jana said "around 3 000 €".
- 🟠 Small payoff: 70×14 €×6 % + 15×38 €×6 % ≈ 93 €/week at retail prices, and cakes over 50 € already carry deposits. Stripe charges 1.5 % + 0.25 €, which is 3.3 % of a 14 € box. A cheaper test is a no-code Stripe Payment Link for cake deposits.
- 🟡 Not checked (law text unreachable): how eKasa treats card payments taken through an online payment gateway under law 384/2025, in force since 1.1.2026. Jana's accountant must confirm.

**Would change my mind:** proof that no-shows cost much more than 93 €/week, or texts and photos arriving now plus Jana accepting about 4,300 €.

Sources: pricing/quotes/2026-03-12-kvetinarstvo-ruza.md, pricing/README.md, [Stripe EEA pricing](https://support.stripe.com/questions/pricing-updates-for-businesses-based-in-the-european-economic-area-(eea)), [podnikajte.sk eKasa](https://www.podnikajte.sk/ekasa/pouzivanie-ekasy-predaj-eshop)

### 🛠️ engineer — NO 78
**Position:** No. Launch with pay-at-pickup, plus an optional online deposit for cakes over 50 € as a fast follow-up, and add full online payments in January.

**Assessment:**
- **Budget:** The base is the florist shape: 68–74 h, about 3 400 €. Adding SK+EN (+300–450 €) and online payments (+700–900 €) gives about 4 400–4 750 €. That is 50 % over Jana's 3 000 €. Without payments and English, about 3 400 € is already slightly over budget.
- **Schedule:** The florist project ran 5 planned weeks and delivered in 6. We have 4 weeks, and the texts and photos haven't arrived. Payments add webhooks, refund handling, and a test pass with the real bank and terminal, which is the part most likely to slip. Estimate +10–14 h (range 8–18 h), so the full scope comes to about 85–95 h.
- **Value:** Payments mostly address the no-show rate. Online payment would cover about 6 % of 70 orders a week, roughly 4 orders at 14 €, so about 60 € a week. Cakes are about 15 a week at 38 €, and the larger ones already carry a deposit. The gain is real but small. Fees (about 1.5 % plus 0.25 € on Stripe EU cards) are minor but are one of Jana's worries.
- **Staff:** Refunds and payment reconciliation add training load during the Christmas rush, and Jana is already worried about staff learning a new system.
- **Middle option:** A cake-only deposit of 30 % takes about 8–10 h of the add-on, since the refund flow can be simplified at first. If Jana wants it at launch, take it as a clearly scoped change request.

**Would change my mind:** Jana raises the budget to about 4 500 € and delivers texts and photos by mid-November. In that case a cake-deposit-only version at launch would be feasible.

### 💰 business — NO 72
**Position:** Don't launch with full online payments on day one. Launch pay-at-pickup, and only add online deposits for cakes if the schedule allows. That cake deposit is the middle option.

**Numbers:**
- **Budget:** The florist-shape build is 3 400 € (68–74 h), already above Jana's 3 000 €. Adding payments (700–900 €) gives about 4 100–4 300 €, roughly 40 % over budget. Payments also bring refund and edge-case testing, and the SK+EN café job with Stripe took 120 h.
- **No-show loss:** 6 % × 70 × 14 € ≈ 59 €/week, plus about 1 cake/week at 38 € ≈ 34 €/week. That is about 90 €/week gross, or about 4 700 €/year in revenue. Margin loss is lower, and prepayment recovers only part of it. Fees are about 1.5 % + 0.25 € per card payment, which is roughly 3 % on a 14 € box and eats part of the gain. Payback on an extra ~800 € is probably 6+ months.
- **Schedule:** The florist job slipped from 5 to 6 weeks, and I have about 4 weeks. Adding payments puts the early-December date at real risk. Under Lucia's hard rule, she can't promise a date before Jana delivers texts and photos.
- **Missing knowledge:** No benchmarks are recorded in the pricing file, so the fee and recovery rates above are assumptions.

**Would change my mind:** Jana says she'd pay about 4 200 € and deliver all texts and photos by mid-November, or her cake no-shows turn out to be well above the 6 % average.

### 👤 client (Jana Kováčová) — NO 70
**Who I am:** Jana Kováčová, owner of Kvások & syn, a 7-person family bakery in Ružinov. I'm budgeting about 3 000 € and I'm anxious about fees, refunds and my staff.

**Reaction:**
- "Online card payments add-on 700–900 €": that is a quarter of my budget. A 14 € roll order loses about 0.30 € to fees, which doesn't worry me. The extra 800 € on top of the base price does. The base price alone is already near 3 400 €, as in the florist project.
- "~4 weeks to early December": the florist job ran 5 weeks planned and 6 delivered. Adding payments puts that at risk. If the system isn't ready when Christmas orders begin, I lose more than I'd save.
- "6 % no-shows, worst on cakes": this is my real pain. Cakes are about 15 a week at 38 €, so a deposit online would solve it. The 70 bread orders at 14 € are not worth the risk, since 6 % of them is about 60 € a week.
- "Refunds when a cake goes wrong": this scares me more than the fees. I would want a clear refund flow, or I'd prefer to refund by hand in the shop at first.
- The middle option (online payment only for cakes over 50 €) sounds right. It builds on the 30 % deposit I already take.

**Would change my mind:** A fixed price of 800 € or less for cake deposits only, a delivery date that doesn't depend on my texts and photos arriving late, and a refund flow my staff can use in two clicks.

## Round 2

### 🟢 optimist — NO 76 (72→76)
**Position:** Launch pay-at-pickup, but include a tightly scoped cake-deposit link (not full payments) as a priced option in the quote. This is still a NO on full online payments from day one.

**Reply to others:**
- Weakest point in the shared NO case: every member lumps "payments" together at 700–900 € and 14–18 h. Jana's own words ("fixed price ≤ 800 € for cake deposits only", refund by hand at first) show that the cake-only slice is a different product. The Optimist and Skeptic both defer it to January without testing it. Engineer's 8–10 h is about 400–500 € at 50 €/h, which fits her ≤ 800 € ceiling.
- Skeptic's no-code Stripe Payment Link is the best fit. It takes about 1–2 h, needs no webhooks, and staff refund from the Stripe dashboard. Cakes are about 15/week × 38 € = 570 €/week, so a 6 % no-show rate costs about 34 €/week. The case is weak, but the cost is almost nil. This holds only if the eKasa and accountant check passes.
- Business says payback takes 6+ months for 800 €. That is right for full payments. It does not apply to a Payment Link at about 100 €.
- Numbers check: the Optimist says 59 €/week for pre-orders and Skeptic says 93 €/week for both. Both are consistent. Nobody has shown that cake no-shows are more costly than the 6 % figure.

**Recommendation:** Launch pay-at-pickup. Cakes get a manual Payment Link, sent by staff after the order, with the order model kept ready for an automated deposit in January. The pickup-slot build is unaffected, and nothing depends on webhooks.

**Would change my mind:** the accountant says gateway payments break eKasa handling, or Jana's texts and photos arrive late.

### 🔴 skeptic — NO 70 (75→70)
**Position:** NO on putting payments in the build. Cake deposits still belong in the recommendation, as a no-code Stripe Payment Link.

**Objections:**
- 🔴 All of us, me included, said cakes "already carry a 30 % deposit". That deposit is taken "in the shop" (kvasok-a-syn.md:18). Once cakes can be ordered online, that protection is gone right before Christmas. The fix is to keep cakes over 50 € phone-only or have staff send a Payment Link.
- 🟠 Optimist's 59 €/week leaves out cakes. The real figure is about 93 €. Engineer's +10–14 h is below what the price list implies (700–900 € = 14–18 h).
- 🟠 "Café with Stripe took 8 weeks" (I used it too) doesn't prove payments caused the delay. That job had 3 locations and two languages (pricing/README.md:18).
- 🟡 Lucia's prices exclude 20 % VAT (README:3). Did Jana's 3 000 € include VAT? Nobody asked. The new eKasa law in force since 1.1.2026: checked, holds. How it treats online deposits is still unverified.

**Reply to others:**
- Engineer: 8–10 h (about 400–500 €) meets Jana's ≤ 800 € condition. But her "date that doesn't depend on my texts" breaks Lucia's hard rule (profile.md:36). So this should be a change request after the texts arrive.

**Would change my mind:** texts by ~13 Nov plus data showing cake no-shows spike in December.

Sources: [vatupdate](https://www.vatupdate.com/2025/12/24/slovak-retailers-must-display-ekasa-receipt-rights-notice-at-checkout-from-january-2026), [podnikam.sk](https://podnikam.sk/tagy/registracna-pokladnica/). stripe.com unreachable, so the fee was not re-checked.

### 🛠️ engineer — NO 80 (78→80)
**Position:** NO to full online payments at launch. The shared NO case is weakest where it lumps cake deposits in with them. A deposit-only option should be a priced, optional line item, not just a "January" idea.

**Assessment:**
- The strongest argument I disagree with is Skeptic's and Optimist's "defer cake deposits to January". Jana says cakes are her real pain, and the 6 % no-show rate hurts most there. About 15 cakes a week at 38 € is ~570 €/week, so ~34 €/week at 6 %. That is small. Business's ~90 €/week total is the right order of magnitude. A deposit doesn't recover the whole loss, so it is a modest gain either way.
- Numbers check. Optimist's 59 €/week and Skeptic's 93 €/week differ because Skeptic adds the cake loss (~34 €), which is right. My own Round 1 "+10–14 h" was loose. The pricing README's 700–900 € is ~14–18 h at 50 €/h, so the scoped version at 8–10 h (400–500 €) is a real saving, but only if refunds are done by hand in the Stripe dashboard.
- Payment Link: it is a no-code way to test cake deposits for ~0 build hours. It has no webhook, so staff must reconcile by hand against orders. That suits ~15 cakes a week. I'd offer it at launch as a manual step in the confirmation email, not as part of the build.
- Jana's conditions ≤800 € and refund in two clicks are compatible with the scoped version. A date independent of her texts and photos is not possible under Lucia's hard rule.

**Reply to others:** Optimist and Skeptic: put the deposit option in the quote as an optional line, not as a vague January idea.

**Would change my mind:** Jana delivers texts and photos by mid-November and accepts ~4 000 €.

### 💰 business — NO 74 (72→74)
**Position:** Launch pay-at-pickup, with cake deposits as a separately priced option of at most 800 € and not part of the day-one commitment. A no-code Stripe Payment Link is a stopgap, not a product.

**Numbers:**
- Weakest point in the shared NO case: the 93 €/week and 59 €/week figures are gross revenue at retail price. They ignore that cake no-shows are the costly ones, because a cake is made to order and can't be resold. Cake no-shows at 38 € × 15 × 6 % ≈ 34 €/week. A cake over 50 € already carries a 30 % deposit, so the unprotected cake loss is smaller than that.
- Engineer's 8–10 h for deposits at 50 €/h is 400–500 €. Jana's ceiling is 800 €, so 8–10 h fits if the refund flow stays manual. Optimist and Skeptic don't price this cheaper version; they only price the full 700–900 € add-on.
- Payment Link check: it needs no code and takes about 1–2 h. But it isn't tied to a pickup slot or an order, so someone reconciles by hand during the rush. That is the staff-learning burden Jana fears. It's fine as a bridge, but I wouldn't promise it as the launch feature.
- Payback: roughly 34 €/week of cake loss, with prepayment recovering part of it. On a 450 € build that is about 3+ months, or more if only part is recovered. That is acceptable but not compelling at launch, and it risks the deadline.

**Reply to others:** Engineer is closest to my view. I agree that deposits are a scoped change request, not part of the base price. Jana's ≤800 € cap is workable, but her "date not dependent on my texts" condition conflicts with Lucia's hard rule, so Lucia can't accept it.

**Would change my mind:** Jana delivers texts and photos by mid-November and signs a fixed 450–800 € deposit change request.

### 👤 client (Jana Kováčová) — NO 78 (70→78)
**Who I am:** Jana Kováčová, owner of Kvások & syn, one shop, 7 staff, budget around 3 000 €.

**Reaction:**
- The council's "4 400–4 750 €" (Optimist, Engineer) bundles English (300–450 €) that I never asked for. Only the cake deposit matters to me. Skeptic and Business (4 100–4 300 €) are closer, but still price payments for all orders, not for cakes.
- My Round 1 ask for a date independent of my texts and photos was unfair. Lucia's rule is right: I control that clock. I'll send texts and photos by 15 November and accept a date confirmed after that.
- Skeptic's no-code Stripe Payment Link for cake deposits is the best idea here. It costs almost nothing, has no new system for staff, and I can refund by hand in the Stripe app at first. Engineer's 8–10 h (about 400–500 €) is also under my 800 € ceiling.
- Weakest point of the shared NO: "add deposits in January" skips the cake rush, which is where the no-shows cost me most.

**Reply to others:** Engineer, I accept your scoped change request, but only after the base date is confirmed. Business, your 90 €/week looks low for Christmas, when cake volume rises.

**Would change my mind:** If cake deposits cannot ship at launch for ≤ 800 € as a separate, optional item, I would want them delayed and handled by hand.

*Chair's note to moderator: the client notes say English "would be nice", and "texts by 15 November" is the simulated client speaking, not Jana.*

## Verdict

**Verdict:** REJECTED · YES 0/5 (0 %) · weighted 0 %

All five members voted NO in round 2: Optimist 76, Skeptic 70, Engineer 80, Business 74, Jana 78. YES confidence is 0 out of a total of 378. Both shares are 0 %, under the 40 % rejection line (100 % minus the 60 % threshold). No argument drifted off the question. English only matters for the budget total.

**Recommendation:** Lucia should recommend launching with pay-at-pickup. She should quote online cake deposits as a separate optional line: about 8–10 h, 400–500 € excl. VAT, refunds done by hand in the Stripe dashboard. That line is confirmed only after the texts arrive and Jana's accountant clears how the eKasa receipt law treats online payments. Until then, cakes over 50 € keep their deposit: either taken in the shop as today, or through a payment link that staff send after the order.

**Why:**
- **Budget (Skeptic, Business, Engineer).** The florist reference is 3 400 € and had no online payments. Adding the payments add-on (700–900 €) gives 4 100–4 300 € excl. VAT, about 40 % over "around 3 000 €". If Jana's 3 000 € includes VAT, it is only 2 500 € excl. VAT, so even the base price is 36 % over. Sources: `pricing/README.md` lines 3, 17, 27.
- **The gain is small and the schedule is tight (Skeptic, Engineer, Business).** No-shows cost about 93 € a week gross: 70 × 14 € × 6 % ≈ 59 € for bread plus 15 × 38 € × 6 % ≈ 34 € for cakes. Jana herself says bread no-shows aren't worth the risk. About 4 weeks remain to early December. The florist project was planned at 5 weeks without payments, and Lucia can't promise any date before texts and photos arrive (`profile.md:36`). So even the base build is at risk without adding 14–18 h of payments.
- **Skeptic's catch shapes the answer.** The 30 % cake deposit is taken "in the shop" (`kvasok-a-syn.md:18`). Cakes ordered online would skip it right before Christmas. That is why the recommendation includes a stopgap for cakes and isn't simply "payments later".

**Open disagreements:**
- **Payment link at launch.** Engineer, Optimist and Jana want it offered in the confirmation email from day one. Business sees it as a stopgap: staff would have to match payments to orders by hand during the rush, which is the staff burden Jana fears. Skeptic would rather make big cakes phone-only, or use the link.
- **Size of the cake loss.** Business puts it at about 34 € a week. Jana says that "looks low for Christmas". Nobody has December data.
- **Cost of a deposit-only option.** Engineer estimates 8–10 h, but only if refunds stay manual. Skeptic notes that the price list implies 14–18 h for payments with a refunds flow.

**Failed evidence:**
- **Failed: Jana's "English that I never asked for" (round 2).** The client file says English "would be nice" (`kvasok-a-syn.md:27`). English stays in the quote as an optional line (300–450 €).
- **Not verified: Jana's "texts and photos by 15 November" (round 2).** This is the simulated client talking and isn't in Lucia's notes. No date can rest on it until Jana confirms in writing.
- **Failed: Jana's "fees on 14 € are ~0.30 €" (round 1).** At 1.5 % + 0.25 €, the fee is about 0.46 € (3.3 %). Tourists with non-EEA cards pay about 3.25 % + 0.25 €. Her vote doesn't change, because she wasn't worried about fees.
- **Partly failed: the florist slip from 5 to 6 weeks, cited by four members as a payments risk.** That project had no payments. The week was lost because "texts came a week late", and the extra 6 h went into slot capacity rules (quote file, line 30). It shows the risk from late texts and slot rules, not from payments.
- **Doesn't isolate payments: "the café with Stripe took 8 weeks".** That project had 3 locations, two languages and 120 h (Skeptic's own correction).
- **Withdrawn or corrected:**
  - Engineer's round-1 "+10–14 h" is below the 14–18 h implied by 700–900 € at 50 €/h.
  - Optimist's "59 €/week" left out cakes; the total is about 93 €.
- **Checked and holds:**
  - Act 384/2025 Z.z. on recording sales exists and has been in force since 1.1.2026, replacing Act 289/2008. A search snippet of its text says deposits count as sales that must be recorded. How online payment-gateway payments are treated is not verified, so the accountant has to answer that.
  - Stripe's 1.5 % + 0.25 € matches its EEA support page, which is dated 2023. A newer Stripe notice shows 1.4 %, so confirm in the Stripe dashboard.
- No vote rests only on failed claims. Jana's round-2 vote leans partly on the English and 15 November claims. Her main reasons (the add-on is about a quarter of her budget, and the Christmas deadline) still hold.

**Next step:** Before quoting, Lucia should email Jana these questions, in this order:
1. Is the 3 000 € including or excluding VAT?
2. On what date will texts and photos arrive (Slovak, plus English if she wants it)? Please confirm in writing. The launch date will be set from that date.
3. Last December, how many cakes were never picked up, split into over 50 € and under 50 €?
4. Can she ask her accountant whether online deposits through Stripe or GoPay have to be recorded in eKasa under 384/2025, and how?
5. English at launch: yes or no (300–450 €)?
6. Until online deposits exist, is it OK that a cake over 50 € is confirmed only after the deposit is paid in the shop or through a link staff send?

Sources:
- [Slov-lex: Act 384/2025 Z.z., version in force from 1.1.2026](https://static.slov-lex.sk/static/SK/ZZ/2025/384/20260101.html)
- [Zákony pre ľudí: Act 384/2025](https://www.zakonypreludi.sk/print/zz/2025-384/znenie-20260101.htm)
- [Asseco wiki: legislation 2026](https://wiki.assecosolutions.sk/sk/home/public/horeca/legislativa2026)
- [Stripe support: pricing updates for businesses in the EEA](https://support.stripe.com/questions/pricing-updates-for-businesses-based-in-the-european-economic-area-(eea))
- [Stripe support: European cross-border fees update](https://support.stripe.com/questions/european-cross-border-fees-update-due-to-network-cost-changes)
- [Studio Ninja: Stripe fees in different countries](https://help.studioninja.co/en/articles/10269673-stripe-fees-in-different-countries)
