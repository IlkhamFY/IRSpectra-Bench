# Submit status — 2026-09-20 (headline n=500)

## Locked paper numbers (Ilkham decision)

- Headline generation **n=500** = 194 locked + all 106 Opus + 200 of
  expand-500 (clean-first, Python `sorted(qid)`, R01–R75 cut):
  **227/500 (45.4%)** top-1; **249/500 (49.8%)** recall.
  List: `docs/headline500_expand200_qids.json`.
  Source: spectro-agent PR #41 commit `48fcd30`
  (`HEADLINE_n500_2026-09-20.md`). **No CIs.**
- 200-alone: 109/200 (54.5%) / 116/200 (58.0%).
- Strata n=500: simple 161/248 & 172/248; complex 66/252 & 77/252.
- **Do not quote 243/519** (drops flagged +106).
- Sensitivity appendix only: n=524 245/524 / 268/524; n=530 247/530 /
  271/530; former n=300 118/300 / 133/300.
- Fig 1 / wall is the **n=500 generation decomposition** (227/22/251;
  249 recalled, 49.8%). Instrumented fverify 58/65 stays n=194;
  58/7/129 is SI protocol-slice only.
- Expansion-106 fverify was **not run**. Do not invent a pooled fverify wall.

## expand-500 (NIGHT_POOL; 200 in headline, all-230 in SI)

- **230/230** Opus deposits; `predictions2.jsonl` 230 lines / 690 candidates.
- All-230: **129/230 (56.1%)** top-1; **138/230 (60.0%)** recall@3.
- Clean 224: **127/224 (56.7%)** / **135/224 (60.3%)**.
- Official fverify: 41/41, 681/681; verify **103/230 (44.8%)** vs self
  **129/230**; verify\|recall **103/138 (74.6%)**. **Not a wall.**
- The 200-cut is a thinking-tier arm — mixed into n=500 with the
  no-thinking 194+106 protocol. Disclose, do not hide.

## Paper

- Fig 1 = Figma Bro `fig1_lead_overview` (protocol + n=500 generation wall).
- Listing 1 = `listing1_irexp_record`.
- Wall diagnostic = `fig_wall_diagnostic` (appendix; n=500, 227/22/251).
- Main compressed so body through Conclusion targets ≤9 ICLR pages.
- Do **not** merge. Do **not** touch ChemRxiv.
