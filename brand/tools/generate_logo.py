import os, cairosvg

OUT = "/home/user/Beutler-cattle-mobile/brand/logo"
os.makedirs(OUT, exist_ok=True)

BLUE   = "#1A3EAF"
BLUE_D = "#122C7C"
BLACK  = "#0B0B0D"
GREY   = "#8B9199"
GREY_L = "#D9DCE1"
PAPER  = "#F4F5F7"

SERIF = "Georgia, 'Times New Roman', 'Liberation Serif', serif"
SANS  = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"

def bull(fill=BLACK, detail=BLUE):
    """Polled Angus bull head, drawn in a 200x200 box."""
    return f'''<g>
    <g fill="{fill}">
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
    </g></g>'''

def roundel(cx, cy, r, ring=BLUE, field=PAPER, hairline=GREY, head=BLACK, detail=BLUE):
    s = (r * 0.88) / 100.0
    return f'''<g>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{ring}"/>
    <circle cx="{cx}" cy="{cy}" r="{r*0.885:.1f}" fill="{field}"/>
    <circle cx="{cx}" cy="{cy}" r="{r*0.80:.1f}" fill="none" stroke="{hairline}" stroke-width="{r*0.018:.2f}"/>
    <g transform="translate({cx - 100*s:.2f},{cy - 100*s:.2f}) scale({s:.4f})">{bull(head, detail)}</g></g>'''

def svg(vb_w, vb_h, body, bg=None):
    rect = f'<rect width="{vb_w}" height="{vb_h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
            f'width="{vb_w}" height="{vb_h}" role="img" '
            f'aria-label="Katus Ranch, Angus Seedstock">\n{rect}\n{body}\n</svg>\n')

# Metrics measured from the rendered wordmark, so the two lines justify to the
# same width and the rule always matches the name.
NAME_W_PER_PT = 8.82      # "KATUS RANCH", serif 700, tracking 0.03em
SUB_W_PER_PT  = 11.01     # "ANGUS SEEDSTOCK", sans 600, tracking 0
SUB_GAPS      = 14.0      # letter gaps that absolute tracking is added to

def name_width(size):
    return NAME_W_PER_PT * size

def wordmark(x, y, anchor="start", name_fill=BLACK, rule_fill=GREY, sub_fill=BLUE, size=78):
    w = name_width(size)
    sub = size * 0.56
    track = (w - SUB_W_PER_PT * sub) / SUB_GAPS
    x0 = x if anchor == "start" else x - w / 2
    # letter-spacing adds a trailing gap, so nudge a centred subline back by half of it
    dx = 0 if anchor == "start" else -track / 2
    return f'''<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{SERIF}" font-size="{size}"
      font-weight="700" letter-spacing="{size*0.03:.2f}" fill="{name_fill}">KATUS RANCH</text>
    <rect x="{x0:.1f}" y="{y + size*0.31:.1f}" width="{w:.1f}" height="{max(2.5,size*0.045):.1f}" fill="{rule_fill}"/>
    <text x="{x+dx:.1f}" y="{y + size*0.95:.1f}" text-anchor="{anchor}" font-family="{SANS}" font-size="{sub:.1f}"
      font-weight="600" letter-spacing="{track:.2f}" fill="{sub_fill}">ANGUS SEEDSTOCK</text>'''

files = {}

# ---- primary horizontal -------------------------------------------------
def primary(reverse=False):
    name = "#FFFFFF" if reverse else BLACK
    sub  = "#8FA6F0" if reverse else BLUE
    rule = GREY if not reverse else GREY
    mark = roundel(150, 150, 122,
                   ring=BLUE,
                   field=(PAPER if not reverse else PAPER),
                   hairline=GREY, head=BLACK, detail=BLUE)
    body = mark + "\n" + wordmark(330, 140, name_fill=name, rule_fill=rule, sub_fill=sub, size=78)
    return svg(1060, 300, body, bg=(BLACK if reverse else None))

files["logo-primary.svg"] = primary(False)
files["logo-primary-reverse.svg"] = primary(True)

# ---- stacked ------------------------------------------------------------
def stacked(reverse=False):
    name = "#FFFFFF" if reverse else BLACK
    sub  = "#8FA6F0" if reverse else BLUE
    mark = roundel(380, 190, 138, ring=BLUE)
    body = mark + "\n" + wordmark(380, 424, anchor="middle", name_fill=name,
                                  rule_fill=GREY, sub_fill=sub, size=72)
    return svg(760, 560, body, bg=(BLACK if reverse else None))

files["logo-stacked.svg"] = stacked(False)
files["logo-stacked-reverse.svg"] = stacked(True)

