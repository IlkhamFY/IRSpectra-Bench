# fverify expand-500 inventory — 2026-09-20

Copied from spectro-agent `cursor/expand-bench-500-b78b`
`data/fverify_expand_500/INVENTORY_2026-09-20.md`.
Official chamfer numbers live in this repo at
`docs/NIGHT_POOL_2026-09-20.md` (verify 103/230 vs self 129/230;
verify|recall 103/138). Paper headline stays n=300.

Blind ¹³C campaign over the 681 unique candidate SMILES prepared by
`scripts/forward_verify_expand500_keyless.py` (`PREP_NOTE.md`). All 41
batches are now on the expand branch. Official chamfer / self-vs-verify
numbers are in spectro-agent `STATUS.md` and `results.txt`
(key restored under `/tmp` only).

Source of the counts: listing `data/fverify_expand_500/raw/f*.json`
against `fbatch_1.txt`…`fbatch_41.txt`, `anon_map.json` (681 smiles → Q000…Q680),
and `candidates.jsonl` (681 rows, `is_true` still absent).

## Coverage

| | count |
|---|---:|
| prep unique SMILES (target) | **681** |
| fbatch files present | **41/41** |
| `raw/f*.json` present | **41/41** |
| unique SMILES with a non-empty numeric ¹³C list | **681/681 (100%)** |
| unique SMILES still missing a ¹³C list | **0** |
| existing batches that are complete vs their fbatch | **41/41** |
| empty / non-numeric predictions | **0** |
| qids with every candidate SMILES covered | **230/230** |
| qids with at least one candidate covered | **230/230** |

## Existing ids (`raw/fN.json`)

**f1–f41** (41 files). Each matches its `fbatch_N.txt` 1:1
(f1–f25 are 17 SMILES; f26–f41 are 16).

| ids | files | SMILES / file | SMILES covered |
|---|---:|---:|---:|
| f1–f25 | 25 | 17 | 425 |
| f26–f41 | 16 | 16 | 256 |
| **present** | **41** | | **681** |

## Missing ids

**none.**

## Score pointer

`forward_verify_main.py score()` ran 2026-09-20 against this bundle
(`is_true` filled in `/tmp` from a lost-vault key; committed
`candidates.jsonl` unchanged). Verbatim footer and tables:
`STATUS.md`, `results.txt`,
`data/benchmark_expand_500/NIGHT_POOL_2026-09-20.md`.
