# External systems — why they were not scored

No on-bench number below was invented. Nothing in this file is a
top-1 or a recall. The question is whether a named system can take
the released solver payload — formula plus printed IR, ¹H, and ¹³C
peak lists — and run here with no paid API.

Checked 2026-09-21. No adapter for any of these systems exists under
`scripts/` in this repo or on spectro-agent `main`.

## IR-Agent

Blocked. Do not run it on these peak lists.

- Input in Noh et al. (arXiv:2508.16112) is a digitized absorbance
  vector, polynomially interpolated onto 500–4000 cm⁻¹. The peak
  assigner then calls `scipy.signal.find_peaks` on that vector
  (`height=1`, `distance=50`). A printed band list is not that vector.
- The retrieval agent needs the NIST IR library. The public repo
  (`HeewoongNoh/IR-Agent`) ships NIST ids and a downloader, not the
  spectra (copyright).
- The agents call a paid chat model (GPT-4o-mini, GPT-4o, or o3-mini
  in the paper). There is no API budget for that.
- Their reported condition does not take a molecular formula.
- Building a fake NIST trace from a printed band list would not be
  their task. Not done.

## NMIRacle

Blocked on input shape, not on a missing license for the code.

- `fedeotto/nmiracle` reads `spectra.h5`: IR (1,800 bins), ¹H
  (10,000 bins), ¹³C (10,000 bins). That is a simulated spectral
  grid (Alberts et al. multimodal set), not an author-printed peak
  list.
- No checkpoint is in this environment, and no peak-list-to-grid
  adapter is in tree. A converter would be a new model of the
  spectrum, not the released bench input.
- Not run.

## Alberts IR transformer

Blocked on input and on weights.

- The published model (`rxn4chemistry/rxn-ir-to-structure`, Zenodo
  10.5281/zenodo.7928396) takes a digitized IR spectrum. The bench
  stores a short list of reported band positions, not that trace.
- Weights are a multi-gigabyte Zenodo archive. Not downloaded.
  No peak-list adapter in tree.
- Not run.

## CASE engines

Blocked on license or on missing constraints.

- ACD/Structure Elucidator, Bruker CMC-se, and Mestrelab Mnova CASE
  are commercial. None is installed. No license in this environment.
- MOLGEN is closed-source.
- Open correlation engines (COCON, LSD) want 2D experiments
  (HMBC/COSY). This bench does not release those.
- The open formula generator that does run offline is MAYGEN 1.8.
  That run is separate (`docs/EXP_ENUMERATOR.md`). It is not a CASE
  system: generation sees the formula only, and it does not consume
  the peak lists except at the optional ¹³C ranker.

## SpectraLLM and the other named rows

No SpectraLLM, Spectro, or NMR-Solver/NMRAgent checkpoint in this
environment accepts `{formula, ir_bands_cm-1, h_nmr, c_nmr}`.
spectro-agent has no adapter. Paid APIs are out of budget.
Not run. No score.
