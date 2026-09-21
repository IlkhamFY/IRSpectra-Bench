# ICLR 2027 review note: IRSpectra-Bench

Reviewer stance: Area Chair reading the double-blind PDF (`main.tex` + `\input` files + `si/supplement.tex` + captions). Locked integers were checked against the prose. Numbers were not "corrected". Contradictions are bugs.

Manuscript: *Molecular Structure Elucidation with Frontier Models: A Benchmark on Literature-Reported IR, 1H, and 13C NMR Peak Lists*. Build root `main.tex`. `\iclrfinalcopy` is commented. The style file therefore prints "Anonymous authors / Paper under double-blind review". That part is in good shape.

---

## 1. Reject-risk score

**Reject-risk: 68 / 100. Verdict: Weak Reject. Confidence: high.**

The stage split is a real object (top-1 = recall x precision|recall, and 45.4% = 49.8% x 91.2% checks). The submission still reads as a consumer-harness diagnostic with a benchmark's title. A sympathetic AC can move this to Borderline only after the headline protocol is described as the mix it is, the two walls stop sharing one name, and the abstract stops claiming results the tables do not contain. As frozen today it is a Weak Reject. It is not a formatting reject and it is not an Accept.

---

## 2. Top 5 reject reasons

1. **Contribution.** The paper's own prior (Priessner et al., cited in Related Work) already states that a re-ranker cannot recover a candidate that was never proposed. IRSpectra-Bench measures that split on one frozen roster. That measurement is worth a paper only if the roster, the scorer, and the protocol are something other groups can trust and extend. Right now the headline is one Claude Opus consumer subscription, no pinned snapshot, no recovered system prompt (SI admits the wrapper was not captured), and a 500-row pool whose construction is hidden. "We release a scorer" is a promise of a benchmark. The PDF is a single-model diagnosis.

2. **Novelty against IR-Agent, CASE, and tool-using LLM chemistry.** IR-Agent (ICLR 2026) is correctly named as the closest IR elucidator and then not run. CASE is correctly described as exhaustive-recall by construction and then not run. Spectro, NMIRacle, Alberts IR transformers, SpectraLLM, NMR-Solver, and NMRAgent are all "not scored on this bench" (Related Work 2.1 and Limitations (v)). The entire contrast with IR-Agent is an uncaptioned 2-row `center` table (Related Work, after the three-regime list): input, metric, "binds". Tool-using agents (ChemCrow, Coscientist) are one sentence. An ICLR reviewer will write: you built a leaderboard and left every relevant system off it, then used their published top-k numbers as if that were an on-bench comparison.

3. **Evaluation honesty.** Three separate problems, each enough to sour a review.
   - Locked protocol mix: 200 of the 500 headline rows are a thinking-tier expand-500 cut pooled with no-thinking runs. Main text, Limitations (i), the AI-use statement, and the SI model card all say the headline used no thinking tier, or that the thinking-tier arm is "not headline".
   - Two walls, one slogan. Generation wall is 227 exact top-1 / 22 in-pool but not top-1 / 251 never proposed. Forward-verify wall is 204 verified / 45 misranked / 251 never proposed. Self-rank top-1 is 227. Forward-verify top-1 is 204. The independent verifier is 23 hits worse on the cohort the abstract is about. The abstract says verification "barely moves top-1". The 60-compound arm (14 to 16) and the protocol slice (55 to 58, p = 0.55) are the only places the margin is discussed, and both go the other way.
   - The abstract's "68--83% of the accuracy collapse ... to real heterogeneous peak lists" is not computable from Table `tab:lit-decomp`. That table has one row per system. The three shifts being averaged (NMR-Solver simulated to real, SpecX random to scaffold, Espejo education to industrial) are not the same shift, and two of them are not literature peak lists.

4. **Clarity.** A reader who believes the abstract, then looks at Figure 1, thinks the paper cannot add. The abstract's "n=500 wall" is 204/45/251. Figure 1's wall is 227/22/251. The conclusion repeats 204/45/251 as "the wall" in the sentence after 227/500, with no figure pointer. The slogan "propose >> verify" is printed next to "weak proposers, good verifiers". Read as a performance comparison, the slogan is backwards. Read as a cost comparison, it is undefined. The integer 22 (in-pool, not top-1) appears in the Figure 1 caption and essentially nowhere in the prose, so the generation wall has no sentence a reviewer can quote.

