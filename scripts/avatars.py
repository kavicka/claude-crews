"""Generate the crew avatars (assets/avatars/*.svg) and the crew grid (assets/the-crew.svg).

Soft 3D vector style: radial-gradient volume, specular highlights, glassy eyes,
contact shadows, and a gentle idle loop (bob, squash, blink) in plain SVG + CSS.

Run: python3 scripts/avatars.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "avatars"

INK = "#2B2522"
ORANGE, CLAY, KRAFT, MUSTARD = "#D97757", "#C46A5A", "#D4A27F", "#E3B25B"
SAGE, TEAL, BLUE, LILAC, CREAM = "#8FA876", "#6FA3A0", "#7FA7C9", "#B49AC4", "#E8DCC8"

# Body shapes in a 96 × 96 box, body roughly centred at (48, 54).
SHAPES = {
    "round": "M48 18 C70 18 82 34 82 54 C82 74 68 86 48 86 C28 86 14 74 14 54 C14 34 26 18 48 18 Z",
    "square": "M30 20 H66 C76 20 80 26 80 36 V70 C80 80 74 86 64 86 H32 C22 86 16 80 16 70 V36 C16 26 20 20 30 20 Z",
    "pill": "M26 28 H70 C80 28 86 38 86 56 C86 74 80 84 70 84 H26 C16 84 10 74 10 56 C10 38 16 28 26 28 Z",
    "drop": "M48 12 C58 26 82 40 82 60 C82 76 68 86 48 86 C28 86 14 76 14 60 C14 40 38 26 48 12 Z",
    "bean": "M40 20 C62 14 84 30 82 54 C80 76 64 88 44 86 C24 84 12 70 14 50 C16 34 24 24 40 20 Z",
    "ghost": "M48 18 C68 18 80 32 80 52 V80 C80 85 76 87 72 84 L66 79 L58 85 L48 79 L38 85 L30 79 L24 84 C20 87 16 85 16 80 V52 C16 32 28 18 48 18 Z",
}

CSS = """
.av-bob{animation:av-bob 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
.av-shadow{animation:av-shadow 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 50%}
.av-eyes{animation:av-blink 5.2s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 50%}
.av-acc{animation:av-acc 3.4s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
@keyframes av-bob{0%,100%{transform:translateY(0) scale(1,1)}45%{transform:translateY(-3px) scale(.985,1.02)}55%{transform:translateY(-3px) scale(.985,1.02)}85%{transform:translateY(0) scale(1.03,.97)}}
@keyframes av-shadow{0%,100%{transform:scale(1,1);opacity:1}50%{transform:scale(.86,.86);opacity:.7}}
@keyframes av-blink{0%,90%,100%{transform:scaleY(1)}93%{transform:scaleY(.08)}96%{transform:scaleY(1)}}
@keyframes av-acc{0%,100%{transform:rotate(0)}50%{transform:rotate(-5deg) translateY(-1px)}}
@media (prefers-reduced-motion: reduce){.av-bob,.av-shadow,.av-eyes,.av-acc{animation:none}}
"""


def mix(hex_color: str, other: str, t: float) -> str:
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def defs(u: str, color: str) -> str:
    light, dark, deep = mix(color, "#FFFFFF", .5), mix(color, "#000000", .28), mix(color, "#000000", .5)
    return f'''<defs>
<radialGradient id="{u}b" cx="34%" cy="26%" r="80%"><stop offset="0" stop-color="{light}"/><stop offset=".45" stop-color="{color}"/><stop offset="1" stop-color="{dark}"/></radialGradient>
<linearGradient id="{u}ao" x1="0" y1="0" x2="0" y2="1"><stop offset=".55" stop-color="{deep}" stop-opacity="0"/><stop offset="1" stop-color="{deep}" stop-opacity=".55"/></linearGradient>
<radialGradient id="{u}rim" cx="78%" cy="70%" r="45%"><stop offset=".6" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFE7D6" stop-opacity=".35"/></radialGradient>
<radialGradient id="{u}sp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
<radialGradient id="{u}sh" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#000" stop-opacity=".5"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="{u}eye" cx="42%" cy="34%" r="70%"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#F4EFE8"/><stop offset="1" stop-color="#D9D1C6"/></radialGradient>
<radialGradient id="{u}iris" cx="40%" cy="35%" r="65%"><stop offset="0" stop-color="#5A4A42"/><stop offset="1" stop-color="#1C1714"/></radialGradient>
<radialGradient id="{u}ck" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FF8F7E" stop-opacity=".55"/><stop offset="1" stop-color="#FF8F7E" stop-opacity="0"/></radialGradient>
<linearGradient id="{u}lid" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient>
<filter id="{u}ds" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="1.6" stdDeviation="1.3" flood-color="#000" flood-opacity=".35"/></filter>
</defs>'''


def glassy_eye(u: str, cx: float, cy: float, rx: float, ry: float, look: float = 1.2) -> str:
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{u}eye)"/>'
            f'<circle cx="{cx + look}" cy="{cy + 1.2}" r="{min(rx, ry) * .62}" fill="url(#{u}iris)"/>'
            f'<circle cx="{cx + look + 1.8}" cy="{cy - 1.4}" r="{min(rx, ry) * .26}" fill="#FFFFFF"/>'
            f'<circle cx="{cx + look - 1.6}" cy="{cy + 2.6}" r="{min(rx, ry) * .11}" fill="#FFFFFF" opacity=".8"/>')


def eyes(u: str, kind: str) -> str:
    arc = f'stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"'
    if kind == "happy":
        return f'<path d="M30 53 Q36 45 42 53" {arc}/><path d="M54 53 Q60 45 66 53" {arc}/>'
    if kind == "sleepy":
        return f'<path d="M30 52 Q36 57 42 52" {arc}/><path d="M54 52 Q60 57 66 52" {arc}/>'
    if kind == "skeptic":
        return (glassy_eye(u, 36, 52, 7.5, 8.5) + glassy_eye(u, 60, 53, 7.5, 8.5)
                + f'<path d="M52 44 H68 V49 Q60 52 52 49 Z" fill="url(#{u}lid)"/>'
                + f'<path d="M28 41 L44 37" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>'
                + f'<path d="M52 45 L68 45" stroke="{INK}" stroke-width="3.2" stroke-linecap="round"/>')
    if kind == "glasses":
        frame = f'stroke="{INK}" stroke-width="2.6"'
        return (glassy_eye(u, 35, 52, 7, 7.5) + glassy_eye(u, 61, 52, 7, 7.5)
                + f'<circle cx="35" cy="52" r="10" fill="#CFE3F2" fill-opacity=".18" {frame}/>'
                + f'<circle cx="61" cy="52" r="10" fill="#CFE3F2" fill-opacity=".18" {frame}/>'
                + f'<path d="M45 51 Q48 48 51 51" {frame} fill="none"/>'
                + '<path d="M29 46 L33 44" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>'
                + '<path d="M55 46 L59 44" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>')
    if kind == "wide":
        return glassy_eye(u, 36, 51, 8.5, 10.5, 1.5) + glassy_eye(u, 60, 51, 8.5, 10.5, 1.5)
    if kind == "focused":
        return (glassy_eye(u, 36, 53, 7.5, 7) + glassy_eye(u, 60, 53, 7.5, 7)
                + f'<path d="M28 44 L44 47" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
                + f'<path d="M52 47 L68 44" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    return glassy_eye(u, 36, 52, 7.5, 8.8) + glassy_eye(u, 60, 52, 7.5, 8.8)


def mouth(kind: str) -> str:
    if kind == "smile":
        return f'<path d="M40 67 Q48 74.5 56 67" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
    if kind == "grin":
        return (f'<path d="M38 65 Q48 79 58 65 Q48 68 38 65 Z" fill="{INK}"/>'
                f'<path d="M42.5 70 Q48 75 53.5 70 Q48 68.5 42.5 70 Z" fill="#E8776A"/>'
                f'<path d="M40 65.6 Q48 67.4 56 65.6 L55 67 Q48 68.6 41 67 Z" fill="#FFFFFF"/>')
    if kind == "o":
        return f'<ellipse cx="48" cy="69" rx="4" ry="5" fill="{INK}"/><ellipse cx="48" cy="71" rx="2.4" ry="2" fill="#E8776A"/>'
    if kind == "smirk":
        return f'<path d="M41 69 Q50 70.5 57 64" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
    return f'<path d="M41 68 Q48 69 55 68" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/>'


def accessory(kind: str) -> str:
    s = f'stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    hi = 'stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" opacity=".7" fill="none"'
    if kind == "clipboard":
        return (f'<rect x="64" y="62" width="22" height="28" rx="3" fill="#FBF7F0" {s}/>'
                f'<rect x="70" y="59" width="10" height="6" rx="2" fill="{KRAFT}" {s}/>'
                f'<path d="M69 72 H81 M69 78 H81 M69 84 H76" stroke="{BLUE}" stroke-width="2.2" stroke-linecap="round"/>')
    if kind == "question":
        return (f'<circle cx="78" cy="20" r="13" fill="#FBF7F0" {s}/>'
                f'<path d="M73.5 16 Q74 11 78.5 11 Q83 11.5 83 16 Q83 19.5 78.5 21 V24" stroke="{ORANGE}" stroke-width="3" stroke-linecap="round" fill="none"/>'
                f'<circle cx="78.5" cy="29" r="2" fill="{ORANGE}"/><path d="M70 13 Q72 9 76 8" {hi}/>')
    if kind == "code":
        return (f'<rect x="58" y="6" width="34" height="22" rx="6" fill="#3A3330" {s}/>'
                f'<path d="M66 12 L62 17 L66 22 M84 12 L88 17 L84 22 M77 11 L73 23" stroke="{SAGE}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "brush":
        return (f'<path d="M86 12 L68 40" stroke="{KRAFT}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M85 13 L72 33" {hi}/>'
                f'<path d="M64 38 Q60 46 66 48 Q72 48 70 42 Z" fill="{ORANGE}" {s}/>')
    if kind == "block":
        return (f'<path d="M76 6 L90 13 L76 20 L62 13 Z" fill="{mix(SAGE, "#FFFFFF", .25)}" {s}/>'
                f'<path d="M62 13 V29 L76 36 V20 Z" fill="{TEAL}" {s}/>'
                f'<path d="M90 13 V29 L76 36 V20 Z" fill="{mix(KRAFT, "#000000", .1)}" {s}/>')
    if kind == "tube":
        return (f'<path d="M77 8 V34 Q80 41 83 34 V8 Z" fill="#E9F2F4" fill-opacity=".85" {s}/>'
                f'<path d="M77.6 22 V34 Q80 38.4 82.4 34 V22 Z" fill="{SAGE}"/>'
                f'<path d="M74 7 H86" {s}/><path d="M79 12 V30" {hi}/>'
                f'<circle cx="80" cy="27" r="1.4" fill="#FFFFFF"/>')
    if kind == "check":
        return (f'<circle cx="78" cy="20" r="13" fill="{SAGE}" {s}/>'
                f'<path d="M72 20 L76.5 24.5 L84 15.5" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M70 14 Q72 9 77 8" {hi}/>')
    if kind == "book":
        return (f'<path d="M60 70 Q70 66 78 70 Q86 66 94 70 V90 Q86 86 78 90 Q70 86 60 90 Z" fill="#FBF7F0" {s}/>'
                f'<path d="M78 70 V90" {s}/><path d="M63 75 Q69 72 75 75 M63 80 Q69 77 75 80" stroke="{KRAFT}" stroke-width="1.6" fill="none"/>')
    if kind == "magnifier":
        return (f'<path d="M84 28 L92 36" stroke="{KRAFT}" stroke-width="5.5" stroke-linecap="round"/>'
                f'<circle cx="76" cy="20" r="11" fill="#CFE3F2" fill-opacity=".55" stroke="{CREAM}" stroke-width="3.6"/>'
                f'<path d="M70 16 Q72 12 76 11" {hi}/>')
    if kind == "receipt":
        return (f'<path d="M64 60 H88 V90 L84 87 L80 90 L76 87 L72 90 L68 87 L64 90 Z" fill="#FBF7F0" {s}/>'
                f'<path d="M69 68 H83 M69 74 H83" stroke="{KRAFT}" stroke-width="2.2" stroke-linecap="round"/>'
                f'<path d="M69 80 H77" stroke="{ORANGE}" stroke-width="2.6" stroke-linecap="round"/>')
    if kind == "coin":
        return (f'<circle cx="78" cy="20" r="13" fill="{MUSTARD}" {s}/>'
                f'<circle cx="78" cy="20" r="9" fill="none" stroke="{mix(MUSTARD, "#000000", .25)}" stroke-width="1.6"/>'
                f'<text x="78" y="25" text-anchor="middle" font-family="Georgia, serif" font-size="14" font-weight="700" fill="{mix(MUSTARD, "#000000", .45)}">€</text>'
                f'<path d="M70 13 Q72 9 77 8" {hi}/>')
    if kind == "envelope":
        return (f'<rect x="60" y="64" width="32" height="22" rx="3" fill="#FBF7F0" {s}/>'
                f'<path d="M60 66 L76 78 L92 66" {s} fill="none"/>'
                f'<circle cx="89" cy="64" r="5" fill="{ORANGE}" stroke="{INK}" stroke-width="2"/>')
    if kind == "pen":
        return (f'<path d="M88 8 L66 38 L62 44 L68 40 L90 10 Z" fill="{MUSTARD}" {s}/>'
                f'<path d="M62 44 L66 38" {s}/><path d="M84 14 L72 31" {hi}/>')
    if kind == "binoculars":
        return (f'<path d="M30 41 H66" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
                f'<rect x="24" y="40" width="20" height="18" rx="7" fill="#3A3330" {s}/><rect x="52" y="40" width="20" height="18" rx="7" fill="#3A3330" {s}/>'
                f'<circle cx="34" cy="50" r="5.5" fill="#9CC1E0"/><circle cx="62" cy="50" r="5.5" fill="#9CC1E0"/>'
                f'<circle cx="32.5" cy="48.5" r="1.8" fill="#FFFFFF"/><circle cx="60.5" cy="48.5" r="1.8" fill="#FFFFFF"/>')
    if kind == "briefcase":
        return (f'<rect x="62" y="68" width="30" height="20" rx="4" fill="{CLAY}" {s}/>'
                f'<path d="M71 68 V64 H83 V68 M62 76 H92" {s} fill="none"/><path d="M66 71 H74" {hi}/>')
    if kind == "books":
        return (f'<rect x="60" y="80" width="32" height="8" rx="2" fill="{BLUE}" {s}/>'
                f'<rect x="63" y="72" width="27" height="8" rx="2" fill="{ORANGE}" {s}/>'
                f'<rect x="61" y="64" width="29" height="8" rx="2" fill="{SAGE}" {s}/>')
    if kind == "sun":
        rays = "".join(f'<path d="M{78 + 14 * c:.1f} {18 + 14 * d:.1f} L{78 + 19 * c:.1f} {18 + 19 * d:.1f}" stroke="{MUSTARD}" stroke-width="3" stroke-linecap="round"/>'
                       for c, d in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)])
        return f'{rays}<circle cx="78" cy="18" r="10" fill="{MUSTARD}" {s}/><path d="M72 14 Q74 10 78 10" {hi}/>'
    if kind == "hardhat":
        return (f'<path d="M24 34 Q24 12 48 12 Q72 12 72 34 Z" fill="{MUSTARD}" {s}/>'
                f'<path d="M18 34 H78" stroke="{mix(MUSTARD, "#000000", .2)}" stroke-width="5" stroke-linecap="round"/>'
                f'<path d="M48 12 V30" {s}/><path d="M30 26 Q32 18 40 15" {hi}/>')
    if kind == "bubble":
        return (f'<path d="M64 8 H90 Q94 8 94 12 V26 Q94 30 90 30 H76 L70 36 V30 H64 Q60 30 60 26 V12 Q60 8 64 8 Z" fill="#FBF7F0" {s}/>'
                f'<circle cx="70" cy="19" r="2" fill="{LILAC}"/><circle cx="77" cy="19" r="2" fill="{LILAC}"/><circle cx="84" cy="19" r="2" fill="{LILAC}"/>')
    if kind == "gavel":
        return (f'<path d="M66 40 L86 20" stroke="{KRAFT}" stroke-width="5" stroke-linecap="round"/>'
                f'<rect x="76" y="4" width="12" height="24" rx="3" transform="rotate(45 82 16)" fill="{CLAY}" {s}/>'
                f'<path d="M58 46 H76" stroke="{mix(KRAFT, "#000000", .3)}" stroke-width="4" stroke-linecap="round"/>')
    return ""


# plugin, name, shape, color, eyes, mouth, accessory, model · effort
AGENTS = [
    ("crew", "planner", "square", BLUE, "focused", "flat", "clipboard", "opus · xhigh"),
    ("crew", "skeptic", "bean", ORANGE, "skeptic", "smirk", "question", "opus · xhigh"),
    ("crew", "web-coder", "round", SAGE, "dot", "smile", "code", "opus · high"),
    ("crew", "ui-builder", "drop", LILAC, "wide", "smile", "brush", "opus · high"),
    ("crew", "plugin-coder", "square", TEAL, "dot", "flat", "block", "opus · high"),
    ("crew", "tester", "pill", MUSTARD, "wide", "o", "tube", "sonnet · high"),
    ("crew", "reviewer", "round", CLAY, "glasses", "flat", "check", "opus · xhigh"),
    ("crew", "docs-writer", "ghost", CREAM, "sleepy", "smile", "book", "sonnet · medium"),
    ("office", "researcher", "round", BLUE, "wide", "o", "magnifier", "sonnet · medium"),
    ("office", "quote-builder", "square", KRAFT, "focused", "smile", "receipt", "opus · high"),
    ("office", "pricing-analyst", "pill", MUSTARD, "dot", "flat", "coin", "sonnet · medium"),
    ("office", "outreach-writer", "drop", ORANGE, "happy", "smile", "envelope", "opus · medium"),
    ("office", "copywriter", "bean", LILAC, "happy", "smirk", "pen", "opus · medium"),
    ("office", "lead-scout", "ghost", SAGE, "dot", "smile", "binoculars", "sonnet · medium"),
    ("office", "job-scout", "round", TEAL, "dot", "smile", "briefcase", "sonnet · medium"),
    ("office", "librarian", "square", CREAM, "glasses", "smile", "books", "sonnet · medium"),
    ("council", "optimist", "round", SAGE, "happy", "grin", "sun", "sonnet · medium"),
    ("council", "skeptic", "bean", CLAY, "skeptic", "smirk", "question", "opus · xhigh"),
    ("council", "engineer", "square", BLUE, "focused", "flat", "hardhat", "sonnet · medium"),
    ("council", "business", "pill", KRAFT, "focused", "smile", "coin", "sonnet · medium"),
    ("council", "client", "drop", LILAC, "dot", "flat", "bubble", "sonnet · medium"),
    ("council", "moderator", "ghost", CREAM, "glasses", "flat", "gavel", "opus · xhigh"),
    # New agents go last, so existing avatars keep their animation delays; the grid groups by plugin.
    ("crew", "coder", "pill", KRAFT, "focused", "smile", "code", "opus · high"),
]


def avatar_body(shape, color, eye, mth, acc, uid="a", delay=0.0) -> str:
    """One avatar in a 96 × 96 coordinate space. `uid` keeps gradient ids unique when many share a document."""
    u = f"{uid}-"
    d = shape_d = SHAPES[shape]
    anim = f'style="animation-delay:-{delay:.2f}s"'
    shadow = f'<ellipse class="av-shadow" {anim} cx="48" cy="90" rx="27" ry="4.5" fill="url(#{u}sh)"/>'
    body = (f'<path d="{d}" fill="url(#{u}b)"/>'
            f'<path d="{shape_d}" fill="url(#{u}ao)"/>'
            f'<path d="{shape_d}" fill="url(#{u}rim)"/>'
            f'<ellipse cx="34" cy="31" rx="11" ry="6" transform="rotate(-28 34 31)" fill="url(#{u}sp)" opacity=".75"/>'
            f'<circle cx="27" cy="40" r="2.2" fill="#FFFFFF" opacity=".55"/>')
    cheeks = f'<ellipse cx="27" cy="63" rx="7" ry="4.5" fill="url(#{u}ck)"/><ellipse cx="69" cy="63" rx="7" ry="4.5" fill="url(#{u}ck)"/>'
    eye_group = f'<g class="av-eyes" {anim.replace("animation-delay:-", "animation-delay:-1")}>{eyes(u, eye)}</g>'
    face = cheeks + eye_group + mouth(mth)
    over = acc in ("hardhat", "binoculars")
    acc_g = f'<g class="av-acc" filter="url(#{u}ds)" {anim}>{accessory(acc)}</g>'
    inner = body + (face + acc_g if over else acc_g + face)
    return defs(u, color) + shadow + f'<g class="av-bob" {anim}>{inner}</g>'


def write_avatars() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for i, (plugin, name, *style, _model) in enumerate(AGENTS):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96" role="img" '
               f'aria-label="{plugin}:{name}"><style>{CSS}</style>{avatar_body(*style, uid="a", delay=i * .37)}</svg>\n')
        (OUT / f"{plugin}-{name}.svg").write_text(svg)


def write_grid() -> None:
    cols, cell_w, cell_h = max(sum(a[0] == s for a in AGENTS) for s in ("crew", "office", "council")), 112, 158
    sections = [("crew", "crew  ·  dev"), ("office", "office  ·  business"), ("council", "council  ·  decisions")]
    W = 24 * 2 + cols * cell_w
    parts, y, n = [], 54, 0
    for key, label in sections:
        members = [a for a in AGENTS if a[0] == key]
        parts.append(f'<text x="24" y="{y}" class="sec">{label}</text>')
        y += 14
        for i, (plugin, name, *style, model) in enumerate(members):
            x = 24 + i * cell_w
            parts.append(f'<g transform="translate({x + 16} {y}) scale(0.83)">{avatar_body(*style, uid=f"g{n}", delay=n * .41)}</g>')
            parts.append(f'<text x="{x + cell_w / 2 - 8}" y="{y + 100}" class="name" text-anchor="middle">{name}</text>')
            parts.append(f'<text x="{x + cell_w / 2 - 8}" y="{y + 117}" class="model" text-anchor="middle">{model}</text>')
            n += 1
        y += cell_h
    H = y - 6
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="The {len(AGENTS)} agents of claude-crews">
<style>
text {{ font-family: "Styrene B", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; fill: #F5F4EE; }}
.sec {{ font-family: "Tiempos Headline", "Copernicus", Georgia, "Times New Roman", serif; font-size: 19px; }}
.name {{ font-size: 13px; font-weight: 600; }}
.model {{ font-size: 11px; fill: #A8A59B; }}
{CSS}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#262624"/>
{chr(10).join(parts)}
</svg>
'''
    (ROOT / "assets" / "the-crew.svg").write_text(svg)


if __name__ == "__main__":
    write_avatars()
    write_grid()
    print(f"{len(AGENTS)} avatars written")
