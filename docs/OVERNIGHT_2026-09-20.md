# Overnight note — 2026-09-20 (ICLR night strengthen)

Headline stays **n=300** generation / **n=194** fverify.

## What is true this morning

- Source of truth: `main.tex` on `cursor/iclr-night-strengthen-20260920-c33d`.
- **Fig 1** is Figma Bro `fig1_lead_overview` (input → generate → verify + n=194 wall).
  Diagnostic wall is `fig_wall_diagnostic` (same 58/7/129 slice) in the appendix.
  Listing 1 is `listing1_irexp_record` (IRexp JSON+mol; SMILES/InChIKey are resource fields).
- Abstract / intro / Table 1 still lock **118/300 (39.3%)** / **133/300 (44.3%)**.
- expand-500 is **generation-scored** in appendix + SI only: **129/230 (56.1%)** top-1, **138/230 (60.0%)** recall; clean **127/224**. No CIs. No fverify precision. Thinking-tier arm. Not the headline.
- IRexp remains a companion Sci Data pointer (Listing 1 + Appendix A). Not merged.

## What changed overnight

- Related Work densified into three agentic regimes; then compressed so the body fits 9 ICLR pages through the Conclusion.
- Bottleneck wording: propose ≫ verify.
- Six used display-equation blocks (7 numbered identities): factorisation, InChIKey-14, top-1, recall@k, prec.|recall, 13C chamfer, pooled estimator.
- **Figure pack (Figma Bro):** lead Fig.~1 (`fig1_lead_overview`); Listing 1 (`listing1_irexp_record`); wall (`fig_wall_diagnostic`). Competing `fig_framework` and sibling `fig1_overview` / `fig_listing_mol` builds removed. SI reprints the three canonical files as Figs.~S1--S3.
- Standalone SI (`si/supplement.tex`) grown: protocol, night-pool tables, cases, prompts, model card, fverify gaps, repro checklist.
- Limitations (vi) + FAQ: fverify not on 106; expand-500 fverify incomplete (31/41).

## What still needs Ilkham / Rodrigo

1. Page-9 / 9-page-main visual check on Overleaf after compile.
   Tectonic: Conclusion on page 9; 14 pages total (refs + appendix).
2. ChemRxiv Cloudflare (human; not this pass).
3. Do not merge spectro-agent #41 as a silent headline replacement.
4. Key restore only if someone re-scores; `answers2.jsonl` stays out of git.

## Locked facts (do not drift)

| item | value |
|---|---|
| Headline n | **300** (194 + all 106; flags in) |
| Top-1 / recall | **118/300 (39.3%) [34–45] / 133/300 (44.3%) [39–50]** |
| Fig 1 / fverify | n=194; 58/7/129; 58/65 (89%) |
| expand-106 fverify | not run |
| expand-500 | 129/230 / 138/230; clean 127/224; SI/appendix only |
| pools | 300 headline; 524 / 519 / 530 exploratory |
| IRexp | companion pointer only |
