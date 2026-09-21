# IRSpectra-Bench

ICLR manuscript: recall/verification diagnosis of LLM structure elucidation.

**Headline:** generation cohort **n=500** — **227/500 (45.4%)** top-1;
**249/500 (49.8%)** recall. Generation wall: **227 / 22 / 251**.
Forward-verify diagnostic (appendix only): **204 / 45 / 251**.
Corpus-reweighted top-1 (validate-clean, not n=500): **26.5%**.
No CIs. Do not quote 243/519.

**Main file:** `main.tex`  
**Compiler:** pdfLaTeX or XeLaTeX + BibTeX  
**Style:** ICLR 2027 (`tex/iclr2027_conference.sty`)

## Layout

```
README.md  LICENSE  main.tex  references.bib  latexmkrc  .gitignore
cover_letter/
figures/            # 6 PDF plates + Listing 1 PubChem PNG
scripts/
si/supplement.tex
tex/                # ICLR 2027 sty/bst, fancyhdr, natbib, listing1_body
```

Figure PDFs: `fig1_lead_overview`, `fig_chemspace`, `fig_robustness`,
`fig_mechanism`, `fig3_method`, `fig_wall_diagnostic`.
Listing 1 molecule art: `figures/listing1_mol_pubchem3d.png` (included
via `tex/listing1_body.tex`).

## Build

```bash
python3 scripts/build_pdf.py          # main ICLR manuscript
python3 scripts/build_si.py           # standalone SI (does not count toward 9 pp)
```

## Fence

Research/benchmark manuscript only. Do not embed the full IRexp Data
Descriptor narrative. Point to the companion Sci Data paper / anonymised
review copy for data details.

## Related

- Companion data paper: `IRexp` (Scientific Data, in preparation)
- Dataset (double-blind review copy): https://anonymous.4open.science/r/peaklist-corpus-review-10C4/
- Named Hugging Face / GitHub hosting is restored at camera-ready; do not put `ilkhamfy/*` URLs in the PDF
