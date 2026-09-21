# NMRTrans on the n=500 roster

Offline same-input run. No paid LLM API. No invented peak intensities.
No confidence intervals.

**Checkpoint.** `little1d/C-H-Formula` file `nmrtrans-c-h-nmr-formula.ckpt`
(sha256 `d184e2280a1623a09b60a052686af343191f9ee99cd89b3570314c15852c4fcd`).
Code `little1d/NMRTrans` commit `9a72756532e60d540f05eafa93d31aecd1cb4362`.
499/499 checkpoint tensors loaded. CPU. Beam 3, `do_sample=False`,
`max_length=82`.

**Questions.** `IlkhamFY/spectro-agent` `48fcd30153df5e331fab43cfa514763db8ee3891`.
Roster: locked clean-main 134 + v3 40 + v2_ctrl 20 + expansion all 106 +
expand-500 headline 200 (`headline500_expand200_qids.json`).

**Gold.** Unique match of (RDKit formula, IR band tuple, ¹³C string) into
`irexp_resolved.jsonl.gz`. 500/500 matched, 0 ambiguous. The solver did
not see SMILES or InChIKeys. Scoring is RDKit `MolToInchiKey`[:14].

**What entered the model.** Formula counts on the released 12-element
vector; printed ¹H shift (midpoint and half-width when the list prints a
range), multiplicity (unknown patterns stay index 0), printed integral,
printed *J* (at most six); printed ¹³C shifts, repeated when the list
prints an *n*C count. NMRTrans turns repeated ¹³C shifts into its
intensity channel. 76/4298 proton peaks had no printed integral and were
stored as 0, not filled in as 1H. 19 shifts outside [0, 220] ppm were
clamped by the model's published /220 normalisation. Nine formulae
contain Se or Sn, which that vector drops. IR bands were not used: the
checkpoint has no IR channel.

**Not rerun (accepted blockers).** NMR-Solver (SimNMR-PubChem, hundreds
of GB), SpectraLLM (>15 GB RAM and intensities), IR-Agent (digitised
NIST), commercial CASE.

## InChIKey-14

| set | n | top-1 | recall (top 3) |
|---|---:|---|---|
| all | 500 | **79/500 (15.8%)** | **102/500 (20.4%)** |
| simple | 248 | 62/248 (25.0%) | 79/248 (31.9%) |
| complex | 252 | 17/252 (6.7%) | 23/252 (9.1%) |
| locked | 194 | 32/194 (16.5%) | 39/194 (20.1%) |
| expansion | 106 | 12/106 (11.3%) | 20/106 (18.9%) |
| expand-500 200-cut | 200 | 35/200 (17.5%) | 43/200 (21.5%) |

86/500 rank-1 strings were not valid RDKit SMILES.

## Training-split overlap

Gold InChIKey-14 against `little1d/NMRTrans-Data` (train 169,863 / val
21,279 / test 21,298). This is constitution identity, not proof that the
same peak list was in the file.

| split | problems | top-1 | recall |
|---|---:|---|---|
| train | 9 | 8/9 | 9/9 |
| val | 2 | 1/2 | 1/2 |
| test | 0 | — | — |
| in none of the three | 489 | **70/489 (14.3%)** | **92/489 (18.8%)** |

Predictions: `predictions.jsonl` (`uid`, `cohort`, `qid`, up to three
SMILES). Per-problem hits: `hits.jsonl`. Aggregates: `scores.json`.
Runner: `scripts/nmrtrans_baseline.py`.
