# Caption and title pass — 2026-09-20

Titles and captions only in `main.tex` and `si/supplement.tex`.
No body-prose rewrite, no metric changes, no SI surgery beyond
heading/caption strings.

Locks kept:

- paper `\title` stays the descriptive ICLR form (not the claim-title)
- generation **227/500**, **249/500**
- wall **204 / 45 / 251**
- no cohort 194/106/200 in captions
- no agent names in captions
- figure and listing captions stay **below** the float
- table captions stay **above** (ICLR default)
- ICLR `Figure N:` / `Listing N:` / `Table N:` labels unchanged

Voice: present tense, `X shows Y`, one sentence what the panel shows.

## Unchanged

| location | string | reason |
|---|---|---|
| `main.tex` `\title` | Molecular Structure Elucidation with Frontier Models: A Benchmark on Literature-Reported IR, $^1$H, and $^{13}$C NMR Peak Lists | already locked descriptive ICLR title |
| SI author block | same title, line-broken | matches main `\title` |
| claim-title comment | Generation Recall, Not Verification, … | unused alternate; do not promote |
| ICLR required heads | Introduction, Related work, Experimental setup, Results, Discussion, Limitations, Conclusion, AI use / Ethics / Reproducibility / Acknowledgements | already short and parallel |

## `main.tex` — section titles

| before | after |
|---|---|
| Difficulty, balance, and scoring contract | Difficulty and scoring |
| Is the model reading the spectra? | Spectral controls |
| Forward-verification decomposition | Forward verification |
| Decomposition across published literature | Literature comparison |
| Dataset pointer (IRexp) | Companion dataset (IRexp) |

## `main.tex` — captions

