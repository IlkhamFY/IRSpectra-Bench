# ICLR 2027 requirements check — 2026-09-20

Source: [ICLR 2027 Author Guidelines](https://www.iclr.cc/Conferences/2027/AuthorGuidelines)
and [Call for Papers](https://iclr.cc/Conferences/2027/CallForPapers), read 2026-09-21.
Style: vendored `tex/iclr2027_conference.{sty,bst}` from the official 2027 zip.

Triage companion: `docs/MAIN_VS_SI_TRIM_2026-09-20.md`.
This is a **submit-readiness** check, not a new-experiment or caption pass.

Compiled this branch (tectonic / XeTeX, Liberation Serif fallback):
**11 pp** total; **Conclusion on p.8**; ruler **ON**; anonymous title block.

---

## Desk-reject / format

| requirement | status | note |
|---|---|---|
| Official 2027 sty + bst | **OK** | `tex/iclr2027_conference.sty`, `.bst`. Do not swap in 2026 sty. |
| Main text ≤ **9 pp** at submit | **OK** | Conclusion p.8. Rebuttal / camera-ready = 10. |
| Refs unlimited | **OK** | After statements; p.9–10 here |
| Appendix after bibliography | **OK** | `\appendix` App.~A dataset pointer, App.~B wall + cases |
| Reviewers not required to read appendix | OK | Standalone `si/supplement.pdf` is extra; ICLR prefers one combined PDF at upload |
| Double-blind: no identity in **main or SI** | **OK with flags** | `\iclrfinalcopy` commented; sty prints “Anonymous authors / Paper under double-blind review”. SI `\author{Anonymous authors}`. Review dataset is anon.4open. **Flags below.** |
| Left-margin line-number **ruler ON** | **OK** | Official sty ruler (not `lineno.sty`). IR-Agent’s no-ruler PDF is camera-ready. Do not kill the ruler to “look like theirs”. |
| Running header | **OK** | `Under review as a conference paper at ICLR 2027` |
| `\iclrfinalcopy` off for OpenReview | **OK** | Uncomment only for camera-ready / named arXiv |
| No `[H]`, no `\enlargethispage` | **OK** | Listing 1 is `[!ht]` |

## Required / recommended statements (do not count toward 9 pp)

| item | ICLR 2027 | ours |
|---|---|---|
| **AI use statement** | **Required.** Does not count. | `\section*{AI use statement}` after Conclusion. Solvers ≠ authors; no thinking tier; editing assist disclosed. |
| Ethics statement | Recommended; end of main text before refs; ≤1 p; does not count | Present; OA peak lists + consumer APIs; no human subjects; licence hedge |
| Reproducibility statement | Recommended; before refs; does not count; should *point* not dump protocol | Present; frozen deposits + consumer-harness hedge; `train_no_bench.jsonl.gz` |
| Acknowledgements | Do not count | Blinded NSERC CREATE; named AccelD / 596133-2025 stay in the cover letter |

Statement order: Conclusion → AI use → Ethics → Repro → Ack → bibliography → appendix.
That matches “end of the main text before references”.

Full AI Policy page was not fetched here (guessed URLs 404). The Author Guidelines
require the statement and point at the conference AI Policy for Authors — keep the
section; do not invent extra policy language.

## Section outline vs IR-Agent (compactness, not claims)

ICLR does **not** prescribe numbered section names beyond the statements.
Typical method paper: Intro → Related → Method → Experiments → Conclusion.

| # | IR-Agent (published ICLR 2026 PDF) | this manuscript |
|---|---|---|
| 1 | Introduction (lab IR context + method) | Introduction (peak-list object + factorisation) |
| 2 | 2.1 ML for IR; 2.2 LLM agents | **2.1** trained models; **2.2** agentic regimes; **2.3** heterogeneous / CASE |
| 3 | Method (TI / Ret / SE) | IRSpectra-Bench (task, scoring) |
| 4 | Experiments | Experimental setup |
| 5 | (results in §4) | Results (headline → contamination → vendors → fverify → literature) |
| 6 | — | Discussion (**includes Limitations paragraph**; no extra numbered Limits) |
| 7 | Conclusion | Conclusion |
| * | Ethics (camera-ready 2026) | AI use + Ethics + Repro (2027) |
| App | Supplementary Material after refs | App.~A–B after refs + standalone SI |

**No weird extra sections.** Removed / not reintroduced: Frozen-roster §, reviewer FAQ,
numbered Limitations section, prompt dumps, model cards.

## Anonymity flags (not fixed in this batch)

| item | risk | action |
|---|---|---|
| `\author{…}` McMaster / emails in source | Hidden while `\iclrfinalcopy` is off | Keep flag off for submit |
| SI `spectro-agent` nickname | Was searchable | **Scrubbed** this rebase (generic “code release” / file paths) |
| Anon.4open `peaklist-corpus-review-10C4` | Correct review host | Keep; do not cite `ilkhamfy/IRexp` or private GitHub |
| IRexp bib `Anonymous, 2026` | OK | Restore names only under `\iclrfinalcopy` |
| Cover letter named | Not in the PDF | Fine |

Guideline: “Any paper where author identity is revealed in either the main text or
the supplementary material will be desk rejected.” Cite own arXiv in **third person**
if needed. Related arXiv does not break anonymity.

## Dual submission / companion resource

| item | status |
|---|---|
| Not a second ICLR paper on IRexp | Stated: this paper **cites** the Sci.\ Data descriptor (in prep.); does not re-present Methods / Data Records |
| arXiv of this work | Allowed; do not point at a named author page in the PDF |
| Workshop / non-proceedings | Allowed if applicable |

## Quotas / reviewing (human / OpenReview — not TeX)

| item | owner |
|---|---|
| Abstract deadline 18 Sep 2026 23:59 AoE; paper 25 Sep 2026 23:59 AoE | Authors |
| No add/remove authors after abstract deadline | Authors |
| ≤20 papers / author; reciprocal reviewing | Authors / OpenReview profiles |
| Genuine abstract (no placeholder) | Authors |
| Code zip or anonymous repo encouraged | Release; not this pass |

## Compile / upload

```
# Official look (Overleaf):
pdflatex main && bibtex main && pdflatex main && pdflatex main

# This environment:
PDF_ENGINE=/tmp/tectonic python3 scripts/build_pdf.py
python3 scripts/build_si.py
```

Upload: **one PDF** (main + appendix) as the paper; optional extra
`si/supplement.pdf` + code zip. Do not compile `main_IRExpBench_only.tex`
as the submission root.

## Locked (unchanged by this check)

Descriptive title. Generation **227/500**, **249/500**. Wall **204 / 45 / 251**.
No 194/106/200 in main. No agent names in the PDF.
