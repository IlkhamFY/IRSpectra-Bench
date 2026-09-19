# Expansion forward-verify — 2026-09-19

**Paper lock.** Headline generation stays **n=300** (118/300 top-1, 133/300 recall).
Figure 1 / Table `tab:fverify` stay the **LLM** instrumented slice **n=194**
(58 verified / 7 mis-ranked / 129 never proposed; 58/65).
This note records a **scripted** expansion arm. It does **not** invent an LLM
expansion precision or a pooled wall.

## What exists

| artefact | where | status |
|---|---|---|
| Expansion questions + Opus predictions | spectro-agent `data/benchmark_expand/` (not on `main`; branches `claude/funny-maxwell-u5S31`, `cursor/pooled-headline-b966`) | 106/106 deposited |
| Expansion answer key | withheld; reconstructed under `/tmp/blind/_key/` by unique (formula, IR, $^{13}$C) match to `irexp_resolved.jsonl.gz` | 106/106 unique |
| Locked LLM fverify | spectro-agent `data/fverify/` + `data/fverify_main/` | complete; 58/7/129 |
| `data/fverify_expand/raw/*.json` (LLM $^{13}$C) | **absent** | blocker for protocol-matched LLM fverify |
| Scripted GNN $^{13}$C chamfer | `scripts/forward_verify_expand.py` | **run**; sidecar `data/fverify_expand/diagnosis.json` |

This postcard repo cannot push to `IlkhamFY/spectro-agent` (no write permission on
the token). The scorer snapshot and the diagnosis sidecar live here; the gold
key and GNN weights stay in spectro-agent.

## Scripted GNN result (real; not LLM)

Same nmrshiftdb2 GNN already reported as **59/65 (91%)** on the locked recall set
versus the LLM verifier's **58/65 (89%)**. Re-run on this VM: **59/65, match**.

On the expansion roster:

| | all ($n{=}106$) | validate-clean ($n{=}101$) |
|---|---|---|
| generation recall | 68/106 (64.2%) | 65/101 (64.4%) |
| top-1, solver self-ranking | 63/106 (59.4%) | 61/101 (60.4%) |
| top-1, GNN-verified | **45/106 (42.5%)** | 43/101 (42.6%) |
| verified / mis-ranked / never-proposed | **45 / 23 / 38** | 43 / 22 / 36 |
| precision \| recall — GNN | 45/68 (66.2%) | 43/65 (66.2%) |
| precision \| recall — self-rank | 63/68 (92.6%) | 61/65 (93.8%) |
| McNemar (self only / verify only) | 20 / 2, $p{=}0.000$ | 19 / 1, $p{=}0.000$ |

Simple / complex (all 106): GNN wall 34/9/10 vs 11/14/28.

The GNN **does not transfer**: it matches the LLM on the locked slice and is
**worse than self-ranking** on the easier expansion draw. That is a result, not
a reason to relabel 45/68 as the paper's 89% claim.

Never-proposed **38/106** is exactly $106-68$ (generation recall). The new split
is verified vs mis-ranked among the 68 recalled.

## LLM campaign — exact blocker and cost

**Blocker:** no blind Opus $^{13}$C deposits for the 301 unique expansion
candidate SMILES. Overlap with locked `fverify*` predictions is **0/301**, so
nothing can be reused.

**Minimal path (no new elucidation):**

1. From spectro-agent with expansion predictions: `python scripts/forward_verify_expand.py prep`
   writes 18 batches of 17 anonymised SMILES (`data/fverify_expand/fbatch_*.txt`).
2. Dispatch each batch to a **plain Opus** forward-predict agent (SMILES only, no
   tools, no observed spectrum) — same protocol as `scripts/forward_verify_main.py`.
3. Deposit `{anon_id: [shifts]}` JSON under `data/fverify_expand/raw/`.
4. `python scripts/forward_verify_expand.py score --llm` (refuses today).
5. Only then may `forward_verify_all.py` grow `diagnosis.json` / `fig_wall`.

**Cost:** 18 Opus forward-predict jobs, ~301 SMILES. No new solver calls, no
Opus Thinking High. Do not run the campaign under a thinking-high model.

Until those JSON files exist, any pooled verified/mis-ranked/wall triple that
includes the expansion is invented.

## What the paper may say

- Generation headline **n=300** unchanged.
- LLM fverify / Figure 1 **n=194**, 58/7/129, 58/65 unchanged.
- Appendix: GNN-scripted expansion wall **45/23/38**, explicitly not LLM.
- Methods/limitations: LLM expansion campaign not run (301 SMILES / 18 batches / 0 overlap).
- Do not merge 45+58 or 38+129 into Figure 1.

Source sidecar: `data/fverify_expand/diagnosis.json`.
