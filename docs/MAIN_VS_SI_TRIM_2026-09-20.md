# Main vs SI triage — 2026-09-20

Dedicated batch: **structure density + SI home + ICLR 9-page honesty**.
No new experiments. No title / caption rewrite. No hygiene pass.

Base: `origin/main` @ `4338931` (`fix listing caption below`).
Open polish PR #15 (`release figures v0.2`) left alone; this branch is from **main**.

ICLR companion: `docs/ICLR_REQUIREMENTS_CHECK_2026-09-20.md`.

## Constraint (Ilkham)

Main must stay **rich and dense** like the IR-Agent ICLR 2026 camera-ready PDF
(compact paragraphs, no skeleton after SI moves). Prefer **cut fluff / repetition**
over moving core results. Only move what is truly supplementary (long protocols,
extra tables, prompt dumps).

Compiled this pass (tectonic / XeTeX): **11 pp PDF**. Body through
**Conclusion on p.8** (≤9 pp main). AI / Ethics / Repro / Ack + refs p.9–10;
appendix p.11. Left-margin **ruler ON**. Double-blind title block.

## This-pass edits (1 move + repetition cuts + outline)

| change | where | why |
|---|---|---|
| **Move** validate-clean extras dump | main App.~B prose → SI already has tables (`si:extras`) | Repeated scaffold / size / reweight integers; reviewer-skip appendix dump |
| Cut setup wall reprint | §4 forward-verify paragraph | 204/45/251 already in abstract, Fig.~1, §5.4, conclusion |
| Fold leftover estimator island | Discussion lead | Eq.~(7) already SI; was a 1-sentence leftover after §5.6 cut |
| Fold Limitations into Discussion | `\paragraph{Limitations.}` (label kept) | IR-Agent has no extra numbered Limits section; inventory stays |
| Related work 2.1 / 2.2 / 2.3 | same prose | ICLR compactness (their 2.1 / 2.2); not a survey inflate |
| Cross-vendor: one paragraph then table | §5.3 | Kill post-table 2-sentence island |
| SI map + SCHEMA.md note | `si/supplement.tex` | Extras dump retired; review-copy schema for standalone SI |

**Not moved** (would thin the claim path): Listing~1, Fig.~1, wall appendix plate,
cases table, headline / formula-only / vendor / 60-arm fverify / literature tables,
mechanism + ladder + chemspace + robustness figures, generate-wide, HOSE/GNN,
fine-tune one-liner, short limits.

## Stay in main

| object | lock / role |
|---|---|
| Descriptive title | Molecular Structure Elucidation with Frontier Models… |
| Abstract claim | n=500; 45.4% (227/500); 49.8% (249/500); wall **204/45/251**; 68–83% |
| n=500 locks | 227 / 249 / 204 / 45 / 251 — no 194/106/200, no 243/519, no CIs |
| Fig.~1 | `fig1_lead_overview` (protocol + fverify wall) |
| Listing~1 | live lstlisting + PubChem 3D (ILJNJJNKEOAREX) |
| Eq.~(1)–(6) | factor, IK14, top-1, recall, prec.\|recall, chamfer |
| Table~1 headline | 227/500, 161/248, 66/252, 249/500 |
| Formula-only table | 3/60 vs 14/60 |
| Cross-vendor table | four families; recall ≪ precision |
| 60-arm fverify table | 14/60 → 16/60; 16/19 |
| Literature table | 68 / 70 / 83% recall share of collapse |
| Worked-cases prose + App.\ table | R06 / R25 / R26 (caption cites `tab:cases`) |
| Fig.~wall appendix plate | dedicated 204/45/251 plate (not a second wall) |
| Short limits | harness, contamination, object, stats, missing SOTA, coverage, deferred, scope |
| ICLR statements | AI use, Ethics, Repro, blinded Ack |

## Move (done or already done)

| candidate | destination | this pass |
|---|---|---|
| Validate-clean extras dump (scaffold 64%, size bins, reweight CIs) | SI `si:extras` | **Cut from App.~B**; headline keeps one-liner |
| Prompt skeletons / deposit schema | SI `si:prompt` | already SI |
| Model cards | SI `si:card` | already SI |
| expand-500 generation + chamfer 103/230 | SI `si:e500`, `si:fverify` | already SI |
| Protocol-slice diagnostic 58/65; 58/7/129 | SI `si:fverify` | already SI |
| Pooled estimator Eq.~(7) | SI `si:eqs` | already SI (Discussion leftover cut) |
| Four-model Claude ladder n=24 | SI cases panels | already SI (main: one clause) |
| Arm wall rows 194 / 106 / 200 | SI wall table only | **never in main prose** |

## Already in SI (do not delete)

| SI section | contents |
|---|---|
| `si:map` / `si:plates` | Fig.~1 reprint, Listing~1 reprint, wall reprint |
| `si:protocol` | four-field contract, pre-reg, stopping, tools |
| `si:eqs` | identities (1)–(7) |
| `si:extras` | stereo, scaffold, Tanimoto, size, corpus-reweight |
| `si:e500` | 129/230, 138/230 (thinking-tier; not headline) |
| `si:pools` | n=500 generation table |
| `si:fverify` | 204/45/251 + arm rows + 103/230 |
| `si:cases` | R06 / R25 / R26 + extra panels |
| `si:prompt` | solver / fverify skeletons |
| `si:card` | headline + vendor cards; literature rows |
| `si:split` | IRexp fence + anon.4open + SCHEMA.md |
| `si:repro` | rescore commands, uncaptured artefacts |

## Flagged, not moved (density)

These look “extra” but are **core claim-path** or caption-locked. Moving them
would make main a thin skeleton.

- Chemspace / robustness / mechanism / ladder figures
- Non-LLM verifiers + derange + fine-tune (Discussion cites 33.5%→54.1%)
- Generate-wide (abstract: “broader sampling lifts recall”)
- App.~A dataset pointer (review URL in the submit PDF)
- App.~B wall plate + cases table (Fig.~1 caption lock + `tab:cases` caption)

## IR-Agent outline (compactness only)

| IR-Agent (ICLR 2026 PDF) | ours after this pass |
|---|---|
| Intro (lab context) + method claim | Intro (peak-list object) + factorisation |
| 2.1 / 2.2 related | **2.1 / 2.2 / 2.3** (same prose) |
| Method | §3 bench + §4 setup |
| Experiments + ablations in-flow | §5 results (tables stay) |
| No numbered Limitations | **Limits as Discussion paragraph** |
| Conclusion | Conclusion |
| Ethics; no 2027 AI-use | AI use + Ethics + Repro (2027) |
| Combined PDF appendix | App.~A–B after refs; standalone SI extra |

We do **not** copy their NIST Top-*k* claims or “first agent” language.

## Page-budget note

Spare page after Conclusion is **not** for new claims. p.6 is figure-dense
(robustness + vendor table + mechanism), not an empty band. No `[H]`, no
`\enlargethispage`. Official submit look remains **pdfLaTeX + Times** on Overleaf.

## Locked (unchanged)

Descriptive title. Metrics 227/249/204/45/251. No 194/106/200 in main.
No Cursor / agent names in the PDF.
