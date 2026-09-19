# LLM fverify-106 — blocker (2026-09-19)

**Paper claim stays unchanged.** Figure 1 / 89% (58/65) is training-free **LLM**
forward-verify on the locked **n=194** Opus candidate pools only. Expansion
generation is scored (63/106 top-1, 68/106 recall). Expansion **LLM** fverify
does not exist. That gap belongs in Limitations until real LLM deposits exist.

This note is the plan + blocker only. **No new metrics for `iclr_paper.tex`.**

## Can we run it this week from existing dumps?

**No.** Opus *solves* for the 106 exist. Opus *forward-¹³C* dumps for those
candidates do not. There is nothing to chamfer. Closing the gap needs a new
**plain Opus** (no thinking-high) blind ¹³C campaign — not re-elucidation.

A nmrshiftdb2 GNN ¹³C chamfer was tried as a proxy on this VM. It is a
**different method**. It is **out of scope** for the ICLR claim and must not
enter the PDF, Figure 1, or the 89% sentence. Sidecar (do not cite):
`data/fverify_expand/diagnosis.json`.

## What is on this VM

| path | what | present? |
|---|---|---|
| IRSpectra-Bench `data/fverify_expand/raw/` | LLM ¹³C `{anon_id: [ppm]}` | **no** (dir absent) |
| spectro-agent `/tmp/spectro-agent/data/fverify_expand/raw/` | same | **empty** |
| spectro-agent `data/fverify/raw/f1–f8.json` | locked 60-arm LLM ¹³C | yes (126 SMILES) |
| spectro-agent `data/fverify_main/raw/f1–f15.json` | locked 134-arm LLM ¹³C | yes (247 SMILES) |
| spectro-agent `data/benchmark_expand/predictions2.jsonl` | Opus **solves**, 106/106, 302 raw / 301 parseable unique SMILES | yes (on expansion branches, not `main`) |
| spectro-agent `data/benchmark_expand/questions2.jsonl` | blind peak lists | yes |
| spectro-agent `data/benchmark_expand/answers2.jsonl` | expansion key | **withheld** (reconstruct under `/tmp/blind/_key/` from `irexp_resolved.jsonl.gz`) |
| overlap locked LLM ¹³C ↔ expansion candidate SMILES | reuse | **0 / 301** |
| `ANTHROPIC_API_KEY` / OpenRouter / similar | API | **unset** |

Locked dumps cannot be reused. Expansion SMILES are a disjoint set.

## Protocol (when someone does run it)

Same as `scripts/forward_verify_main.py` / `docs/FORWARD_VERIFY.md` in
[IlkhamFY/spectro-agent](https://github.com/IlkhamFY/spectro-agent):

1. `prep` from `predictions2.jsonl` (top-3, RDKit-canonical, de-dup).
2. Shuffle unique SMILES, anonymise (`E000`…), batch size **17**.
3. Each batch: **plain Opus**, tools off, SMILES only — predict ¹³C peak lists.
   Never the observed spectrum, qid, or sibling set.
4. Deposit `{anon_id: [shifts]}` JSON under `data/fverify_expand/raw/`.
5. Mechanical chamfer vs observed ¹³C; then `forward_verify_all.py` may grow
   `diagnosis.json` / `fig_wall` **only if** Ilkham signs off on pooling.

Do **not** use Claude Opus Thinking High. Do **not** re-solve the 106.

## Cost

| | |
|---|---|
| Unique SMILES to predict | **301** |
| Jobs at batch size 17 | **18** |
| New elucidation / thinking-high | **0** |
| Reusable locked ¹³C | **0** |
| Token/dollar | not quoted here (no API on this VM; subscription-style agent jobs in the locked campaign) |

Locked precedent: 8 jobs (126 SMILES) + 15 jobs (247 SMILES). Expansion is the
same class of work, not a new solver sweep.

## Minimal path (spectro-agent, not this postcard)

Repo: `IlkhamFY/spectro-agent`, branch with `data/benchmark_expand/`
(`claude/funny-maxwell-u5S31` or `cursor/pooled-headline-b966`). This token
cannot push that repo.

1. Generalise `scripts/forward_verify_main.py` to `SRC=data/benchmark_expand`
   (or a dedicated `forward_verify_expand.py` that writes **LLM** batches only).
2. Reconstruct the key under `/tmp/blind/_key/` for `is_true`; never commit
   `answers2.jsonl` or a `candidates.jsonl` that carries `is_true`.
3. Dispatch 18 plain-Opus batches → `data/fverify_expand/raw/`.
4. Score; report verified / mis-ranked / never-proposed **only then**.
5. Paper update is a **separate** PR after those JSON files exist.

Until step 3 lands, any expansion verification-precision or pooled wall is
invented. Leave Limitations as: expansion LLM fverify was not run.