| float | before | after |
|---|---|---|
| Fig. 1 | IRSpectra-Bench protocol and $n{=}500$ fverify. Blind peak lists $+$ formula $\rightarrow$ closed-book LLM proposes a ranked pool $\rightarrow$ optional forward $^{13}$C chamfer re-rank (Eq. chamfer) $\rightarrow$ InChIKey-14 (Eq. ik14). Generate: $249/500$ (49.8%) recall in top 3; select: $204/249$ (81.9%) verified \| pool ($49.8\%\times 81.9\%=40.8\%$ verified). Wall: $204$ verified / $45$ misranked / $251$ never proposed. Propose is the wall, not verify. | The protocol plate shows blind peak-list elucidation on $n{=}500$: peak lists $+$ formula $\rightarrow$ ranked pool $\rightarrow$ optional forward $^{13}$C re-rank (Eq. chamfer) $\rightarrow$ InChIKey-14 (Eq. ik14); generate $249/500$ (49.8%) recall in top 3; select $204/249$ (81.9%) verified \| pool ($49.8\%\times 81.9\%=40.8\%$ verified); wall $204$ verified / $45$ misranked / $251$ never proposed. |
| Fig. chemspace | Chemistry of the literature cohort. (a) MW (median 306). (b) RDKit rings (median 2). (c) C–F bonds. (d) N atoms. Mid-size literature space, not a NIST toy set. | The histograms show molecular weight, ring count, C–F bonds, and nitrogen atoms for the $n{=}500$ literature cohort (median MW 306; median 2 rings). |
| Listing 1 | Example IRexp JSON record (commercial DoR; ILJNJJNKEOAREX). Solvers see only formula and printed peak lists; SMILES / InChIKey are resource fields. Gold scored by Eq. ik14. v3-R25 remains the mechanism case (Figure mechanism). | The listing shows one IRexp JSON record (commercial DoR; ILJNJJNKEOAREX): solvers see only formula and printed peak lists; SMILES and InChIKey are resource fields scored by Eq. ik14. |
| Table headline | Headline elucidation ($n{=}500$). No CIs. | Headline scores show top-1 and recall on $n{=}500$ (confidence intervals not reported). |
| Table formula-only | Formula-only control (paired, $n{=}60$). | The formula-only control shows paired top-1 and recall on $n{=}60$. |
| Fig. robustness | Robustness on instrumented arms (formula-only / cross-vendor $n{=}60$; recency): formula-only collapse, flat recency, four-vendor recall $\ll$ precision. | The robustness panels show formula-only, recency, and four-vendor checks on the $n{=}60$ arms: formula-only collapse, flat recency, and recall $\ll$ precision. |
| Table cross-vendor | Cross-vendor decomposition ($n{=}60$). Recall and precision use different denominators. | Cross-vendor scores show generation recall versus verification precision on $n{=}60$ (different denominators). |
| Fig. mechanism | Locked v3-R25: self-rank prefers 3-pyridyl; forward $^{13}$C recovers 2-pyridyl (chamfer 0.42 vs 1.30 ppm) — a verify-save, not a recall win (Table cases). | Case v3-R25 shows self-rank preferring 3-pyridyl, while forward $^{13}$C recovers 2-pyridyl (chamfer 0.42 vs 1.30 ppm; Table cases). |
| Table fverify | Forward-verify on the 60-compound arm. $n{=}500$ in Table headline is generation (self-rank). The instrumented protocol-slice diagnostic is SI. | Forward-verify scores show self-rank versus re-rank on the 60-compound arm; $n{=}500$ generation is in Table headline. |
| Fig. ladder | Inference ladder on the 60-compound arm: 23% → 27% → 30% top-1. Generate-wide lifts recall (32% → 42%); the wall is proposal, not ranking. | The inference ladder shows top-1 on the 60-compound arm: 23% → 27% → 30% (generate-wide recall 32% → 42%). |
| Table literature | Selected literature decomposition rows (connectivity-scored or as published). | Literature rows show selected systems, connectivity-scored or as published. |
| Fig. wall | Forward-verify wall on $n{=}500$: **204** verified / **45** misranked / **251** never proposed (249 recalled). Propose is the wall, not verify. Generation remains $227/500$ top-1 and $249/500$ recall (Figure 1). | The forward-verify wall shows the $n{=}500$ split: **204** verified / **45** misranked / **251** never proposed (249 recalled); generation remains $227/500$ top-1 and $249/500$ recall (Figure 1). |
| Table cases | Worked cases from released candidate files. $^{13}$C chamfers in ppm; Tanimoto Morgan $r{=}2$. | Worked cases show three failure modes from released candidate files ($^{13}$C chamfers in ppm; Tanimoto Morgan $r{=}2$). |

## SI — titles

| before | after |
|---|---|
| IRSpectra-Bench --- protocol, scale tables, cases, and reproducibility | IRSpectra-Bench: protocol, tables, cases, and reproducibility |
| Cross-reference to the main manuscript | Cross-reference to the main text |
| Solver-facing contract | Solver contract |
| Stopping and pooling rules | Stopping and pooling |
| expand-500 generation | expand-500 generation scores |
| Headline generation | Headline generation scores |
| $n{=}500$ unified wall | $n{=}500$ wall |
| Instrumented protocol slice | Protocol-slice diagnostic |
| expand-500 official score | Official expand-500 score |
| Proposal miss --- main-R06 / C29H30FNO2 | Proposal miss: main-R06 / C29H30FNO2 |
| Verify-save --- v3-R25 / C10H14N2O | Verify-save: v3-R25 / C10H14N2O |
| Verify-fail --- v3-R26 / C14H11N3O3 | Verify-fail: v3-R26 / C14H11N3O3 |
| Listing 1 | Example payload |
| Additional reported panels | Additional panels |
| Prompt skeletons and deposit schema | Prompts and deposit schema |
| Headline solver-facing skeleton | Headline prompt |
| Forward-verify skeleton | Forward-verify prompt |
| Cross-vendor card ($n{=}60$) | Cross-vendor model card ($n{=}60$) |
| Literature decomposition | Literature comparison |

## SI — captions

