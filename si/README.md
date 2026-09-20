# IRSpectra-Bench supplementary information

Standalone SI for the ICLR manuscript. **Does not count toward the 9-page main.**

- Source: `si/supplement.tex`
- Build: `python3 scripts/build_si.py` (or tectonic on `si/supplement.tex`)
- Output: `si/supplement.pdf`
- Numbers: only locked n=300 / n=194 facts plus
  `docs/NIGHT_POOL_2026-09-20.md` and
  `docs/FVERIFY_EXPAND500_INVENTORY_2026-09-20.md`
  (copied from spectro-agent `cursor/expand-bench-500-b78b`).

**Headline stays n=300.** Exploratory n=524 / n=519 / n=530 are SI/appendix only.
No expand-500 fverify precision. No invented CIs.

## Sections (growth vs the first night stub)

1. Figure / listing map (Fig 1 = `fig1_lead_overview`; Listing 1 = `listing1_irexp_record`; wall = `fig_wall_diagnostic`)
2. Full blind protocol + pre-reg pointers + stopping rules
3. Scoring equations (same 7 identities as the main text; no new metrics)
4. Locked n=194 / +106 / n=300 / n=295 tables with strata
5. expand-500 generation (129/230, 138/230; clean 127/224)
6. Pool options 300 / 524 / 519 / 530 / 295
7. Honest fverify coverage (194 complete; 106 not run; 500 = 31/41)
8. Extra failure / success case panels
9. Prompt skeletons + deposit schema
10. Hyperparameters / model cards / hardware
11. Two-paper split + anonymity
12. Reproducibility checklist + FAQ

## Figure numbering

Does **not** re-number main-text Fig 1 (framework + wall) or Listing 1.
SI reuses those files as extra panels only.
