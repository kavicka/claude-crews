`checkout` now accepts one coupon code or a list of them. All 22 tests pass and typecheck is clean. One thing changed for single codes, explained next. Nothing is committed.

**Behaviour change for single codes:** a fixed coupon worth more than the cart is now capped at the cart's subtotal. For example, `"GIFT25"` (worth 2500) on a 1000 cart used to give a total of **−1800**; it now gives a discount of 1000 and a total of **0**. Because `"X"` and `["X"]` have to give the same result, the cap applies to single codes too. Every other single-string result is unchanged.

**What changed**
- The new signature is `checkout(items, codes?: string | readonly string[], now?)`. A string is treated as a one-item list. Empty strings are ignored, and a repeated code counts once.
- When several codes are given, each discount is worked out on the original subtotal and the discounts are added up. The order of codes doesn't matter, and two percent coupons add rather than compound (10% + 15% = 25%). A coupon's minimum spend is checked against the original subtotal.
- The first unknown or expired code (in the order given) throws the same error message as before.
- `Receipt` has the same shape as before. There's a short doc comment on `checkout` describing these rules.
- Files changed: `src/checkout.ts` (+22/−2) and `src/checkout.test.ts` (18 new tests; the 4 original tests are untouched).

**Results**
- **Tests:** `npm test` passes 22/22 and `npm run typecheck` is clean. The repo has no lint script.
- **Review:** approved with only minor comments. I acted on two: a hard-coded expected total instead of one recalculated in the test, and a new test where an expired code comes before an unknown one. I re-ran tests and typecheck afterwards and both still pass.
- I couldn't save the diff file for the reviewer: the environment blocked writing into `.git`, so I pasted the original code into its brief instead.
- No docs were written because the repo has no README or docs.

**Decisions taken without you (planner defaults plus the skeptic's changes)**
1. Discounts add up against the original subtotal instead of applying one after another.
2. Repeated codes are silently counted once; they don't raise an error.
3. One bad code fails the whole checkout; it isn't skipped.
4. No list of applied codes was added to `Receipt`.
5. Percent discounts are still not rounded, so amounts can include fractions of a cent, as before.
6. The total discount is capped at the subtotal, including for single codes (the change above).
7. `null` isn't part of the type. It still means "no coupon" at runtime.

**Follow-ups**
- Fractions of a cent become more likely when coupons are combined: WELCOME10 + SUMMER15 on a 1005 cart gives a discount of 251.25. Rounding discounts would fix this but changes existing outputs.
- Adding up percent coupons can be generous (two 50% coupons make the order free). Decide whether some coupons shouldn't be combinable.

**Proposed commit message**
```
feat(checkout): accept multiple coupon codes

Stacked discounts are computed against the original subtotal and summed;
the total discount is clamped to the subtotal (fixes negative totals).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