5. **Related work and positioning.** Section 2 is a citation stack sorted into three regimes, plus a limitations sentence ("not scored") misplaced as related work. It does not say how IR-Agent builds its pool, what a CASE enumerator would do with a formula plus these peak lists, or why MolPuzzle's harness inversion (GPT-4o 1.4% vs 57.8%, Introduction) is or is not the same failure as low generation recall. The useful sentence is already in the draft: "We do not claim to beat SpectraLLM or IR-Agent on their native sets." The paper then offers no substitute comparison on its own set. Positioning-by-abstention is not a related-work section.

---

## 3. Storytelling and density

Overall: closer to a compressed technical note than to an IR-Agent-grade ICLR paper. The scoring section is the one place a reader feels a person derived something. Intro, Related Work, the results grab-bag, and the discussion are thin, repetitive, or slogan-driven. Several paragraphs have the cadence of a model summarising a longer memo: short declaratives, a bolded punchline, a citation cluster, no mechanism.

Specific spots:

- **Abstract.** Six claims in six sentences, most of them bolded. It asks "which stage fails", then answers with the forward-verify triple before the reader has been told that a second triple exists. "We ask an operational question" and "proposal, not ranking, is the expensive stage" are template lines. The last two sentences (vendor replication, 68--83%) are the ones a reviewer will check and fail to verify from the main table.

- **Introduction, first paragraph** (`sec:introduction`, the block before Eq. 1). A list of systems and one sharp fact (MolPuzzle harness inversion). No picture of what a literature peak list actually looks like, and no statement of what "constitution" means, until later. The operational-question sentence that closes the next paragraph repeats the abstract. Eq. 1 and the denominator warning are the first original prose. Keep those. The paragraph above them can lose a third of the citations.

- **Contributions list.** Item 2 restates the abstract numbers and points the recall-bound diagnosis at the appendix forward-verify figure. Item 4 ("a literature decomposition") oversells a script the main table does not document. This list does not add a thought that the abstract missed.

- **Dataset-pointer paragraph** (Introduction, immediately before Figure 1). This is a legal aside about a different manuscript. It stops the argument in the worst possible place, between the contributions and the lead figure. It is also the Sci Data theater called out in Section 4.

- **Related Work 2.1** (four lines). "Spectro, NMIRacle, Alberts IR transformers and CASE are not scored" is a limitation. As the opening of Related Work it tells the reviewer the bench is empty.

- **Related Work 2.2.** The (i)/(ii)/(iii) regime split is the right outline and it is written as telegrams. IR-Agent gets the only paragraph with a mechanism (SE re-rank cannot repair a missing candidate; TI+Ret features cannot either). That paragraph is IR-Agent-grade. The uncaptioned 2-row table under it throws the mechanism away. Regime (iii) ends by repeating Eqs. 1--3.

- **Related Work 2.3 and the jump into Section 3.** "IRSpectra-Bench is an openly redistributable literature-peak-list suite with a stage decomposition, measured on Claude and replicated across three other model families." Then Section 3 starts "Each of 500 problems supplies...". There is no problem-setup section and no handoff. The task definition itself (formula, IR band list, 1H/13C lists, no name, no SMILES) is clear and should stay. What is missing is one paragraph that says: closed book, k <= 3, constitution = InChIKey-14, success factorises as Eq. 1. That paragraph currently arrives as equations after a difficulty digression.

- **Difficulty paragraph** (Section 3.2, "near-50/50 by design"). Important, and buried. The corpus is 17.5% simple / 82.5% complex; the leaderboard is balanced; reweighted top-1 is 26.5% [21--32] on a validate-clean subset. This is the sentence that should sit under the headline table. It currently sits above the scoring equations, where a skimming reviewer will not treat it as a result.

- **Experimental setup.** Three `\paragraph`s. The solver paragraph is honest about the consumer harness and then false about thinking tier (see Section 4). "One sub-agent per batch" is never defined. The forward-verify paragraph introduces chamfer and then says the ranker cannot raise recall, which the reader already knows from Eq. 1. The prompt is not here. SI later admits it was not captured and prints a reconstructed skeleton. For a benchmark, that is a hole in the methods, not a supplement detail.

