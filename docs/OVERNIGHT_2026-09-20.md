# Overnight note — 2026-09-20 (ICLR night strengthen)

Headline is **n=500** generation (227/500, 249/500; R01–R75 cut).
Wall is the **n=500 generation decomposition** (227/22/251).
Instrumented fverify stays n=194 (SI protocol-slice).

## What is true this morning

- Source of truth: `main.tex` on `cursor/iclr-night-strengthen-20260920-c33d`.
- **Fig 1** is Figma Bro `fig1_lead_overview` (input → generate → verify + n=500 wall).
  Diagnostic wall is `fig_wall_diagnostic` (227/22/251) in the appendix.
  Listing 1 is `listing1_irexp_record` (IRexp JSON+mol; SMILES/InChIKey are resource fields).
- Abstract / intro / Table 1 lock **227/500 (45.4%)** / **249/500 (49.8%)**. No CIs.
- expand-500 200-cut is **in the headline** (109/200 / 116/200; R01–R75). All-230 129/230 / 138/230 and official fverify 103/230 vs 129/230 stay SI. No CIs. Not a wall. Thinking-tier arm on the 200.
- IRexp remains a companion Sci Data pointer (Listing 1 + Appendix A). Not merged.

## What changed overnight

- Related Work densified into three agentic regimes; then compressed so the body fits 9 ICLR pages through the Conclusion.
- Bottleneck wording: propose ≫ verify.
- Six used display-equation blocks (7 numbered identities): factorisation, InChIKey-14, top-1, recall@k, prec.|recall, 13C chamfer, pooled estimator.
- **Figure pack (Figma Bro):** lead Fig.~1 (`fig1_lead_overview`); Listing 1 (`listing1_irexp_record`); wall (`fig_wall_diagnostic`). Competing `fig_framework` and sibling `fig1_overview` / `fig_listing_mol` builds removed. SI reprints the three canonical files as Figs.~S1--S3.
- Standalone SI (`si/supplement.tex`) grown: protocol, night-pool tables, cases, prompts, model card, fverify gaps, repro checklist.
- Limitations (vi) + FAQ: fverify not on 106; expand-500 official score SI-only (103/230 vs 129/230).

## What still needs Ilkham / Rodrigo

1. Page-9 / 9-page-main visual check on Overleaf after compile.
   Tectonic: Conclusion on page 9; 14 pages total (refs + appendix).
2. ChemRxiv Cloudflare (human; not this pass).
3. Do not merge spectro-agent #41. n=500 integers already copied from `48fcd30`.
4. Key restore only if someone re-scores; `answers2.jsonl` stays out of git.

## Locked facts (do not drift)

| item | value |
|---|---|
| Headline n | **500** (194 + all 106 + 200; R01–R75 cut) |
| Top-1 / recall | **227/500 (45.4%) / 249/500 (49.8%)** — no CIs |
| Fig 1 / wall | n=500 generation; 227/22/251; 249 recalled (49.8%) |
| fverify slice | n=194; 58/65 (89%); 58/7/129 SI protocol-slice only |
| expand-106 fverify | not run |
| expand-500 200 / all | 109/200 / 116/200 in headline; 129/230 / 138/230 SI; fverify 103/230 vs 129/230 SI |
| pools | 500 headline; 300 / 524 / 530 sensitivity; do not quote 519 |
| IRexp | companion pointer only |
