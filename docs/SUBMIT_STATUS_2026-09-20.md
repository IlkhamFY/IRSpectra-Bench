# Submit status — 2026-09-20 (headline n=500)

## Locked paper numbers (Ilkham decision)

- Headline generation **n=500 only**:
  **227/500 (45.4%)** top-1; **249/500 (49.8%)** recall.
  Diagnosis wall: **204 / 45 / 251** (verified / misranked /
  never-proposed). Roster: frozen qid lists.
  Generation source: spectro-agent PR #41 commit `48fcd30`
  (`HEADLINE_n500_2026-09-20.md`).
  Wall source: spectro-agent PR #68 `data/fverify_n500/WALL_n500.md`.
  **No CIs.** Do not print 194/106/200 in main prose.
- Strata n=500: simple 161/248 & 172/248; complex 66/252 & 77/252.
- **Do not quote 243/519**.
- Fig 1 = n=500 fverify (`fig1_lead_overview`: 249/500, 204/249, 40.8%;
  wall 204/45/251). `fig_wall_diagnostic` reprints that wall.
- Instrumented 58/7/129 and expand-500 103/230 stay SI arms.

## expand-500 (NIGHT_POOL; 200 in headline, all-230 in SI)

- **230/230** Opus deposits; `predictions2.jsonl` 230 lines / 690 candidates.
- All-230: **129/230 (56.1%)** top-1; **138/230 (60.0%)** recall@3.
- Clean 224: **127/224 (56.7%)** / **135/224 (60.3%)**.
- Official fverify: 41/41, 681/681; verify **103/230 (44.8%)** vs self
  **129/230**; verify\|recall **103/138 (74.6%)**. **SI arm, not the wall.**
- The 200-cut is a thinking-tier arm — mixed into n=500 with the
  no-thinking 194+106 protocol. Disclose, do not hide.

## Paper

- Fig 1 = `fig1_lead_overview` (protocol + n=500 fverify 249/500,
  204/249, 40.8%; wall 204/45/251). Generation remains 227/500, 249/500.
- Listing 1 = `listing1_irexp_record`.
- Wall diagnostic = `fig_wall_diagnostic` (fverify 204/45/251).
- Instrumented fverify 58/7/129 is SI-only (`fig_wall_fverify_slice`).
- Main compressed so body through Conclusion targets ≤9 ICLR pages.
- Do **not** merge. Do **not** touch ChemRxiv.
