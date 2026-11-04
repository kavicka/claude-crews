"""Draw assets/bench-results.svg from examples/coupon-demo/bench/results/*/result.json.

One dot per run, a tick at the mean, four panels with their own scales.
Run: python3 scripts/bench_chart.py
"""
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "examples" / "coupon-demo" / "bench" / "results"
OUT = ROOT / "assets" / "bench-results.svg"

VARIANTS = [("vibe-medium", "One prompt · medium"), ("vibe-xhigh", "One prompt · xhigh"), ("crew", "/crew:ship")]
PANELS = [
    # title, value, axis min, axis max, axis label format, mean label format
    ("Hidden tests passed (of 12)", lambda r: r["score"]["hidden_passed"], 6, 12, "{:.0f}", "{:.1f}"),
    ("Tests in the suite after", lambda r: r["score"]["own_tests_total"], 0, 30, "{:.0f}", "{:.0f}"),
    ("Cost per run (USD)", lambda r: r["cost_usd"] or 0, 0, 2, "${:.0f}", "${:.2f}"),
    ("Wall time (min)", lambda r: r["wall_seconds"] / 60, 0, 8, "{:.0f}", "{:.1f}"),
]

BG, INK, MUTED, GRID, DOT, MEAN = "#262624", "#F5F4EE", "#A8A59B", "#3A3936", "#7FA7C9", "#F5F4EE"
LABEL_W, PANEL_W, VAL_W, GAP, ROW_H, TOP, PAD = 160, 140, 48, 18, 46, 74, 24


def main() -> None:
    runs = [json.loads(p.read_text()) for p in RESULTS.glob("*/result.json")]
    width = PAD + LABEL_W + len(PANELS) * (PANEL_W + VAL_W) + (len(PANELS) - 1) * GAP + PAD
    height = TOP + ROW_H * len(VARIANTS) + 58
    n = {v: sum(r["variant"] == v for r in runs) for v, _ in VARIANTS}
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
           f'role="img" aria-label="Coupon benchmark, {min(n.values())} runs per variant: hidden tests, tests written, '
           f'cost and time for one prompt at medium and xhigh effort and for crew:ship">',
           '<style>text{font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:%s}'
           '.h{font-size:13px;font-weight:600}.l{font-size:13px}.m{font-size:11px;fill:%s}.v{font-size:12px;font-weight:600}</style>'
           % (INK, MUTED),
           f'<rect width="{width}" height="{height}" rx="14" fill="{BG}"/>',
           f'<text x="{PAD}" y="30" class="m">Same task, {min(n.values())} runs per variant · one dot per run, tick = mean · '
           f'examples/coupon-demo/bench</text>']

    for row, (key, label) in enumerate(VARIANTS):
        cy = TOP + ROW_H * row + ROW_H / 2
        out.append(f'<text x="{PAD}" y="{cy + 4}" class="l">{label}</text>')

    for p, (title, get, lo, hi, fmt, mfmt) in enumerate(PANELS):
        x0 = PAD + LABEL_W + p * (PANEL_W + VAL_W + GAP)
        out.append(f'<text x="{x0}" y="{TOP - 16}" class="h">{title}</text>')
        for row in range(len(VARIANTS)):
            cy = TOP + ROW_H * row + ROW_H / 2
            out.append(f'<line x1="{x0}" x2="{x0 + PANEL_W}" y1="{cy}" y2="{cy}" stroke="{GRID}" stroke-width="1"/>')
        base = TOP + ROW_H * len(VARIANTS) + 6
        out.append(f'<text x="{x0}" y="{base + 12}" class="m">{fmt.format(lo)}</text>')
        out.append(f'<text x="{x0 + PANEL_W}" y="{base + 12}" class="m" text-anchor="end">{fmt.format(hi)}</text>')

        def sx(v: float) -> float:
            return x0 + (min(max(v, lo), hi) - lo) / (hi - lo) * PANEL_W

        for row, (key, _) in enumerate(VARIANTS):
            vals = [get(r) for r in runs if r["variant"] == key]
            if not vals:
                continue
            cy = TOP + ROW_H * row + ROW_H / 2
            seen: dict[float, int] = {}
            for v in sorted(vals):
                k = round(sx(v))
                offset = seen.get(k, 0)
                seen[k] = offset + 1
                dy = (offset % 2 * 2 - 1) * (offset + 1) // 2 * 7 if offset else 0
                out.append(f'<circle cx="{sx(v):.1f}" cy="{cy + dy:.1f}" r="4.5" fill="{DOT}" stroke="{BG}" stroke-width="2"/>')
            mean = statistics.mean(vals)
            out.append(f'<line x1="{sx(mean):.1f}" x2="{sx(mean):.1f}" y1="{cy - 13}" y2="{cy + 13}" stroke="{MEAN}" stroke-width="2" stroke-linecap="round"/>')
            out.append(f'<text x="{x0 + PANEL_W + VAL_W - 4}" y="{cy + 4}" class="v" text-anchor="end">{mfmt.format(mean)}</text>')

    out.append("</svg>")
    OUT.write_text("\n".join(out) + "\n")
    print(OUT.relative_to(ROOT), width, height)


if __name__ == "__main__":
    main()
