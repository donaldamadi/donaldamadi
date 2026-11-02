"""Generate the profile README's SVGs (light and dark) with Geist Serif embedded as a subset.

GitHub serves README images without access to web fonts, so each SVG carries
only the glyphs it uses, as a base64 woff2. Regenerate after editing any text:

    pip install fonttools brotli
    npm pack geist@1.9.0 && tar -xzf geist-1.9.0.tgz
    python3 scripts/make_svgs.py package/dist/fonts/geist-serif/GeistSerif-Regular.woff2 assets

Geist Serif is (c) Vercel, SIL Open Font License 1.1.
"""
import base64, io, sys
from fontTools.ttLib import TTFont
from fontTools import subset

FONT, OUT = sys.argv[1], sys.argv[2]
_full = TTFont(FONT)
_cmap = _full.getBestCmap()
_hmtx = _full["hmtx"]
_upm = _full["head"].unitsPerEm

def width(text, size):
    return sum(_hmtx[_cmap.get(ord(ch), _cmap[ord("?")])][0] for ch in text) * size / _upm

def font_face(texts):
    chars = set("".join(texts)) | set(" ")
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
    f = TTFont(FONT); s = subset.Subsetter(opts); s.populate(text="".join(sorted(chars))); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'GS';src:url(data:font/woff2;base64,{b64}) format('woff2');}}"

THEMES = {
    "light": dict(bg="#fafafa", panel="#ffffff", tray="#f4f4f5", line="#e5e5e5", line2="#d4d4d4",
                  ink="#0a0a0a", dim="#525252", faint="#6b6b6b", accent="#2563eb", green="#047857", greensoft="#04785714"),
    "dark": dict(bg="#0a0a0a", panel="#161616", tray="#1f1f1f", line="#2a2a2a", line2="#3a3a3a",
                 ink="#fafafa", dim="#b4b4b4", faint="#8f8f8f", accent="#60a5fa", green="#34d399", greensoft="#34d3991f"),
}

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text(x, y, size, fill, t, anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(t)}</text>'

# ---------------------------------------------------------------- hero
HERO_LINES = ["I build mobile and web products,", "from the first screen to the", "server behind it."]
HERO_NAME = "Donald Amadi"
HERO_SUB = "Product engineer in Lagos. React Native, React, Flutter, TypeScript, Node.js."
HERO_ROWS = ["Spaces", "Owambe at Ikoyi", "Lekki market run", "Campus tour", "Sunday service", "Finding Tolu", "24", "m", "warmer", "admin / spaces", "DA"]

def hero(c, ff):
    W, H = 900, 300
    size = 34
    longest = max(width(l, size) for l in HERO_LINES)
    assert longest < 520, longest
    sub_w = width(HERO_SUB, 15); assert sub_w < 560, sub_w
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Donald Amadi. I build mobile and web products, from the first screen to the server behind it. {HERO_SUB}">',
         f"<style>{ff} text{{font-family:'GS','Times New Roman',serif;}}</style>",
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>']
    # name
    s.append(f'<rect x="40" y="34" width="28" height="28" rx="7" fill="{c["ink"]}"/>')
    s.append(text(54, 53, 13, c["bg"], "DA", "middle"))
    s.append(text(78, 54, 17, c["ink"], HERO_NAME))
    for i, l in enumerate(HERO_LINES):
        s.append(text(40, 112 + i * 40, size, c["ink"], l, extra='letter-spacing="-0.3"'))
    s.append(text(40, 254, 15, c["dim"], HERO_SUB))
    # art: browser window + phone, right side
    bx, by, bw, bh = 600, 60, 260, 168
    s.append(f'<rect x="{bx-6}" y="{by-6}" width="{bw+12}" height="{bh+12}" rx="16" fill="{c["tray"]}"/>')
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="11" fill="{c["panel"]}" stroke="{c["line"]}"/>')
    for k in range(3):
        s.append(f'<circle cx="{bx+14+k*10}" cy="{by+14}" r="3" fill="{c["line2"]}"/>')
    s.append(f'<rect x="{bx+50}" y="{by+7}" width="{width("admin / spaces",10)+14:.1f}" height="15" rx="4" fill="{c["tray"]}"/>')
    s.append(text(bx+57, by+18, 10, c["faint"], "admin / spaces"))
    s.append(f'<line x1="{bx}" y1="{by+28}" x2="{bx+bw}" y2="{by+28}" stroke="{c["line"]}"/>')
    s.append(text(bx+14, by+48, 12, c["ink"], "Spaces"))
    for i, r in enumerate(HERO_ROWS[1:5]):
        y = by + 70 + i * 24
        s.append(f'<line x1="{bx+14}" y1="{y-15}" x2="{bx+bw-14}" y2="{y-15}" stroke="{c["line"]}"/>')
        s.append(text(bx+14, y, 11, c["dim"], r))
    # phone in front
    px, py, pw, ph = 770, 120, 100, 160
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="20" fill="{c["panel"]}" stroke="{c["line2"]}"/>')
    s.append(f'<rect x="{px+6}" y="{py+6}" width="{pw-12}" height="{ph-12}" rx="15" fill="{c["tray"]}"/>')
    s.append(f'<rect x="{px+38}" y="{py+12}" width="24" height="3" rx="1.5" fill="{c["line2"]}"/>')
    s.append(text(px+pw/2, py+32, 9, c["faint"], "Finding Tolu", "middle"))
    cx, cy = px + pw/2, py + 72
    s.append(f'<circle cx="{cx}" cy="{cy}" r="28" fill="{c["panel"]}" stroke="{c["line2"]}"/>')
    s.append(f'<path transform="translate({cx} {cy}) rotate(38) scale(0.36)" d="M0 -50 L24 4 L7 -3 L7 44 L-7 44 L-7 -3 L-24 4 Z" fill="{c["green"]}"/>')
    s.append(text(cx, py+128, 18, c["ink"], "24", "middle"))
    s.append(text(cx, py+144, 10, c["green"], "warmer", "middle"))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- PinDey card
