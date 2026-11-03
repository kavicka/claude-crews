# 5. crew:reviewer (opus · xhigh)

**Verdict:** APPROVE WITH NITS

**Findings**
- 🟠 **Should fix**: `src/checkout.test.ts:80-84, 113-124`: no test checks the rule that two percent coupons always apply in catalog order. Rule 3 of the plan says this order decides the per-step rounding, so the result never depends on input order. The code does it correctly (`checkout.ts:67-71`), but every test that stacks two percent coupons passes them in catalog order, and both test carts round to the same cent either way. A later "stable sort of the input" refactor would apply percent coupons in input order without any test failing. About 30 % of carts differ by one cent between the two orders. Fix: add one case on a cart where the order matters, with the codes in reverse catalog order:
  ```ts
  const r = checkout([{ sku: "x", priceCents: 4405, qty: 1 }], ["SUMMER15", "WELCOME10"], JULY);
  expect(r.discountCents).toBe(1036); // input order would give 1035
  expect(r.totalCents).toBe(4043);
  ```

**Checked and fine:** validation order and messages; duplicates and catalog order; no mutation of the caller's array; minimums against the original subtotal including the exact threshold; `Math.round` exact on `.5` cases and no `-0`; the zero cap; empty input (`""`, `[]`, `undefined`); API only widens; all 18 plan cases present, none weakened; nothing changed outside `src`. Ran `npm test` (22/22) and `npm run typecheck` (clean).

## Fix loop
The finding went to crew:tester verbatim; the new case was added and the suite re-run (see the results in [../README.md](../README.md)).

## What this caught in the other run
The vibe-coded version applies percent coupons in input order. Checked after the fact: `["SUMMER15","WELCOME10"]` gives a discount of 1035 and `["WELCOME10","SUMMER15"]` gives 1036 on the same 4405-cent cart. Same coupons, different price.
