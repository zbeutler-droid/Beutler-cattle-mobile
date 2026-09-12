# Katus Ranch — Angus Seedstock

Brand mark and logo system, drawn from the hand-painted sign on the ranch
trailer: a Western slab wordmark, white letters carrying a colored keyline on a
black plate, the two irons standing either side, and a script line for the
country. The teal of the original sign is replaced by royal blue.

The bull is drawn **polled** — no horns — which is how the breed reads to a
cattleman at a glance.

## Colors

| Role | Name | Hex | Notes |
| --- | --- | --- | --- |
| Primary | Royal Blue | `#1A3EAF` | Keyline, letters on paper, ring, banner |
| Primary (dark) | Deep Royal | `#122C7C` | Crest keyline, pressed states |
| Primary (light) | Sky Royal | `#8FA6F0` | Subline on black backgrounds only |
| Ink | Angus Black | `#0B0B0D` | The bull, the plate, keyline on paper |
| Neutral | Ranch Grey | `#8B9199` | Rules, hairlines, secondary text |
| Neutral (light) | Fence Grey | `#D9DCE1` | Script line on black, dividers |
| Surface | Paper | `#F4F5F7` | Roundel field, light app background |

## The two treatments

The wordmark is always two colors. Which two depends on the ground:

- **On black** — white letters, royal blue keyline. This is the trailer sign.
- **On paper** — royal blue letters, black keyline. Same pair, swapped, so the
  fill still dominates and the spurred serifs stay crisp at small sizes.

Never set the wordmark in one flat color; the keyline is the identity.

## Files

| File | Use |
| --- | --- |
| `logo/logo-sign.svg` | **The sign** — full plate with both irons. Trailer, gate, banner, catalog cover |
| `logo/logo-primary.svg` | Horizontal lockup — default, light backgrounds |
| `logo/logo-primary-reverse.svg` | Horizontal lockup on black / dark UI |
| `logo/logo-stacked.svg` | Stacked lockup with the country line |
| `logo/logo-stacked-reverse.svg` | Stacked lockup on black / dark UI |
| `logo/logo-badge.svg` | Crest — signage, jackets, sale-day print |
| `logo/logo-mark.svg` · `-reverse.svg` | Roundel mark alone — avatars, watermarks |
| `logo/logo-mark-mono-black.svg` | One color — branding iron, embroidery, fax |
| `logo/logo-mark-mono-white.svg` | One color knockout on photos |
| `logo/brand-x7.svg` · `brand-bar7.svg` | The X7 and bar-7 irons as standalone art |
| `logo/app-icon.svg` · `-dark.svg` | Mobile app icon, both appearances |
| `logo/*.png` | Rendered exports (2000 / 1680 / 1200 / 1024 / 512 / 64 px) |

The irons are traced to match the sign photograph. If either one is off from the
registered brand, fix `brand_x7()` / `brand_bar7()` in the generator and every
file picks up the change.

## Usage

- **Clear space:** keep free space equal to the roundel's radius on all sides;
  on the sign plate, the printed border is the clear space — nothing sits inside it.
- **Minimum size:** horizontal lockup 200 px / 1.75 in wide; sign plate 3 in
  wide; roundel alone 24 px.
- **Backgrounds:** use the reverse files on anything darker than Ranch Grey.
  Never place the paper version on a mid-blue field.
- **Don't:** recolor the bull, stretch the lockup, re-typeset the wordmark, drop
  the keyline, or add bevels, gradients or drop shadows.

## Typography

| Role | Face | Where |
| --- | --- | --- |
| Display | Rye | KATUS RANCH, the irons |
| Gothic | Oswald 600 | ANGUS SEEDSTOCK |
| Script | Yellowtail | Watauga, South Dakota |

All three are OFL-licensed (see `fonts/NOTICE.md`). **The logo files contain no
text and no font references** — the generator converts every letter to outline
paths at build time, so the SVGs render identically on any machine, in any
browser, at any print shop.

## Regenerating

```
pip install fonttools brotli cairosvg
python3 brand/tools/generate_logo.py
```

The script is the single source of truth: bull geometry, palette, letterform
treatment and every lockup metric live there, and it rewrites the whole of
`brand/logo/`.
