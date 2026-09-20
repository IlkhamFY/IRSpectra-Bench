# IRSpectra-Bench supplementary information

Standalone SI for the ICLR manuscript. **Does not count toward the 9-page main.**

- Source: `si/supplement.tex`
- Build: `python3 scripts/build_si.py` (or tectonic on `si/supplement.tex`)
- Output: `si/supplement.pdf`
- Numbers: headline n=500 from `docs/HEADLINE_N500_2026-09-20.md`
  (spectro-agent PR #41 `48fcd30`) plus n=500 generation wall,
  `docs/NIGHT_POOL_2026-09-20.md`, and
  `docs/FVERIFY_EXPAND500_INVENTORY_2026-09-20.md`.

**Headline is n=500** (227/500 top-1; 249/500 recall). 200-cut:
`docs/headline500_expand200_qids.json` (clean-first, string-sorted,
R01–R75). Former n=300 and n=524 / n=530 are SI/appendix only.
**Do not quote 243/519.** No CIs on n=500.
Official expand-500 fverify: 103/230 verify vs 129/230 self (no CIs; not a wall).
Wall is n=500 generation (227/22/251). Old fverify 58/7/129 is SI protocol-slice only.

## Sections

1. Figure / listing map (Fig 1 = `fig1_lead_overview`; Listing 1 = `listing1_irexp_record`; wall = `fig_wall_diagnostic`)
2. Visual plate reprints (SI Figs. S1--S3)
3. Full blind protocol + pre-reg pointers + stopping rules
4. Scoring equations
5. Former n=300 / +106 / n=295 tables
6. expand-500 generation (129/230, 138/230; 200-cut 109/200)
7. Pool options **500** / 300 / 524 / 530 / 295
8. Honest fverify (194 protocol-slice 58/7/129; 106 not run; 500 official 103/230 vs 129/230)
9. Extra cases, prompts, model card, reproducibility checklist
