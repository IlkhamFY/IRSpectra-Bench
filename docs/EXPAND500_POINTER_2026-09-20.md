# expand-500 pointer — 2026-09-20

Companion sources (spectro-agent `cursor/expand-bench-500-b78b`):

- `data/benchmark_expand_500/NIGHT_POOL_2026-09-20.md` (copied here)
- `data/fverify_expand_500/INVENTORY_2026-09-20.md` (copied here)
- `data/benchmark_expand_500/STATUS.md`

**Paper headline stays n=300.** No CIs. Official fverify is SI-only.

| item | value |
|---|---|
| draw | 230; seed 2026500; 115/115; 6 flags (R26, R31, R102, R105, R107, R138) |
| deposits | 230/230; 690 candidates |
| all-230 generation | **129/230 (56.1%)** top-1; **138/230 (60.0%)** recall@3 |
| clean-224 | **127/224 (56.7%)** / **135/224 (60.3%)** |
| exploratory n=524 | 194+all106+clean224 → 245/524 (46.8%) / 268/524 (51.1%) |
| alt n=519 | 194+clean101+clean224 → 243/519 / 265/519 |
| n=530 | 194+all106+all230 → 247/530 / 271/530 |
| fverify-500 | **41/41**, 681/681. Official score: verify **103/230 (44.8%)** vs self **129/230**; verify\|recall **103/138 (74.6%)**. Clean: 103/224 / 103/135. **No CIs. Not a wall.** |
| protocol | thinking-tier arm — not interchangeable with no-thinking headline |
| key | withheld after the score pass |
