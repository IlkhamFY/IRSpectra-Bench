# Thinking-tier 200 vs earlier 300

Recomputed 2026-09-21 from deposited candidate lists. Scorer: RDKit
InChIKey-14 (first 14 characters), up to three ranked SMILES. Script:
`scripts/exp_split_thinking.py`. Tables: `results/exp_split_thinking.csv`,
`results/exp_split_thinking.json`. Per-compound hits (no structures):
`results/exp_split_thinking_per_qid.csv`.

The pooled headline stays **227/500** top-1 and **249/500** recall.
This note only splits that pool. No CIs.

## What was scored

| slice | what | protocol |
|---|---|---|
| locked 194 | main clean + v3 + v2_ctrl | no-thinking |
| +106 | all deposited Opus expansion | no-thinking |
| earlier 300 | locked 194 + all 106 | no-thinking |
| thinking 200 | expand-500 validate-clean, `sorted(qid)[:200]` (R01–R75) | thinking-tier |
| headline 500 | earlier 300 + thinking 200 | mixed |

Gold for the locked 194 is the committed `answers2.jsonl`. Gold for +106
and expand-500 is not in the tree. It was rebuilt in memory by a unique
`(formula, IR band list, 13C string)` match to `irexp_resolved.jsonl.gz`:
**106/106** and **230/230** unique, **0** InChIKey-14 collisions against
the locked set or each other. The key was not written.

Sources: spectro-agent `main` for the locked answers, raw predictions, and
`irexp_resolved`; `cursor/expand-bench-500-b78b` @ `48fcd30` for expansion
questions and `predictions2.jsonl`. The 200-qid list in this repo matches
that branch.

## Generation (recomputed)

| slice | n | top-1 | recall@3 | gen wall (top-1 / recalled-not-top-1 / never) |
|---|---:|---|---|---|
| locked 194 | 194 | 55/194 (28.4%) | 65/194 (33.5%) | 55 / 10 / 129 |
| +106 | 106 | 63/106 (59.4%) | 68/106 (64.2%) | 63 / 5 / 38 |
| **earlier 300** | **300** | **118/300 (39.3%)** | **133/300 (44.3%)** | **118 / 15 / 167** |
| **thinking 200** | **200** | **109/200 (54.5%)** | **116/200 (58.0%)** | **109 / 7 / 84** |
| headline 500 | 500 | 227/500 (45.4%) | 249/500 (49.8%) | 227 / 22 / 251 |

Self-rank on the pool remains 227/249. Strata on the two slices:

| slice | simple top-1 | simple recall | complex top-1 | complex recall |
|---|---|---|---|---|
| earlier 300 | 88/151 | 96/151 | 30/149 | 37/149 |
| thinking 200 | 73/97 | 76/97 | 36/103 | 40/103 |

Addition: 118+109 = 227 and 133+116 = 249. The script exits if that
identity fails.

## Forward-verify wall (not recomputed)

Chamfer was not re-run. `candidates.jsonl` still has no `is_true`.
The arm counts below are the deposited `data/fverify_n500/wall.json`
table (`cursor/fverify-n500-unify-629c`). The earlier-300 row is the
sum of the locked-194 and +106 arms. Those sums match the generation
recall and never-proposed counts above, which is a check, not a new
verify pass.

| slice | verified | misranked | never-proposed |
|---|---:|---:|---:|
| locked 194 | 58 | 7 | 129 |
| +106 | 56 | 12 | 38 |
| **earlier 300** | **114** | **19** | **167** |
| **thinking 200** | **90** | **26** | **84** |
| n=500 | 204 | 45 | 251 |

On the earlier 300, self-rank top-1 (118) exceeds chamfer-verified (114)
by 4. On the thinking 200 the gap is 109 vs 90. Ranking, not proposal,
is where the thinking-tier cut loses more.

## What this does not say

The thinking-tier 200 is an easier draw as well as a different harness
(simple top-1 73/97 vs 88/151 on the earlier 300). The 54.5% vs 39.3%
gap is not a clean thinking-on/thinking-off effect. Do not replace
227/500 with either slice.
