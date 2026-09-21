# Grok 4.7 rescore after NMRTrans

Stance: harsh Area Chair. Read of `main` at `774633d` (PR #48 merged onto the QC #47 tree). No new model runs. This note does not edit `main.tex` or `si/supplement.tex`. Locked Claude integers stay as deposited.

Prior anchor: the QC #47 memo `docs/CLOSE_MINUSES.md` at `fc15c4b` (dropped from `main` in `69c8c8a`). That memo scored **52 / 100, Borderline**, and named the empty board as the hole that still blocked 45.

---

## Score

| | reject-risk | verdict |
|---|---|---|
| QC #47 (`fc15c4b`), empty board | **52 / 100** | Borderline |
| This pass, NMRTrans on `774633d` | **46 / 100** | **Borderline** |

Confidence: medium. 46 is the midpoint of two readings. Both stay above 45. Both stay far above 10.

- Sympathetic reading: one external proposer is now on all 500, the IR omission and the nine training keys are printed next to 79/500, and what remains is the unreproducible harness plus the pooled protocol. **43.**
- Hostile reading: the PDF still says this roster is not a cross-system comparison; the only external number ignores IR; IR-Agent and CASE are absent; 45.4% is still an unreproducible mix of 39.3% and 54.5%. **49.**

46 is the number I will defend.

## How far NMRTrans moved the empty board

QC #47 bought two points with cross-references and a chamfer heading. It left the board empty. PR #48 is an experiment, and that is a different kind of movement.

Counted from `data/baseline_nmrtrans/hits.jsonl` at `774633d` (500 rows; cohort and difficulty joins to `predictions.jsonl`):

| | top-1 | recall (top 3) |
|---|---|---|
| NMRTrans, all 500 | **79/500 (15.8%)** | **102/500 (20.4%)** |
| simple / complex | 62/248 (25.0%) / 17/252 (6.7%) | 79/248 (31.9%) / 23/252 (9.1%) |
| locked / expansion / expand-500 200-cut | 32/194 / 12/106 / 35/200 | 39/194 / 20/106 / 43/200 |
| Claude headline (unchanged) | 227/500 (45.4%) | 249/500 (49.8%) |

The run is offline CPU inference of `little1d/C-H-Formula` file `nmrtrans-c-h-nmr-formula.ckpt` (sha256 `d184e2280a1623a09b60a052686af343191f9ee99cd89b3570314c15852c4fcd`, 499/499 tensors, code commit `9a72756`), beam 3, `do_sample=False`. Inputs are formula plus printed ¹H and ¹³C. IR was not passed in. Nine gold InChIKey-14 values sit in the released training split (8/9 top-1, 9/9 inside the beam); two sit in validation (1/2 top-1); none sit in the released test split. Held out of those three splits: **70/489 (14.3%)** top-1 and **92/489 (18.8%)** recall. The 79 and 102 were re-counted here. The overlap row, the 86/500 invalid rank-1 SMILES, and the adapter notes are taken from `scores.json` and the SI table, which agree with each other.

A review that says the board has no second proposer is no longer available. The same 500 constitutions, the same InChIKey-14 contract, and a published decoder now sit beside 227/500 and 249/500. The gap runs in the paper's direction on both strata: 79 against 227 overall, 17/252 against 66/252 on complex. Generation failure is no longer a single-harness anecdote.

Movement: **−6** (52 → 46). Four of those points are the procedural fact: full roster, released scorer, hashed checkpoint, no paid API. The other two points of the old seven-point gap down to 45 stay on the table, because the checkpoint does not read IR and the manuscript still says this roster is not a cross-system comparison. A caveated baseline is worth three times the QC prose pass. It is not worth the seventh point.

## Remaining P0 holes

1. **Harness replay.** The Claude headline is still a consumer-subscription deposit. The SI reproducibility section still records no snapshot, temperature, seed, or wrapper. Scoring the deposited JSONL is reproducible. Regenerating 227/500 requires fields that were not recorded. The NMRTrans command line is pinned; the headline command line is not. A pinned Claude replay was already defined as insufficient, by itself, to get under 45. That hole is still open, and it still sits on top of 46.

2. **Thinking mix.** The SI table is the honest split: no-thinking 118/300 (39.3%) top-1 and 133/300 (44.3%) recall; thinking-tier expand-500 cut 109/200 (54.5%) and 116/200 (58.0%). The sums are 227 and 249. The abstract percentage is still the pool. NMRTrans does not show the same jump: 35/200 (17.5%) on the thinking-tier cut against 32/194 (16.5%) on the locked slice. The mix is a property of the Claude headline, and it is still the headline.

3. **IR unused.** The checkpoint has no IR channel, and the runner does not invent one. Main text and SI say so in the same place as 79/500. The task in the title is formula plus printed IR, ¹H, and ¹³C. 79/500 is a formula-plus-NMR number on problems that also contain IR bands. Adapter friction belongs in the same caveat, as deposited: 86/500 rank-1 strings are not valid RDKit SMILES; 76/4298 proton peaks were stored with integral 0; 19 shifts were clamped by the published /220 map; nine Se or Sn formulae are dropped by the 12-element vector. A reader can treat 15.8% as an under-call of an IR-capable model. The PDF has no measurement that closes that reading.

4. **Train overlap.** 9/500 gold keys are in the released training split. Overlap is constitution identity, not a shared peak list. Eight of those nine keys are top-1 hits, so 8 of the 79 successes are constitutions the checkpoint was trained to emit. The comparison number is the held-out row, 70/489 and 92/489. The Claude rate on those same 489 rows is not in the deposit, and this note does not invent it. Disclosure keeps the overlap from being a hidden-leak reject. It keeps 15.8% from being the clean headline.

5. **IR-Agent and CASE are still missing.** SpectraLLM, NMR-Solver, Spectro, NMIRacle, and the Alberts transformers are missing with them. The SI states that NMRTrans is not a score for those systems, and it lists the blockers: NIST absorbance and licence, commercial CASE and the 2D correlations these tables omit, intensities and RAM, search-index size, spectral grids. The experiment named when the score was 54 was IR-Agent on this payload, or a formula-constrained enumerator if that port would be fake. NMRTrans is a third object, a published 1D-NMR decoder. It retires "no external proposer." The systems discussed in related work are still unscored.

## Is ≤45 honest? Is ~10 still fantasy?

**≤45 is not the honest score on this tree.** The condition written at 54 was one external proposer on formula plus the printed IR, ¹H, and ¹³C lists, scored with the released script, with recall and top-1 printed beside 249/500 and 227/500. NMRTrans takes formula and the printed NMR lists. IR is unused by construction of the checkpoint. The same paragraph then says the roster is still not a cross-system comparison. Pricing that deposit at 45 would spend a caveat the manuscript is still carrying. 46 leaves the caveat in the number. The next honest step under 45 is an external proposer that consumes the IR list these tables print, or a formula-constrained enumerator on the constraints the tables contain, on all 500, with the same script. A harness replay without that proposer stays above the line.

**~10 is still fantasy.** A 10 is a PDF whose P0 list is empty: a replayable headline, one protocol inside 227/500, a baseline that sees IR, a train-overlap row that is not carrying successes, and IR-Agent or CASE scored on these lists. Five of those items are open at `774633d`. With a replayable headline and only this NMRTrans deposit, the floor I would defend is the low 40s. Ten needs a different experimental section.

## What this note does not do

- No edit to `main.tex`, `si/supplement.tex`, figures, or `data/baseline_nmrtrans/`.
- No new confidence interval.
- No Claude score recomputed on the 489 held-out keys.
- No 68–83% restored, and no IR-Agent or CASE number written in as a result.
