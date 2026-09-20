# WALL_BUILD_SPEC — `fig_wall_diagnostic`

Main wall is the **n=500 generation bottleneck**. Propose is the wall, not verify.

Locked integers (no CIs): **227 | 22 | 251**.

- top-1 exact: **227**
- in candidate set but not top-1: **22** (=249−227)
- never proposed in top-3: **251** (=500−249)
- recalled (top-3): **249 (49.8%)**

Do **not** put 58/7/129 on this plate. That instrumented
forward-verify diagnostic lives only as `fig_wall_fverify_slice`
(SI protocol slice; not the paper wall).

## Frame

| | Print (pt) | @2x px |
|--|------------|--------|
| Width | 504 | 1008 |
| Height | 102 | 204 |

## Segments (left → right, proportional to n=500)

| Count | Fill | Label under |
|-------|------|-------------|
| 227 | `#00897B` | top-1 exact |
| 22 | `#E53935` | in set, not top-1 |
| 251 | `#5F6368` | never proposed |

- White bold numbers **inside** segments
- Bracket over 227+22 with label **`249 recalled (49.8%)`**
- Thin visual gaps between segments (~1.5 pt)

## Pack files

- Regenerated: `figures/fig_wall_diagnostic.{svg,pdf,png}`
- Lead Fig 1 wall callouts use the same 227/22/251 integers
- SI-only fverify diagnostic: `figures/fig_wall_fverify_slice.{svg,pdf,png}`
