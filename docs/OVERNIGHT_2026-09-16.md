# Overnight note — 2026-09-16 (v0.10)

Blind-safety + prose pass on `iclr_paper.tex` after PR #2 dropped the difficulty-bar figure. **No new experimental claims. Headline stays n=194.**

## Status (what is true this morning)

- Source of truth: `iclr_paper.tex` on `main` once this release merges (`release v0.10`).
- `\iclrfinalcopy` remains **commented off**. Compiled PDF prints **Anonymous authors / Paper under double-blind review** and the ICLR left-margin submission ruler. Running header: *Under review as a conference paper at ICLR 2026*.
- Companion bib `yabbarov2026irexp` is **Anonymous**. Dataset URL in the PDF is only  
  `https://anonymous.4open.science/r/peaklist-corpus-review-10C4/`  
  Private `IlkhamFY/peaklist-corpus-review` and `ilkhamfy/IRexp` do **not** appear in the PDF.
- Acknowledgements stay grant-number-free / McMaster-free (NSERC CREATE training program only). Cover letter still has the Rodrigo McMaster template + NSERC 596133-2025 — that is for chairs, not the anonymous PDF.
- Diagnosis wall is **Figure 1** (lead figure). `fig1_difficulty` is **not** cited. Files still sit unused in `figures/fig1_difficulty.{png,pdf}` — do not re-add.
- Compiled check (tectonic, 11 pages): 0 undefined refs; 0 `Yabbarov` / `ilkhamfy` / `huggingface` / `McMaster` hits in PDF text. Main text through reproducibility ends on **p.8**; ethics/acks + refs + appendix occupy p.9–11. Within a 9-page main-body budget if refs/appendix are excluded.
- **+106 expansion:** spectro-agent branch `claude/funny-maxwell-u5S31` is still writing Opus batches (latest visible: `single_R22`, 2026-09-14). **No pooled n=300 artefacts exist in this repo.** Leaderboard and manuscript stay n=194.

## What changed overnight (prose / consistency only)

- Grammar: missing *is* in the 50/50 vs reweighted sentence; “operational setting” → “task”; “scoring is:” → “Scoring is reproducible”; “it gets 30/37” given an explicit subject; conclusion no longer “recovers from” / “mirrored at a mirror”.
- Abstract now labels the formula-only / generate-wide numbers as the **n=60** arm (headline n=194 unchanged).
- Appendix no longer points at missing `docs/figures/` archive plates or `docs/archive/combined_PAPER.md`. Dataset pointer stays the anonymous.4open URL.
- Stale `iclr_paper.bbl` had been the **named** companion entry (`Yabbarov, Sondhi, Vargas-Hernández`). Rebuilt so a copy-paste bbl cannot leak identity. Regenerated `scripts/build_pdf.py` now puts `tex/` on `TEXINPUTS`.
- README + leaderboard dataset pointer: anonymous.4open, not `huggingface.co/datasets/ilkhamfy/IRexp`. Leaderboard carries an explicit **do not pool to n=300** lock.

Numbers in tables/abstract (28.4% / 15.2% / 34% / 89% (58/65) / formula-only 23%→5% / generate-wide 32%→42%) were **not** rewritten.

## Morning checklist

1. **Merge** this `release v0.10` PR to `main` (or cherry-pick if you want a direct main bump). Overleaf: pull GitHub.
2. Rebuild PDF on Overleaf (pdfLaTeX + BibTeX). Confirm bibliography sorts **Anonymous (2026)** for IRexp, not Yabbarov. Confirm Figure 1 is still the diagnosis wall.
3. **Do not** change headline n or CIs to 300 unless `spectro-agent` `claude/funny-maxwell-u5S31` has a complete pre-reg score dump **copied into this repo**. If that dump arrives, a separate release should update tables, CIs, wall figure, and limitations (vi) together.
4. `docs/ICLR_PAPER.md` is a **stale markdown snapshot** (still has `fig1_difficulty` and `ilkhamfy/IRexp`). Do not copy it into Overleaf. Either ignore it or sync it from TeX after submit.
5. This postcard repo still lacks frozen predictions / `scripts/score_submission.py` / `data/train_no_bench.jsonl.gz` (they live in spectro-agent). The paper now says “code release” rather than “this repository.” Decide the anonymous code dump URL before submit.
6. Camera-ready only: uncomment `\iclrfinalcopy`, **delete** the `\lhead{Under review…}` override, restore named IRexp bib + HF URL + full acknowledgements (see `docs/ANONYMITY_ICLR.md`).
7. Optional polish (not blockers): table overfulls ~2–4 pt; literature table underfulls; Spectro bib still lists Sondhi / Vargas-Hernández (published prior work — leave it).
8. Cover letter is ready as-is (named, funded). Do not paste it into the anonymous PDF zip.

## Locked facts (do not drift)

