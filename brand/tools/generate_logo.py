#!/usr/bin/env python3
"""Katus Ranch — Angus Seedstock logo system.

Everything ships from this one file: the bull-head geometry, the palette, the
lockup metrics, and the wordmark itself. Wordmark text is converted to outlines
from the fonts in brand/fonts/ at build time, so the published SVGs carry no
font dependency and render identically everywhere.

    pip install fonttools brotli cairosvg
    python3 brand/tools/generate_logo.py

Letterforms follow the hand-painted trailer sign: a Western slab with spurred
serifs, white letters carrying a colored outline on a black plate.
"""

import os

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
FONTS = os.path.join(BRAND, "fonts")
OUT = os.path.join(BRAND, "logo")

# ---------------------------------------------------------------- palette ---
BLUE   = "#1A3EAF"   # Royal Blue — the one saturated color
BLUE_D = "#122C7C"   # Deep Royal
SKY    = "#8FA6F0"   # Sky Royal, dark grounds only
BLACK  = "#0B0B0D"   # Angus Black
GREY   = "#8B9199"   # Ranch Grey
GREY_L = "#D9DCE1"   # Fence Grey
PAPER  = "#F4F5F7"   # Paper
WHITE  = "#FFFFFF"

DISPLAY = os.path.join(FONTS, "rye.woff2")          # Rye — Western slab
SCRIPT  = os.path.join(FONTS, "yellowtail.woff2")   # Yellowtail — sign script
GOTHIC  = os.path.join(FONTS, "oswald-600.ttf")     # Oswald 600 — condensed gothic

# ------------------------------------------------------------ type as art ---
_fonts = {}


def _font(path):
    if path not in _fonts:
        _fonts[path] = TTFont(path)
    return _fonts[path]


def glyphs(fp, text, size, tracking=0.0):
    """[(path_d, advance)] for each character, drawn on a baseline at y=0."""
    f = _font(fp)
    scale = size / f["head"].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    out = []
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            out.append(("", size * 0.3 + tracking))
            continue
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        gs[name].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, 0, 0)))
        out.append((pen.getCommands(), hmtx[name][0] * scale + tracking))
    return out


def text_path(fp, text, size, tracking=0.0):
    """(path_d, width) for a straight line of text starting at x=0, baseline y=0."""
    d, x = [], 0.0
    for seg, adv in glyphs(fp, text, size, tracking):
        if seg:
            d.append(f'<path d="{seg}" transform="translate({x:.2f},0)"/>')
        x += adv
    return "".join(d), x - tracking


def text_width(fp, text, size, tracking=0.0):
    return text_path(fp, text, size, tracking)[1]


def cap_height(fp, size):
    f = _font(fp)
    scale = size / f["head"].unitsPerEm
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord("K")]
    from fontTools.pens.boundsPen import BoundsPen
    bp = BoundsPen(gs)
    gs[name].draw(bp)
    return (bp.bounds[3] - bp.bounds[1]) * scale


def fit_tracking(fp, text, size, target_w):
    """Tracking that stretches `text` to exactly target_w."""
    base = text_width(fp, text, size, 0)
    gaps = max(1, len(text) - 1)
    return (target_w - base) / gaps


def arc_text(fp, text, size, cx, cy, r, tracking=0.0):
    """Text centred on the top of a circle, glyphs standing off radius r."""
    gl = glyphs(fp, text, size, tracking)
    total = sum(a for _, a in gl) - tracking
    x, parts = -total / 2, []
    for seg, adv in gl:
        if seg:
            mid = x + (adv - tracking) / 2
            deg = mid / r * 180 / 3.141592653589793
            parts.append(
                f'<g transform="translate({cx},{cy}) rotate({deg:.3f}) '
                f'translate({-(adv - tracking) / 2:.2f},{-r})">'
                f'<path d="{seg}"/></g>'
            )
        x += adv
    return "".join(parts)


def outlined(inner, fill, outline, width):
    """Sign painter's outline: the same shapes struck wide underneath, then filled.

    This is the trailer-sign treatment — white letters carrying a colored keyline.
    It only works on a dark ground; on paper use `shadowed`.
    """
    return (f'<g fill="{outline}" stroke="{outline}" stroke-width="{width:.2f}" '
            f'stroke-linejoin="round">{inner}</g>'
            f'<g fill="{fill}">{inner}</g>')


def signwriting(inner, dark_ground, size):
    """Pick the right two-color treatment for the ground.

    Dark: white letters, royal keyline — the trailer sign exactly.
    Light: royal letters, black keyline — the same two colors, swapped so the
    fill still dominates and Rye's spurs stay crisp on paper.
    """
    if dark_ground:
        return outlined(inner, WHITE, BLUE, size * 0.085)
    return outlined(inner, BLUE, BLACK, size * 0.07)


