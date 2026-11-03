// Hidden acceptance tests. Neither run saw this file. Copied into src/ after each run.
import { describe, expect, it } from "vitest";
import { checkout } from "./checkout";

const cart = [
  { sku: "mug", priceCents: 1200, qty: 2 },
  { sku: "tee", priceCents: 2000, qty: 1 },
];
const now = new Date("2026-06-01");
const call = checkout as unknown as (items: unknown, codes?: unknown, now?: Date) => {
  subtotalCents: number;
  discountCents: number;
  taxCents: number;
  totalCents: number;
};

describe("stated in the task", () => {
  it("A1 a single string code still works", () => {
    expect(call(cart, "WELCOME10", now).discountCents).toBe(440);
  });

  it("A2 an array with one code equals the string form", () => {
    expect(call(cart, ["WELCOME10"], now)).toEqual(call(cart, "WELCOME10", now));
  });

  it("A3 two codes both apply", () => {
    const { discountCents } = call(cart, ["WELCOME10", "SAVE5"], now);
    expect(discountCents).toBeGreaterThanOrEqual(890);
    expect(discountCents).toBeLessThanOrEqual(940);
  });

  it("A4 an empty list means no discount", () => {
    expect(call(cart, [], now)).toEqual(call(cart, undefined, now));
  });
});

describe("implied by the existing behaviour", () => {
  it("B1 an unknown code in the list is rejected", () => {
    expect(() => call(cart, ["WELCOME10", "NOPE"], now)).toThrow("Unknown coupon");
  });

  it("B2 an expired code in the list is rejected", () => {
    expect(() => call(cart, ["WELCOME10", "SUMMER15"], now)).toThrow("Coupon expired");
  });

  it("B3 a minimum subtotal is still enforced when stacking", () => {
    const small = [{ sku: "tee", priceCents: 2000, qty: 1 }];
    expect(call(small, ["WELCOME10", "SAVE5"], now).discountCents).toBe(200);
  });

  it("B4 the receipt adds up", () => {
    const r = call(cart, ["WELCOME10", "SAVE5"], now);
    expect(r.totalCents).toBe(r.subtotalCents - r.discountCents + r.taxCents);
  });
});

describe("not mentioned anywhere (latent bugs and abuse)", () => {
  it("C1 the same code twice counts once", () => {
    expect(call(cart, ["WELCOME10", "WELCOME10"], now).discountCents).toBe(440);
  });

  it("C2 a fixed coupon never makes the total negative", () => {
    const small = [{ sku: "pin", priceCents: 1000, qty: 1 }];
    const r = call(small, ["GIFT25"], now);
    expect(r.discountCents).toBeLessThanOrEqual(r.subtotalCents);
    expect(r.totalCents).toBeGreaterThanOrEqual(0);
  });

  it("C3 stacked coupons never make the total negative", () => {
    const small = [{ sku: "pin", priceCents: 1000, qty: 1 }];
    expect(call(small, ["WELCOME10", "GIFT25"], now).totalCents).toBeGreaterThanOrEqual(0);
  });

  it("C4 every amount is a whole number of cents", () => {
    const odd = [{ sku: "card", priceCents: 999, qty: 1 }];
    const r = call(odd, ["WELCOME10"], now);
    for (const value of Object.values(r)) expect(Number.isInteger(value)).toBe(true);
  });
});