| Item | Value |
|---|---|
| Headline n | 194 |
| Top-1 / reweighted | 28.4% [22–35] / 15.2% |
| Recall / precision \| recall | 34% (65/194) / 89% (58/65) |
| Lead figure | `fig_wall` (diagnosis) |
| Dataset URL in PDF | anonymous.4open `…/peaklist-corpus-review-10C4/` |
| `\iclrfinalcopy` | OFF |

---

# Overnight note — 2026-09-16 (v0.11)

Independent pre-registered **+106 expansion** is now locally scored (Opus). Reported as a
**separate, non-headline** replication. **Headline stays n=194.** Do not pool to n=300.

## Expansion facts (locked; do not round further)

| Item | Value |
|---|---|
| Draw | n=106 pre-registered blind compounds |
| Scoring | RDKit InChIKey-14 (constitution) |
| Opus top-1 | **63/106 (59%)** |
| Opus generation recall | **68/106 (64%)** |
| Spectral validation | 101/106 clean; **5× ¹³C-overread flags** |
| Clean subset | top-1 **61/101 (60%)**, recall **65/101 (64%)** |
| Forward-verify on expansion | **not run** |
| Fable cross-model arm | **incomplete (68/106)** |
| Headline cohort | **n=194** until pooling is explicitly approved |
| Pooling | licensed by pre-reg; **deferred** pending forward-verify + clean-flag handling |

Source run: spectro-agent branch `claude/funny-maxwell-u5S31`. No pooled n=300 artefacts
in this repo. Expansion top-1 is higher than the locked 28.4% headline; the paper frames
that as **found on a new draw**, not as replacing the n=194 diagnosis.

## What changed overnight (v0.11)

- `iclr_paper.tex`: new Results subsection **§5.6 Pre-registered expansion** with the
  exact counts above, plus Appendix B Table `tab:expansion`. One sentence each in
  Discussion and Limitations (vi) that pooling is licensed but deferred and the
  headline tables/CIs/Figure 1 stay n=194.
- Headline Table 1, abstract, contributions, wall figure, and n=194 CIs **unchanged**.
- Double-blind locks unchanged: `\iclrfinalcopy` OFF; companion bib Anonymous; dataset
  URL only `https://anonymous.4open.science/r/peaklist-corpus-review-10C4/`; no
  `ilkhamfy` / Hugging Face personal URLs in the PDF.
- `docs/LEADERBOARD.md`: separate expansion block, explicitly **non-headline**.
- `scripts/build_pdf.py`: Tectonic now gets `-Z search-path=tex/` (TEXINPUTS is ignored).

## Compiled check (tectonic, 11 pages)

- Anonymous authors / Paper under double-blind review; running header *Under review as a conference paper at ICLR 2026*.
- 0 undefined refs; 0 `Yabbarov` / `ilkhamfy` / `huggingface` / `McMaster` hits in PDF text.
- Companion bib prints **Anonymous (2026)** for IRexp.
- Dataset URL is only the anonymous.4open review copy (line-wrapped in the PDF).
- Figure 1 remains the n=194 diagnosis wall. Table 1 remains n=194 28.4% / 33.5%.
- §5.6 + Appendix B Table 6 carry the expansion counts and the pooling-deferred sentence.
- Main text through conclusion / reproducibility / ethics / acks lands on **p.9**; refs + appendix occupy p.9–11.

## Morning checklist (v0.11)

1. **Open PR, do not merge** unless trivially safe. Prefer morning human review: the
   expansion rate (59%) is much higher than 28.4% and is easy to misread as a new
   headline.
2. Rebuild PDF on Overleaf. Confirm Figure 1 is still the n=194 diagnosis wall; Table 1
   still n=194; new expansion table is labelled independent / not pooled.
3. Blind scan: Anonymous authors; bibliography **Anonymous (2026)** for IRexp; 0
   `Yabbarov` / `ilkhamfy` / `huggingface` / `McMaster` in PDF text.
4. **Do not** rewrite headline n or CIs to 300. Pooling still waits on (i)
   forward-verify on the 106, (ii) clean-flag handling of the 5 ¹³C-overread
   records, (iii) explicit pooling approval. Fable arm is incomplete (68/106) and
   must not be scored as a full expansion row.
5. Frozen expansion predictions / score dump live in spectro-agent, not this postcard
   repo. Copy them in before any pooled-n rewrite.

## Locked facts (do not drift)

| Item | Value |
|---|---|
| Headline n | 194 |
| Headline top-1 / reweighted | 28.4% [22–35] / 15.2% |
| Headline recall / precision \| recall | 34% (65/194) / 89% (58/65) |
| Expansion n (non-headline) | 106 (clean 101) |
| Expansion Opus top-1 / recall | 63/106 (59%) / 68/106 (64%) |
| Lead figure | `fig_wall` (diagnosis, n=194) |
| Dataset URL in PDF | anonymous.4open `…/peaklist-corpus-review-10C4/` |
| `\iclrfinalcopy` | OFF |

