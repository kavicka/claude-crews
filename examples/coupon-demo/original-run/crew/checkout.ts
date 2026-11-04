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

/**
 * Whole-cent discount of one coupon on `baseCents`, between 0 and `baseCents`.
 * The coupon's minimum is checked against `qualifyingCents` (the original subtotal when stacking).
 */
export function discountFor(coupon: Coupon, baseCents: number, qualifyingCents = baseCents): number {
  if (coupon.minSubtotalCents && qualifyingCents < coupon.minSubtotalCents) return 0;
  return coupon.kind === "percent"
    ? Math.round((baseCents * coupon.value) / 100)
    : Math.min(coupon.value, baseCents);
}

/** A string becomes one code; "" is ignored. The caller's array is never mutated. */
function normalizeCodes(codes?: string | readonly string[]): string[] {
  const list = typeof codes === "string" ? [codes] : (codes ?? []);
  return list.filter((code) => code !== "");
}

/**
 * Validates every code (first invalid one throws), then applies the unique coupons
 * percent-first in catalog order to a running amount, so input order never matters.
 */
function stackedDiscount(codes: string[], subtotalCents: number, now: Date): number {
  for (const code of codes) findCoupon(code, now);
  const chosen = COUPONS.filter((c) => codes.includes(c.code));
  const ordered = [
    ...chosen.filter((c) => c.kind === "percent"),
    ...chosen.filter((c) => c.kind === "fixed"),
  ];
  let runningCents = subtotalCents;
  for (const coupon of ordered) {
    runningCents -= discountFor(coupon, runningCents, subtotalCents);
  }
  return subtotalCents - runningCents;
}

export function checkout(
  items: Item[],
  codes?: string | readonly string[],
  now: Date = new Date(),
): Receipt {
  const subtotalCents = subtotal(items);
  const discountCents = stackedDiscount(normalizeCodes(codes), subtotalCents, now);
  const afterDiscount = subtotalCents - discountCents;
  const taxCents = Math.round(afterDiscount * TAX_RATE);
  return {
    subtotalCents,
    discountCents,
    taxCents,
    totalCents: afterDiscount + taxCents,
  };
}