# ------------------------------------------------------------------- bull ---
def bull(fill=BLACK, detail=BLUE):
    """Polled (hornless) Angus bull head, drawn in a 200x200 box."""
    return f'''<g fill="{fill}">
      <path d="M141 74 C 157 71 170 79 177 95 C 168 105 152 104 143 97 Z"/>
      <path d="M59 74 C 43 71 30 79 23 95 C 32 105 48 104 57 97 Z"/>
      <path d="M100 36 C 123 36 141 46 147 63 C 151 78 150 92 146 104 C 143 114 138 121 133 127
               C 132 145 120 161 100 161 C 80 161 68 145 67 127 C 62 121 57 114 54 104
               C 50 92 49 78 53 63 C 59 46 77 36 100 36 Z"/>
    </g>
    <g fill="{detail}">
      <path d="M69 92 C 76 86 87 87 91 94 C 84 99 73 99 69 92 Z"/>
      <path d="M131 92 C 124 86 113 87 109 94 C 116 99 127 99 131 92 Z"/>
      <ellipse cx="91" cy="137" rx="5" ry="3.2" transform="rotate(-20 91 137)"/>
      <ellipse cx="109" cy="137" rx="5" ry="3.2" transform="rotate(20 109 137)"/>
    </g>'''


def roundel(cx, cy, r, ring=BLUE, field=PAPER, hairline=GREY, head=BLACK, detail=BLUE):
    s = (r * 0.88) / 100.0
    return f'''<g>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{ring}"/>
    <circle cx="{cx}" cy="{cy}" r="{r * 0.885:.1f}" fill="{field}"/>
    <circle cx="{cx}" cy="{cy}" r="{r * 0.80:.1f}" fill="none" stroke="{hairline}"
      stroke-width="{r * 0.018:.2f}"/>
    <g transform="translate({cx - 100 * s:.2f},{cy - 100 * s:.2f}) scale({s:.4f})">
      {bull(head, detail)}</g></g>'''


# --------------------------------------------------------- livestock brands ---
def brand_x7(cx, cy, h, fill=WHITE):
    """The X7 iron, as it sits on the trailer sign: X over 7."""
    x_d, xw = text_path(DISPLAY, "X", h * 0.58)
    s_d, sw = text_path(DISPLAY, "7", h * 0.52)
    return (f'<g fill="{fill}">'
            f'<g transform="translate({cx - xw / 2:.1f},{cy - h * 0.04:.1f})">{x_d}</g>'
            f'<g transform="translate({cx - sw / 2:.1f},{cy + h * 0.46:.1f})">{s_d}</g>'
            f'</g>')


def brand_bar7(cx, cy, h, fill=WHITE):
    """The bar-7 iron: a seven under a full bar."""
    s_d, sw = text_path(DISPLAY, "7", h * 0.62)
    bar_w = sw * 1.5
    return (f'<g fill="{fill}">'
            f'<rect x="{cx - bar_w / 2:.1f}" y="{cy - h * 0.34:.1f}" width="{bar_w:.1f}"'
            f' height="{h * 0.16:.1f}"/>'
            f'<g transform="translate({cx - sw / 2:.1f},{cy + h * 0.40:.1f})">{s_d}</g>'
            f'</g>')


# ------------------------------------------------------------------- shell ---
def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" '
            f'aria-label="Katus Ranch, Angus Seedstock">\n{rect}\n{body}\n</svg>\n')


def wordmark(x, baseline, size, dark_ground, anchor="start", one_line=True):
    """KATUS RANCH over a rule over ANGUS SEEDSTOCK. Returns (markup, width, bottom)."""
    sub_fill = SKY if dark_ground else BLUE
    rule_fill = GREY

    name_d, name_w = text_path(DISPLAY, "KATUS RANCH" if one_line else "KATUS", size, size * 0.02)
    x0 = x if anchor == "start" else x - name_w / 2

    sub_size = size * 0.32
    track = fit_tracking(GOTHIC, "ANGUS SEEDSTOCK", sub_size, name_w)
    sub_d, _ = text_path(GOTHIC, "ANGUS SEEDSTOCK", sub_size, track)
    sub_cap = cap_height(GOTHIC, sub_size)

    rule_y = baseline + size * 0.30
    rule_h = max(3, size * 0.045)
    sub_base = rule_y + rule_h + size * 0.20 + sub_cap

    inner = f'<g transform="translate({x0:.1f},{baseline:.1f})">{name_d}</g>'
    body = (signwriting(inner, dark_ground, size)
            + f'<rect x="{x0:.1f}" y="{rule_y:.1f}" width="{name_w:.1f}" '
              f'height="{rule_h:.1f}" fill="{rule_fill}"/>'
            + f'<g fill="{sub_fill}" transform="translate({x0:.1f},{sub_base:.1f})">{sub_d}</g>')
    return body, name_w, sub_base


