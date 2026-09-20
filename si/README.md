# IRSpectra-Bench supplementary information

Standalone SI for the ICLR manuscript. **Does not count toward the 9-page main.**

- Source: `si/supplement.tex`
- Build: `python3 scripts/build_si.py` (or tectonic on `si/supplement.tex`)
- Output: `si/supplement.pdf`
- Numbers: headline n=500 from `docs/HEADLINE_N500_2026-09-20.md`
  (spectro-agent PR #41 `48fcd30`),
  `docs/NIGHT_POOL_2026-09-20.md`, and
  `docs/FVERIFY_EXPAND500_INVENTORY_2026-09-20.md`.

**Headline is n=500** (227/500 top-1; 249/500 recall).
Wall is the generation decomposition **227 / 22 / 251**.
Roster: frozen qid lists. **Do not quote 243/519.** No CIs on n=500.
Official expand-500 fverify: 103/230 verify vs 129/230 self (no CIs; not a wall).
Instrumented fverify is a protocol-slice diagnostic, not the paper wall.

## Sections

1. Figure / listing map (Fig 1 = `fig1_lead_overview`; Listing 1 = `listing1_irexp_record`; wall = `fig_wall_diagnostic`)
2. Visual plate reprints (SI Figs. S1--S3 = n=500 plates)
3. Full blind protocol + frozen-qid pointers + stopping rules
4. Scoring equations
5. Validate-clean extras (not the headline)
6. expand-500 generation (129/230, 138/230)
7. Headline pool n=500 only
8. Honest fverify (protocol-slice diagnostic; official 103/230 vs 129/230)
9. Extra cases, prompts, model card, reproducibility checklist
