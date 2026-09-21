# ICLR submit compare — 2026-09-20

Structured diff of **our** ICLR 2027 manuscript (`main.tex` @ `b3cae24` + this PR)
against the user-attached PDF:

**IR-Agent: Expert-Inspired LLM Agents for Structure Elucidation from Infrared Spectra**
(Noh, Lee, Na, Kim, Park; “Published as a conference paper at ICLR 2026”;
arXiv:2508.16112v2, 19 May 2026; 29 pages).

This is a **style / structure / tone** compare. Do **not** copy IR-Agent
claims or numbers. Our locked integers stay: generation **227/500** and
**249/500**; wall **204 / 45 / 251**. Descriptive title and PubChem 3D
Listing 1 stay.

Compiled here with tectonic/XeLaTeX. **Before this PR:** 12 pages, Latin
Modern fallback, `Underfull \vbox` 10000 on the Listing 1 break, body
through Conclusion on p.9 only via `\enlargethispage{8\baselineskip}`.
**After this PR:** 11 pages, Liberation Serif (Times-metric), Listing 1
in-flow on p.4, body through Conclusion on **p.8** (under the 9-page
submit cap). Official look is still **pdfLaTeX + Times** on Overleaf.

---

## 1. Template / style

| item | IR-Agent PDF (theirs) | ours (`main.tex`) | ICLR 2027 rule | action |
|---|---|---|---|---|
| Venue style | ICLR 2026 conference sty | Vendored `tex/iclr2027_conference.sty` | Use [ICLR 2027 zip](https://media.iclr.cc/Conferences/ICLR2027/iclr-2027-style-files.zip) | Keep 2027. Do not “match” 2026 year. |
| Running header | **Published as a conference paper at ICLR 2026** | **Under review as a conference paper at ICLR 2027** | Review: “Under review…”. Camera-ready: “Published as…”. | Correct for a submit draft. |
| Left line numbers | **None** | Official **left ruler** (000, 001, …) | Official sty draws the ruler **unless** `\iclrfinalcopy` | **Keep ON for OpenReview.** Theirs is camera-ready / arXiv, not the review build. |
| Authors on title | Named (KAIST / KRICT) | `\author{…}` is filled but **not printed**; sty substitutes “Anonymous authors / Paper under double-blind review” | Double-blind: identity must not appear in PDF or SI | Correct. Uncomment `\iclrfinalcopy` only for camera-ready / a named arXiv. |
| Main-text limit | 10 pp body through Conclusion, then statements / refs / SI (29 pp total) | After this PR: Conclusion on **p.8**; AI / Ethics / Repro / Ack / refs p.9–10; appendix p.11 (11 pp total) | Submit: **≤9 pp** main. Rebuttal / camera-ready: 10. Refs + appendix unlimited. AI / Ethics / Repro / Acknowledgements **do not count**. | Under the cap. Do not spend the spare page on new claims. |
| Required AI use | Not present (2026 camera-ready) | Present, solvers-not-authors | **Required** in 2027; does not count | Keep. |
| Ethics | One paragraph (hallucination / expert supervision) | Dataset / API / licensing | Recommended; ≤1 p; does not count | Keep; theirs is more “method risk”, ours is more “data release”. |
| Reproducibility | Code URL + appendix pointer | Frozen deposits + consumer-harness hedge | Recommended; does not count | Keep. |
| Acknowledgements | Named NRF / IITP grants | NSERC CREATE; named grant IDs omitted | Does not count; still a mild identity cue | Fine for now; restore AccelD / 596133-2025 only under `\iclrfinalcopy`. |
| Appendix placement | After refs, marked “Supplementary Material” | After refs (`\appendix`) + standalone `si/supplement.pdf` | Either in-PDF after refs or a second file | Both is allowed. Prefer one combined PDF at upload. |
| Font | Times (official ICLR) | `times.sty` + **XeLaTeX/tectonic → Latin Modern fallback** (`TU/ptm/*` undefined) | Official sample is pdfLaTeX + Times | **Prefer pdfLaTeX.** This PR loads TeX Gyre Termes under XeTeX so Overleaf/tectonic does not look looser than Times. |
| Anonymity extras | Public GitHub in abstract | Anon.4open dataset URL; IRexp bib is `Anonymous, 2026` | No author-identifying host in PDF / SI | Good. Do not cite `ilkhamfy/IRexp` or McMaster in the PDF. |

### Line numbers (explicit)

ICLR does **not** use `\linenumbers` from `lineno.sty`. The 2026/2027
conference sty draws a **left-margin ruler** in review mode and **turns
it off** under `\iclrfinalcopy`.

| build | `\iclrfinalcopy` | ruler | header | authors |
|---|---|---|---|---|
| OpenReview submit | commented (current) | **ON** | Under review … 2027 | Anonymous |
| arXiv / camera-ready | uncommented | **OFF** | Published as … 2027 | Named |

The attached IR-Agent PDF is the **second row**. Matching it by killing
our ruler would make an **incorrect** 2027 submission PDF.

---

## 2. Typography / whitespace (ours)

Compiled warnings (tectonic, before this PR’s layout pass):

- `Underfull \vbox (badness 10000)` at the Listing 1 page break
  (`main.tex` ~344) — the visible **half-page hole**
- `Underfull \vbox (badness 2538)` around the literature table
- `Underfull \hbox (badness 10000)` in `tab:lit-decomp` and `tab:cases`
  (`p{…}` cells wrapping “Espejo Morales”, “Alberts”, case formulae)
- Font-shape warnings: `TU/ptm/m/n` etc. undefined (Times not actually used)
- PDF 1.7 figure included in a 1.5 output (`fig1_lead_overview.pdf`)

### What the pages actually look like

| page | symptom | cause |
|---|---|---|
| 2 | Fig. 1 on top, then leftover intro + contributions | `[t]` float. Acceptable; IR-Agent also leads with a method figure. |
| **4** | **Large empty band** after the scoring identities, before §4 | Listing 1 is `\begin{figure}[H]` (`float`). Too tall to stay on p.4; ICLR `\flushbottom` **stretches** the leftover. This is the “weird gap”. |
| 5 | Caption → `\vspace{0.35em}` → `framed` JSON + PubChem 3D | Extra skip + default `\FrameSep`. Plate itself is fine. |
| 6–7 | Fig. 3 / 4 OK; Fig. 5 (ladder) at `0.40\linewidth` | Side gutters. |
| 8 | Literature table: author names split across rows | Narrow `p{2.6cm}` / `p{2.4cm}` + no `\raggedright`. |
| 9 | Limitations + Conclusion crammed | `\enlargethispage{8\baselineskip}` (and `5\baselineskip` before Acknowledgements). Hack to hold the 9-page wall. |
| 12 | Appendix wall + cases; bottom leftover | Normal last-page slack. |

IR-Agent has **no** `[H]`, **no** `\enlargethispage`, **no** `framed`
listing, and wraps several tables beside body text (Table 1, Table 3).
Their floats sit closer to the ICLR defaults (`\textfloatsep` etc.).
We already tighten float seps (10 / 8 / 8 pt); the remaining holes are
placement, not those lengths.

### This PR’s layout fixes (no metric changes)

1. Listing 1: `[H]` → `[!ht]` so p.4 can fill; drop the 0.35em skip.
2. `tex/listing1_body.tex`: smaller `\FrameSep` / `\FrameRule` (keep
   JSON + PubChem 3D side-by-side).
3. Fig. 5 width `0.40` → `0.58` to kill side gutters.
4. Literature / cases tables: `>{\raggedright\arraybackslash}p{…}`.
5. XeTeX: TeX Gyre Termes so the page is Times-metric, not LM.
6. Dropped both `\enlargethispage` hacks. Conclusion still ends on p.8.

Do **not** turn off the ruler to “look like theirs”.

---

## 3. Content

### 3.1 Introduction density

| | IR-Agent | ours |
|---|---|---|
| Opening | ~1 page of **lab context**: IR vs MS vs NMR; cost / speed / accessibility; why IR is first-line; why interpretation is still expert work | **Three sentences** then the factorisation identity. Field is assumed. |
| Method vs measurement | New multi-agent **method** (TI / Ret / SE) | **Benchmark + stage split** (propose ≫ verify) |
| Contributions | Framework + complementarity + experiments | Bench, wall, contamination / vendors, literature decomposition |
| Tone | “We propose… first LLM-agent IR elucidator” | “top-1 is the wrong primitive”; lock-memo integers |

**Consider (do not copy claims):** one short paragraph *before* the
factorisation on why printed IR+$^1$H/$^{13}$C lists are the chemist’s
object, and why that object is not a NIST absorbance trace. That is
what their intro is doing for IR-only spectra.

**Do not** add new performance numbers, CIs, or “first” language.

### 3.2 Related work

| | IR-Agent | ours |
|---|---|---|
| Structure | `2.1` ML for IR; `2.2` LLM agents for science | Three `\paragraph`s + a 2-row comparison table |
| Prose | “ML as a game changer in molecular science…” then citations | Citation stacks; little industry connective tissue |
| Positioning | “Unlike prior work, we emulate experts and stay extensible” | Honest “not scored on our bench”; IR-Agent called out as closest concurrent IR agent |

Keep the honesty and the IR-Agent row. Optional later (not this PR):
split into `2.1` / `2.2` subsections so it *looks* like an ICLR method
paper. Do not inflate into a survey.

### 3.3 Experiments

| | IR-Agent | ours |
|---|---|---|
| Data | 9,052 NIST **experimental IR traces**, all phases | **n=500** literature **peak lists** (IR+$^1$H+$^{13}$C+formula) from IRexp |
| Protocol | Train translator; agents on top; 80/10/10 | Closed-book consumer LLM; frozen deposits |
| Headline metric | Top-$k$ exact SMILES (InChI) ± std over 3 seeds | top-1 / recall@3 / prec.|recall; **no CIs** on $n{=}500$ |
| Ablations | TI vs Ret vs both; single vs multi; extra chemical info | Formula-only, recency, four vendors, generate-wide, HOSE/GNN |
| Case figures | Two large agent-trace figures in the main | One mechanism (v3-R25) + three-row appendix table |

Different papers. Do not import their NIST Top-$k$ table or “first
agent” claim. Our missing on-bench SpectraLLM / IR-Agent / CASE scores
are already Limitation (v) — leave that gap stated.

### 3.4 Limitations tone

| IR-Agent | ours |
|---|---|
| One paragraph in Ethics + SI §D: peak *shape/intensity* unused; translator-bound; retrain on new libraries | Eight numbered attacks on p.9, then a deleted FAQ appendix |

Theirs reads as “here is the method’s scientific limit”.
Ours reads as a **reviewer-proofing checklist** (harness, contamination,
statistics, SOTA, deferred audit). That is safer for a benchmark paper
and ICLR-legal. It is also why the page looks denser and more anxious
than theirs.

This PR shortens only the **repeated** wall reprint in (vi). Do not
soften (i)–(v) or invent a chemist audit.

### 3.5 What they do that we should consider

Not copy; consider if it helps *our* paper:

1. **One lab-context paragraph** in the intro (peak lists as the
   published object; IR cheap / first-line; not a digitised trace).
2. **Wrap a small table beside text** (their Table 1 / 3) once we are
   off the 9-page knife-edge — optional, not this PR.
3. **Method-overview figure as Figure 1** — we already do this
   (`fig1_lead_overview`). Keep it.
4. **Limitations as science, not inventory** — keep the inventory;
   stop reprinting 204/45/251 in every section.
5. **Single combined PDF** (main + appendix) at OpenReview upload;
   `si/supplement.pdf` as extra file is optional.
6. **pdfLaTeX Times** so the page matches every other ICLR PDF.
7. **No `[H]` / no `\enlargethispage`** in the submit tex.

### 3.6 What we should cut or move to SI

Already in SI (do not delete from SI): 24-compound Claude ladder,
generate-wide, HOSE/GNN, expand-500 chamfer, protocol-slice wall,
pooled estimator identity, prompt skeletons.

**Clear main-text cuts (this PR; no science gutted):**

| move | why |
|---|---|
| §5.6 “Frozen roster and pooled estimator” + Eq. (7) | Restated in Discussion and in SI §eqs. Pure repetition. |
| Headline 24-compound Haiku ⊂ … ⊂ Fable sentence | Already `si` “Four-model Claude ladder”; underpowered; clutters p.6. |
| Limitation (vi) full reprint of Fig. 1 integers | Point at Fig. 1 / wall; keep 204/45/251 once in the abstract + Fig. 1 + appendix. |

**Do not move:** Listing 1 (PubChem 3D), n=500 locks, descriptive title,
formula-only / vendor tables, literature decomposition, mechanism
figure, wall appendix plate.

**Do not add:** new metrics, CIs on $n{=}500$, Figma / design-tool
mentions in tex, a SOTA scoreboard we did not run.

---

## 4. ICLR 2027 accept / desk-reject checklist

From the [2027 Author Guidelines](https://www.iclr.cc/Conferences/2027/AuthorGuidelines)
against this repo:

| check | status |
|---|---|
| Official 2027 sty + bst | Yes (`tex/iclr2027_conference.{sty,bst}`) |
| ≤9 pp main at submit | Yes, Conclusion on p.9 (knife-edge) |
| Anonymous title block | Yes |
| No identity in SI | SI says “Anonymous authors”; main appendix uses anon.4open |
| AI use statement | Yes |
| Ethics / Repro | Yes (optional but present) |
| Appendix after refs | Yes |
| Line-number ruler for review | Yes — **keep** |
| Reciprocal reviewing / 20-paper quota | Human / OpenReview; not a tex issue |
| Dual submission vs Sci. Data companion | Stated: this paper cites IRexp, does not re-present a Data Descriptor |
| Code supplement | Encouraged; not this PR |

Inconsistencies that are **ours**, not ICLR:

- XeLaTeX + `times` without a Times-like OpenType face
- `[H]` + `\enlargethispage` (not forbidden, looks non-template)
- Reviewer FAQ was already removed from `main.tex` (good)
- `main_IRExpBench_only.tex` is an orphan; do not compile it as the
  submission root

---

## 5. Compile notes

```
# Official look (Overleaf default if set to pdfLaTeX):
pdflatex main && bibtex main && pdflatex main && pdflatex main

# This environment: tectonic (XeTeX). After this PR it should load
# TeX Gyre Termes instead of Latin Modern.
PDF_ENGINE=/tmp/tectonic python3 scripts/build_pdf.py
```

`\iclrfinalcopy` stays **commented** on this branch.
