# Prose pass — 2026-09-15 (v0.5)

Point-fix polish of `iclr_paper.tex` (abstract through limitations / closing matter). No figure redesign. Ack AccelD / NSERC 596133-2025 left intact. IRexp kept as companion *Scientific Data* Data Descriptor (in preparation) with HF mirror pointer — no Data Descriptor re-presentation.

## Changes

1. **Abstract** — "Generating wider lifts recall…" → "Generate-wide sampling lifts recall…" (match forward-verify section label).
2. **Introduction** — colon + imperative ("take … recover") → gerunds ("taking … recovering").
3. **Related work (Espejo)** — comma splice "they ask which architecture, we ask which stage" → "…architecture, while we ask which stage".
4. **Benchmark (task inputs)** — "annotation does not carry the headline" → "named-ring annotation does not drive the headline numbers".
5. **Primary metrics note** — "CIs are bootstrap 95%" → "Confidence intervals are bootstrap 95%".
6. **Discussion** — broken "What compounds is open experimental data…" → "Those gains compound with open experimental data…".
7. **Conclusion** — "Data Descriptor (in prep.)" → "Data Descriptor (in preparation)" (match dataset pointer / bib note).
8. **Appendix** — "Supplementary figures currently shared with the combined manuscript under" → "Supplementary figures archived under" (drop combined-paper leftover).

## Checked, left unchanged

- Author block + `\iclrfinalcopy` + restored "Under review…" running header (intentional named under-review hybrid; not flipped to blind or to "Published as…").
- AccelD / NSERC funding reference 596133-2025 acknowledgement.
- IRexp cite carefulness: companion Sci. Data / in preparation; this ICLR paper cites that resource and does not re-present a Data Descriptor; Related work + Limitations still state Spectro / NMIRacle / Alberts IR transformers / CASE **not scored** on-bench.
- No on-bench score claims for those missing baselines; ladder gains still framed as diagnostic (p=0.55 / p=0.34).
- British spellings (digitised, centre, analysable) kept consistent.

## Remaining blockers

1. **ORCID** — not in author block / footnotes.
2. **Zenodo** (or equivalent archival DOI) — not linked for frozen predictions / code release; HF `ilkhamfy/IRexp` only.
3. **Blind vs final** — authors visible under `\iclrfinalcopy` while `\lhead` still says under review; for true double-blind submission revert to anonymous author and drop `\iclrfinalcopy`; for camera-ready keep authors and drop the under-review `\lhead` override (sty default "Published as…").
