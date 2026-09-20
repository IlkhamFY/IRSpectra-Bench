# IRSpectra-Bench — ICLR research manuscript

Clean manuscript repository for the **IRSpectra-Bench** ICLR-track paper
(recall/verification diagnosis of LLM structure elucidation).
**Headline:** pooled generation cohort **n=500** (194 locked + all 106
expansion + 200 validate-clean expand-500; clean-first, string-sorted
qid, R01–R75 cut): **227/500 (45.4%)** top-1; **249/500 (49.8%)** recall.
List: `docs/headline500_expand200_qids.json`. No CIs. Do not quote 243/519.
Former **n=300** and n=524 / n=530 are appendix / sensitivity. Figure 1 is
the Figma Bro lead plate (`fig1_lead_overview`). Listing 1 is
`listing1_irexp_record`. The diagnostic wall (`fig_wall_diagnostic`)
repeats the locked n=194 slice (58/7/129). expand-500 official fverify
(103/230 vs self 129/230) is SI only — see
`docs/HEADLINE_N500_2026-09-20.md`.

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
figures/                    # Fig 1 = fig1_lead_overview.pdf; Listing 1 = listing1_irexp_record.pdf
si/supplement.tex           # standalone SI (does not count toward 9 pp)
si/supplement.pdf           # compiled SI
docs/LEADERBOARD.md
docs/BENCHMARK.md
docs/SUBMISSION.md
docs/NIGHT_POOL_2026-09-20.md
scripts/build_pdf.py
scripts/build_si.py
OVERLEAF.md
COMMIT_POLICY.md
```

## Build PDF locally

```bash
python3 scripts/build_pdf.py          # main ICLR manuscript
python3 scripts/build_si.py           # standalone SI → si/supplement.pdf
```

The SI holds the full blind protocol, expand-500 / pool tables (headline is n=500),
prompt skeletons, model card, extra cases, official expand-500 fverify
(103/230 vs 129/230; not a wall), and the reproducibility checklist.
Main text stays ≤9 ICLR pages through the Conclusion.

## Fence

This repo is **research/benchmark only**. Do not embed the full IRexp Data Descriptor
Methods / Data Records / licence-pool narrative. Point to the companion Sci Data
paper / anonymised review copy for data details.

## Related

- Companion data paper: `IRexp` (Scientific Data, in preparation)
- Dataset (double-blind review copy): https://anonymous.4open.science/r/peaklist-corpus-review-10C4/
- Named Hugging Face / GitHub hosting is restored at camera-ready; do not put `ilkhamfy/*` URLs in the PDF
