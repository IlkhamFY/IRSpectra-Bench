# Overleaf setup — IRSpectra-Bench (ICLR)

## Recommended: GitHub sync

1. Create GitHub repo `IlkhamFY/IRSpectra-Bench` and push this tree to `main`.
2. Overleaf → **New Project** → **Import from GitHub** → select `IlkhamFY/IRSpectra-Bench`.
3. Menu → **Main document** → `iclr_paper.tex`.
4. Menu → **Compiler** → **pdfLaTeX** (or XeLaTeX).
5. Keep `\iclrfinalcopy` **commented** for anonymous review; uncomment for camera-ready.

## Alternative: zip upload

1. Upload `IRSpectra-Bench-overleaf.zip`.
2. Set main document to `iclr_paper.tex`.
3. Compiler: **pdfLaTeX**.

## Folder structure Overleaf sees

```
iclr_paper.tex
references.bib
iclr2026_conference.sty
iclr2026_conference.bst
fancyhdr.sty
natbib.sty
figures/*.png
```

## What NOT to upload

- Symlinks (none in this tree)
- Full IRexp jsonl dumps / Sci Data sn-jnl manuscript
- Agent scaffolding / cursor branches
- Secrets, tokens, `.env`
- Held-out expert-audit answer keys (if any)

## Notes

- Figures resolve via `graphicspath` to `figures/`.
- Style files are vendored from the ICLR Master-Template.
