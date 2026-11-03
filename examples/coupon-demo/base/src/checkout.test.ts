import { describe, expect, it } from "vitest";
import { checkout } from "./checkout";

const cart = [
  { sku: "mug", priceCents: 1200, qty: 2 },
  { sku: "tee", priceCents: 2000, qty: 1 },
];

describe("checkout", () => {
  it("totals a cart without a coupon", () => {
    expect(checkout(cart)).toEqual({
      subtotalCents: 4400,
      discountCents: 0,
      taxCents: 880,
      totalCents: 5280,
    });
  });

  it("applies a percent coupon", () => {
    expect(checkout(cart, "WELCOME10").discountCents).toBe(440);
  });

  it("applies a fixed coupon above its minimum", () => {
    expect(checkout(cart, "SAVE5").discountCents).toBe(500);
  });

  it("rejects an unknown coupon", () => {
    expect(() => checkout(cart, "NOPE")).toThrow("Unknown coupon");
  });
});
