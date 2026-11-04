/** Opening hours by day of week (0 = Sunday), in local time "HH:MM". Closed days are null. */
export const OPENING_HOURS: Record<number, { open: string; close: string } | null> = {
  0: { open: "07:00", close: "12:00" },
  1: null,
  2: { open: "07:00", close: "18:00" },
  3: { open: "07:00", close: "18:00" },
  4: { open: "07:00", close: "18:00" },
  5: { open: "07:00", close: "18:00" },
  6: { open: "07:00", close: "18:00" },
};

export const TIME_ZONE = "Europe/Bratislava";
