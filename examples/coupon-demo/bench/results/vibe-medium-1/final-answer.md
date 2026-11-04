`checkout(items, codes?: string | string[], now?)` now takes one code or a list of codes, and a single string works as before. All 10 tests pass (the 4 existing ones and 6 new ones) and the typecheck is clean.

The request didn't say how coupons should combine, so I made these choices in `src/checkout.ts`:

- **Order matters.** Coupons are applied in the order given, and each one discounts what's left after the earlier ones. On a 4400¢ cart, `["SAVE5", "WELCOME10"]` takes 890¢ off, but `["WELCOME10", "SAVE5"]` takes 940¢. If you want a fixed rule instead, such as percent coupons always going first, that's a one-line sort.
- **Minimum spend uses the original cart total.** A coupon with a minimum (like `SAVE5`'s 3000¢) is checked against the cart subtotal before discounts. Otherwise an earlier coupon could push the cart below the minimum and cancel a later one. To support this, `discountFor` takes an optional third `subtotalCents` argument, which defaults to the old behaviour.
- **The discount is capped at the subtotal,** so the total can't go below zero.
- **Invalid lists fail the whole checkout.** Repeating a code throws `Duplicate coupon: …`, and an unknown or expired code anywhere in the list throws, the same as for a single code.
- **Empty input means no coupon.** An empty array and empty strings are treated like passing nothing.

**One change to single-code behaviour:** the cap also applies when only one code is given. Before, `GIFT25` on a cart under 25.00 produced a negative total. Now it brings the total down to 0. That looked like a bug to me, but tell me if you relied on the old result.