# ---- badge / crest ------------------------------------------------------
def badge():
    cx = cy = 260
    body = f'''<circle cx="{cx}" cy="{cy}" r="252" fill="{BLACK}"/>
  <circle cx="{cx}" cy="{cy}" r="244" fill="{BLUE}"/>
  <circle cx="{cx}" cy="{cy}" r="192" fill="{PAPER}"/>
  <circle cx="{cx}" cy="{cy}" r="182" fill="none" stroke="{GREY}" stroke-width="3"/>
  <g transform="translate({cx-128},{cy-142}) scale(1.28)">{bull()}</g>
  <path id="arcTop" d="M {cx-216} {cy} a 216 216 0 0 1 432 0" fill="none"/>
  <path id="arcBottom" d="M {cx-216} {cy} a 216 216 0 0 0 432 0" fill="none"/>
  <text font-family="{SERIF}" font-size="44" font-weight="700" letter-spacing="4" fill="#FFFFFF">
    <textPath href="#arcTop" startOffset="50%" text-anchor="middle">KATUS RANCH</textPath></text>
  <text font-family="{SANS}" font-size="26" font-weight="600" letter-spacing="7" fill="#FFFFFF">
    <textPath href="#arcBottom" startOffset="50%" text-anchor="middle">ANGUS SEEDSTOCK</textPath></text>
  <g fill="#FFFFFF">
    <rect x="{cx-235}" y="{cy-9}" width="13" height="13" transform="rotate(45 {cx-228.5} {cy-2.5})"/>
    <rect x="{cx+222}" y="{cy-9}" width="13" height="13" transform="rotate(45 {cx+228.5} {cy-2.5})"/>
  </g>'''
    return svg(520, 520, body)

files["logo-badge.svg"] = badge()

# ---- mark only ----------------------------------------------------------
files["logo-mark.svg"] = svg(300, 300, roundel(150, 150, 146))

# ---- monochrome ---------------------------------------------------------
def mono(ink):
    field = "none"
    s = 146 * 0.88 / 100
    body = f'''<circle cx="150" cy="150" r="146" fill="none" stroke="{ink}" stroke-width="16"/>
  <circle cx="150" cy="150" r="117" fill="none" stroke="{ink}" stroke-width="3"/>
  <g transform="translate({150-100*s:.2f},{150-100*s:.2f}) scale({s:.4f})">{bull(ink, "none")}</g>'''
    return svg(300, 300, body)

files["logo-mark-mono-black.svg"] = mono(BLACK)
files["logo-mark-mono-white.svg"] = mono("#FFFFFF")

# ---- app icon -----------------------------------------------------------
def app_icon(dark=False):
    bg   = BLACK if dark else PAPER
    head = "#FFFFFF" if dark else BLACK
    body = f'''<rect width="512" height="512" rx="112" fill="{bg}"/>
  <rect x="16" y="16" width="480" height="480" rx="98" fill="none" stroke="{BLUE}" stroke-width="22"/>
  <g transform="translate(61,23) scale(1.95)">{bull(head, BLUE)}</g>
  <rect x="196" y="372" width="120" height="5" fill="{GREY}"/>
  <text x="256" y="438" text-anchor="middle" font-family="{SANS}" font-size="46" font-weight="700"
    letter-spacing="7" dx="-3.5" fill="{BLUE if not dark else '#8FA6F0'}">KATUS</text>'''
    return svg(512, 512, body)

files["app-icon.svg"] = app_icon(False)
files["app-icon-dark.svg"] = app_icon(True)

for n, s in files.items():
    with open(os.path.join(OUT, n), "w") as f:
        f.write(s)

png = {
    "logo-primary.svg": [("logo-primary.png", 2000)],
    "logo-stacked.svg": [("logo-stacked.png", 1200)],
    "logo-badge.svg": [("logo-badge.png", 1040)],
    "logo-mark.svg": [("logo-mark.png", 600)],
    "app-icon.svg": [("app-icon-1024.png", 1024), ("app-icon-512.png", 512), ("favicon-64.png", 64)],
    "app-icon-dark.svg": [("app-icon-dark-1024.png", 1024), ("app-icon-dark-512.png", 512)],
    "logo-primary-reverse.svg": [("logo-primary-reverse.png", 2000)],
    "logo-stacked-reverse.svg": [("logo-stacked-reverse.png", 1200)],
    "logo-mark-mono-black.svg": [("logo-mark-mono-black.png", 600)],
}
for src, outs in png.items():
    for name, w in outs:
        cairosvg.svg2png(url=os.path.join(OUT, src), write_to=os.path.join(OUT, name), output_width=w)
print("\n".join(sorted(os.listdir(OUT))))
