# FIG1_BUILD_SPEC — `fig1_lead_overview`

Lead figure for IRSpectra-Bench ICLR paper. System + diagnosis in one glance.
**Not** an IR-Agent “Overall Framework / TI Expert / Ret Expert” clone.

## Frame

| | Print (pt) | @1x px (72 dpi) | @2x px (preview) |
|--|------------|-----------------|------------------|
| Width | 504 (7.0 in) | 504 | 1008 |
| Height | 288 (4.0 in) | 288 | 576 |

Figma: create frame `fig1_lead_overview` at **1008 × 576**, set export scale 0.5 for print PDF, or keep 504 × 288 and export @2x.

## Auto-layout (top → bottom)

1. **Row A — Protocol strip** (horizontal, 3 equal cards)
   - Padding: 14 pt outer
   - Gap between cards: 10 pt
   - Card size: width = `(504 − 28 − 20) / 3` ≈ **152 pt**; height **88 pt**
   - Alignment: top stretch; cards vertical stack: title → body → annot
   - Small muted arrow between cards (optional; do not invent tool glyphs)

2. **Row B — Decomposition equation** (centered)
   - Gap from Row A bottom ≈ 28 pt
   - Three text lines, center-aligned

3. **Row C — Wall diagnostic bar**
   - Gap from equation support ≈ 16–20 pt
   - Full width minus 14 pt padding each side
   - Segment widths **proportional to counts** (total 194)
   - Bracket over first two segments only
   - Punchline + thin callout under bar

## Component inventory

| Component | Contents |
|-----------|----------|
| `Card/Input` | Title `1 · Input`; body formula + peak lists; annot `blind peak lists (not traces)` |
| `Card/Generation` | Title `2 · Generation`; body LLM ranked candidates; annot `true enters pool 65/194 (34%)` |
| `Card/Verification` | Title `3 · Verification`; body forward-verify / re-rank; annot `selects true 58/65 (89%) when present` |
| `Equation` | `top-1 = generation recall × verification precision\|recall` + `30% ≈ 34% × 89%` + support line |
| `WallBar` | teal 58 \| vermil 7 \| grey 129; bracket `65 recalled (34%)` |
| `Punchline` | `No re-ranking repairs the 129 never proposed` |
| `Callout` | `Verification alone: 28% → 30% (diagnostic, not an accuracy advance)` |

## Verbatim numeric strings (must appear exactly)

- `65/194 (34%)`
- `58/65 (89%)`
- `30% ≈ 34% × 89%`
- `58/194 = 30%`
- `58` / `7` / `129`
- `65 recalled (34%)`
- `129 never proposed`
- `28% → 30%`

## Colors / type

See `TOKENS.md`. Wall fills: `#00897B`, `#E53935`, `#5F6368`. Numbers inside bar: white bold.

## Figma paste handoff (no plugin)

1. Import `vectors/fig1_lead_overview.svg` (File → Place / drag).
2. Or rebuild from this spec using Auto Layout frames matching sizes above.
3. Keep SVG text as editable text layers where Figma allows; otherwise overlay text matching verbatim strings.
4. Export: PDF (vector) + PNG @2x for Overleaf preview.
5. Cross-check against overnight cloud agent `bc-201e83c7` repo vectors at morning review.

## Source files in this pack

- `vectors/fig1_lead_overview.svg` / `.pdf` / `.png`
- `sources/LOCKED_FACTS.md`
