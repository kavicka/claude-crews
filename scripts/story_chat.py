"""Generate the animated chat excerpts of the bakery story (assets/bakery-*.svg).

Every line is condensed from the recorded runs in examples/bakery/runs; the full
transcripts and outputs are there. Run: python3 scripts/story_chat.py
"""
import html
import json
from pathlib import Path

from avatars import AGENTS, CREAM, CSS, INK, KRAFT, MUSTARD, ORANGE, SAGE, avatar_body

ROOT = Path(__file__).resolve().parent.parent
STORY = ROOT / "examples" / "bakery" / "story.json"
W, PAD, LH = 760, 20, 20
STYLE = {f"{plugin}:{name}": style for plugin, name, *style, _model in AGENTS}
COLORS = {"crew": "#7FA7C9", "office": MUSTARD, "council": "#B49AC4"}
KIND = {
    # kind: (bubble fill, bubble stroke, label shown after the speaker's name)
    "agent": ("#30302E", "#45443F", ""),
    "you": ("#3A3530", "#6B5D50", ""),
    "ask": ("#3B2F2A", ORANGE, "asks you"),
    "deliver": ("#2E3529", SAGE, "for the client"),
}


def chip_color(text: str) -> str:
    t = text.upper()
    if t.startswith(("YES", "GO", "APPROVE", "PASSED", "FAIR", "✓")):
        return SAGE
    if t.startswith(("NO", "RETHINK", "CHANGES", "REJECTED", "UNDER", "OVER")):
        return ORANGE
    return MUSTARD


def face(msg: dict, i: int, x: float, y: float) -> str:
    key = msg.get("avatar")
    if key:
        return f'<g transform="translate({x - 6} {y - 4}) scale(0.46)">{avatar_body(*STYLE[key], uid=f"s{i}", delay=i * .53)}</g>'
    label = "You" if msg["kind"] == "you" else "?"
    fill = CREAM if msg["kind"] == "you" else ORANGE
    return (f'<circle cx="{x + 16}" cy="{y + 17}" r="15" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            f'<text x="{x + 16}" y="{y + 22}" class="ini">{label}</text>')


def build(act: dict) -> str:
    msgs = act["messages"]
    cycle = max(14.0, 2.4 * len(msgs) + 5)
    y, kfs, groups = 58, [], []
    for i, m in enumerate(msgs):
        lines = m.get("lines", [])
        h = 28 + LH * (1 + len(lines))
        fill, stroke, label = KIND[m["kind"]]
        start = (0.6 + i * 2.3) / cycle * 100
        kfs.append(f"@keyframes {act['id']}{i}{{0%,{start:.1f}%{{opacity:0;transform:translateY(8px)}}"
                   f"{start + 3:.1f}%,93%{{opacity:1;transform:translateY(0)}}98%,100%{{opacity:0}}}}")
        who_color = CREAM if m["kind"] == "you" else (ORANGE if m["kind"] == "ask" else COLORS.get(m.get("avatar", "").split(":")[0], KRAFT))
        who = html.escape(m["who"]) + (f' <tspan class="tag">· {label}</tspan>' if label else "")
        g = [f'<g class="b" style="animation-name:{act["id"]}{i}">',
             f'<rect x="{PAD + 44}" y="{y}" width="{W - PAD * 2 - 44}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}"/>',
             face(m, i, PAD, y),
             f'<text x="{PAD + 58}" y="{y + 21}" class="who" fill="{who_color}">{who}</text>',
             f'<text x="{PAD + 58}" y="{y + 22 + LH}" class="head">{html.escape(m["head"])}</text>']
        for k, line in enumerate(lines):
            g.append(f'<text x="{PAD + 58}" y="{y + 22 + LH * (k + 2)}" class="line">{html.escape(line)}</text>')
        if m.get("chip"):
            c = chip_color(m["chip"])
            wchip = 14 + 7.2 * len(m["chip"])
            g.append(f'<rect x="{W - PAD - 14 - wchip}" y="{y + 9}" width="{wchip}" height="22" rx="11" fill="{c}" opacity=".18"/>')
            g.append(f'<text x="{W - PAD - 14 - wchip / 2}" y="{y + 24}" class="chip" fill="{c}">{html.escape(m["chip"])}</text>')
        g.append("</g>")
        groups.append("\n".join(g))
        y += h + 10
    H = y + 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{html.escape(act["aria"])}">
<style>
text{{font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:#F5F4EE}}
.ini{{font-size:10px;font-weight:700;fill:{INK};text-anchor:middle}}
.who{{font-size:12.5px;font-weight:700}}
.tag{{font-weight:400;fill:#A8A59B}}
.head{{font-family:Georgia,"Times New Roman",serif;font-size:16px}}
.line{{font-size:13px;fill:#A8A59B}}
.chip{{font-size:12px;font-weight:700;text-anchor:middle}}
.top{{font-size:12px;fill:#A8A59B;font-family:ui-monospace,"SF Mono",Menlo,monospace}}
.b{{opacity:0;animation-duration:{cycle:.1f}s;animation-iteration-count:infinite;animation-timing-function:ease-out}}
@media (prefers-reduced-motion: reduce){{.b{{animation:none;opacity:1}}}}
{CSS}
{chr(10).join(kfs)}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#262624"/>
<text x="{PAD}" y="36" class="top">{html.escape(act["caption"])}</text>
{chr(10).join(groups)}
</svg>
'''


if __name__ == "__main__":
    for act in json.loads(STORY.read_text())["acts"]:
        path = ROOT / "assets" / f"bakery-{act['id']}.svg"
        path.write_text(build(act))
        print(path.relative_to(ROOT))