PD_STATUS = "Live in production"
PD_NAME = "PinDey"
PD_ONE = "Find your friends in a crowd, phone to phone."
PD_TAG = "“Where you dey? We go find you.”"
PD_SURF = ["Flutter app", "Next.js website", "Next.js back office", "NestJS API"]
PD_STEPS = [("42 m", "keep walking"), ("11 m", "warmer"), ("2 m", "very close, look around")]
PD_URL = "pindey.app"

def pindey(c, ff):
    W, H = 900, 280
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="PinDey, live in production at pindey.app. {PD_ONE} Where you dey? We go find you. Built end to end: a Flutter app, a Next.js website and back office, and a NestJS API.">',
         f"""<style>{ff} text{{font-family:'GS','Times New Roman',serif;}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s infinite ease-out}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.6}}100%{{transform:scale(2.8);opacity:0}}}}
.arrow{{transform-box:view-box;transform-origin:735px 120px;animation:hunt 9s infinite ease-in-out}}
@keyframes hunt{{0%{{transform:rotate(-70deg)}}12%{{transform:rotate(35deg)}}24%{{transform:rotate(-20deg)}}36%{{transform:rotate(12deg)}}50%,62%{{transform:rotate(0deg);opacity:1}}68%,100%{{transform:rotate(0deg);opacity:0}}}}
.near{{opacity:0;animation:near 9s infinite}}
@keyframes near{{0%,64%{{opacity:0}}70%,96%{{opacity:1}}100%{{opacity:0}}}}
.d{{opacity:0;animation:step 9s infinite both}}.d2{{animation-delay:3s}}.d3{{animation-delay:6s}}
@keyframes step{{0%{{opacity:0}}4%,30%{{opacity:1}}33%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.pulse,.arrow,.near{{animation:none}}.d{{animation:none}}.d1{{opacity:1}}}}
</style>""",
         f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>',
         f'<rect x="20" y="20" width="{W-40}" height="{H-40}" rx="12" fill="{c["panel"]}" stroke="{c["line"]}"/>']
    s.append(f'<circle class="pulse" cx="52" cy="56" r="4" fill="{c["green"]}"/><circle cx="52" cy="56" r="4" fill="{c["green"]}"/>')
    s.append(text(64, 60, 13, c["green"], PD_STATUS))
    s.append(text(44, 118, 46, c["ink"], PD_NAME, extra='letter-spacing="-0.5"'))
    s.append(text(46, 150, 17, c["ink"], PD_ONE))
    s.append(text(46, 176, 15, c["green"], PD_TAG))
    x = 46
    for label in PD_SURF:
        w = width(label, 12) + 18
        s.append(f'<rect x="{x:.1f}" y="200" width="{w:.1f}" height="24" rx="6" fill="{c["tray"]}"/>')
        s.append(text(x + 9, 216, 12, c["dim"], label))
        x += w + 8
    assert x < 600, x
    s.append(text(560, 60, 13, c["faint"], PD_URL))
    # The Finder
    cx, cy = 735, 120
    s.append(f'<circle cx="{cx}" cy="{cy}" r="72" fill="{c["bg"]}" stroke="{c["line2"]}"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="48" fill="none" stroke="{c["line"]}"/>')
    s.append(f'<g class="arrow"><path transform="translate({cx} {cy}) scale(0.95)" d="M0 -50 L24 4 L7 -3 L7 44 L-7 44 L-7 -3 L-24 4 Z" fill="{c["green"]}"/></g>')
    s.append(f'<g class="near"><circle cx="{cx}" cy="{cy}" r="10" fill="{c["green"]}"/><circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{c["green"]}" stroke-opacity=".5"/></g>')
    for i, (d, label) in enumerate(PD_STEPS, start=1):
        fill = c["green"] if i > 1 else c["dim"]
        s.append(f'<g class="d d{i}">{text(cx, 222, 15, c["ink"], d, "middle")}{text(cx, 242, 13, fill, label, "middle")}</g>')
    s.append("</svg>")
    return "\n".join(s)

used = HERO_LINES + [HERO_NAME, HERO_SUB, "DA"] + HERO_ROWS + [PD_STATUS, PD_NAME, PD_ONE, PD_TAG, PD_URL] + PD_SURF + [a + b for a, b in PD_STEPS]
ff = font_face(used)
for theme, c in THEMES.items():
    for name, fn in (("hero", hero), ("pindey", pindey)):
        svg = fn(c, ff)
        open(f"{OUT}/{name}-{theme}.svg", "w").write(svg)
        print(name, theme, len(svg), "bytes")