- **Results opening** (after Table `tab:headline`, the long paragraph that starts "On the validate-clean subset"). Scaffold 64%, Tanimoto 0.66, three size bins, 76.6% constitutional isomers, 22.6% Murcko, a battery subset n=46, and a pointer to an underpowered four-model ladder. Six results, four denominators, one paragraph. This is the densest "AI compression" in the paper. The isomer fact is the most interesting chemical sentence in Results and it is trapped in the dump.

- **Forward verification** (`sec:forward-verify`). The 60-arm table, the n=500 wall sentence, three worked cases, generate-wide, and non-LLM verifiers are one subsection. The non-LLM paragraph (HOSE tie, GNN 59/65 vs 58/65, derangement p=0.001, fine-tune 33.5% to 54.1%) is four experiments with no design. "The training-free ceiling remains recall-limited" is a slogan standing in for a result.

- **Discussion and Conclusion.** Discussion opens by repeating 227/249 and "propose >> verify", then says the contribution "is not an IRexp Data Descriptor", which is a defensive aside, not a discussion. The agentic-implications paragraph restates the wall and names IR-Agent, MolQuest, and Espejo again. Limitations (i)--(viii) are the best prose in the paper: specific, numbered, and unwilling to spin p=0.55 into a gain. The conclusion throws that discipline away and returns to the abstract, including the Sci Data sentence.

Caption voice is one template: "The protocol plate shows", "The histograms show", "The robustness panels show", "The inference ladder shows", "The forward-verify wall shows". Fine once. Five times, it reads generated.

What is already at the right density: Eq. 1 and Eqs. `eq:top1`--`eq:prec`; the InChIKey-14 definition; the formula-only paragraph (short, with the nested McNemar); the three worked cases in the appendix table; Limitations.

---

## 4. Number and claim hygiene

Locked targets, for the record:

- Generation: top-1 227/500 (45.4%), recall 249/500 (49.8%), self-rank 227/249 (91.2%). Identity holds: 0.498 x 0.912 = 0.454.
- Generation wall, and this is what Figure 1 must show: 227 / 22 / 251.
- Forward-verify diagnostic wall: 204 / 45 / 251. Recalled 204+45 = 249. Same 251 never proposed. This wall is a different bar.

### Figure 1 vs the fverify wall

No `\ref{fig:fig1}` is attached to 204/45/251. The Figure 1 caption integers are the generation wall. The appendix figure `fig:fig-wall` and its caption are the fverify wall, and that caption points generation back at Figure 1. The SI crosswalk (`si:map`) says the same thing. Those three locations are clean. Do not "fix" them by painting 204 onto Figure 1.

The confusion is in the prose, and it is enough to make a reviewer distrust every later number.

| Location | What it says | Bug |
|---|---|---|
| Abstract, sentence on "Independent forward verification" | calls 204/45/251 "the n=500 wall" | This is the first wall the reader meets. Figure 1, on the next page, prints a different triple and the caption never says "self-rank, not forward-verify". |
| Figure 1 caption | arrow chain includes "optional forward 13C re-rank", then prints select 227/249 and wall 227/22/251 | The integers are the generation wall. The arrow tells the reader those integers came out of the chamfer re-rank. They did not. Chamfer-ranked-first on this cohort is 204. |
| Contributions, item 2 | generation numbers, then 204/45/251 "Figure `fig:fig-wall`" | The citation target is the right figure. The item still presents the diagnostic wall as the recall-bound result, and that figure lives in the appendix. |
| Results, end of `sec:headline` | 227/249 "is not forward-verification precision", then 204/45/251 with `fig:fig-wall` | This sentence is correct. It is also the first time the main text admits the two quantities differ, and it still omits 227 vs 204 as top-1 counts. |
| `sec:forward-verify`, after the 60-arm table | "margin over self-ranking is small and unresolved", then again 227/249 and 204/45/251 | The "small margin" is the 60-arm (14/60 self, 16/60 forward) and the SI protocol slice (p=0.55). On n=500 the forward-verify top-1 count is 204 against self-rank 227. That is a 23-hit drop, 45.4% to 40.8%. The paper never writes 204 < 227. |
| Conclusion | 227/500 and 249/500, then "the wall is 204/45/251" | No figure pointer. A reviewer will attach this sentence to Figure 1. |
| Limitations (vi) | 204/45/251 with `fig:fig-wall` | Citation is correct. Repeating the triple for the sixth time still does not state the comparison to 227. |

