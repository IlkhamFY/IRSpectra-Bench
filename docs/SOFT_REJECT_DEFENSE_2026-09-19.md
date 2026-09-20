# Soft-reject defense — 2026-09-19

Manuscript pass on `iclr_paper.tex` for ICLR 2027 (full-paper deadline 2026-09-25 AoE).
No new experimental numbers. No thinking-high / Opus re-solves.

Locked facts used (do not invent beyond these):

| item | value |
|---|---|
| headline n | 300 = 194 locked + all 106 expansion |
| top-1 / gen. recall | 118/300 (39%); 133/300 (44%) |
| reweighted top-1 | 27% (26.5% on validate-clean n=295) |
| fig_wall / fverify | n=194 only: 58 verified / 7 mis-ranked / 129 never proposed; 58/65 = 89% |
| expansion vs locked top-1 | 59% vs 28% (63/106 vs 55/194) |
| solver | Claude Opus consumer harness; no thinking tier; no snapshot |
| IRexp | companion resource pointer, not a co-headline Data Descriptor |

## Top reviewer attacks (and where the PDF answers them)

1. **“39% top-1 vs a grim wall — they pooled a hidden easy set.”**
   Abstract, Table 2, §5.6, Limitations (vi), Fig.~1(c) / wall captions, Appendix FAQ.
   Expansion is easier (59% vs 28% top-1) and is **disclosed**. The wall is **not**
   an n=300 figure.

2. **“fig_wall / 89% is the n=300 result.”**
   Fig.~1 is the protocol plate; panel (c) and the later diagnostic wall caption
   say explicitly: locked n=194 only; not a pooled n=300 wall; expansion has no
   fverify. 58/65 stays on that slice.

3. **“Consumer Claude, no snapshot, not reproducible — reject.”**
   Setup + Limitations (i) + FAQ. Inference is not bit-exact; **scoring** of frozen
   deposits is. No thinking tier; we do **not** recommend thinking-high as a
   revision path.

4. **“Why no SpectraLLM / IR-Agent / CASE SOTA table?”**
   Related work now contrasts **setting**: SpectraLLM = fine-tuned on
   simulated/standardised multi-spectral corpora (QM9S; Alberts USPTO multimodal);
   IR-Agent = NIST IR + re-rank a proposed pool; curated/education benches are
   cleaner objects. This paper is literature peak lists + off-the-shelf + stage
   split. None of those systems is scored here. Limitations (v): no method SOTA chase.

5. **“IRexp is a second paper stuffed into this PDF.”**
   Abstract / intro pointer retitled **resource, not co-headline**. Listing 1
   credits IRexp as the band-list source. Appendix A remains a pointer, not a
   Data Descriptor dump.

6. **“fverify on 106 is missing, so the diagnosis is incomplete.”**
   Stated in Limitations (vi) and FAQ. Self-ranking precision on the pooled
   generation cohort (118/133) is **not** interchangeable with 58/65.

7. **“They are claiming a solved elucidator / accuracy advance.”**
   Abstract lead is proposal ≪ verification. Ladder p=0.55 / p=0.34 stay
   diagnostic. Title already matches the claim.

8. **“Wrong ICLR year / desk-reject style.”**
   Official ICLR 2027 sty/bst vendored; running header and cover letter year
   updated. Required AI-use statement added (does not count toward 9 pages).

9. **“They have a hidden n=500 result / they under-claim scale.”**
   §5.6 scale-roadmap + Limitations (vi) + FAQ: 230/230 deposits exist;
   **no top-1**; key withheld; thinking-tier arm ≠ no-thinking headline.
   Headline stays n=300. Do not invent 519/524 pooled n.

10. **“Agentic literature (IR-Agent ICLR 2026 / MolQuest / Espejo) already
    solved this; this is a thin bench.”**
    Related work now types three regimes. IR-Agent re-ranks a proposed pool
    (NIST IR). This paper measures the missing stage split on literature
    peak lists. Discussion: the next agent is a proposer, not a second verifier.

## What changed in the 2026-09-20 night pass (no new metrics)

- `main.tex`: denser agentic Related Work (three regimes); propose ≫ verify;
  §5.6 scale-roadmap (230/230 deposited, unscored); Limitations (vi) + FAQ
  cover expand-500 and “no fverify on 106 or 230”.
- `references.bib`: IR-Agent venue → ICLR 2026 (verified poster / official repo).
- Companion STATUS pointer: `docs/EXPAND500_POINTER_2026-09-20.md`.

## What changed in v0.23

- `iclr_paper.tex`: abstract/intro claim sharpen; SpectraLLM/IR-Agent/curated
  contrast; Listing 1 (abridged v3-R25 payload; full numeric lists not invented);
  honest Fig. 1 caption; denser Limitations; Appendix Reviewer FAQ; ICLR 2027
  macros; mandatory AI-use statement.
- `tex/iclr2027_conference.sty` + `.bst` from
  https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip
  (year string only vs 2026 sty).
- Cover letter / README year → 2027.
- This memo.

Listing 1 uses only already-disclosed fragments (v3-R25 / C10H14N2O / IR 1679 /
2-pyridyl picolinamide) plus ellipsis for unpublished full shift lists. No
fabricated peak tables.

## Experiments that would help next (not run here)

This postcard repo has no frozen prediction dumps or `score_pooled.py`.
Cheap re-score is not possible without the spectro-agent data tree.
**Do not** run expensive Opus solves before the 2026-09-25 deadline unless a
human explicitly unlocks compute.

| experiment | why it helps | cost / status |
|---|---|---|
| **fverify-106** | Closes attack (6). Would let a pooled wall exist. Until then, never invent 58/7/129-style triples on n=300. | Needs `forward_verify_main.py` on expansion candidates + observed 13C; **not on disk here**. |
| **Labeled cheap-model appendix** | Shows the recall ≪ precision split is not Opus-specific beyond the n=60 vendor arm (already in Table 4). A frozen Haiku/Sonnet or local 7–8B deposit on a **labeled** subset would be an appendix table, not a headline. | Only if deposits already exist. Do **not** start thinking-high or new Opus. |
| Spectro / NMIRacle / Alberts / CASE on-bench | Closes “missing cheminformatics baselines.” | Heavy; not a 6-day job. Leave to released scorer. |
| SpectraLLM / IR-Agent on this bench | Closes SOTA-chase attack only if someone ports them. Different inputs (simulated traces / NIST IR). | Out of scope for this pass. |
| Expert-chemist audit | Already formally deferred. | Human, not LLM. |

## What this pass does **not** do

- No new metrics, CIs, or figure redesigns.
- No thinking-high recommendation or runs.
- No IRexp Methods / licence-pool dump.
- No pooled fig_wall.
- No commit of expansion `answers2.jsonl`.
