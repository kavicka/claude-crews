`checkout(items, codes?: string | string[], now?)` now accepts several coupon codes, and a single string still works as before. All 15 tests and the typecheck pass: the 4 original tests unchanged plus 11 new ones.

**How stacking works** (`src/checkout.ts:66`):
- **Discounts add up.** Each coupon's discount is worked out on the subtotal before any discount, and the amounts are added together. So `["WELCOME10", "SAVE5"]` on a 4400 cart takes off 440 + 500 = 940.
- **Order doesn't matter.** Because every coupon looks at the same subtotal, the same codes give the same total in any order. The other option was to apply each coupon to what's left after the previous one, but then the price would depend on the order the customer typed the codes. One side effect: two percent coupons add up (10% + 15% = 25% off) rather than compounding (23.5%).
- **Minimum spend uses the original subtotal.** For example, `SAVE5` still applies alongside `WELCOME10` on a 3000 cart, even though the discounted amount is below its 3000 minimum.
- **One bad code fails the whole checkout.** An unknown or expired code throws an error, the same way a single bad code always has.
- **Empty values mean no coupon.** `""`, `undefined` and `[]` all apply nothing. Empty strings inside an array are skipped.

**Decisions to check:**
1. **The total discount is now capped at the subtotal.** This also changes the single-string case: before, `checkout([{ priceCents: 1000, qty: 1 }], "GIFT25")` gave a total of −1800, and now it gives 0. That was already a bug, and stacking coupons would hit it much more often, so I fixed it here. If you'd rather keep that change separate, it's one line (`Math.min(...)`).
2. **Entering the same code twice throws** `Duplicate coupon: X`, in line with how invalid codes are handled. If you'd rather quietly ignore the repeat, change the `throw` in `resolveCoupons` to skip it.

Nothing is committed yet.
