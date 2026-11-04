I've finished adding multi-coupon support: `checkout(items, codes?: string | readonly string[], now?)` now takes one code or a list, and a single string works as before. 24 of 24 tests pass and the typecheck is clean. Nothing is committed.

**Changes:**
- **`src/checkout.ts`**
  - The codes are turned into a list and all of them are checked before any discount is applied.
  - Coupons then apply in a fixed order, and each discount is taken from what is left of the total.
  - `discountFor` gained an optional third parameter (`eligibilityCents`), so existing two-argument calls still work.
  - The `Receipt` shape is unchanged.
- **`src/checkout.test.ts`:** the 4 original tests are untouched, and there are 20 new ones.

**Review:** approved with two small nits, which I fixed and re-tested:
- I clarified the doc comment about the order codes are checked in, and added a test for it.
- I removed a redundant array copy and a value that was computed twice.

**Decisions taken without you, as instructed (planner defaults plus the skeptic's changes):**
1. `undefined`, `""`, `[]` and `""` entries inside a list all mean "no coupon". Codes must match exactly, including case.
2. It's all or nothing. Each code, in input order, is checked for unknown or expired first, then for being a repeat (`Duplicate coupon: X`). The first problem throws and no receipt is returned.
3. **Stacking:** percent coupons apply before fixed ones, and percents compound (10% + 15% gives 23.5% off, not 25%). Within each kind, coupons apply in their order in the `COUPONS` list, so the order you pass them in can't change the result. The skeptic found a 1-cent difference without this.
4. `minSubtotalCents` is checked against the original subtotal, not the amount left after earlier coupons.
5. Repeated codes are rejected rather than silently removed. There's no limit on how many coupons can be combined, and no per-coupon breakdown on the receipt.

**Behaviour changes that also affect a single code:**
- **Rounding:** percent discounts now round to whole cents. Before, a 1234-cent cart with `"WELCOME10"` gave a discount of 123.4 and a total of 1332.6; now it's 123 and 1333.
- **Capping:** a discount can no longer exceed what's left of the total. Before, a 1000-cent cart with `"GIFT25"` gave a total of −1800; now it's 0. This is required once coupons stack, or totals go negative.

**Things to check:**
- **Possible follow-up:** percent-before-fixed is the more generous order for the customer. If you'd rather favour the merchant, switch to fixed-first or add the percentages instead of compounding.
- **Leftover files:** the coder agent left two untracked notes in `.claude/agent-memory-local/crew-web-coder/`. Delete them or add them to `.gitignore` before committing.
- **Review diff:** the sandbox blocked saving the diff under `.git`, so the reviewer read the changed files directly instead.

**Proposed commit:**
```
feat(checkout): accept multiple coupon codes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
