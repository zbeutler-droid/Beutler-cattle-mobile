# Katus Ranch — Angus Seedstock

Brand mark and logo system. The mark is a polled (hornless) Angus bull head —
correct for the breed — set in a royal blue roundel, with the ranch name in a
serif wordmark over a grey rule and `ANGUS SEEDSTOCK` letterspaced in royal blue.

## Colors

| Role | Name | Hex | Notes |
| --- | --- | --- | --- |
| Primary | Royal Blue | `#1A3EAF` | Ring, subline, icon border |
| Primary (dark) | Deep Royal | `#122C7C` | Pressed/hover states, shadows |
| Primary (light) | Sky Royal | `#8FA6F0` | Subline on black backgrounds only |
| Ink | Angus Black | `#0B0B0D` | Bull head, wordmark |
| Neutral | Ranch Grey | `#8B9199` | Rules, hairlines, secondary text |
| Neutral (light) | Fence Grey | `#D9DCE1` | Dividers, disabled states |
| Surface | Paper | `#F4F5F7` | Roundel field, light app background |

## Files

| File | Use |
| --- | --- |
| `logo/logo-primary.svg` | Horizontal lockup — default, light backgrounds |
| `logo/logo-primary-reverse.svg` | Horizontal lockup on black / dark UI |
| `logo/logo-stacked.svg` | Stacked lockup — square-ish spaces, print |
| `logo/logo-stacked-reverse.svg` | Stacked lockup on black / dark UI |
| `logo/logo-badge.svg` | Crest/seal — signage, cattle tags, catalog covers |
| `logo/logo-mark.svg` | Roundel mark alone — avatars, watermarks |
| `logo/logo-mark-mono-black.svg` | One-color black — fax, branding iron, embroidery |
| `logo/logo-mark-mono-white.svg` | One-color white — knockout on photos |
| `logo/app-icon.svg` | Mobile app icon, light |
| `logo/app-icon-dark.svg` | Mobile app icon, dark |
| `logo/*.png` | Rendered exports (1024/512/64 px as listed) |

## Usage

- **Clear space:** keep free space equal to the roundel's radius on all sides.
- **Minimum size:** horizontal lockup 180 px / 1.5 in wide; mark alone 24 px.
- **Backgrounds:** use the reverse files on anything darker than Ranch Grey.
  Never place the standard lockup on a mid-blue field.
- **Don't:** recolor the bull head, stretch the lockup, re-typeset the wordmark
  at different tracking, or add effects (bevels, drop shadows, gradients).

## Typography

- Wordmark: Georgia / Times New Roman (serif stack), 700, tracking 0.03 em.
- Subline: Helvetica Neue / Arial (sans stack), 600, tracked to justify to the
  wordmark width.

The SVGs keep the text live so they can be edited. For a final production logo,
convert the text to outlines in your vector editor once the licensed brand fonts
are chosen — that guarantees identical rendering everywhere.

## Regenerating

```
pip install cairosvg
python3 brand/tools/generate_logo.py
```

The script is the single source of truth: the bull head geometry, colors, and
lockup metrics live there, and it rewrites every SVG and PNG in `brand/logo/`.
