`checkout` now accepts one coupon code or a list of them, and passing a single string works exactly as before. All 15 tests pass and the typecheck is clean. Nothing is committed.

**What changed** (`src/checkout.ts`, `src/checkout.test.ts`):
- **New signature:** `checkout(items, codes?: string | readonly string[] | null, now?)`.
- **Clean-up of the codes:** empty codes are ignored and duplicates count once.
- **Validation:** every code is checked before any discount is added. If one is unknown or expired, the whole call throws the same error message as today.
- **Stacking:** each coupon's discount is worked out from the original subtotal and the discounts are added together. So 10% + 15% is 25% off, and the order of the codes doesn't matter.
- **Tests:** 11 new tests sit in a separate block; the 4 existing ones are unchanged.

**Review:** approved with two notes. I fixed the small one (a simpler, correctly commented sum). The other is the negative-total issue below.

**Decisions made without you (benchmark mode):**
- **Planner defaults I kept:**
  - Coupons stack by adding up, not compounding.
  - A coupon's minimum spend is checked against the original subtotal, so `SAVE5` still applies even when another coupon brings the amount below its 3000 minimum.
  - Duplicates and empty codes are dropped silently.
  - Codes still match exactly, including case.
  - The receipt has the same fields as before.
  - Every combination is allowed; there is no rule like "at most one percent coupon".
- **Skeptic changes I folded in:**
  - **No rounding and no cap on the discount**, so single-string results don't change. The planner had proposed both, but they would have changed two single-coupon results today: 100.5 becoming 101, and a total of -600 becoming 0.
  - `null` still means "no coupon", as before.
  - A read-only array (`as const`) is accepted.
  - Two redundant planned tests were dropped.

**Follow-ups:**
- **Negative totals (important):** combining coupons can now push the total below zero on carts where no single coupon could. For example, `GIFT25` plus `WELCOME10` on a 2600 cart gives 2760 off and a total of -192. You'd want a cap on the discount, or a rejection, before customers can enter more than one code.
- **Fractional cents:** percent discounts still aren't rounded, so a discount can come out as 100.5.
- I skipped the documentation step because the repo has no README or other docs.

**Proposed commit:**
```
feat(checkout): accept multiple coupon codes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