The integer 22 is in the Figure 1 caption, the SI reprint caption, and the SI map. It is not in the abstract, the results table, or the conclusion. The generation wall therefore has no main-text sentence.

### Overclaims

- **"No thinking tier."** Experimental setup ("the core protocol uses ... no thinking tier"), Limitations (i) ("no snapshot, temperature, seed, or thinking tier"), AI-use statement ("Inference used no thinking tier"). The locked headline is a size-weighted mix: the expand-500 cut inside n=500 is a declared thinking-tier consumer run. SI `si:e500` says that arm "is not interchangeable with the no-thinking core protocol" and does not say that 200 of its rows are inside the headline. SI model card: "expand-500 solver ... thinking-tier (declared; not headline)". "Not headline" is false for the 200-cut. SUBMIT-facing docs already say "disclose, do not hide". The PDF hides it.
- **"Verification alone barely moves top-1"** (abstract). On the 60-arm, self-rank 23% and forward-verify 27%, and generate-wide top-1 23% to 30% with p=0.34. On n=500, forward-verify top-1 is 204/500 against self-rank 227/500. "Barely moves" is the wrong verb for the cohort in the previous sentence. The expand-500 arm in SI (verify 103/230 vs self 129/230) has the same sign as the n=500 wall and is also absent from that abstract sentence.
- **"Good verifiers (227/249)"** (Discussion opening). 227/249 is self-ranking precision given the true structure was proposed. The independent forward verifier's precision on the same recalled set is 204/249 (81.9%). Calling the model a good verifier on the strength of its own rank, while the verifier the paper built loses 23 top-1 hits, is spin. The 251 never-proposed bin still dominates either bar. That part of the slogan can stay if the 227-vs-204 sentence is next to it.
- **"68--83%"** (abstract and `sec:literature`). Table `tab:lit-decomp` does not contain the paired source numbers. Espejo education to industrial and SpecX random to scaffold are not "curated or simulated spectra to real heterogeneous peak lists". NMR-Solver's simulated row is not printed. A reviewer cannot audit the percentage. The sentence also lets a meta-analysis of other papers' top-k stand in for a result on IRSpectra-Bench.
- **"Four vendor families"** (abstract, contributions item 3). The replication is Table `tab:cross-vendor`, n=60. Claude on that arm is 14/60 top-1 (23%) and 19/60 recall (32%), with mean 2.20 candidates against 3.00 for the others. The headline 45.4% is a different pool. The asymmetry (precision|recall above recall) does show up on all four rows. The abstract reads as if four vendors reproduced 45.4%.
- **"Pre-registered"** (contributions: "pre-registered InChIKey-connectivity scorer"). SI `si:protocol` says sampler seeds for early draws were not captured and the roster is frozen but not exactly re-drawable. A frozen list is not a pre-registration. Use "frozen".
- **Confidence intervals.** Section 3.2: "Confidence intervals are bootstrap 95%". Table `tab:headline` caption: "confidence intervals not reported". The header comment and the SI both forbid invented n=500 intervals. The methods sentence promises a procedure the headline table refuses. Report intervals for the n=60 tests that have them, and say in the same sentence that n=500 is a point estimate.
- **Corpus reweight omitted from the lead.** 26.5% top-1 and 31.3% recall, validate-clean, reweighted to the 17.5/82.5 corpus mix, appear in Section 3.2 and again in Discussion. They are absent from the abstract and from Table `tab:headline`. A balanced 50/50 leaderboard at 45.4%, against a corpus that is 82.5% complex, will be quoted as "LLMs solve 45% of literature structures". The paper already computed the transportable number. Leave it next to 45.4% or accept that reviewers will quote the larger one.
- **"Propose >> verify".** Used in the abstract, contributions, discussion, conclusion, and SI. Delete the symbol. Write one plain sentence: of the 500 problems, 251 never contain the true structure in the top-3 pool; given it is in the pool, self-rank places it first 227 times out of 249.

### Sci Data and foreign-manuscript cruft

