# 1. crew:planner (opus · xhigh)

### Goal
Let `checkout(items, codes?: string | readonly string[], now?)` stack several coupons. They apply in a fixed order that does not depend on how the user typed them. A single string keeps today's errors and today's results whenever those results were already whole, non-negative cents.

### Context found
- `src/checkout.ts:49-60`: `checkout` is the only caller of `findCoupon`/`discountFor`. Its `code ?` check treats `""` as no coupon.
- `checkout.ts:35-42`: `findCoupon` throws `Unknown coupon: X` / `Coupon expired: X`. Reuse it unchanged.
- `checkout.ts:44-47`: `discountFor` uses one `amountCents` for both the minimum check and the discount base. Two existing bugs live here and stacking makes both worse:
  - Percent discounts are not rounded (4455 × 10% = 445.5).
  - Fixed discounts are not capped (GIFT25 on a 1000-cent cart gives a total of -1800).
- `checkout.ts:15-20`: within one coupon kind, `COUPONS` catalog order breaks ties. SUMMER15 expired on 2025-09-01, so every test that uses it needs an explicit `now`.
- `checkout.test.ts:11` compares the whole Receipt with `toEqual`, so adding a field to `Receipt` breaks it.
- Baseline: `npm test` passes 4/4 and `npm run typecheck` is clean.

### Rules both coders follow
1. **Normalize the input.** A string becomes `[string]`. Drop `""`. Remove exact duplicates, keeping the first. If nothing is left, apply no discount.
2. **Check every code before computing.** Run `findCoupon` on each code in input order. The first invalid code throws its existing message.
3. **Sort a copy.** Percent coupons come first, then fixed ones. Within each kind, keep `COUPONS` order. The result does not depend on input order; each "x% off" applies to the cart amount; fixed amounts and the zero cap come last, so the cap lives in one place; the catalog tie-break pins per-step rounding.
4. **Apply each coupon to a running amount** that starts at the subtotal:
   - The minimum is checked against the original subtotal, not the running amount. Below the minimum, the coupon adds 0 and throws nothing (as today).
   - Percent: `Math.round(running * value / 100)`. Percents compound: 10% + 15% = 23.5%, never more than 100%.
   - Fixed: `min(value, running)`.
5. **Result:** `discountCents` is a whole number with `0 ≤ discountCents ≤ subtotal`, so tax and total are never negative.

```ts
export function checkout(items: Item[], codes?: string | readonly string[], now?: Date): Receipt
function normalizeCodes(codes?: string | readonly string[]): string[]
export function discountFor(coupon: Coupon, baseCents: number, qualifyingCents = baseCents): number // integer, 0..baseCents
```

### Steps
1. **web-coder**, `src/checkout.ts`: implement rules 1-5. Leave `findCoupon`, `Receipt`, `COUPONS` and the error strings unchanged. Never mutate the caller's array. Done when `npm run typecheck` is clean and the 4 existing tests pass.
2. **tester**, `src/checkout.test.ts`: keep the 4 existing tests and add the cases below. Done when `npm test` is green.
3. **reviewer**: review the diff against rules 1-5 and the risks below.

### Test cases
Unless noted, the cart is 4400 (mug 1200×2 + tee 2000). Receipt values are `{subtotal, discount, tax, total}`.

| # | Case | Expected |
|---|---|---|
| 1 | `"WELCOME10"` vs `["WELCOME10"]` | identical receipts, discount 440 |
| 2 | `["WELCOME10","SAVE5"]` | `{4400, 940, 692, 4152}` |
| 3 | `["SAVE5","WELCOME10"]` | same as #2 (fixed-first would give 890) |
| 4 | cart 3200, `["WELCOME10","SAVE5"]` | discount 820, total 2856 (a minimum checked on the running amount would give 320) |
| 5 | cart 2400, same codes | discount 240, no throw |
| 6 | cart 3000, `"SAVE5"` | discount 500 (exact minimum qualifies) |
| 7 | `["WELCOME10","SUMMER15"]`, now 2025-08-01 | discount 1034, not 1100 |
| 8 | same codes, now 2025-10-01 | throws `Coupon expired: SUMMER15` |
| 9 | `["WELCOME10","NOPE"]` and `["NOPE","BAD"]` | throws `Unknown coupon: NOPE` |
| 10 | `["WELCOME10","WELCOME10"]` | discount 440 |
| 11 | `[]`, `[""]`, `""` | each equals `checkout(cart)` |
| 12 | cart 4455×1, `"WELCOME10"` | `{4455, 446, 802, 4811}`; adding SUMMER15 (now 2025-08-01) gives discount 1047, total 4090 |
| 13 | cart 1000, `"GIFT25"` | `{1000, 1000, 0, 0}` |
| 14 | cart 2000, `["GIFT25","WELCOME10"]` | discount 2000, total 0 |
| 15 | empty cart, `"GIFT25"` | all zeros |
| 16 | caller's codes array after the call | unchanged |
| 17 | `["WELCOME10"] as const` | compiles |
| 18 | invariant loop over every subset of the 4 coupons × carts {0, 1000, 2400, 3200, 4455}, now 2025-08-01 | discount is a whole number, 0 ≤ discount ≤ subtotal, total ≥ 0, total = subtotal − discount + tax |

### Risks
- **Single-string behavior changes on purpose in two cases:** fractional cents are now rounded, and totals that went negative now stop at 0.
- **Business risk:** unlimited stacking can make a cart free, e.g. GIFT25 + SAVE5 on 3000.
- **Clock-dependent tests:** SUMMER15 is already expired, so tests must always pass `now`.
- **Sorting:** sorting in place would mutate the caller's array.
- **`toEqual` and `-0`:** a `-0` from rounding would fail the comparison.

### Open questions (default in brackets)
1. Percent or fixed first? [Percent first.]
2. Minimum checked against original subtotal or running amount? [Original subtotal.]
3. Do multiple percents compound or add? [Compound.]
4. Should one invalid code fail the whole checkout? [Fail, naming the first bad code.]
5. Duplicate ignored or rejected? [Ignored.]
6. Stacking limits or non-stackable coupons? [None.]
7. Single-string path gets the rounding and zero-cap fixes too? [Yes.]
8. Rounding mode? [`Math.round` per coupon.]
9. Receipt lists applied codes? [No.]
10. Normalize case or whitespace? [No, only `""` is ignored.]
