`checkout(items, codes?: string | string[], now?)` now accepts several coupon codes, and a single string still works. All 11 tests pass (the 4 existing ones plus 7 new ones) and the typecheck is clean.

I had to choose how coupons combine, since stacking makes the result depend on it. My choices, in `src/checkout.ts`:

- **Percent before fixed:** all percent coupons apply first, then fixed ones, so the result is the same whatever order the codes are entered in. Each discount comes off what's left after the earlier ones. For example, WELCOME10 + SAVE5 on a 4400 cart gives 4400 − 10% = 3960, then − 500 = 3460.
- **Minimum spend uses the original subtotal:** a coupon like SAVE5 (minimum 3000) still applies even if an earlier percent discount takes the running amount below 3000.
- **One bad code fails the whole checkout:** an unknown or expired code throws, as before, even when it's mixed in with valid ones.
- **Repeated codes are rejected:** something like `["WELCOME10", "WELCOME10"]` throws, so a code can't be stacked on itself.
- **Empty input:** an empty array or empty strings are treated as no coupon.
- **The total can't go negative:** the discount is capped at the subtotal. **This changes existing single-code behaviour:** before, GIFT25 on a 1000 cart gave a negative total; now it gives 0.

`discountFor` is still exported, but `checkout` no longer uses it. It checks a coupon's minimum against whatever amount it's given, which in a stack would be the reduced running amount rather than the original subtotal.

If you'd rather have different rules, such as applying codes in the order given or allowing only one percent coupon, each is a small change.
