# Grok 4.7 re-risk pass

Stance: harsh Area Chair, after P0 honesty (PR #42, on `main`) and this prose pass. No new model runs. Locked integers were not touched. `\iclrfinalcopy` stays off.

Manuscript title is now *Proposal, Not Ranking, Binds Structure Elucidation from Literature Peak Lists*. Conclusion ends on page 9. AI-use statement starts on page 10.

---

## Score

| | reject-risk | verdict |
|---|---|---|
| `docs/GROK47_ICLR_REVIEW.md` (PR #41), before P0 | **68 / 100** | Weak Reject |
| This pass | **54 / 100** | **Borderline** |

Confidence: medium. 54 is not a Weak Accept, and it is not ≤45.

P0 (protocol mix disclosed, two walls named apart, 68–83% removed, four vendors scoped to n=60) was already on `main` before this diff. That removed the self-contradiction tax. It did not remove the empty-comparison tax. This pass spends the remaining prose budget on positioning. A sympathetic AC can now read a coherent diagnostic. A datasets-track AC who still wants a populated board can still land at borderline-reject. Both readings are fair. 54 is the midpoint I will defend. Calling it 45 would be marketing.

**Why it does not go under ~55 without an experiment.** The PDF is one closed-book Claude Opus consumer run, with 200/500 rows from a thinking-tier cut, and no IR-Agent, CASE, Spectro, NMIRacle, Alberts, or SpectraLLM number on these 500 inputs. Reframing that fact is not the same as filling it. Reproducibility of the deposits is real; reproducibility of the inference is not. Those two holes are larger than any remaining sentence.

**The one experiment that would make ≤45 honest.** Score **one external proposer on the same 500 inputs** (formula + printed IR / ¹H / ¹³C lists, not a NIST trace and not an invented adapter) with the released InChIKey-14 script, and print recall and top-1 beside 249/500 and 227/500.

Preferred system: IR-Agent, **only if** it can consume that payload. If the licence or the input makes that a fake port, do not run it. Run a formula-constrained constitutional enumerator that uses only the constraints these tables actually contain, same k≤3 budget or an explicit larger budget, same scorer. A pinned Claude replay with a captured wrapper would fix the methods hole and would **not**, by itself, get under 45. The empty comparison is the larger hole.

---

## What changed

- **Title and abstract.** "A Benchmark" is gone from the title. The abstract says the object is a frozen roster, an InChIKey-14 contract, and replayable deposits, and that trained and tool-using systems are not scored here. 45.4% sits in the same paragraph as corpus-reweighted **26.5%**. Forward verification is named as a secondary drop of 23 (227→204), not as the wall. Four vendors are scoped to the 60-compound arm in the same sentence as formula-only 3/60.
- **Contributions.** Item 1 is the roster and the scorer. Item 4 is "what is not a comparison." The literature-decomposition contribution, which oversold an identity script, is gone.
- **Related work.** Spectro / NMIRacle / Alberts are explicitly not run. The IR-Agent mechanism paragraph stays. The old "intended comparison route" and "on-bench scores left to the scorer" lines are gone. One paragraph, *Not on this roster*, states API / licence / input mismatch and the claim that survives: 251 never proposed, 22 self-rank misses, top-1 227→204. No comparison table.
- **Headline table.** Starred rows put 26.5% [21–32] and 31.3% [25–37] directly under 45.4% / 49.8% / 91.2%, marked as a validate-clean reweight, not an n=500 interval. Results text says 22 of the misses are self-rank and 251 were never proposed.
- **Cross-vendor.** Claude's 14/60 (23%) is written as not the 45.4% headline. The +52.5 / +26.3 / +23.3 / +9.2 contrasts are kept and labelled as different denominators.
- **Harness.** Setup states what is frozen (qids, gold InChIKey-14, JSONL, scorers) and what is not (snapshot, temperature, seed, wrapper; roster not re-drawable). Limitations point at that split instead of apologising twice. Reproducibility statement says: replay the deposits; do not expect a bit-exact subscription rerun.
- **One story.** Abstract, Figure 1 caption, results lead, and conclusion all use generation wall = 227 / 22 / 251. The appendix figure is the forward-verify diagnostic 204 / 45 / 251. "Forward-verify wall" is gone from `main.tex` and from SI prose. SI "propose ≫ verify" slogan is gone.
- **Page budget.** Body through the conclusion is 9 pages. Robustness and mechanism figures stayed on the main text. Literature comparison was shortened, not deleted. SI lost an empty "pre-registered draws" paragraph and retitled that subsection *Frozen roster*.

Integers not changed: 227/500, 249/500, 227/249, 227/22/251, 204/45/251, 26.5% [21–32], 31.3% [25–37], four-vendor table, formula-only 3/60. No 68–83%. No four-vendor claim on n=500. Figure 1 path is still `fig1_lead_overview.pdf`. No PDF/PNG edits.

---

## What still blocks Accept

1. **No same-input external score.** The paper now admits this. Admission is not a baseline. Accept on a benchmark-shaped claim needs at least one other proposer on these lists.
2. **The headline harness cannot be replayed.** No snapshot, no seed, no temperature, wrapper not captured. Scoring the JSONL is reproducible. The 45.4% is a deposit, not a procedure.
3. **The 500 is a mixture.** 200/500 are a thinking-tier expand-500 cut. Disclosed, not separated, not a controlled comparison. A reviewer can still say the headline blends two protocols.
4. **Transport of 45.4%.** The corpus-mix correction is 26.5% on a validate-clean subset, not a reweight of the full 500. The balanced roster still flatters anyone who quotes only the abstract's first percentage — the 26.5% is now adjacent, and it is still the number a careful reader will use against you.
5. **n=60 is doing too much work.** Formula-only, recency, and four vendors are not the cohort the title is about. Candidate budgets differ (2.20 vs 3.00).

---

## Leftover list

### P0 — still open, prose cannot close

- Same-input external proposer on all 500, scored with the released script (the experiment above).
- Pinned snapshot **and** captured headline wrapper, or an explicit decision that the JSONL is the only artifact and the harness claim is retired. The second option is already the prose. It does not satisfy an AC who requires bit-level replay.
- A main-text split of the 200 thinking-tier rows versus the earlier rows, using numbers that already exist. Do not invent a third wall to do it. Until that split is shown, 45.4% is a pooled protocol.

### P1 — real, not reject-by-themselves once P0 is honest

- Reweight 26.5% / 31.3% is not an n=500 figure. Say so everywhere it appears (done). Recompute it on the full roster only if the weights already exist. Do not invent the interval.
- Four-vendor arm stays n=60. Do not promote it.
- No expert-chemist audit. Leave it as a limitation.
- Formula-only is 3/60, not 3/500.
- Literature top-k rows are an identity, not a result. They stay in the SI.
- n=500 headline has no confidence interval. Do not add one.
- Early sampler seeds were not stored. The roster is frozen, not re-drawable. Do not call it pre-registered.
- Stereo, traces, and 2D correlations remain out of the headline by construction.

### Do not do

- Do not restore 68–83%.
- Do not put IR-Agent / CASE / SpectraLLM scores on this bench without a run.
- Do not call 204/45/251 "the wall."
- Do not turn `\iclrfinalcopy` on for double-blind review.
