# 4. crew:web-coder (opus · high) and crew:tester (sonnet · high), in parallel

## web-coder
Implemented rules 1-5 in `src/checkout.ts` using the skeptic's simpler shape. Every code is checked with `findCoupon` in input order. Then `COUPONS` is filtered by those codes, which removes duplicates and keeps catalog order. Percent coupons go before fixed ones, applied to a running amount. The minimum is checked against the original subtotal.

- `discountFor(coupon, baseCents, qualifyingCents = baseCents)` rounds percent discounts with `Math.round` and caps fixed ones with `Math.min(value, baseCents)`.
- Private helpers `normalizeCodes` and `stackedDiscount`.
- `findCoupon`, `Receipt`, `COUPONS` and the error strings unchanged; the caller's array is never mutated.
- Verified every value in the plan's table and the 80-case invariant loop with a scratch script before the tests landed.

Suggested commit:
```
feat(checkout): stack multiple coupons in a fixed order

Accept string | readonly string[]; validate all codes first, apply
percent before fixed in catalog order on a running amount, check
minimums against the subtotal, round to whole cents and cap at subtotal.
```

## tester
Wrote cases 1-18 into `src/checkout.test.ts` before the implementation landed (17 red, 5 green), then re-ran: 22/22 green, typecheck clean.

- Case 16 passes a frozen array, so an in-place sort would throw.
- Case 17 (`as const`) only proves anything under `npm run typecheck`, which is now part of "done".
- Case 18 runs all 16 coupon subsets × 5 carts and checks the invariants (whole cents, 0 ≤ discount ≤ subtotal, total ≥ 0, receipt adds up).
- Not covered on purpose: case and whitespace normalisation (plan says no), blocking the free cart (accepted follow-up).
