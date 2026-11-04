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

  describe("multiple codes", () => {
    it("accepts a one-element array like a single string", () => {
      expect(checkout(cart, ["WELCOME10"])).toEqual(checkout(cart, "WELCOME10"));
    });

    it("treats an empty array as no coupon", () => {
      expect(checkout(cart, [])).toEqual(checkout(cart));
    });

    it("stacks percent before fixed regardless of order", () => {
      // 4400 - 10% = 3960, then - 500 = 3460 => discount 940
      expect(checkout(cart, ["WELCOME10", "SAVE5"]).discountCents).toBe(940);
      expect(checkout(cart, ["SAVE5", "WELCOME10"]).discountCents).toBe(940);
    });

    it("checks minimum subtotal against the cart subtotal", () => {
      const small = [{ sku: "tee", priceCents: 3000, qty: 1 }];
      // 3000 qualifies for SAVE5 even though WELCOME10 brings it to 2700 first
      expect(checkout(small, ["WELCOME10", "SAVE5"]).discountCents).toBe(800);
    });

    it("never discounts below zero", () => {
      // 4400 - 440 = 3960, - 2500 = 1460, - 500 = 960
      expect(checkout(cart, ["GIFT25", "SAVE5", "WELCOME10"]).discountCents).toBe(3440);
      const tiny = checkout([{ sku: "pin", priceCents: 1000, qty: 1 }], ["GIFT25"]);
      expect(tiny.discountCents).toBe(1000);
      expect(tiny.totalCents).toBe(0);
    });

    it("rejects duplicate codes", () => {
      expect(() => checkout(cart, ["WELCOME10", "WELCOME10"])).toThrow("Duplicate coupon");
    });

    it("rejects the whole checkout if any code is unknown or expired", () => {
      expect(() => checkout(cart, ["WELCOME10", "NOPE"])).toThrow("Unknown coupon");
      expect(() => checkout(cart, ["WELCOME10", "SUMMER15"], new Date("2025-10-01"))).toThrow(
        "Coupon expired",
      );
    });
  });
});
