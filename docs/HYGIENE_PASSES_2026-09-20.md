# Hygiene passes — 2026-09-20 night / 2026-09-21 morning

Compiled surface only (`main.tex`, `si/supplement.tex`, `cover_letter/cover_letter.tex`).
No new experiments, numbers, or ablations. Locked metrics unchanged:
generation **227/500** and **249/500**; forward-verify **204 / 45 / 251**.

## Pass 1 — agent / AI artifacts

Removed from the SI PDF source (none were in `main.tex` or the cover letter):

- `spectro-agent` tree name, commit `48fcd30`, and companion-repo pointers
- dated lock-memo filenames (`HEADLINE_N500_2026-09-20.md`, `NIGHT_POOL_2026-09-20.md`, `POOLED_HEADLINE_2026-09-16.md`, `SUBMISSION.md`)
- `/tmp/blind/_key/` restore/delete diary and `answers2.jsonl` working-tree notes
- `collect_round.py` / `validate_benchmark.py` / `prep` “was not run” ops list
- tectonic compile recipe and engine version
- “Fable incomplete arm” model-card row (rephrased; n=24 Haiku ⊂ … ⊂ Fable ladder kept)
- leftover `thinking-high` jargon (already gone; `thinking-tier` kept as the protocol label)

Not found on the compiled surface (left untouched): Figma Bro, Chem Partner, Cursor, OpenClaw, Jarvis, Anode, postcard, reviewer FAQ, “as a reviewer”, TODO/FIXME.
Grok 4.6 remains the vendor-arm model name (locked table).

## Pass 2 — tone

- Cut “honest account” / “state honestly” honest-gaps asides
- Cut “swing wildly” and “next ICLR-relevant agent is a proposer” (body only)
- Main-text 204/45/251 integers kept in contributions, setup, results, limitations (vi), and conclusion (scientific meat; not hollowed)
- SI source/map chatter still cut
- Discussion hedge kept: nonsignificant ladder steps are not an accuracy headline
- No IR-Agent industry padding added. Existing closest-concurrent contrast kept
- `\title`, section titles, and every `\caption{...}` left at `570a124` (#25 polish + #27 2.1–2.3 / Limitations-as-Discussion)
- Rebased onto `main` @ `570a124`; #27 main→SI trim kept (setup wall reprint already dropped there)

## Pass 3 — consistency

- Listing 1 captions already below the framed plate (main + SI); left as-is
- No `[H]`, no `\enlargethispage`
- Descriptive title unchanged
- Table captions remain ICLR-standard (above the tabular)
- Locked metrics only; no new integers

## Pass 4 — anonymity (main / SI)

- Neutralized SI `spectro-agent` / commit-hash / night-memo crumbs
- IRexp bib stays `Anonymous`; dataset URL stays anonymous.4open
- Author block still gated on `\iclrfinalcopy` (commented)
- Cover letter remains named (McMaster letterhead; not double-blind)

## Pass 5 — light intro

One sentence: “honest account of which stage binds” → “measurement of which stage binds”.
No added lab-context paragraph.

## Left alone (not PDF)

`main_IRExpBench_only.tex`, `docs/*` lock memos, `si/README.md` operator notes, figures.
Cover letter already clean; no edits.
