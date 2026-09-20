# WALL_BUILD_SPEC — `fig_wall_diagnostic`

Chem Partner 2026-09-20 morning: **227 | 22 | 251** (n=500 generation decomposition).

Label semantics (NOT the old fverify wall):
- **227** = exact top-1
- **22** = in pool, not top-1
- **251** = never proposed (in top-3)
- Bracket = recall@3: **249 recalled (49.8%)**

## Frame

| | Print (pt) | @2x px |
|--|------------|--------|
| Width | 504 | 1008 |
| Height | 102 | 204 |

(Paper original authored ~6.3 × 1.42 in; this pack uses full 7.0 in column width for Figma alignment.)

## Segments (left → right, proportional to n=500)

| Count | Fill | Label under |
|-------|------|-------------|
| 227 | `#00897B` | exact top-1 |
| 22 | `#E53935` | in pool, not top-1 |
| 251 | `#5F6368` | never proposed |

- White bold numbers **inside** segments
- Bracket over 227+22 with label **`249 recalled (49.8%)`**
- Thin visual gaps between segments (~1.5 pt)

## Pack files

- Regenerated: `vectors/fig_wall_diagnostic.{svg,pdf,png}`
- Paper originals for audit: `vectors/fig_wall_paper_original.{pdf,png}` (legacy n=194 artwork — audit only)

Keep as **diagnostic** companion; lead with `fig1_lead_overview`.