This is still in the PDF-visible text. It should be a single resource pointer (counts + anonymous review URL). No journal, no article type, no "in preparation".

- Introduction, dataset-pointer paragraph: "a *Scientific Data* manuscript (in preparation)" plus `\citep{yabbarov2026irexp}`.
- Discussion: "not an IRexp Data Descriptor".
- Limitations (vii): "parser audit deferred to the Sci. Data companion".
- Conclusion: "documented separately as a *Scientific Data* Data Descriptor (in preparation)".
- Ethics statement: "companion Data Descriptor".
- Appendix `app:dataset`: the section exists to say IRexp is not a Data Descriptor, then cites an anonymised *Scientific Data* Data Descriptor (in preparation). The anonymous.4open.science URL is the right artifact. The rest of the section is theater.
- `references.bib` entry `yabbarov2026irexp`: journal `Sci. Data`, note "Data Descriptor, in preparation". That note prints in the reference list. Reviewers treat an unreadable companion as a missing dataset even when a review copy exists.
- SI `si:split` repeats the Data Descriptor paragraph.
- `cover_letter/cover_letter.tex` (not the paper, but it is what an AC reads): same "companion Scientific Data Data Descriptor, in preparation".

`\iclrfinalcopy` is off. Author names and emails in the source `\author` block do not print. The bib entry is `author = {Anonymous}`. Acknowledgements name NSERC CREATE and withhold the grant number. That is an acceptable double-blind residual. Do not uncomment `\iclrfinalcopy` for the submission build.

No 243/519 in `main.tex` body. No 194/106/200 in main prose. Those absences match the lock. The SI forward-verify arm table does print locked-194 / expansion-106 / expand-200 and they sum to 204/45/251. That table is the disclosure the main text is missing. Its caption says "arm rows are not the headline", which is how a reader is talked out of noticing that the three arms are the headline.

---

## 5. Figure and table narrative

**Figure 1** (`fig:fig1`, `fig1_lead_overview`). Right integers, half-right story. The plate is the object a reviewer will remember, and it currently shows the generation factorisation (249/500, 227/249, 45.4%, bar 227/22/251). That is the lead this paper can defend. It does not carry the abstract, because the abstract's lead number is 204. The caption's protocol arrow runs through forward 13C re-rank and then quotes self-rank. Fix the caption so the bar is labelled self-rank, and so 204/45/251 is named as a different figure. After that, Figure 1 is sufficient as the lead plate. It does not need a second redesign.

**What the main floats fail to do.**

- Table `tab:headline` has top-1 and recall only. The paper's actual claim is the third factor, 227/249, and it is not in the table. Simple vs complex (161/248 vs 66/252) is in the table and is good. Add one row for precision|recall. Do not add a forest of CIs.
- There is no main-text table or figure a reviewer can look at to see 227/22/251 and 204/45/251 with the definitions side by side. The diagnostic bar is Appendix Figure `fig:fig-wall`, after the bibliography. The result the abstract opens with is an appendix float. Either move that float into `sec:forward-verify` or, cheaper, add three lines under the headline table. Reprints in the SI do not fix a main-text narrative hole.
- Figure `fig:fig-chemspace` (MW, rings, C--F, N; median MW 306, median 2 rings) is fine supporting context and it is not a result. It earns its slot only if the simple/complex definition points at it. Right now the two are pages apart in spirit: the figure is in 3.1, the definition is in 3.2.
- Listing 1 is the right artifact (formula and peak lists vs resource fields). It is long for the main text. The gold SMILES and InChIKey are on the plate, with a caption that says solvers do not see them. Keep the caption sentence. If page count breaks, the listing is the first float to move to SI. The JSON-in-SI reprint plus the second shortened JSON in `si:prompt` is three copies.
- Table `tab:formula-only` and Figure `fig:fig-robustness` tell one n=60 story (formula-only collapse, flat year, vendor gap). The figure caption repeats the table. One of them is enough in the main text.
- Table `tab:cross-vendor` is the replication. It needs one sentence in the caption or immediately under it: this arm is not the n=500 headline; Claude here is 23% top-1, not 45.4%; candidate budgets differ.
- Figure `fig:fig-mechanism` (v3-R25, chamfer 0.42 vs 1.30) is the one case that makes verification concrete. Keep it. The verify-fail case (v3-R26, 1.35 vs 1.36) is the more important chemical fact and it has no figure. A sentence under this figure is enough. A second structure panel is not.
- Table `tab:fverify` reports only the 60-arm, inside a section whose prose is about n=500. A reader using the table to check the wall will not find 204. Put the n=500 triple in that table, with a column or a second row block, and label the 60-arm as the arm.
- Figure `fig:fig3-method` (23% to 27% to 30% on n=60) is a ladder the limitations correctly call nonsignificant (p=0.55 and p=0.34). A main-text figure of a non-result invites the overclaim the limitations are trying to kill. Move it to SI or demote it to one sentence.
- Table `tab:lit-decomp` is the right idea and an unauditable one. "This work + forward-verify" at 29.9% / 33.5% is a protocol slice, sitting in a column of n=500 and n=450 numbers. The caption says "protocol slice (SI)" in the row and "as published" in the caption. Reviewers will compare 29.9% to NMR-Solver's 52.9%. Give the paired before/after rows that produce 68%, 70%, and 83%, or delete the percentages.

