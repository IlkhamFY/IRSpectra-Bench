# WALL_BUILD_SPEC — `fig_wall_diagnostic`

Main wall is the **n=500 forward-verify bottleneck**. Propose is the wall, not verify.

Locked integers (no CIs): **204 | 45 | 251** (fverify wall).
Generation headline remains 227/500 top-1 and 249/500 recall.

- verified: **204**
- misranked: **45**
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
| 204 | `#00897B` | verified |
| 45 | `#E53935` | misranked |
| 251 | `#5F6368` | never proposed |

- White bold numbers **inside** segments
- Bracket over 204+45 with label **`249 recalled (49.8%)`**
- Thin visual gaps between segments (~1.5 pt)

## Pack files

- Regenerated: `figures/fig_wall_diagnostic.{svg,pdf,png}`
- This plate is n=500 fverify **204/45/251** only. Lead Fig 1
  (`fig1_lead_overview`) is the generation wall **227/22/251**.
- SI-only protocol-slice diagnostic: `figures/fig_wall_fverify_slice.{svg,pdf,png}`
