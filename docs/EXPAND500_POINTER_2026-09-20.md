# expand-500 pointer — 2026-09-20 (ICLR night pass)

Companion source of truth (spectro-agent, not this postcard repo):

- branch: `cursor/expand-bench-500-b78b`
- file: `data/benchmark_expand_500/STATUS.md`
- PR: IlkhamFY/spectro-agent#41 (draft; title still says 55/230 — STATUS is newer)

**Cite only these facts in the ICLR PDF. Do not invent a top-1.**

| item | value |
|---|---|
| draw | 230 compounds; seed 2026500; 115 simple / 115 complex |
| exclusion | 375 prior InChIKey-14s (locked 194 + withheld +106) |
| collisions with prior rounds | 0 InChIKey-14; 0 (formula, IR, ¹³C) |
| pre-solver ¹³C-overread flags | 6 (R26, R31, R102, R105, R107, R138); 224 spectrally clean |
| Opus deposits | **230/230 (100%)** |
| `predictions2.jsonl` | written; 230 lines; 690 candidates |
| `score2` / top-1 / recall | **not run** |
| expand-500 fverify | **not run** |
| expansion-106 fverify | **not run** (unchanged) |
| paper headline | **n=300** (194 locked + all 106). STATUS.md still says n=295 — that lock is stale. |
| key | withheld (`answers2.jsonl` not in tree) |
| protocol note | deposits used `claude-opus-5-thinking-high` — **not** interchangeable with the no-thinking n=300 headline until scored under a declared contract |

Do **not**:

- write an expand-500 top-1, CI, or recall
- draw a pooled n=500 or n=524 wall
- treat 295+224=519 or 300+224=524 as a result
- merge expand-500 into the ICLR headline
- claim expansion-106 fverify
