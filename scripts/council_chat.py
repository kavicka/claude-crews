"""Generate assets/council-chat.svg, the animated excerpt of the real council run in examples/council-demo.

Run: python3 scripts/council_chat.py
"""
import html
from pathlib import Path

from avatars import AGENTS, CREAM, CSS, INK, KRAFT, ORANGE, SAGE, avatar_body

ROOT = Path(__file__).resolve().parent.parent
W, PAD, LH, CYCLE = 760, 20, 20, 20.0
STYLE = {name: style for plugin, name, *style, _model in AGENTS if plugin == "council"}

# speaker, avatar key (None = the user), name colour, headline, detail lines, vote
MSGS = [
    ("you", None, CREAM, "/council:vote --full Should Maya take the 6-month contract?", ["11 000 €/month for 6 months, but she must pause her 3-year client A."], None),
    ("optimist", "optimist", SAGE, "Take it, but negotiate the transition first.", ["+30 000 € gross in 6 months; payments work raises her rates."], "YES 70"),
    ("skeptic", "skeptic", ORANGE, "Not as set up. A will be lost, not paused.", ["A year without A costs 33 600 €, more than the whole gain."], "NO 65"),
    ("engineer", "engineer", "#7FA7C9", "Take it if A and B commit to a return path.", ["Low technical risk; the 3-week start is the danger."], "YES 70"),
    ("client A", "client", "#B49AC4", "\"Maybe\" means I'll replace you by month 3.", ["Keep 4–6 h/week for me and I stay."], "YES 62"),
    ("skeptic", "skeptic", ORANGE, "Round 2 — correction: I counted A twice.", ["Losing A after the contract costs 16 800 €, not 33 600 €."], "NO 55"),
    ("moderator", "moderator", KRAFT, "PASSED · 4/5 YES (80 %) · weighted 82 %", ["Take it only with a paid bridge for A + a notice clause.", "5 claims failed the evidence check and were dropped."], None),
]


def build() -> str:
    y, kfs, groups = 58, [], []
    for i, (who, key, col, head, lines, vote) in enumerate(MSGS):
        h = 28 + LH * (1 + len(lines))
        start = (0.6 + i * 2.3) / CYCLE * 100
        kfs.append(f"@keyframes m{i}{{0%,{start:.1f}%{{opacity:0;transform:translateY(8px)}}{start + 3:.1f}%,93%{{opacity:1;transform:translateY(0)}}98%,100%{{opacity:0}}}}")
        if key:
            face = f'<g transform="translate({PAD - 6} {y - 4}) scale(0.46)">{avatar_body(*STYLE[key], uid=f"c{i}", delay=i * .53)}</g>'
        else:
            face = (f'<circle cx="{PAD + 16}" cy="{y + 17}" r="15" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>'
                    f'<text x="{PAD + 16}" y="{y + 22}" class="ini">You</text>')
        g = [f'<g class="b" style="animation-name:m{i}">',
             f'<rect x="{PAD + 44}" y="{y}" width="{W - PAD * 2 - 44}" height="{h}" rx="12" class="bub"/>',
             face,
             f'<text x="{PAD + 58}" y="{y + 21}" class="who" fill="{col}">{html.escape(who)}</text>',
             f'<text x="{PAD + 58}" y="{y + 22 + LH}" class="head">{html.escape(head)}</text>']
        for k, line in enumerate(lines):
            g.append(f'<text x="{PAD + 58}" y="{y + 22 + LH * (k + 2)}" class="line">{html.escape(line)}</text>')
        if vote:
            vc = SAGE if vote.startswith("YES") else ORANGE
            g.append(f'<rect x="{W - PAD - 86}" y="{y + 9}" width="72" height="22" rx="11" fill="{vc}" opacity=".18"/>')
            g.append(f'<text x="{W - PAD - 50}" y="{y + 24}" class="vote" fill="{vc}">{vote}</text>')
        g.append("</g>")
        groups.append("\n".join(g))
        y += h + 10
    H = y + 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Animated council debate from a real run">
<style>
text{{font-family:"Styrene B","Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:#F5F4EE}}
.bub{{fill:#30302E;stroke:#45443F}}
.ini{{font-size:10px;font-weight:700;fill:{INK};text-anchor:middle}}
.who{{font-size:12.5px;font-weight:700}}
.head{{font-family:"Tiempos Headline","Copernicus",Georgia,"Times New Roman",serif;font-size:16px}}
.line{{font-size:13px;fill:#A8A59B}}
.vote{{font-size:12px;font-weight:700;text-anchor:middle}}
.top{{font-size:12px;fill:#A8A59B;font-family:ui-monospace,"SF Mono",Menlo,monospace}}
.b{{opacity:0;animation-duration:{CYCLE}s;animation-iteration-count:infinite;animation-timing-function:ease-out}}
@media (prefers-reduced-motion: reduce){{.b{{animation:none;opacity:1}}}}
{CSS}
{chr(10).join(kfs)}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#262624"/>
<text x="{PAD}" y="36" class="top">#council · real run, excerpts · full transcript in examples/council-demo</text>
{chr(10).join(groups)}
</svg>
'''


if __name__ == "__main__":
    svg = build()
    (ROOT / "assets" / "council-chat.svg").write_text(svg)
    print(svg.split('height="')[1].split('"')[0])