**SI dumps that hurt.**

- `si:plates` reprints Figure 1, Listing 1, and the wall. `si:cases` reprints the case table and the mechanism figure. `si:card` reprints the cross-vendor table. `si:eqs` reprints the equations. A reviewer who opens the SI sees the paper again, then a verbatim `score2` footer, then a reconstructed prompt the authors say is not the prompt. Cut reprints. Keep the arm table, the validate-clean extras, the expand-500 chamfer score (103/230 vs 129/230), and the model card.
- The arm table in `si:fverify` is the one SI object that should survive, and its caption currently argues against its own rows ("arm rows are not the headline"). Those three rows sum to the headline wall. Say that, and say the 200-cut is the thinking-tier portion. Leaving the table and miscaptioning it is worse than omitting it.
- `si:cases` "Additional panels" and the four-model Claude ladder (n=24, "Haiku subset Sonnet subset Opus subset Fable", "protocol asymmetry", no numbers) read as leftovers. "Difficulty variation. Pre-registered draws differ in difficulty." is an empty paragraph. Delete both or give the numbers.
- `si:prompt` prints a prompt skeleton and then says the headline wrapper was not captured. State the hole once, in Limitations (i). A fake prompt in the SI will be screenshotted as the method.
- `si:split` is the Sci Data section again.

Main-text float budget, after the cuts above: Figure 1, chemspace, one headline table that includes both walls, formula-only (table or figure, not both), cross-vendor table, one case figure, literature table with paired rows. Listing 1 stays if it still fits in 9 pages. The appendix wall figure can stay as the full bar once the main table has the integers.

---

## 6. Concrete fix list (next four days, to the ~25 Sep 2026 AoE deadline)

Edits are substitutions. The main text is already at a conference page budget. Do not append a new section.

### P0. Ship-blockers

1. **Split the walls in four places, and write 227 vs 204 once.**
   - Abstract, the "Independent forward verification" sentence: delete "the n=500 wall of 204/45/251" from the abstract, or replace it with one clause that uses both names. Suggested content: self-rank top-1 is 227/500; an independent 13C chamfer re-rank of the same pools places the true structure first in 204/500 (204 verified / 45 misranked / 251 never proposed). Proposal still accounts for the 251. Forward verification does not improve the headline.
   - Figure 1 caption: delete "optional forward 13C re-rank" from the arrow that introduces the 227/22/251 bar. Add four words: "solver self-rank, not forward-verify". Leave the integers 227 / 22 / 251 alone.
   - Results, end of `sec:headline` (the sentence that already cites `fig:fig-wall`): add "forward-verify top-1 is 204/500, against self-rank 227/500". Delete the later copy of the same triple in `sec:forward-verify` and point back.
   - Conclusion, "the wall is 204...": name it "forward-verify diagnostic" and point at `fig:fig-wall`. Keep 227/500 and 249/500 as the generation result. Do not leave "the wall" unqualified.
   - `sec:forward-verify` "margin ... small and unresolved": scope that clause to the 60-arm and the protocol slice. The n=500 comparison is a drop, and it needs its own sentence.

