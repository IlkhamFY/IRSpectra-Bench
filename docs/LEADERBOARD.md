# IRSpectra-Bench leaderboard

Blind structure elucidation from **molecular formula + IR + ¹H + ¹³C** peak lists exactly as reported in open-access papers. Constitution scoring uses RDKit InChIKey connectivity (first 14 characters) unless noted.

**Paper:** [IRexp and IRSpectra-Bench](https://github.com/IlkhamFY/spectro-agent) (manuscript in preparation, 2026).

---

## Main benchmark (headline n = 300)

Paper headline is the **pooled generation cohort**: 194 locked + all 106 expansion
(five ¹³C-overread flags R12, R22, R25, R82, R91 **included**). Counts from
`docs/POOLED_HEADLINE_2026-09-16.md` / spectro-agent `scripts/score_pooled.py`
(n=300 sensitivity row). Validate-clean n=295 is appendix / sensitivity, not the
lead number. Forward-verification is the n=194 instrumented slice — do not invent
a pooled verification-precision or a pooled `fig_wall`.

| Rank | Model / method | Top-1 ↑ | Recall (top-3) ↑ | Gen. recall | Verif. prec. \| recall | Notes |
|---:|---|--:|--:|--:|--:|---|
| 1 | Claude Fable 5 | **46%** | 54% | — | — | 24-compound subset only |
| 2 | Claude Opus (solver self-rank, pooled) | **39.3%** (118/300) | 44.3% (133/300) | 44.3% | 88.7% (118/133 self-rank) | **Headline n=300**; self-rank ≠ forward-verify |
| 3 | Claude Opus + generate-wide + forward-verify | **30%** | — | 42% | 72% | 60-compound arm |
| 4 | Claude Opus + forward-verify | 30% | 33.5% | 34% | **89%** (58/65) | Locked n=194 instrumented slice |
| 5 | Claude Opus (solver self-rank, locked) | 28.4% | 33.5% | 34% | 85% | Locked n=194 slice |
| 6 | Grok 4.6 | — | — | 53% | 62% | 60-compound arm |
| 7 | Gemini 3.7 Flash | — | — | 50% | 73% | 60-compound arm |
| 8 | GPT-5.6 Sol | — | — | 42% | 68% | 60-compound arm |
| 9 | Claude Sonnet | 21% | 25% | — | — | 24-compound subset |
| 10 | Claude Haiku | 0% | 4% | — | — | 24-compound subset |

Bootstrap 95% CIs for the headline row: top-1 **39.3% [34–45]**, recall **44.3% [39–50]**.
Corpus-reweighted (17.5% simple / 82.5% complex, validate-clean n=295): top-1 **26.5% [21–32]**, recall **31.3% [25–37]**.
Stereo-sensitive InChIKey top-1 (n=295): **93/295 (31.5%)**.

**Key finding:** verification precision exceeds generation recall for every vendor tested — the binding constraint is *candidate proposal*, not spectral ranking.

### By difficulty (Claude Opus, headline n = 300)

| Stratum | n | Top-1 | Recall |
|---|---:|--:|--:|
| All | 300 | 118/300 (39.3%) | 133/300 (44.3%) |
| Simple | 151 | 88/151 (58.3%) | — |
| Complex | 149 | 30/149 (20.1%) | — |

Stratum recall is tabulated for validate-clean n=295 in the appendix / `docs/POOLED_HEADLINE_2026-09-16.md`.

### Honest slices (locked vs expansion)

The expansion slice is easier for this solver than the locked 194 (59% vs 28% top-1).
That gap is a result, not a reason to keep n=194 as the paper headline.

| set | n | top-1 | recall |
|---|---:|---|---|
| locked 194 | 194 | 55/194 (28.4%) | 65/194 (33.5%) |
| expansion all | 106 | 63/106 (59.4%) | 68/106 (64.2%) |
| **headline pool (194+all 106)** | **300** | **118/300 (39.3%)** | **133/300 (44.3%)** |
| validate-clean (194+101; appendix) | 295 | 116/295 (39.3%) | 130/295 (44.1%) |

---

## Pre-registered expansion (n = 106) — pooled into n=300

Independent pre-registered blind draw, scored after the n=194 cohort was locked.
Constitution scoring is RDKit InChIKey-14. All 106 enter the paper headline; clean 101
is the appendix / sensitivity row. Forward-verify is the n=194 instrumented slice.

| Rank | Model / method | Top-1 ↑ | Recall (top-3) ↑ | Gen. recall | Verif. prec. \| recall | Notes |
|---:|---|--:|--:|--:|--:|---|
| — | Claude Opus (expansion, all) | **59.4%** (63/106) | 64.2% (68/106) | 64.2% (68/106) | — | Enters headline n=300 |
| — | Claude Opus (expansion, clean) | **60.4%** (61/101) | 64.4% (65/101) | 64.4% (65/101) | — | Appendix n=295 |
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
python scripts/score_pooled.py            # constitution; n=300 paper headline is the 194+all 106 row
python scripts/score_pooled.py --stereo   # 93/295 (31.5%) on validate-clean
python scripts/score_main.py              # locked n=194 slice
python scripts/forward_verify_all.py      # n=194 instrumented slice
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
| **IRSpectra-Bench** (194 locked + all 106 expansion) | 300 | Paper headline (generation) |
| IRSpectra-Bench (194 locked + 101 clean expansion) | 295 | Appendix / sensitivity |
| IRSpectra-Bench (locked main + v3 + v2_ctrl) | 194 | Instrumented slice; forward-verify / fig_wall |
| IRSpectra-Bench (pre-reg expansion, all / clean) | 106 / 101 | All 106 in headline; clean 101 in appendix |
| expand-500 (pre-reg draw toward n≈500) | 230 / 224 clean | **SI only.** 129/230 (56.1%) top-1; 138/230 recall. No CIs. No fverify. Not the n=300 headline. |
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

*Last updated: 2026-09-20 (headline n=300 unchanged; expand-500 SI-only 129/230 top-1, 138/230 recall; no CIs; no fverify). External submissions listed after verification.*
