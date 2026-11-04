`checkout` now takes `codes?: string | string[]`. A single string works exactly as before, and the 4 original tests pass unchanged. I added 11 tests for multiple codes; all 15 pass and the typecheck is clean.

The change is in `src/checkout.ts`. A single string, an array or nothing all become one list, each code is looked up and checked for expiry, and the discounts are added together. The request didn't say how stacked coupons should combine, so I made these choices:

- **Every coupon is measured against the cart subtotal.** Percent coupons take their percentage of the subtotal, and minimum-spend rules check the subtotal. So `WELCOME10 + SUMMER15` is a flat 25% off, and the order of the codes never changes the result. The other common approach applies coupons one after another, each to what's left. That makes order matter, and an earlier coupon can push the cart below a later coupon's minimum.
- **The total discount can't exceed the subtotal.** Before this change, `GIFT25` on a cart under $25 already gave a negative total, and stacking makes that much easier to hit. **This also changes single-code behaviour, but only in that case:** the total now stops at 0 instead of going negative.
- **A repeated code is rejected** with a "Duplicate coupon" error rather than being applied twice. If you'd rather ignore repeats quietly, it's a one-line change.
- **One bad code fails the whole checkout.** An unknown or expired code throws, just as it does for a single code. Valid codes in the same list are not partly applied.
- **Empty strings are ignored**, the same way `checkout(cart, "")` already meant "no coupon".

One existing issue I left alone: percent discounts aren't rounded, so an odd subtotal gives fractional cents (15% of 1234 is 185.1). Adding up several coupons carries that through. If you want, I can round each discount to whole cents.

I haven't committed anything.
