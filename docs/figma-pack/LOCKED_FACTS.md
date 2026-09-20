# Locked facts — Chem Partner wall 2026-09-20 morning (n=500)

Source: spectro-agent `data/fverify_n500/WALL_n500.md` (PR #68).
Generation headline is separate and unchanged.

## Generation (not the wall)
- top-1: **227/500 (45.4%)**
- recall@3: **249/500 (49.8%)**
- never proposed: **251**
- self-rank: **227/249 (91.2%)**
- identity: 45.4% = 49.8% × 91.2%

## Diagnosis wall (n = 500 fverify)
- verified: **204**
- misranked: **45**
- never-proposed: **251**
- recalled: 204+45 = **249**
- punchline: "No re-ranking repairs the 251 never proposed in top-3"
- NO CIs
- Label semantics: verified / misranked / never proposed

## Superseded (do not use on figures)
- Old n=194 wall: verified 58 | mis-ranked 7 | never proposed 129; 65/194 (34%); 58/65 (89%); 28%→30%

## Listing 1 (unchanged asset)
Listing 1 JSON: exact fields from /workspace/IRexp_fresh/scientific_data.tex lst:example
Molecule assets: /workspace/IRexp_fresh/figures/fig_example_mol_rdkit.{pdf,png}
