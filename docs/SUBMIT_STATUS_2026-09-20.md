# Submit status — 2026-09-20 (night harden)

## Locked paper numbers (unchanged headline)

- Headline generation **n=300** = 194 locked + all 106 Opus (flags included): 118/300 (39.3%) top-1; 133/300 (44.3%) recall.
- Validate-clean **n=295** stays appendix / sensitivity.
- Fig 1 / instrumented fverify stays **n=194 only** (58/7/129; 58/65 = 89%).
- Expansion-106 fverify was **not run**. Do not invent a pooled wall.

## expand-500 (NIGHT_POOL; SI / appendix only)

From spectro-agent `data/benchmark_expand_500/NIGHT_POOL_2026-09-20.md`
(see `docs/EXPAND500_POINTER_2026-09-20.md` and `docs/NIGHT_POOL_2026-09-20.md`):

- **230/230** Opus deposits; `predictions2.jsonl` 230 lines / 690 candidates.
- Generation: **129/230 (56.1%)** top-1; **138/230 (60.0%)** recall@3.
- Clean 224: **127/224 (56.7%)** / **135/224 (60.3%)**.
- Exploratory pools: 524 = 245/524 / 268/524; 519 = 243/519 / 265/519; 530 = 247/530 / 271/530.
- **No CIs.** expand-500 fverify official score: 41/41, 681/681; verify **103/230 (44.8%)** vs self **129/230**; verify\|recall **103/138 (74.6%)**. Clean 103/224 / 103/135. **Not a wall.**
- Deposits used a thinking-tier arm — not interchangeable with the no-thinking headline.
- Headline stays n=300.

## Paper (this night pass)

- Fig 1 = Figma Bro `fig1_lead_overview` (protocol + n=194 wall).
- Listing 1 = `listing1_irexp_record`.
- Wall diagnostic = `fig_wall_diagnostic` (appendix; n=194 only).
- Display equations (1)–(7) used in text.
- Standalone SI grown (`si/supplement.pdf`).
- Main compressed so body through Conclusion targets ≤9 ICLR pages.
- Two-paper split unchanged.

## Still open (human — morning)

- ChemRxiv: Cloudflare handoff (do not burn night time).
- Rodrigo: review density / page-9 / agentic forward-look on this PR.
- Do **not** merge spectro-agent#41 as a silent headline replacement.
- Overleaf: pull this branch after merge, rebuild pdfLaTeX+BibTeX.
