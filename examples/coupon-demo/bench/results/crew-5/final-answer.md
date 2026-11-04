`checkout` now accepts one coupon code or a list of them: `checkout(items, codes?: string | readonly string[], now?)`. Passing a single string still works and gives the same result as before, except in one edge case (see below). All 24 tests pass, including the 4 original ones unchanged, and the typecheck is clean. Nothing is committed.

**How codes are handled:**
- Empty codes are ignored, and a repeated code is applied once (matching is exact: same case, no trimming).
- Every code is looked up before anything is calculated. The first unknown or expired code throws the same error as today.
- Each coupon's discount is worked out on the original subtotal, and the discounts are added up. So the order of the codes doesn't matter, and 10% + 15% gives 25% off.
- The total discount can't exceed the subtotal.

Only `checkout` in `src/checkout.ts` changed; `discountFor`, `findCoupon` and the receipt shape are untouched. The new tests are in `src/checkout.test.ts`.

**Review:** approved with two minor notes.
- **Fixed:** passing `null` (for example `"coupon": null` from a JSON body) now crashed checkout, where before it meant no coupon. I made `null` mean no coupon again and added a test for it.
- **Left for later:** percent coupons can produce fractional cents, and stacking adds those fractions together (a 4399-cent cart with WELCOME10 + SUMMER15 gives a discount of 1099.75). This already happened before the change.

**Decisions I made without you, as instructed:**
1. **Discounts add up rather than compound.** Each coupon is calculated on the original subtotal, and minimum-spend rules are checked against the original subtotal too. So SAVE5 still applies even when other coupons bring the amount paid below 3000.
2. **The cap also applies to a single string.** This is the one change single-string callers will see: GIFT25 on a 2400 cart now gives a total of 0 instead of -120, and the receipt's discount shows the capped 2400, not 2500.
3. **Empty and duplicate codes:** an empty string, an empty list or no codes all mean no coupon; empty entries are skipped and duplicates count once.
4. **All or nothing:** one bad code fails the whole checkout, and the first bad one in the list decides the error message.
5. **No rounding fix.** The planner proposed rounding percent discounts to whole cents, but the skeptic pointed out that would change single-string results, so I left it out.
6. **No combination rules:** any coupons can be used together, since coupons have no field saying otherwise.

**Follow-ups:**
- Round discounts to whole cents (the leftover review note).
- Decide whether summing every coupon is too generous; for example, WELCOME10 + SUMMER15 + GIFT25 all stack.

I couldn't save the diff file into `.git` because the permission was denied, so I gave the reviewer the change inline. There are no docs to update; the repo has no README.

**Proposed commit:**
```
feat(checkout): accept multiple coupon codes

checkout(items, codes?: string | readonly string[], now?) applies each
coupon to the original subtotal, sums the discounts and caps them at the
subtotal. Single-string and undefined callers keep working.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
