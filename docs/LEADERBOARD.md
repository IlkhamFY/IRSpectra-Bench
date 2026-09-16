# IRSpectra-Bench leaderboard

Blind structure elucidation from **molecular formula + IR + ¹H + ¹³C** peak lists exactly as reported in open-access papers. Constitution scoring uses RDKit InChIKey connectivity (first 14 characters) unless noted.

**Paper:** [IRexp and IRSpectra-Bench](https://github.com/IlkhamFY/spectro-agent) (manuscript in preparation, 2026).

---

## Main benchmark (headline n = 295)

Paper headline is the **pooled generation cohort**: 194 locked + 101 validate-clean expansion
(five ¹³C-overread flags R12, R22, R25, R82, R91 excluded). Counts from
`docs/POOLED_HEADLINE_2026-09-16.md` / spectro-agent `scripts/score_pooled.py`.
Forward-verification has **not** been run on the expansion — do not invent a pooled
verification-precision or a pooled `fig_wall`. Sensitivity n=300 (194+all 106) is
118/300 (39.3%) top-1; not the headline.

| Rank | Model / method | Top-1 ↑ | Recall (top-3) ↑ | Gen. recall | Verif. prec. \| recall | Notes |
|---:|---|--:|--:|--:|--:|---|
| 1 | Claude Fable 5 | **46%** | 54% | — | — | 24-compound subset only |
| 2 | Claude Opus (solver self-rank, pooled) | **39.3%** (116/295) | 44.1% (130/295) | 44.1% | 89.2% (116/130 self-rank) | **Headline n=295**; self-rank ≠ forward-verify |
| 3 | Claude Opus + generate-wide + forward-verify | **30%** | — | 42% | 72% | 60-compound arm |
| 4 | Claude Opus + forward-verify | 30% | 33.5% | 34% | **89%** (58/65) | Locked n=194 only |
| 5 | Claude Opus (solver self-rank, locked) | 28.4% | 33.5% | 34% | 85% | Locked n=194 slice |
| 6 | Grok 4.6 | — | — | 53% | 62% | 60-compound arm |
| 7 | Gemini 3.7 Flash | — | — | 50% | 73% | 60-compound arm |
| 8 | GPT-5.6 Sol | — | — | 42% | 68% | 60-compound arm |
| 9 | Claude Sonnet | 21% | 25% | — | — | 24-compound subset |
| 10 | Claude Haiku | 0% | 4% | — | — | 24-compound subset |

Bootstrap 95% CIs for the headline row: top-1 **39.3% [34–45]**, recall **44.1% [39–49]**.
Corpus-reweighted (17.5% simple / 82.5% complex): top-1 **26.5% [21–32]**, recall **31.3% [25–37]**.
Stereo-sensitive InChIKey top-1: **93/295 (31.5%)**.

**Key finding:** verification precision exceeds generation recall for every vendor tested — the binding constraint is *candidate proposal*, not spectral ranking.

### By difficulty (Claude Opus, headline n = 295)

| Stratum | n | Top-1 | Recall |
|---|---:|--:|--:|
| All | 295 | 116/295 (39.3%) | 130/295 (44.1%) |
| Simple | 147 | 87/147 (59.2%) | 94/147 (63.9%) |
| Complex | 148 | 29/148 (19.6%) | 36/148 (24.3%) |

### Honest slices (locked vs expansion)

The expansion slice is easier for this solver than the locked 194 (60% vs 28% top-1).
That gap is a result, not a reason to keep n=194 as the paper headline.

| set | n | top-1 | recall |
|---|---:|---|---|
| locked 194 | 194 | 55/194 (28.4%) | 65/194 (33.5%) |
| expansion clean | 101 | 61/101 (60.4%) | 65/101 (64.4%) |
| **headline pool (194+101)** | **295** | **116/295 (39.3%)** | **130/295 (44.1%)** |
| sensitivity (194+all 106) | 300 | 118/300 (39.3%) | 133/300 (44.3%) |

---

## Pre-registered expansion (n = 106) — pooled into n=295 after clean-flag exclusion

Independent pre-registered blind draw, scored after the n=194 cohort was locked.
Constitution scoring is RDKit InChIKey-14. Clean 101 compounds enter the paper headline;
all-106 is a sensitivity row only. Forward-verify on the expansion is **pending**.

| Rank | Model / method | Top-1 ↑ | Recall (top-3) ↑ | Gen. recall | Verif. prec. \| recall | Notes |
|---:|---|--:|--:|--:|--:|---|
| — | Claude Opus (expansion, all) | **59.4%** (63/106) | 64.2% (68/106) | 64.2% (68/106) | — | Sensitivity; flags included |
| — | Claude Opus (expansion, clean) | **60.4%** (61/101) | 64.4% (65/101) | 64.4% (65/101) | — | Enters headline n=295 |
| — | Claude Fable 5 (expansion) | — | — | — | — | Incomplete (68/106); never pooled |

---

## Evaluate your model

### 1. Download the benchmark (questions only — no answers in the solver prompt)

```bash
git clone https://github.com/IlkhamFY/spectro-agent.git
cd spectro-agent
pip install -r requirements.txt
```

Questions (blind inputs):

- `data/benchmark_main/questions2.jsonl` (140; use `clean_qids.json` for validated subset)
- `data/benchmark_v3/questions2.jsonl` (40)
- `data/benchmark_v2_ctrl/questions2.jsonl` (20)

Each row: `qid`, `formula`, `ir_bands_cm-1`, `h_nmr`, `c_nmr`. **No structure hints.**

### 2. Run your elucidator

Return up to **three ranked SMILES** per `qid`. Protocol:

- Inputs: formula + IR + ¹H + ¹³C only (as printed in the source paper).
- No web search, no structure hints, no answer-key access.
- Document model version, prompt, and tool access in your submission.

### 3. Score locally

Write predictions as JSONL:

```json
{"qid": "R01", "candidates": ["SMILES_rank1", "SMILES_rank2", "SMILES_rank3"]}
```

```bash
python scripts/score_submission.py --predictions my_run.jsonl --name "YourModel-1.0"
# optional strict stereochemistry scoring:
python scripts/score_submission.py --predictions my_run.jsonl --stereo
```

Reproduce the official headline numbers (spectro-agent):

```bash
python scripts/score_pooled.py            # n=295 constitution → data/pooled_headline.json
python scripts/score_pooled.py --stereo   # 93/295 (31.5%)
python scripts/score_main.py              # locked n=194 slice
python scripts/forward_verify_all.py      # n=194 only until expansion fverify exists
```

### 4. Submit to the leaderboard

Open a GitHub issue or PR on [IlkhamFY/spectro-agent](https://github.com/IlkhamFY/spectro-agent) with:

1. `--name` label for the table
2. `score_submission.py` output (copy-paste)
3. Predictions file (`my_run.jsonl`) or link to reproducible run
4. Model ID, date, and brief protocol note (tools, candidate budget, reasoning tier)
5. Confirmation: blind protocol, no answer-key access

We will verify scoring with `scripts/score_submission.py` before adding a row.

---

## Subsets & extensions

| Benchmark | n | Purpose |
|---|---:|---|
| **IRSpectra-Bench** (194 locked + 101 clean expansion) | 295 | Paper headline (generation) |
| IRSpectra-Bench (locked main + v3 + v2_ctrl) | 194 | Locked slice; forward-verify / fig_wall |
| IRSpectra-Bench (pre-reg expansion, clean / all) | 101 / 106 | Clean 101 in headline; all-106 sensitivity |
| IRSpectra-Bench (main clean only) | 134 | Spectrally validated main round |
| IRSpectra-Bench-Electrolyte | 46 | Battery-electrolyte functional classes |
| Cross-vendor arm | 60 | Same compounds, multiple vendors (`docs/CROSS_VENDOR.md`) |
| Model comparison subset | 24 | Claude Haiku → Fable ladder |

---

## Related resources

- **IRexp dataset (review copy):** https://anonymous.4open.science/r/peaklist-corpus-review-10C4/ — use `data/train_no_bench.jsonl.gz` to avoid benchmark leakage. Named Hugging Face hosting is restored at camera-ready.
- **Cross-vendor protocol:** `docs/CROSS_VENDOR.md`
- **Forward-verification:** `docs/FORWARD_VERIFY.md`
- **Full reproduction:** `README.md` in repository root

---

## Citation

If you use IRSpectra-Bench or report numbers on it, please cite:

```bibtex
@article{yabbarov2026irspectra,
  title   = {{IRexp} and {IRSpectra-Bench}: redistributable experimental {IR} band lists,
             a blind peak-list benchmark, and a recall-bound diagnosis of {LLM} elucidation},
  author  = {Yabbarov, Ilkham and Sondhi, Rudra and Vargas-Hern{\'a}ndez, Rodrigo A.},
  year    = {2026},
  note    = {Manuscript in preparation; target J. Chem. Inf. Model.}
}
```

*Last updated: 2026-09-16 (v0.12 pooled headline n=295). External submissions listed after verification.*
