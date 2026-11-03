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

export function discountFor(coupon: Coupon, amountCents: number): number {
  if (coupon.minSubtotalCents && amountCents < coupon.minSubtotalCents) return 0;
  return coupon.kind === "percent" ? (amountCents * coupon.value) / 100 : coupon.value;
}

export function checkout(items: Item[], code?: string, now: Date = new Date()): Receipt {
  const subtotalCents = subtotal(items);
  const discountCents = code ? discountFor(findCoupon(code, now), subtotalCents) : 0;
  const afterDiscount = subtotalCents - discountCents;
  const taxCents = Math.round(afterDiscount * TAX_RATE);
  return {
    subtotalCents,
    discountCents,
    taxCents,
    totalCents: afterDiscount + taxCents,
  };
}
