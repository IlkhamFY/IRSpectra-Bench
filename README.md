# IRSpectra-Bench — ICLR research manuscript

Clean manuscript repository for the **IRSpectra-Bench** ICLR-track paper
(recall/verification diagnosis of LLM structure elucidation).
**Headline:** pooled generation cohort **n=300** (194 locked + all 106 expansion).
Validate-clean **n=295** is appendix / sensitivity. Figure 1 (`fig1_lead_overview`) is the
protocol + recall-bound diagnosis plate. The diagnostic wall
(`fig_wall_diagnostic` / `fig_wall`) is the n=194 instrumented forward-verify slice. A larger expand-500
round is **230/230 deposited and unscored** — see
`docs/EXPAND500_POINTER_2026-09-20.md`. Do not invent a top-1.

**Main Overleaf file:** `main.tex`  
**Compiler:** pdfLaTeX or XeLaTeX (+ BibTeX)  
**Template:** ICLR 2027 conference style (vendored)

## Layout

```
main.tex                    # source of truth (Overleaf main document)
iclr_paper.tex              # compatibility shim: \input{main}
main_IRExpBench_only.tex    # optional orphan alternate; not the ICLR build root
references.bib
iclr2027_conference.sty/.bst
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
