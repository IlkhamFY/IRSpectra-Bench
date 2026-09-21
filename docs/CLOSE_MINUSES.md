# Closed minuses — 21 September 2026

Manuscript QC on `main` after the appendix move (`5edbce9`).
No new model calls. No IR-Agent, CASE, SpectraLLM, or NMR-Solver score.
Locked integers were not rewritten:

| item | value |
|---|---|
| top-1 | 227/500 |
| recall | 249/500 |
| self-rank | 227/249 |
| generation wall | 227 / 22 / 251 |
| forward-verify diagnostic | 204 / 45 / 251 |

Title is unchanged. Main text ends at the conclusion on page 9; references start on page 10. Appendix material stays in `si/supplement.tex`. The thinking-tier expand-500 cut (200 of 500) is not described as a no-thinking run.

## Closed in this diff

- **Stale equation pointer.** The SI said the scoring displays matched main-text Eqs. (1)–(7). Main has Eqs. (1)–(6). The pool estimator is SI-only, and the SI now says so.
- **Dangling limitation number.** The prompt section cited “Limitations (i)” after that list was folded into one paragraph. It now points at Experimental setup and Limitations.
- **Orphan appendix label.** `\label{app:dataset}` is gone. The IRexp pointer is `\label{si:split}`.
- **Literature table pointer.** The cross-reference map pointed at the forward-verify section for a table that lives under literature comparison (`si:lit`).
- **Chemspace denominator.** `figures/fig_chemspace.pdf` is the validate-clean plate (locked + clean expansion, legend “locked” / “expansion”, generator `n=295`). The caption and the main-text pointer called it the `n=500` cohort. Median MW 306 and median 2 rings stay attached to that plate. The thinking-tier cut is stated as absent from it.
- **Chamfer versus self-rank.** On the 60-compound arm, Claude self-rank top-1 is 14/60 and recall is 19/60. The 16/19 cell is chamfer forward-verify, the same quantity as the other three vendor rows (`scripts/cross_vendor_gap.py` in spectro-agent: “did the chamfer re-rank put it first”). The table heading now says chamfer. 16/19 does not multiply with 19/60 to 14/60.
- **Protocol-slice rounding.** 65/194, 55/194, and 58/194 are printed as 33.5%, 28.4%, and 29.9%, matching the headline lock and the literature row. The integers are unchanged. 58/65 is 89.2% in both SI tables.
- **Figure paths.** Every `\includegraphics` target exists: `fig1_lead_overview.pdf`, `fig_robustness.pdf`, `fig_mechanism.pdf`, `fig_chemspace.pdf`, `fig3_method.pdf`, `fig_wall_diagnostic.pdf`, `listing1_mol_pubchem3d.png`. Fig. 1 draws generation 249/500, 227/249, 45.4%, and 227/22/251. The forward-verify plate is `fig_wall_diagnostic.pdf` (204/45/251). No tex comment calls a figure a soft placeholder.
- **Robustness plate versus the four-vendor table.** The figure also draws Composer 2.5 (12/60), GPT-5.6 Luna (9/60), DeepSeek V4 Pro (8/60, partial formula gate), and Nemotron 3.5 (0/60). The caption says those four are not table rows, and that the scatter is chamfer.
- **Process captions and reviewer lines.** Cut “moved to keep the ICLR body on budget”, “home of the table moved off the ICLR body”, “the claim that does not need those systems”, “adapter invented so their names can sit in a results table”, “not a board of elucidators”, and “Do not expect a bit-exact regeneration”.
- **Underfull claims that had no number.** The n=24 ladder no longer asserts an unshown nesting or an unnamed protocol asymmetry. The unnamed “named-ring annotation” sentence is gone. The 137-miss denominator for 76.6% / 22.6% is in the main text, as in the SI.
- **Two protocols inside 227/500.** SI table: no-thinking 118/300 (39.3%) and 133/300 (44.3%); thinking-tier 109/200 (54.5%) and 116/200 (58.0%). Sums are 227 and 249. Not a second headline, and not printed as a 194/106/200 split in the main prose.
- **PDF identity leak.** The Spectro bibliography entry printed coauthor names. The review PDF now says Anonymous, with the names kept in a source comment for camera-ready. `pdftotext` on `main.pdf` has no Yabbarov, Sondhi, Vargas, or McMaster.
- **Foreign bibliography block.** Uncited CSI:FingerID, ACD/SE history, CASMI, MSNovelist, and the generic spectroscopy-review entries that belonged to the other manuscript are removed. Cited `buevich2016synergistic` stays.
- **SI build.** `scripts/build_si.py` falls back to pdfLaTeX, same as the main build. Both PDFs compile. The SI log has no overfull or underfull box. Main has two residuals, below.
- **Offline contrast, one sentence.** SI reproducibility: external systems were not run (input, licence, or compute); formula-only recovery is 3/60 top-1 and 3/60 recall.

## Not closed

These were not given a score.

- **Same-input external proposer on all 500.** IR-Agent wants a NIST absorbance vector and a copyrighted library. SpectraLLM wants intensities and does not fit in this machine. NMR-Solver’s search index does not fit on disk. Commercial CASE is unlicensed, and open correlation CASE wants 2D spectra this roster does not have. Spectro, NMIRacle, and the Alberts transformers want spectral grids or traces. No adapter was built. Not re-run here.
- **Formula enumerator past heavy atoms ≤ 12.** Draft PR #44 already ran MAYGEN 1.8 on the 31 headline compounds at that cap: 15 formulas exhausted with gold InChIKey-14 in 15/15, and chamfer top-1 4/5 on the five sets of at most 80,000 constitutions. Pilots above 12 heavy atoms did not exhaust. That subset is not an n=500 result, and it was not extended on this VM. The SI does not quote 15/31 or 4/500.
- **Bit-exact replay** of the consumer harness (snapshot, temperature, seed, wrapper).
- **Expert-chemist audit** and the abandoned leave-one-modality arm.
- **n=24 ladder counts.** The leaderboard’s rounded percents were not turned back into integers.
- **Fig. 1 file.** It is a 300 dpi JPEG (no font layer), with the generation integers above. It was not redrawn.
- **Main title underfull** (badness 1210) from the locked title’s line break. The wording was not changed.
- **Page 2 underfull vbox** (badness 10000) under the short Fig. 1. The page still has the figure and the surrounding section; the float does not fill the `\flushbottom` page.

## Reject-risk after this diff only

**52 / 100.** Borderline. Same decision as the prior 54.

This diff does not put a second proposer on the 500 inputs. That hole, the unreproducible subscription run, and the fact that 45.4% pools a 39.3% no-thinking block with a 54.5% thinking-tier block are still the paper. Showing the split is the honest reading of 45.4%, not a reason to hide it. A reviewer who wants a populated board is not answered by cleaner cross-references.

What did move is self-inflicted contradiction: chamfer 16/19 presented as if it factorised to self-rank 14/60, a 295-compound plate captioned as n=500, and a pointer at a main-text equation that is not there. Those are worth about two points. They are not worth calling the paper a 45.
