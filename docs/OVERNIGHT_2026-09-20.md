# Overnight note — 2026-09-20 (ICLR night strengthen)

No new experimental scores. Headline stays **n=300** generation / **n=194** fverify.

## What is true this morning

- Source of truth: `main.tex` on `cursor/iclr-night-strengthen-20260920-c33d`.
- **Fig 1** is now `fig1_overview` (pipeline + closed-book peak reasoning + n=194 wall).
  The old `fig_wall` stays as a diagnostic figure in §5.4 (same 58/7/129 slice).
  Listing 1 is the IRexp JSON+molecule box (v3-R25; gold held out).
- Abstract / intro / Table 1 still lock **118/300 (39.3%)** / **133/300 (44.3%)**.
- `fig_wall` caption still: locked n=194 only; expansion has no fverify.
- expand-500: **230/230 deposited, unscored** (companion STATUS; local pointer
  `docs/EXPAND500_POINTER_2026-09-20.md`). No top-1 in the PDF.
- IRexp remains a companion Sci Data pointer (Listing 1 + Appendix A). Not merged.

## What changed overnight

- Related Work densified into three agentic regimes (lab tools / spectrum-native
  re-rankers / agentic-search benches). IR-Agent bib → ICLR 2026.
- Bottleneck wording: propose ≫ verify (proposal is the expensive stage).
- §5.6 scale-roadmap paragraph: 230/230 deposits; scoring deferred; thinking-tier
  caveat; not pooled.
- Limitations (vi) + Appendix FAQ: fverify not on 106 **or** 230; no n≈500 top-1.
- Soft-reject memo updated.
- **Figure pack:** lead Fig.~1 (`fig1_overview`: pipeline / peak reasoning / n=194
  wall); old wall kept as §5.4 diagnostic; Listing 1 upgraded to IRexp
  JSON+molecule box. No new metrics.

## What still needs Ilkham / Rodrigo

1. Page-9 / 9-page-main visual check on Overleaf after compile.
   Tectonic build is 14 pages total; Conclusion currently opens page 10
   (Limitations fills page 9). Fig 1 is taller than the old wall. No text was
   cut to fake a 9-page main.
2. ChemRxiv Cloudflare (human; not this pass).
3. Whether to restore the expand-500 key and score **after** ICLR PDF freeze —
   not before, unless you explicitly unlock it. Scoring needs
   `scripts/export_round.py --restore` on spectro-agent; this postcard repo
   cannot re-score.
4. Do not treat STATUS.md's stale “headline stays n=295” line as the ICLR lock.

## Locked facts (do not drift)

| item | value |
|---|---|
| Headline n | **300** (194 + all 106; flags in) |
| Top-1 / recall | **118/300 (39.3%) [34–45] / 133/300 (44.3%) [39–50]** |
| fig_wall / fverify | n=194; 58/7/129; 58/65 (89%) |
| expand-106 fverify | not run |
| expand-500 | 230/230 deposited; **unscored**; no fverify |
| IRexp | companion pointer only |
