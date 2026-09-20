# Final source of truth — 2026-09-20

Audit of IRSpectra-Bench after Rodrigo Vargas-Hernández Overleaf edits
and the n=500 / fverify-wall night pass. **Do not merge.** **Do not
force-push.** Additive commits only on PR #14.

## Which repo / branch / PR

| object | value |
|---|---|
| Manuscript repo | https://github.com/IlkhamFY/IRSpectra-Bench |
| Working branch | `cursor/iclr-night-strengthen-20260920-c33d` |
| Pull request | https://github.com/IlkhamFY/IRSpectra-Bench/pull/14 (draft; do not merge) |
| Base | `main` @ `4d0e253` (`release submit status 2026-09-19`) |
| Data / scoring repo | https://github.com/IlkhamFY/spectro-agent |
| Generation integers | spectro-agent PR **#41** `48fcd30` (`HEADLINE_n500_2026-09-20.md`) — https://github.com/IlkhamFY/spectro-agent/pull/41 |
| Diagnosis wall | spectro-agent PR **#68** `data/fverify_n500/WALL_n500.md` — https://github.com/IlkhamFY/spectro-agent/pull/68 |

Do **not** merge spectro-agent #41 or #68 from this manuscript pass.
Integers were copied only.

## Overleaf

| item | value |
|---|---|
| GitHub sync | Import `IlkhamFY/IRSpectra-Bench`; **Pull GitHub** after PR #14 lands or while reviewing this branch |
| Main document | **`main.tex`** (repo root). `iclr_paper.tex` is a `\input{main}` shim |
| Compiler | pdfLaTeX or XeLaTeX + BibTeX; styles via `latexmkrc` → `tex/` (ICLR **2027**) |
| Postcard root | `README.md`, `LICENSE`, `main.tex`, `iclr_paper.tex`, `references.bib`, `.gitignore`, `latexmkrc` |
| Do not compile | `main_IRExpBench_only.tex` (optional Overleaf orphan; not the ICLR build) |
| Project URL | **Not stored in this repository.** Overleaf is GitHub-synced; no `overleaf.com/project/…` URL is committed. Setup notes: `docs/OVERLEAF.md`. After PR #13, Overleaf can Pull `main` without the rename conflict. |

If a human pastes the Overleaf project URL later, put it here — not in the PDF.

## What is final (manuscript vs SI vs data)

| layer | path | role |
|---|---|---|
| **ICLR manuscript** | `main.tex` + `references.bib` + `figures/` | Source of truth for title, claims, captions, 9-page body through Conclusion |
| **SI** | `si/supplement.tex` → `si/supplement.pdf` | Protocol, pool tables, cases, prompts, model card, n=500 wall reprint + optional arm table, expand-500 chamfer arm (103/230). Does **not** count toward 9 pp |
| **Cover letter** | `cover_letter/cover_letter.tex` + McMaster letterhead | Named authors, AccelD grant, Rodrigo signatory. Not double-blind |
| **Generation data** | spectro-agent PR #41 | 227/500 top-1, 249/500 recall; roster / qid cut |
| **Wall data** | spectro-agent PR #68 | fverify **204 / 45 / 251** |
| **Dataset review copy** | https://anonymous.4open.science/r/peaklist-corpus-review-10C4/ | IRexp commercial DoR; private source `IlkhamFY/peaklist-corpus-review` (do not cite) |

Stale markdown (`docs/ICLR_PAPER.md`) is a snapshot. Do not copy it into Overleaf.

## Locked numbers

### Generation (label as generation; not the wall)

| metric | integer |
|---|---|
| top-1 | **227/500 (45.4%)** |
| recall@3 | **249/500 (49.8%)** |
| self-rank | **227/249 (91.2%)** |

Identity: **45.4% = 49.8% × 91.2%**. No CIs. Do not quote 243/519.

### Diagnosis wall (THE wall)

| | verified | misranked | never-proposed |
|---|---:|---:|---:|
| **n=500 fverify** | **204** | **45** | **251** |

Recalled = 204+45 = **249/500**. Propose is the wall, not verify.

Generation **227 / 22 / 251** is top-1 / (recalled-but-not-top-1) / never-proposed.
Use it only when labeled as **generation**. It is **not** the wall.

### Not the wall (SI / appendix / historical)

| triple | role |
|---|---|
| 58 / 7 / 129 | old n=194 instrumented fverify; SI protocol-slice only |
| 227 / 22 / 251 | generation decomposition; not the wall |
| 103/230 vs 129/230 | expand-500 official chamfer arm (SI); not a second wall |
| n=300 / 118/300 / 133/300 | former headline (appendix / dated notes) |
| 194 / 106 / 200 | roster composition; do **not** print in main prose |

## Figures (filenames must match captions)

| float | file | caption lock |
|---|---|---|
| Fig 1 | `figures/fig1_lead_overview.{pdf,png,svg}` | protocol + n=500 **fverify**: 249/500 recall, 204/249 verified\|pool, 40.8% verified; wall **204/45/251** |
| Listing 1 | `figures/listing1_irexp_record.{pdf,png,svg}` | IRexp JSON + molecule (NTJIYHYWVZYBEX; commercial DoR) |
| Wall | `figures/fig_wall_diagnostic.{pdf,png,svg}` | fverify **204/45/251** |
| SI-only slice | `figures/fig_wall_fverify_slice.*` | 58/7/129 protocol-slice; not cited as the paper wall |

`figures/fig_wall.{pdf,png}` is a leftover sibling. Main no longer `\includegraphics`s it.
`main_IRExpBench_only.tex` still points at `fig_wall.png` — leave that orphan alone.

