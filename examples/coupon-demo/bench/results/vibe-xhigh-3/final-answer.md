`checkout(items, codes?: string | string[], now?)` now accepts one coupon code or a list of them, and a single string still works as before. All 12 tests pass (the 4 existing ones plus 8 new ones for multiple codes), and the typecheck is clean.

The request didn't say how stacked coupons should combine, so I chose these rules in `src/checkout.ts`:

- **Each coupon is worked out on the full subtotal, then the discounts are added up.** On the 4400¢ test cart, `["WELCOME10", "SAVE5"]` gives 440 + 500 = 940¢ off. The order of the codes doesn't change the result, and a minimum spend like `SAVE5`'s is still checked against the cart total. If you'd rather have each coupon apply to what's left after the previous one, that's a small change, but then the order matters.
- **The total discount can't be more than the subtotal**, so the total can't go below zero. This also changes single-coupon behaviour in one case: before, `GIFT25` on a cart under 25.00 gave a negative total, and now it gives 0.
- **A repeated code is applied only once**, so `["WELCOME10", "WELCOME10"]` takes 10% off, not 20%.
- **One bad code fails the whole checkout.** An unknown or expired code anywhere in the list throws an error, as a single bad code already did.
- **Empty strings and an empty list mean no coupon**, matching how `""` was already treated.

One older issue I left alone: percentage coupons can give fractions of a cent. For example, 10% of 1234¢ gives a discount of 123.4¢, and that fraction carries through to the total. Rounding it is a separate decision, so I didn't make it here.