| float | before | after |
|---|---|---|
| Map table | Main-text objects and their counterparts in this supplement. | The map shows main-text objects and their counterparts in this supplement. |
| Fig. lead reprint | Reprint of main-text Figure 1 (`fig1_lead_overview`). Generate $249/500$ (49.8%) recall in top 3; select $204/249$ (81.9%) verified \| pool ($49.8\%\times 81.9\%=40.8\%$ verified). Wall: $204$ verified / $45$ misranked / $251$ never proposed. | The reprint shows main-text Figure 1: generate $249/500$ (49.8%) recall in top 3; select $204/249$ (81.9%) verified \| pool ($49.8\%\times 81.9\%=40.8\%$ verified); wall $204$ verified / $45$ misranked / $251$ never proposed. |
| Listing reprint | Example IRexp JSON record (commercial DoR; reprint of main-text Listing 1; ILJNJJNKEOAREX) — PubChem 3D CID 57398578. SMILES and InChIKey are resource fields, not solver payload. | The reprint shows main-text Listing 1, an IRexp record (commercial DoR; ILJNJJNKEOAREX; PubChem CID 57398578): SMILES and InChIKey are resource fields, not solver payload. |
| Fig. wall reprint | Reprint of the $n{=}500$ forward-verify wall (`fig_wall_diagnostic`): $204$ verified / $45$ misranked / $251$ never proposed. Source: spectro-agent `data/fverify_n500/WALL_n500.md`. Generation remains $227/500$ top-1 and $249/500$ recall. | The reprint shows the $n{=}500$ forward-verify wall: $204$ verified / $45$ misranked / $251$ never proposed; generation remains $227/500$ top-1 and $249/500$ recall. |
| Validate-clean extras | Validate-clean extras. Same scorer; not the $n{=}500$ headline. | Validate-clean extras show scaffold and stereo metrics under the same scorer, not the $n{=}500$ headline. |
| Size bins | Size bins on validate-clean $n{=}295$. | Size bins show top-1 and recall on validate-clean $n{=}295$. |
| expand-500 generation | expand-500 generation (`score2`, InChIKey-14). No confidence intervals. | expand-500 scores show generation under `score2` (InChIKey-14; confidence intervals not reported). |
| Headline generation | Headline generation on the frozen $n{=}500$ roster. Confidence intervals are not reported. This table is generation only. | Headline scores show generation on the frozen $n{=}500$ roster (confidence intervals not reported). |
| $n{=}500$ wall table | $n{=}500$ forward-verify wall, copied from `data/fverify_n500/WALL_n500.md`. No confidence intervals. Arm rows are not the headline. | The forward-verify wall shows the $n{=}500$ split (confidence intervals not reported; arm rows are not the headline). |
| Protocol-slice table | Instrumented forward-verify diagnostic on a protocol slice. Not the $n{=}500$ wall (204/45/251). | A protocol-slice diagnostic shows forward verification, not the $n{=}500$ wall (204/45/251). |
| expand-500 chamfer | expand-500 official chamfer score. Arm score, not the $n{=}500$ wall and not the headline. | Official expand-500 chamfer scores show an arm result, not the $n{=}500$ wall and not the headline. |
| Case grid | Three-mode case grid. Same integers as main-text Table `tab:cases`. | The case grid shows three failure modes, with the same integers as the main-text case table. |
| Fig. v3-R25 | Locked v3-R25 verify-save (main-text Figure 5). Self-rank prefers 3-pyridyl; forward $^{13}$C recovers 2-pyridyl (chamfer 0.42 vs 1.30 ppm). | Case v3-R25 shows a verify-save (main-text Figure 5): self-rank prefers 3-pyridyl, while forward $^{13}$C recovers 2-pyridyl (chamfer 0.42 vs 1.30 ppm). |
| Headline model card | Headline solver. Unrecorded fields are left blank rather than guessed. | The headline solver card shows recorded fields; unrecorded fields are left blank. |
| Cross-vendor card | Cross-vendor decomposition. Recall and precision use different denominators. | Cross-vendor scores show generation recall versus verification precision (different denominators). |
| Literature table | Selected literature decomposition rows (as in main-text Table 6). | Literature rows show selected systems, matching the main-text literature table. |
