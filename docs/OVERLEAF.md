# Overleaf setup — IRSpectra-Bench (ICLR)

## GitHub sync
1. Import `IlkhamFY/IRSpectra-Bench` from GitHub.
2. Main document: `main.tex` (repo root). `iclr_paper.tex` is a `\input{main}` shim.
3. Compiler: **pdfLaTeX** (or XeLaTeX).
4. Styles resolve via `latexmkrc` → `tex/` (ICLR **2027** sty/bst).
5. After a GitHub Pull: if Overleaf still shows a manual-merge dialog, click Continue
   or discard any leftover `overleaf-*` branch. Do not compile `main_IRExpBench_only.tex`.

## Root (postcard)
`README.md`, `LICENSE`, `main.tex`, `iclr_paper.tex`, `references.bib`, `.gitignore`, `latexmkrc`.

## Folders
- `tex/` — ICLR sty/bst + natbib/fancyhdr
- `figures/`, `scripts/`, `docs/`, `si/`, `cover_letter/`

## Project URL
No `overleaf.com/project/…` URL is stored in this repo. Overleaf is
GitHub-imported from `IlkhamFY/IRSpectra-Bench`. After PR #13, Pull
GitHub (main document = `main.tex`). Lock: `docs/FINAL_SOURCE_OF_TRUTH_2026-09-20.md`.
