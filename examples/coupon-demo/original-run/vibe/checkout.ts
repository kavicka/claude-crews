export type Item = {
  sku: string;
  priceCents: number;
  qty: number;
};

export type Coupon = {
  code: string;
  kind: "percent" | "fixed";
  value: number;
  minSubtotalCents?: number;
  expiresAt?: string;
};

export const COUPONS: Coupon[] = [
  { code: "WELCOME10", kind: "percent", value: 10 },
  { code: "SAVE5", kind: "fixed", value: 500, minSubtotalCents: 3000 },
  { code: "GIFT25", kind: "fixed", value: 2500 },
  { code: "SUMMER15", kind: "percent", value: 15, expiresAt: "2025-09-01" },
];

export const TAX_RATE = 0.2;

export type Receipt = {
  subtotalCents: number;
  discountCents: number;
  taxCents: number;
  totalCents: number;
};

export function subtotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.priceCents * item.qty, 0);
}

export function findCoupon(code: string, now: Date = new Date()): Coupon {
  const coupon = COUPONS.find((c) => c.code === code);
  if (!coupon) throw new Error(`Unknown coupon: ${code}`);
  if (coupon.expiresAt && new Date(coupon.expiresAt) < now) {
    throw new Error(`Coupon expired: ${code}`);
  }
  return coupon;
}

export function discountFor(coupon: Coupon, amountCents: number, subtotalCents = amountCents): number {
  if (coupon.minSubtotalCents && subtotalCents < coupon.minSubtotalCents) return 0;
  const raw = coupon.kind === "percent" ? Math.round((amountCents * coupon.value) / 100) : coupon.value;
  return Math.min(raw, Math.max(amountCents, 0));
}

function normalizeCodes(codes?: string | string[]): string[] {
  const list = codes === undefined ? [] : Array.isArray(codes) ? codes : [codes];
  const trimmed = list.map((c) => c.trim()).filter((c) => c !== "");
  const seen = new Set<string>();
  for (const code of trimmed) {
    if (seen.has(code)) throw new Error(`Duplicate coupon: ${code}`);
    seen.add(code);
  }
  return trimmed;
}

/**
 * Applies coupons to the cart. Percent coupons are applied before fixed ones, each to the
 * amount left after the previous ones, so the result does not depend on the order of codes.
 * Minimum-subtotal rules are checked against the cart subtotal; the discount never exceeds it.
 */
export function checkout(items: Item[], codes?: string | string[], now: Date = new Date()): Receipt {
  const subtotalCents = subtotal(items);
  const coupons = normalizeCodes(codes)
    .map((code) => findCoupon(code, now))
    .sort((a, b) => (a.kind === b.kind ? 0 : a.kind === "percent" ? -1 : 1));
  let discountCents = 0;
  for (const coupon of coupons) {
    discountCents += discountFor(coupon, subtotalCents - discountCents, subtotalCents);
  }
  const afterDiscount = subtotalCents - discountCents;
  const taxCents = Math.round(afterDiscount * TAX_RATE);
  return {
    subtotalCents,
    discountCents,
    taxCents,
    totalCents: afterDiscount + taxCents,
  };
}
