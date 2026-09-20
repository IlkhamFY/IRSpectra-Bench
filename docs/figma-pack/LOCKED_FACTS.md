# Locked paper facts (from /workspace/irspectra-main/iclr_paper.tex)

- Title theme: Generation recall, not verification, binds LLM structure elucidation from literature spectra
- n = 194 compounds (IRSpectra-Bench)
- top-1 exact constitution overall: 28.4% [22–35]; simple 48.0%; complex 8.3%
- recovered top-3: 33.5%; simple 54.1%; complex 12.5%
- generation recall: 65/194 = 34%
- Wall diagnostic: verified 58 | mis-ranked 7 | never proposed 129
  - bracket: "65 recalled (34%)" over 58+7
  - precision|recall forward-verification: 58/65 = 89%
  - verification alone moves whole-benchmark top-1 only 28% → 30%
  - forward-verified top-1: 58/194 (30%)
- Formula-only control (n=60): 3/60 (5%) vs formula+IR+1H+13C 14/60 (23%)
- IRexp pointer: 121,233 records; 43,060 structure-linked; 33,201 full quadruples

Listing 1 JSON: exact fields from /workspace/IRexp_fresh/scientific_data.tex lst:example
Molecule assets: /workspace/IRexp_fresh/figures/fig_example_mol_rdkit.{pdf,png}
Existing wall: /workspace/irspectra-main/figures/fig_wall.{pdf,png}
Wall script reference: /workspace/spectro-agent/scripts/make_fig_wall.py
