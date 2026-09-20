# IRSpectra-Bench — ICLR research manuscript

Clean manuscript repository for the **IRSpectra-Bench** ICLR-track paper
(recall/verification diagnosis of LLM structure elucidation).
**Headline:** generation cohort **n=500** only: **227/500 (45.4%)** top-1;
**249/500 (49.8%)** recall. Diagnosis wall: **204 / 45 / 251**
(verified / misranked / never-proposed; spectro-agent
`data/fverify_n500/WALL_n500.md`). Generation 227/249/251 is top-1 /
recall / never-proposed, not the wall. Roster: frozen qid lists in the
code release. No CIs. Do not quote 243/519. Do not print 194/106/200
in main prose. Figure 1 is `fig1_lead_overview` (generation). Listing 1
is `listing1_irexp_record`. `fig_wall_diagnostic` is the n=500 fverify
wall. expand-500 official fverify (103/230 vs self 129/230) is an SI arm.

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
prompt skeletons, model card, extra cases, the n=500 fverify wall
(`WALL_n500.md`; 204/45/251) with an optional arm table, expand-500
arm fverify (103/230 vs 129/230), and the reproducibility checklist.
Main text stays ≤9 ICLR pages through the Conclusion.

## Fence

This repo is **research/benchmark only**. Do not embed the full IRexp Data Descriptor
Methods / Data Records / licence-pool narrative. Point to the companion Sci Data
paper / anonymised review copy for data details.

## Related

- Companion data paper: `IRexp` (Scientific Data, in preparation)
- Dataset (double-blind review copy): https://anonymous.4open.science/r/peaklist-corpus-review-10C4/
- Named Hugging Face / GitHub hosting is restored at camera-ready; do not put `ilkhamfy/*` URLs in the PDF