2. **Stop claiming a uniform no-thinking headline.**
   - Experimental setup, solver paragraph (~"no thinking tier"): replace with the locked mix. A declared part of the frozen n=500 roster (the expand-500 cut that completes the 500) was run under a thinking-tier consumer harness. The earlier rows were not. Scoring is the same InChIKey-14 contract. Do not add a 194/106/200 results table to the main text if page count is the constraint. Do not write "no thinking tier" about the pooled number.
   - Limitations (i) and the AI-use statement: same correction. "Inference used no thinking tier" is false for the headline pool.
   - SI model card row "expand-500 solver ... not headline": change to "200 of this thinking-tier arm is inside the n=500 headline".
   - SI `si:fverify` arm-table caption: the three arm rows compose the 204/45/251 wall. Say so.

3. **Pull the unauditable claims out of the abstract.**
   - Abstract "68--83%": either add the paired before/after top-1 and top-k for those three shifts to Table `tab:lit-decomp` (the script is already named in the text) and describe each shift in its own words, or delete the percentage from the abstract and from `sec:literature`. Do not describe SpecX's scaffold split or Espejo's education-to-industrial drop as a collapse onto literature peak lists.
   - Abstract "verification alone barely moves top-1": delete, or scope it to the n=60 arm and add the n=500 sign (204 vs 227).
   - Abstract and contributions "four vendor families": add "on a 60-compound arm" in the abstract. Under Table `tab:cross-vendor`, one sentence that Claude's 23% on this arm is not the 45.4% headline, and that recall rankings are approximate because of the 2.20 vs 3.00 candidate budgets.

4. **Strip the companion-journal theater. One resource sentence.**
   - Delete the dataset-pointer paragraph in the Introduction. If a pointer is still wanted, one sentence at the end of Section 3.1: peak lists are taken from IRexp (121,233 records; 43,060 structure-linked; 33,201 full quadruples); review copy at the anonymous.4open.science URL already in the appendix. No journal name, no "Data Descriptor", no "manuscript in preparation", no `\citep` to an unreadable article.
   - Delete the matching sentences in the Discussion, Limitations (vii), Conclusion, Ethics (point licensing at the review copy and the mixed PMC-OA / Chemotion line you already have), Appendix `app:dataset` (keep the URL, delete the bullet about the companion manuscript), SI `si:split`, and the cover letter.
   - `references.bib` `yabbarov2026irexp`: remove this entry if nothing cites it after the cuts. A printed "Sci. Data, in preparation" reference is an invitation to reject the dataset as unavailable.

### P1. What changes the review if the P0 edits land

5. **Narrow the claim so it matches the experiments.** Abstract and contributions item 1 currently sell "a blind peak-list benchmark" on which frontier elucidation has been measured. The body measures one harness and leaves IR-Agent, CASE, Spectro, NMIRacle, Alberts, and SpectraLLM unscored (Limitations (v)). Move that sentence from the limitations into the abstract. Title and contributions should say "stage-split diagnosis of a closed-book harness on a frozen literature roster". If a real on-bench baseline already exists in the code release (the IRexp fine-tune is the only one with a significant McNemar, p=0.015, on a slice), give it one main-text row with its denominator. Do not stand up a new experimental program this week and do not imply those systems were compared.

6. **Replace the uncaptioned Related Work table.** Same location (the `center` tabular after the IR-Agent paragraph). Make it a real float with a caption. Rows: IR-Agent, one CASE enumerator, Priessner / NMR-Solver style re-rankers, this work. Columns: input (NIST IR vs literature peak lists vs simulated), whether the true structure is known to be in the pool, whether recall is reported, whether it was run on IRSpectra-Bench. The last column will be "no" for everyone but this work. That honesty is stronger than the current 2-row "binds" table. Keep the IR-Agent mechanism paragraph. Cut regime (i) to a clause.

7. **Put the transportable number next to the headline.** Table `tab:headline`: add precision|recall 227/249 (91.2%), and a footnote or a last row for corpus-reweighted 26.5% top-1 / 31.3% recall on the validate-clean subset, marked as not the leaderboard. One sentence in `sec:headline` that the 50/50 simple/complex design (248/252) is why 45.4% sits above the reweighted figure. The reweight intervals are already written; do not invent n=500 intervals.

