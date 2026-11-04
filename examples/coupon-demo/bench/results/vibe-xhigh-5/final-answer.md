`checkout(items, codes?: string | string[], now?)` now accepts a single code or a list of codes. All 4 original tests pass unchanged, and `tsc` is clean. I added 10 tests, so there are 14 in total, all passing.

**How stacking works** (`src/checkout.ts`):
- **Pricing:** Each coupon is priced against the original subtotal and the discounts are added up. Two percent coupons add together (10% + 15% = 25% off) rather than compounding (which would give 23.5%). The order of the codes doesn't affect the result.
- **Minimums:** `minSubtotalCents` is always checked against the real subtotal. For example, `SAVE5` still applies after `WELCOME10` on a 3200¢ cart, even though the cart is below 3000¢ once the 10% comes off.
- **Errors:** If any code is unknown or expired, the whole checkout throws, as a single bad code did before.
- **Duplicates and blanks:** A repeated code applies once. Empty strings are ignored, so `[]`, `[""]` and `""` all mean "no coupon".

**Behavior change:** the total discount is now capped at the subtotal. Without the cap, stacked coupons could easily push totals negative. This also affects one single-code case: `GIFT25` on a cart under 25.00 used to give a negative total and negative tax, and now gives 0. In every other case, a single string returns exactly what it did before.

**Not changed:** percent coupons can still produce fractional cents (e.g. 15% of 1234¢ is 185.1¢). That was already the case before this change, and stacking makes it more likely to show up. I can round discounts to whole cents if you want.

If you'd rather percent coupons compound instead of add, it's a small change to the reduce in `checkout`. I haven't committed anything.
