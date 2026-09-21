# Formula enumerator — MAYGEN 1.8

Offline constitutional isomer generator. No LLM call. Scorer is RDKit
InChIKey-14, the same contract as 227/500 and 249/500. This is not a
score on those 500.

Scripts: `scripts/exp_formula_enum.py`, `scripts/exp_formula_enum_recall.py`.
Tables: `results/exp_formula_enum.csv`, `results/exp_formula_enum.json`,
`results/exp_formula_enum_per_qid.csv`.

## What was declared before the hits

Headline compounds with heavy-atom count ≤ 12. That is **31** compounds,
**30** formulas. The other **469** were not run. Pilots on this VM, 30s,
partial files discarded: C7H10O4 (HA 11), C10H18O2 (HA 12), C9H9ClO3S
(HA 14), C12H10FNO (HA 15), and C10H8Br4O2 (HA 16) each passed 5×10⁵
structures without exhausting. HA>12 is out of scope, not a hidden
subsample of a finished 500.

Inside the 31, each formula got 45s. A timeout deletes the partial
file. That is not evidence the gold was absent.

Top-1 is the isomer with the lowest symmetric chamfer between the
deposited nmrshiftdb GNN (`data/nmrshiftdb/gnn_c13.pt` in spectro-agent)
and the printed ¹³C list. Ranking ran only when the unique InChIKey-14
set had at most 80,000 members. Larger finished sets were scanned for
membership only. The scan stopped at the first hit, so the line number
in the per-qid file is not the size of the isomer set.

## Results

| set | n | InChIKey-14 recall | top-1 |
|---|---:|---|---|
| generation finished in 45s | 15 | **15/15** | 4/5 on the ranked subset; 10 sets were not ranked |
| ranked (≤80,000 constitutions) | 5 | 5/5 | **4/5** (GNN top-3 is also 4/5) |
| timeout at 45s | 14 | not established | not ranked |
| MAYGEN rejected the formula | 2 | 0/2 | not ranked |
| declared attempt, HA≤12 | 31 | 15/15 of the sets that finished | 4/5 of the sets that were ranked |

The two rejections are C7H18Sn and C9H14OSi. MAYGEN uppercases the
formula and does not accept Sn or Si. Cl, Br, and I did run.

Ranked sets (full unique counts):

| qid | formula | isomers | enum top-1 | Opus top-1 | Opus recall@3 |
|---|---|---:|---:|---:|---:|
| locked R41 | C6H13NO2 | 23,708 | 1 | 0 | 0 |
| locked R60 | C9H16O | 29,172 | 0 | 1 | 1 |
| thinking R110 | C6H8O2 | 10,872 | 1 | 1 | 1 |
| thinking R187 | C8H17BrO | 1,157 | 1 | 1 | 1 |
| thinking R190 | C11H24O | 2,426 | 1 | 1 | 1 |

On these five, Opus is also 4/5 top-1, on a different miss (R60 vs R41).

On all 15 compounds whose isomer list was exhausted, the deposited
Opus candidates are **11/15** top-1 and **12/15** recall@3. Enumerator
recall on that same 15 is 15/15. Those recalls are not the same
quantity: the enumerator recall is membership in the full
constitutional set, and the Opus recall is membership in three
proposed SMILES.

15/15 finished is what standard-valence orderly generation should do
when it is allowed to finish. It is a coverage check, not a solver
score. The solver number from this run is the GNN top-1, **4/5**, on
five small formulas.

## What this does not say

Do not quote 15/31, 4/31, or anything over 500. Do not put this row
next to 227/500 as if the denominators matched. The 251 never-proposed
on the headline are mostly past HA 12, which this generator did not
finish.
