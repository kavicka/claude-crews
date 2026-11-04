`checkout(items, codes?: string | string[], now?)` now accepts a list of coupon codes, and passing a single string works the same as before. All 11 tests pass (4 old, 7 new) and the type check is clean. The change is in `src/checkout.ts` and isn't committed yet.

You didn't say how stacked coupons should combine, so I chose these rules:

- **Order matters:** coupons apply in the order given, each to the amount left after the earlier ones. On the 4400¢ test cart, `["WELCOME10", "SAVE5"]` takes 940¢ off, but `["SAVE5", "WELCOME10"]` takes 890¢.
- **Minimum spend:** a coupon's minimum (like SAVE5's 3000¢) is checked against the amount after earlier discounts. So `["GIFT25", "SAVE5"]` only applies GIFT25.
- **One bad code fails everything:** if any code is unknown or expired, the whole checkout throws. Codes aren't silently skipped.
- **Repeats are rejected:** passing the same code twice throws `Duplicate coupon`.
- **No coupon:** `[]` behaves like passing no codes, as `""` already did.

Decision for you: if a store wants the same total whatever order codes are entered in, the usual fix is to always apply percentage coupons before fixed-amount ones. That's a small change if you want it.

**Change to single-code behaviour:** a discount can no longer be larger than what's left to pay. Before, GIFT25 on a 1000¢ cart gave a negative total. It now gives 0, and there's a test for it.

One older issue I left alone: percentage discounts can still produce fractions of a cent (10% of 4405¢ is 440.5¢). Stacking can now carry that fraction into later discounts. Rounding each discount to whole cents would fix it, but that changes how single-coupon results are rounded, so I didn't do it without asking.
