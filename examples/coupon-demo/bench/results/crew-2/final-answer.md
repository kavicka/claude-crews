`checkout` now accepts one coupon code or a list of them, and a single string gives exactly the same result as before. All 21 tests pass (the 4 original ones are unchanged) and the typecheck is clean. The reviewer approved with two minor notes: I fixed the first, and the second is the follow-up below. Nothing is committed.

**How codes combine:**
- **Signature:** `checkout(items, codes?: string | readonly string[], now?)`.
- **Discount:** each coupon is worked out against the original subtotal and the amounts are added together, so order doesn't matter. Two percent coupons add up (10% + 15% = 25%), and a coupon's minimum spend is checked against the original subtotal.
- **Duplicates and blanks:** a repeated code counts once. Empty strings, `[]` and `[""]` mean no coupon. Spaces and letter case are not cleaned up, so `"welcome10"` is still unknown.
- **Errors:** every code is checked first, and the first unknown or expired code in the list throws the existing error, so you never get a partly discounted receipt.
- **Receipt:** keeps the same four fields.

**Decisions made without you** (the benchmark said not to wait; these are the planner's defaults plus the skeptic's changes):
1. **No rounding and no cap on the discount (skeptic's change).** The planner wanted both, but that would have changed what single codes return today. So these existing problems remain:
   - A percent coupon can give fractional cents (4405 with WELCOME10 gives 440.5).
   - GIFT25 on a small cart gives a negative total.
   Tests now pin this behaviour down, so a later fix will have to update them on purpose.
2. **Adding the percentages instead of compounding them,** checking minimums against the original subtotal, ignoring duplicates rather than rejecting them, and no rules about which coupons may be combined are all assumptions. These are business decisions you didn't make.
3. **`readonly string[]` instead of `string[]`,** so constant arrays can also be passed in. Any `string[]` still works.

**Follow-up, which you should decide before real customers use this:** stacking makes negative totals much easier to hit. For example, GIFT25 + WELCOME10 on a 20.00 cart gives a total of −8.40. I suggest a separate fix that:
- caps the discount at the subtotal;
- rounds discounts to whole cents;
- optionally marks which coupons can be combined.

**Process notes:**
- I renamed one test whose name was wrong and added the missing check that stacked discounts are not capped.
- Saving the diff into `.git` for the reviewer was blocked by a permission prompt, so I gave the reviewer the diff in its brief instead.
- I skipped the docs step because the repo has no README or other docs.

Files changed: `src/checkout.ts` (only `checkout` and its doc comment) and `src/checkout.test.ts` (17 new tests).

**Proposed commit:**
```
feat(checkout): accept multiple coupon codes

checkout(items, codes?: string | readonly string[], now?) now stacks
coupons: each is evaluated against the original subtotal and summed;
duplicates and empty codes are ignored; all codes are validated first.
Single-string calls behave exactly as before.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
