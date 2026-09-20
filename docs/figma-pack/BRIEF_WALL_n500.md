# BRIEF — Locked wall n=500 (Chem Partner 2026-09-20 morning)

**Superseded the same day.** The shipped wall is n=500 **fverify 204/45/251**
(`docs/FINAL_SOURCE_OF_TRUTH_2026-09-20.md`). Generation 227/22/251 below is
generation, not THE wall. Keep this file as the morning changelog only.

**Pack root:** `/workspace/iclr-figma-pack-2026-09-20/`  
**Supersedes wall numbers in:** `BRIEF_0800ET.md` (old n=194 fverify wall)  
**Timezone:** America/New_York

## Changelog (old → new)

| | Old (fverify n=194) | New (generation decomp n=500) |
|--|---------------------|-------------------------------|
| n | 194 | **500** |
| Segment A | verified **58** | **exact top-1 227** |
| Segment B | mis-ranked **7** | **in pool, not top-1 22** |
| Segment C | never proposed **129** | **never proposed 251** |
| Bracket | 65 recalled (34%) | **249 recalled (49.8%)** = recall@3 |
| Product / top-1 | 58/194 = 30% | **227/500 = 45.4%** |
| Among recalled | 58/65 = 89% | **227/249 = 91.2%** |
| Equation | 30% ≈ 34% × 89% | **45.4% = 49.8% × 91.2%** |
| Punchline | …129 never proposed | **…251 never proposed in top-3** |
| Callout | Verification alone: 28% → 30% | **deleted** (no new locked pair) |

Scrub from figure text: 194, 106, 200, 58, 7, 129, 65/194, 58/65, 28%→30%, and fverify labels “verified”/“mis-ranked” on the wall.

## Locked values (exact — do not invent)

- n = **500**
- exact top-1 **227** | in pool, not top-1 **22** | never proposed **251**
- recalled = 227+22 = **249** (recall@3)
- generation recall@3 = 249/500 = **49.8%** → show `249/500 (49.8%)`
- among recalled, top-1 = 227/249 ≈ **91.2%** → prefer `227/249 (91.2%)`
- top-1 product = 227/500 = **45.4%** → `45.4% = 49.8% × 91.2%`
- No CIs on these wall numbers
- Listing 1 JSON unchanged

## Regenerated assets

- `vectors/fig1_lead_overview.{svg,pdf,png}`
- `vectors/fig_wall_diagnostic.{svg,pdf,png}`
- Listing1 assets left alone
