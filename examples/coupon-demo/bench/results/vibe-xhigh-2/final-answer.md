`checkout(items, codes?: string | string[], now?)` now accepts one code or a list of codes. Passing a single string gives the same results as before, with one exception noted below. All 14 tests pass (the 4 existing ones plus 10 new ones), and the type check is clean. I haven't committed anything.

**How several coupons combine** (in `src/checkout.ts`):
- **Each coupon is checked against the cart subtotal**, not against what's left after the other coupons, and the discounts are added together. So the order of the codes doesn't affect the result, and a minimum like SAVE5's "spend $30" refers to the cart. For example, WELCOME10 + SAVE5 on the $44 test cart takes off $4.40 + $5.00 = $9.40.
- **Percent coupons add up rather than compound.** WELCOME10 + SUMMER15 gives 25% off, not 23.5%.
- **A repeated code counts once**, so `["WELCOME10", "WELCOME10"]` is still 10%. Empty strings and an empty list mean no coupon, as `""` did before.
- **One bad code stops the whole checkout.** If any code is unknown or expired, it throws the same error a single code would.

**The one change for single codes:** the total discount now can't exceed the cart subtotal. Before, GIFT25 ($25 off) on a $10 cart produced a negative total of −$18.00; now the total is $0. I added this cap because stacked fixed coupons would hit that case far more often. It's one `Math.min` in `checkout` if you'd rather not have it.

Unchanged: percent discounts still aren't rounded to whole cents, so totals can include fractions of a cent.

If you'd rather apply coupons one after another, each on the amount left over, that's a small change. But then the order of the codes affects the price, and a minimum like SAVE5's can stop applying if another coupon is used first.
