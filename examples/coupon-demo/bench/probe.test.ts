// Extra checks run after each attempt, next to the hidden tests. Not shown to any agent.
import { it } from "vitest";
import { writeFileSync } from "node:fs";
import { checkout } from "./checkout";

const call = checkout as unknown as (items: unknown, codes?: unknown, now?: Date) => { totalCents: number };

const perms = (a: string[]): string[][] =>
  a.length <= 1 ? [a] : a.flatMap((x, i) => perms([...a.slice(0, i), ...a.slice(i + 1)]).map((p) => [x, ...p]));

function totalOrError(items: unknown, codes: string[], now: Date): string {
  try {
    return String(call(items, codes, now).totalCents);
  } catch (e) {
    return "throws: " + String((e as Error).message).split(":")[0];
  }
}

// Same coupons in every order, on carts from 5.00 to 200.00: how many carts get more than one total?
function orderDependence(codes: string[], now: Date) {
  let carts = 0;
  let dependent = 0;
  let example = "";
  for (let p = 500; p <= 20000; p += 7) {
    const cart = [{ sku: "x", priceCents: p, qty: 1 }];
    const totals = new Set(perms(codes).map((order) => totalOrError(cart, order, now)));
    carts++;
    if (totals.size > 1) {
      dependent++;
      if (!example) example = `${p} cents: ${[...totals].join(" vs ")}`;
    }
  }
  return { carts, dependent, example };
}

it("probe", () => {
  const out = {
    // SUMMER15 is still valid on this date, so two percent coupons can stack.
    two_percent: orderDependence(["WELCOME10", "SUMMER15"], new Date("2025-06-01")),
    percent_and_fixed: orderDependence(["WELCOME10", "SAVE5", "GIFT25"], new Date("2026-06-01")),
    // The skeptic's free-cart case from the original run: GIFT25 + SAVE5 on a 30.00 cart.
    free_cart_total: totalOrError([{ sku: "x", priceCents: 3000, qty: 1 }], ["GIFT25", "SAVE5"], new Date("2026-06-01")),
  };
  writeFileSync(process.env.PROBE_OUT as string, JSON.stringify(out));
});
