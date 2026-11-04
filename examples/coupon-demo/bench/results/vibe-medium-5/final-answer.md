`checkout(items, codes?: string | string[], now?)` now takes either one code or a list. A single string still works as before, and so do the existing call sites. All 11 tests pass (4 old, 7 new) and the type check is clean. The changes are in `src/checkout.ts` and `src/checkout.test.ts`.

The request didn't say how coupons should combine, so I made these choices. They're described in a comment above the function and are easy to change:

- **All or nothing:** if any code is unknown or expired, the whole checkout throws, as a single bad code does today. The same code entered twice also throws (`Duplicate coupon`).
- **Order doesn't matter:** percent coupons apply first, then fixed ones, each on what's left after the previous one. `["SAVE5", "WELCOME10"]` and `["WELCOME10", "SAVE5"]` give the same total. Percent-first is better for the customer. If you'd prefer coupons to apply in the order they're entered, that's a one-line change.
- **Minimum spend uses the original subtotal:** a 3200¢ cart still gets SAVE5 (minimum 3000¢) even after WELCOME10 brings it down to 2880¢. Otherwise adding a coupon could cancel another one.
- **Discounts stop at zero:** the total discount can't exceed the subtotal.

**One change to existing behavior:** because of the zero cap, a single `GIFT25` on a cart under 2500¢ now gives a 0 total. Before, it gave a negative total, which looked like a bug.

**Left unchanged:** percent discounts can still produce fractions of a cent (only tax is rounded), as before. Stacking two percent coupons makes this more likely, so you may want to round each discount.