def script_line(text, cx, baseline, size, fill):
    d, w = text_path(SCRIPT, text, size)
    return f'<g fill="{fill}" transform="translate({cx - w / 2:.1f},{baseline:.1f})">{d}</g>', w


files = {}

# ----------------------------------------------------- the sign (hero) ------
def sign():
    W, H = 1120, 780
    cx = W / 2
    k_size = 172
    k_d, k_w = text_path(DISPLAY, "KATUS", k_size, k_size * 0.02)
    # RANCH is set to KATUS's measured width so the two lines read as one slab
    r_size = k_size * k_w / text_width(DISPLAY, "RANCH", k_size, k_size * 0.02)
    r_d, r_w = text_path(DISPLAY, "RANCH", r_size, r_size * 0.02)
    k_base, r_base = 356, 356 + k_size * 1.13

    inner = (f'<g transform="translate({cx - k_w / 2:.1f},{k_base})">{k_d}</g>'
             f'<g transform="translate({cx - r_w / 2:.1f},{r_base:.1f})">{r_d}</g>')

    sub_size = 48
    track = fit_tracking(GOTHIC, "ANGUS SEEDSTOCK", sub_size, k_w * 0.64)
    sub_d, sub_w = text_path(GOTHIC, "ANGUS SEEDSTOCK", sub_size, track)
    scr, _ = script_line("Watauga, South Dakota", cx, 716, 46, GREY_L)

    body = f'''<rect width="{W}" height="{H}" fill="{BLACK}"/>
  <rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{BLUE}" stroke-width="7"/>
  <rect x="32" y="32" width="{W - 64}" height="{H - 64}" fill="none" stroke="{GREY}" stroke-width="1.5"/>
  <g transform="translate({cx - 100:.1f},30)">{bull(WHITE, BLUE)}</g>
  {brand_x7(118, 430, 150)}
  {brand_bar7(W - 118, 430, 150)}
  {outlined(inner, WHITE, BLUE, 15)}
  <rect x="{cx - k_w / 2:.1f}" y="608" width="{k_w:.1f}" height="3" fill="{GREY}"/>
  <g fill="{WHITE}" transform="translate({cx - sub_w / 2:.1f},668)">{sub_d}</g>
  {scr}'''
    return svg(W, H, body)


files["logo-sign.svg"] = sign()

# ---------------------------------------------------------- horizontal ------
def primary(reverse=False):
    size = 96
    mark = roundel(160, 160, 128, ring=BLUE,
                   field=(BLACK if reverse else PAPER),
                   hairline=(BLUE_D if reverse else GREY),
                   head=(WHITE if reverse else BLACK))
    wm, w, bottom = wordmark(352, 160, size, reverse)
    W = 352 + w + 40
    return svg(round(W), 320, mark + "\n" + wm, bg=(BLACK if reverse else None))


files["logo-primary.svg"] = primary(False)
files["logo-primary-reverse.svg"] = primary(True)

# ------------------------------------------------------------- stacked ------
def stacked(reverse=False):
    size = 104
    name_w = text_width(DISPLAY, "KATUS RANCH", size, size * 0.02)
    W = round(name_w + 120)
    cx = W / 2
    mark = roundel(cx, 190, 138, ring=BLUE,
                   field=(BLACK if reverse else PAPER),
                   hairline=(BLUE_D if reverse else GREY),
                   head=(WHITE if reverse else BLACK))
    wm, w, bottom = wordmark(cx, 430, size, reverse, anchor="middle")
    scr, _ = script_line("Watauga, South Dakota", cx, bottom + 74,
                         46, GREY if not reverse else GREY_L)
    return svg(W, round(bottom + 110), mark + "\n" + wm + "\n" + scr,
               bg=(BLACK if reverse else None))


files["logo-stacked.svg"] = stacked(False)
files["logo-stacked-reverse.svg"] = stacked(True)

