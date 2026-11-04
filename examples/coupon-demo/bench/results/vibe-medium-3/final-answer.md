`checkout(items, codes?: string | string[], now?)` now accepts several coupon codes, and a single string still works exactly as before. All 12 tests pass (the 4 existing ones plus 8 new ones) and the typecheck is clean. I haven't committed anything.

The request didn't say how stacked coupons should combine, so I had to choose. These choices are in `src/checkout.ts` and are easy to change:

- **Each coupon is worked out against the original subtotal, then the discounts are added up.** So `WELCOME10` + `SAVE5` on a 4400¢ cart gives 440 + 500 = 940¢ off. The order of the codes doesn't affect the result, and minimum-spend rules like `SAVE5`'s are checked against the cart's full value. Two percent coupons add together (10% + 15% = 25%) rather than one applying after the other.
- **The total discount is capped at the subtotal, so the total can never go below zero.** This also changes one single-code case: before, `GIFT25` alone on a cart under 25.00 gave a negative total. Now it comes to 0.
- **Using the same code twice throws a `Duplicate coupon` error.** Otherwise `["WELCOME10", "WELCOME10"]` would give 20% off.
- **If any code is unknown or expired, the whole checkout fails.** It doesn't quietly skip the bad code, which matches how a single bad code already behaves.
- An empty array, or an empty string, means no coupon, as `""` did before.

Separately, percent coupons can still give fractional cents (for example, 10% of 4405¢ is 440.5¢). That was already the case before this change and I didn't touch it, but you may want to round discounts as well as tax.