8. **Explain the denominator zoo in `sec:forward-verify`.** One small table, replacing the current 60-only `tab:fverify`: rows for n=500 self-rank, n=500 forward-verify, 60-arm, protocol slice. Columns: recall, self top-1, verify top-1. The sign change (slice slightly up, n=500 down, expand-500 arm 103 vs 129 down) should be visible without SI. Delete the second prose copy of 204/45/251.

9. **Kill the slogan.** Search-and-replace "propose >> verify" in `main.tex` and `si/supplement.tex`. One definition, in the discussion: 251 of 500 failures are missing proposals; 22 of 500 are self-rank misses; 45 of 500 are forward-verify misses among the recalled. Then stop repeating it.

### P2. Density, captions, SI. Do these only after P0.

10. **Results grab-bag** (paragraph after `tab:headline`). Keep two numbers in main: size trend (67.9% / 42.8% / 16.7% with n=53/152/90) and the isomer fact (76.6% of analysable top-1 misses are constitutional isomers; 22.6% share the Murcko scaffold). Move battery n=46 and the n=24 model ladder fully into SI, with the ladder's actual counts or not at all.

11. **Captions.** Drop "The X shows" on all five main figures. Figure 1 caption is the one to spend time on (P0 item 1). Chemspace: "n=500 literature cohort, median MW 306, median 2 rings." Robustness: either cut the figure or stop repeating Table `tab:formula-only`.

12. **Figure `fig:fig3-method`.** Move to SI. A nonsignificant ladder should not be a main float.

13. **Listing 1.** If the PDF exceeds the page limit after the P0 rewrites, move the listing to SI and leave a four-line payload schema in the setup section. Do not keep three copies (main, SI reprint, SI shortened JSON).

14. **SI cuts.** Delete reprinted plates, reprinted equations, reprinted cross-vendor table, the reconstructed prompt listing, the empty "Difficulty variation" paragraph, and `si:split`. Keep: arm composition table (recaptioned, P0 item 2), validate-clean extras, expand-500 generation and chamfer tables, model card, the statement that the headline wrapper was not captured.

15. **Methods CI sentence** (Section 3.2, "Confidence intervals are bootstrap 95%"). Change to: n=60 paired tests use McNemar; earlier validate-clean intervals are bootstrap 95%; n=500 headline numbers are point estimates with no interval.

16. **"Pre-registered"** in contributions. Change to "frozen".

---

## 7. What is already strong

- The factorisation is right and the arithmetic closes. Top-1 227/500, recall 249/500, self-rank 227/249, and 45.4% = 49.8% x 91.2%. Figure 1, the SI map, and `scripts/make_fig_wall.py` all keep 204/45/251 off that plate. The appendix wall caption distinguishes the two bars. This is the part of the paper that should be the lead, and the integers on the plate are already the locked ones.
- The failure mode is chemically specific. Appendix cases cover a true structure that never enters the pool (main-R06), a self-rank error the chamfer fixes (v3-R25, 0.42 vs 1.30 ppm), and a near-tie the chamfer does not fix (v3-R26, 1.35 vs 1.36 ppm). The 76.6% constitutional-isomer rate among analysable misses matches those cases: wrong connectivity at the right formula, not a random SMILES failure.
- The authors already refuse the bad headlines, in the limitations. Contamination is "a strong bound, not exclusion" (formula-only 3/60, year correlation r = -0.007). The ladder p-values are printed (0.55 and 0.34). They say they do not beat IR-Agent or SpectraLLM on those systems' own sets. The scorer is constitution-level InChIKey-14, with stereo reported separately (93/295 on validate-clean) instead of being quietly ignored. Frozen predictions plus a mechanical scorer are the right release shape.
- Simple vs complex is a real gap (65% vs 26% top-1) and the corpus-reweight (26.5%) shows they know the 50/50 roster flatters the headline. That pair, stated once next to 45.4%, is more persuasive than the literature meta-analysis.
- Double-blind mechanics are in place: `\iclrfinalcopy` commented, anonymous author substitution in the style file, anonymous bib entry, anonymous dataset URL. Leave that machinery alone while the prose is fixed.

The paper is one honest rewrite away from a coherent Weak Reject / Borderline object, and several missing baselines away from anything stronger. The rewrite is the part that fits in four days. Shipping the current abstract on top of the current Figure 1 will spend the review on a phantom inconsistency.