# --------------------------------------------------------------- badge ------
def badge():
    cx = cy = 300
    arc = arc_text(DISPLAY, "KATUS RANCH", 62, cx, cy, 214, 3)
    sub_size = 32
    track = fit_tracking(GOTHIC, "ANGUS SEEDSTOCK", sub_size, 300)
    sub_d, sub_w = text_path(GOTHIC, "ANGUS SEEDSTOCK", sub_size, track)
    scr, _ = script_line("Watauga, SD", cx, cy + 176, 34, GREY_L)
    ban_y, ban_h = cy + 76, 58
    body = f'''<circle cx="{cx}" cy="{cy}" r="292" fill="{BLACK}"/>
  <circle cx="{cx}" cy="{cy}" r="283" fill="{BLUE}"/>
  <circle cx="{cx}" cy="{cy}" r="218" fill="{BLACK}"/>
  <circle cx="{cx}" cy="{cy}" r="208" fill="none" stroke="{GREY}" stroke-width="3"/>
  {outlined(arc, WHITE, BLUE_D, 9)}
  <g transform="translate({cx - 100 * 1.08:.1f},{cy - 172:.1f}) scale(1.08)">{bull(WHITE, BLUE)}</g>
  {brand_x7(cx - 150, cy - 44, 60, WHITE)}
  {brand_bar7(cx + 150, cy - 44, 60, WHITE)}
  <rect x="{cx - sub_w / 2 - 30:.1f}" y="{ban_y}" width="{sub_w + 60:.1f}" height="{ban_h}"
    fill="{BLUE}" stroke="{WHITE}" stroke-width="2"/>
  <g fill="{WHITE}" transform="translate({cx - sub_w / 2:.1f},{ban_y + 39})">{sub_d}</g>
  {scr}'''
    return svg(600, 600, body)


files["logo-badge.svg"] = badge()

# ---------------------------------------------------------------- marks -----
files["logo-mark.svg"] = svg(300, 300, roundel(150, 150, 146))
files["logo-mark-reverse.svg"] = svg(
    300, 300, roundel(150, 150, 146, field=BLACK, hairline=BLUE_D, head=WHITE), bg=BLACK)


def mono(ink):
    s = 146 * 0.88 / 100
    body = f'''<circle cx="150" cy="150" r="146" fill="none" stroke="{ink}" stroke-width="16"/>
  <circle cx="150" cy="150" r="117" fill="none" stroke="{ink}" stroke-width="3"/>
  <g transform="translate({150 - 100 * s:.2f},{150 - 100 * s:.2f}) scale({s:.4f})">
    {bull(ink, "none")}</g>'''
    return svg(300, 300, body)


files["logo-mark-mono-black.svg"] = mono(BLACK)
files["logo-mark-mono-white.svg"] = mono(WHITE)

# --------------------------------------------------------------- brands -----
files["brand-x7.svg"] = svg(200, 200, brand_x7(100, 100, 150, BLACK))
files["brand-bar7.svg"] = svg(200, 200, brand_bar7(100, 100, 150, BLACK))

# ------------------------------------------------------------- app icon -----
def app_icon(dark=False):
    # The head alone: at 32 px a wordmark turns to mush, and the silhouette is
    # what people recognise in a home-screen grid anyway.
    bg   = BLACK if dark else PAPER
    head = WHITE if dark else BLACK
    s = 2.25
    body = f'''<rect width="512" height="512" rx="112" fill="{bg}"/>
  <rect x="16" y="16" width="480" height="480" rx="98" fill="none" stroke="{BLUE}" stroke-width="22"/>
  <g transform="translate({256 - 100 * s:.1f},{256 - 98.5 * s:.1f}) scale({s})">{bull(head, BLUE)}</g>'''
    return svg(512, 512, body)


files["app-icon.svg"] = app_icon(False)
files["app-icon-dark.svg"] = app_icon(True)

# ------------------------------------------------------------------ write ---
os.makedirs(OUT, exist_ok=True)
for name, content in files.items():
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content)

PNGS = {
    "logo-sign.svg": [("logo-sign.png", 1680)],
    "logo-primary.svg": [("logo-primary.png", 2000)],
    "logo-primary-reverse.svg": [("logo-primary-reverse.png", 2000)],
    "logo-stacked.svg": [("logo-stacked.png", 1200)],
    "logo-stacked-reverse.svg": [("logo-stacked-reverse.png", 1200)],
    "logo-badge.svg": [("logo-badge.png", 1200)],
    "logo-mark.svg": [("logo-mark.png", 600)],
    "logo-mark-mono-black.svg": [("logo-mark-mono-black.png", 600)],
    "app-icon.svg": [("app-icon-1024.png", 1024), ("app-icon-512.png", 512),
                     ("favicon-64.png", 64)],
    "app-icon-dark.svg": [("app-icon-dark-1024.png", 1024), ("app-icon-dark-512.png", 512)],
}

if __name__ == "__main__":
    import cairosvg
    for src, outs in PNGS.items():
        for name, width in outs:
            cairosvg.svg2png(url=os.path.join(OUT, src),
                             write_to=os.path.join(OUT, name), output_width=width)
    print("\n".join(sorted(os.listdir(OUT))))
