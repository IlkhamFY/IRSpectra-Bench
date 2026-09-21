# LISTING1_BUILD_SPEC — live IRexp listing

ICLR Listing 1 is **not** a baked SVG/PDF plate. It is the live
`listing[!ht]` float + `framed` two-column layout in `main.tex`
(`tex/listing1_body.tex`). **Not** a clone of the IRexp Scientific Data
`lst:example` urea (NTJIYHYWVZYBEX).

## Layout (IRexp pattern)

- **No in-artwork title.** Caption sits **below** the framed plate via
  a real `\caption` on the `listing` float (same ICLR
  ``Listing~N:'' typography as figure captions). Do not restore a
  manual `\textbf{Listing N.}` header above the plate, and do not use
  `[H]` (it leaves large holes).
- **Framed two-column:**
  - Left **0.62\textwidth**: live `lstlisting` style `irexpjson`
  - Right **0.34\textwidth**: PubChem 3D conformer
    (`figures/listing1_mol_pubchem3d.png`)
- Do not draw `Listing 1. Example IRexp JSON record…` inside a graphic.

## Molecule (PubChem 3D only)

InChIKey `ILJNJJNKEOAREX-UHFFFAOYSA-N`, PubChem CID **57398578**,
PMC12566713 commercial-DoR record. Fetch via PUG:

```
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/ILJNJJNKEOAREX-UHFFFAOYSA-N/cids/JSON
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/57398578/conformers/JSON
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/57398578/PNG?record_type=3d&image_size=large
```

Not RDKit 2D. Rebuild:

```bash
python scripts/make_listing1.py
```

Writes `figures/listing1_mol_pubchem3d.png` (canvas punched to alpha).

## Exact JSON (verbatim field values)

Commercial-DoR row from `ilkhamfy/IRexp` `irexp_resolved_commercial`
(PMC12566713). `formula` is **not** stored on the IRexp dump row; the
listing adds RDKit `C12H11BrN4` from `smiles` so formula + peak lists
are visible. SMILES / InChIKey remain resource fields.

Canonical copy: `docs/figma-pack/listing1_exact_record.json`.
Display copy (with formula): `tex/listing1_body.tex`.

## What NOT to invent

- Do not drop `h_nmr` / `c_nmr` / band list entries
- Do not revert to NTJIYHYWVZYBEX / the Sci Data urea
- Do not replace the PubChem 3D PNG with a flat 2D drawing
- Do not bake a combined JSON+molecule plate

## Source provenance

- Hugging Face `ilkhamfy/IRexp` → `data/irexp_resolved_commercial.jsonl.gz`
  (`license_pool=commercial`, CC-BY)
- Formula: RDKit from the record SMILES (`C12H11BrN4`)
- 3D: PubChem PUG `record_type=3d` for CID 57398578
