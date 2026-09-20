# Design tokens — IRSpectra-Bench ICLR Figma pack

Exact values. Do not invent alternate metrics or decorative icons.

## Color

| Token | Hex | Role |
|-------|-----|------|
| `verified` / teal | `#00897B` | Wall segment: verified; generation/verification success annotations |
| `mis-ranked` | `#E53935` | Wall segment: mis-ranked |
| `never-proposed` | `#5F6368` | Wall segment: never proposed (dominant mass) |
| `ink` | `#1A1A1A` | Primary text, bracket, equation |
| `muted` | `#6B7280` | Secondary labels, callouts, arrows |
| `card-fill` | `#F7F7F5` | Protocol cards, listing frame fill |
| `card-stroke` | `#E5E5E0` | Card / frame borders |
| `white` | `#FFFFFF` | Page background; numbers inside wall segments |

No gradients. No drop shadows.

## Type

| Style | Size (pt) | Weight | Line-height | Use |
|-------|-----------|--------|-------------|-----|
| `card-title` | 10 | 700 | 1.2 | Protocol card headings |
| `card-body` | 8.5 | 400 | 1.35 | Protocol card body |
| `card-annot` | 7.5 | 600 | 1.2 | Teal annotations under cards |
| `eq-label` | 11 | 600 | 1.3 | Decomposition equation text |
| `eq-numbers` | 12 | 700 | 1.2 | `30% ≈ 34% × 89%` |
| `eq-support` | 7.5 | 400 | 1.2 | Supporting fractions under equation |
| `wall-num` | 11–12 | 700 | 1 | White counts inside bar (`58`, `7`, `129`) |
| `wall-label` | 8–9 | 400 | 1 | Under-bar category names |
| `wall-bracket` | 9–10 | 600 | 1 | `65 recalled (34%)` |
| `punchline` | 9 | 600 | 1.2 | `No re-ranking repairs the 129 never proposed` |
| `callout` | 7.5 | 400 | 1.2 | Verification alone note |
| `listing-title` | 10 | 700 | 1.2 | Listing 1 title line |
| `listing-json` | 6.2 | 400 (mono) | 1.45 | Exact JSON fields |

Font stack: DejaVu Sans / Helvetica / Arial (sans). JSON: DejaVu Sans Mono / Courier New.

## Spacing (print pt; Figma @2x = ×2 px)

| Token | pt | @2x px |
|-------|----|--------|
| page padding | 12–14 | 24–28 |
| card gap | 10 | 20 |
| card radius | 6 | 12 |
| card inner pad | 10 | 20 |
| row gap (A→B, B→C) | ~20–28 | 40–56 |
| wall segment visual gap | ~1.2–1.5 | ~2–3 |

## What NOT to invent

- Any accuracy other than locked list in `sources/LOCKED_FACTS.md`
- Tool icons implying TI Expert / Ret Expert / IR-Agent multi-panel clones
- Fake spectra traces (inputs are **blind peak lists**)
- Alternate wall splits (must remain **58 / 7 / 129**)
- Truncated Listing 1 NMR strings (wrap only; keep full field values)
