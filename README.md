# IRSpectra-Bench — ICLR research manuscript

Clean manuscript repository for the **IRSpectra-Bench** ICLR-track paper
(recall/verification diagnosis of LLM structure elucidation).

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
paper / HF dataset for data details.

## Related

- Companion data paper: `IRexp` (Scientific Data)
- Dataset: https://huggingface.co/datasets/ilkhamfy/IRexp
- Historical monorepo: https://github.com/IlkhamFY/spectro-agent