## Metadata consistency vs `main` (2026-09-20 audit)

| item | on this branch | vs `origin/main` | action |
|---|---|---|---|
| Title | Generation Recall, Not Verification, Binds LLM Structure Elucidation from Literature Spectra | unchanged | keep |
| Alternate Rodrigo title | comment only in `main.tex` | same comment | keep as comment; do not promote |
| Authors | Ilkham Yabbarov¹†, Rudra Sondhi¹, Rodrigo A. Vargas-Hernández¹,²,³† | unchanged | keep |
| Affiliations | Chem/ChemBio; Brockhouse; CSE — McMaster, Hamilton ON L8S 4L8 | unchanged | keep |
| Emails | yabbaroi@mcmaster.ca, vargashr@mcmaster.ca | unchanged | keep; hidden until `\iclrfinalcopy` |
| Dataset name | **IRSpectra-Bench** = bench; **IRexp** = companion Sci Data resource | same fence | keep; never merge IRExp-Data as co-headline |
| Repo URL in PDF | none (double-blind) | same | keep |
| Review dataset | anonymous.4open `peaklist-corpus-review-10C4` | same | keep |
| Named HF | `ilkhamfy/IRexp` camera-ready only | same | do not put in PDF |
| Zenodo | not minted (`docs/SUBMISSION.md` still TODO) | same | do not invent a DOI |
| License | MIT, © 2026 Ilkham Yabbarov, Rodrigo A. Vargas-Hernandez; datasets under source licences | unchanged | keep |
| Acknowledgements (PDF) | blinded NSERC CREATE; AccelD name omitted | unchanged | keep for double-blind |
| AccelD grant | cover letter only: NSERC 596133-2025 (CREATE AccelD / Acceleration Consortium) | same grant, n=500 numbers updated | keep in letter; restore named ack at camera-ready |
| Postcard | root files as in `docs/OVERLEAF.md` | README layout listed `OVERLEAF.md` at root (files live in `docs/`) | README paths corrected this pass |

## Rodrigo-origin edits that must be preserved

These came from Overleaf (`8c74a65` and earlier “Updates from Overleaf”)
and from the McMaster letter / author block. **Do not wipe.**

1. **Understatement.** Not a solved elucidator. Nonsignificant ladder steps
   do not license a solved-elucidator headline. Consumer harness / no snapshot
   stated honestly. No invented CIs.
2. **Companion IRexp (not a second ICLR paper).** Listing 1 + Appendix A
   pointer only. Do not embed Data Descriptor Methods / licence-pool dump.
   v0.23 harden against the Overleaf abstract that co-headlined **IRExp-Data**
   (~43K) with IRSpectra-Bench — that rewrite stays **out** of `main.tex`.
3. **Orphan Overleaf draft.** `main_IRExpBench_only.tex` + Overleaf-only
   `references.bib` entries. Rodrigo title, IRExp-Data abstract, ICLR 2026
   sty internally, n=300 / 58/65. Header already says: not the ICLR build.
   Keep the file; do not compile it for submission.
4. **Alternate title comment** in `main.tex` (Rodrigo-leaning, claim-dropping).
   Comment only.
5. **Author / affiliation / dagger emails** as written (Rodrigo corresponding
   with Ilkham; three McMaster units).
6. **McMaster letterhead** (`cover_letter/mcm-col_png.png`) and **Rodrigo
   signatory** on the cover letter.
7. **AccelD** named in the cover letter (596133-2025). PDF acknowledgements
   stay blinded until camera-ready.
8. **Anonymous IRexp bib** (`author = {Anonymous}`) and anonymous.4open URL.
9. **Double-blind switches:** `\iclrfinalcopy` commented; running header
   “Under review as a conference paper at ICLR 2027”.

## Leftovers found this audit (fixed only if they presented an old wall as THE wall)

Live TeX (`main.tex`, `si/supplement.tex`, cover letter) already used
fverify **204/45/251** as the wall and labeled **227/500 & 249/500** as
generation. No `n=300` / `n=194` / `58/7/129` / `227/22/251` as THE wall
in `main.tex`.

Clear leftovers (current-night notes / postcard, not dated historical locks):

- `README.md` called Fig 1 “generation”
- `docs/OVERNIGHT_2026-09-20.md` and `docs/NIGHT_POOL_2026-09-20.md` header
  still said the wall is generation **227/22/251**
- `docs/SUBMIT_STATUS_2026-09-20.md` called Fig 1 generation
- `docs/EXPAND500_POINTER_2026-09-20.md` said “official fverify is SI-only”
  (true of 103/230; false of the n=500 wall)
- `docs/LEADERBOARD.md` still said “forward-verify is the n=194 slice”
- `docs/figma-pack/FIG1_BUILD_SPEC.md` and `BRIEF_WALL_n500.md` still specified
  the generation 227/22/251 plate (superseded by the shipped fverify Fig 1)
- `docs/ANONYMITY_ICLR.md` still pointed at `iclr_paper.tex`

**Left untouched on purpose** (dated locks / Rodrigo orphan):

- `docs/POOLED_HEADLINE_2026-09-16.md`, `docs/OVERNIGHT_2026-09-16.md`,
  `docs/SUBMIT_STATUS_2026-09-19.md`, `docs/SOFT_REJECT_DEFENSE_2026-09-19.md`
- `docs/ICLR_PAPER.md` body (stale snapshot; banner only)
- `main_IRExpBench_only.tex`
- `docs/BENCHMARK.md` (n=21 pilot)
- LICENSE copyright line (Ilkham + Rodrigo; same as `main`)
