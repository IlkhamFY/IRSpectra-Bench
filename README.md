# IRSpectra-Bench — ICLR research manuscript

Clean manuscript repository for the **IRSpectra-Bench** ICLR-track paper
(recall/verification diagnosis of LLM structure elucidation).
**Headline:** pooled generation cohort **n=300** (194 locked + all 106 expansion).
Validate-clean **n=295** is appendix / sensitivity. Figure 1 (`fig_wall`) is the n=194
instrumented forward-verify slice. See `docs/POOLED_HEADLINE_2026-09-16.md`.

**Main Overleaf file:** `iclr_paper.tex`  
**Compiler:** pdfLaTeX or XeLaTeX (+ BibTeX)  
**Template:** ICLR 2026 conference style (vendored)

## Layout

```
iclr_paper.tex              # source of truth
references.bib
iclr2026_conference.sty/.bst
fancyhdr.sty, natbib.sty
figures/                    # figures cited by the paper
docs/LEADERBOARD.md
docs/BENCHMARK.md
docs/SUBMISSION.md
scripts/build_pdf.py
OVERLEAF.md
COMMIT_POLICY.md
```

## Build PDF locally

```bash
python3 scripts/build_pdf.py
```

## Fence

This repo is **research/benchmark only**. Do not embed the full IRexp Data Descriptor
Methods / Data Records / licence-pool narrative. Point to the companion Sci Data
paper / anonymised review copy for data details.

## Related

- Companion data paper: `IRexp` (Scientific Data, in preparation)
- Dataset (double-blind review copy): https://anonymous.4open.science/r/peaklist-corpus-review-10C4/
- Named Hugging Face / GitHub hosting is restored at camera-ready; do not put `ilkhamfy/*` URLs in the PDF
