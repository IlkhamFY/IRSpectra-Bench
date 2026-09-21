# LISTING1_BUILD_SPEC — `listing1_irexp_record`

ICLR Listing 1 plate. **Not** a clone of the IRexp Scientific Data
`lst:example` urea (NTJIYHYWVZYBEX). Rebuild with
`python scripts/make_listing1.py` (uses `scripts/drawmol.py`).

## Frame

Width 504 pt (7.0 in). **Height is content-tight** (no phantom strip under
the JSON). Do not force 280 pt.

## Layout

- **No in-artwork title.** LaTeX already prints `Listing 1:` via the float
  caption. Do not draw `Listing 1. Example IRexp JSON record…` on the plate.
- **Framed two-column** (rounded rect, fill `#F7F7F5`, stroke `#E5E5E0`):
  - Left **~62%**: monospace JSON (exact fields; wrap long NMR — do not truncate values)
  - Gap **~4%**
  - Right **~34%**: molecule image centered (`listing1_mol_rdkit.pdf` / `.png`)
- Molecule **canvas is transparent** (border-connected white punched to
  alpha). Heteroatom label knockouts stay opaque. Frame fill shows through.

## Exact JSON (verbatim field values)

Commercial-DoR row from `ilkhamfy/IRexp` `irexp_resolved_commercial`
(PMC12566713). `formula` is **not** stored on the IRexp dump row; the
build script adds RDKit `CalcMolFormula` from `smiles` so formula + peak
lists are visible. SMILES / InChIKey remain resource fields.

```json
{
  "id": "ILJNJJNKEOAREX-UHFFFAOYSA-N",
  "ir_bands_cm-1": [3144.0, 3110.0, 3066.0, 2931.0, 2863.0, 1632.0, 1589.0, 1565.0, 1485.0],
  "ir_source": "experimental",
  "source_doi": "PMC:12566713",
  "pmcid": "PMC12566713",
  "h_nmr": "8.83 (s, 1H), 8.04 (s, 1H), 7.81 (d, J = 8.8 Hz, 2H), 7.72 (d, J = 8.8 Hz, 2H), 3.56 (s, 4H)",
  "c_nmr": "157.5, 140.3, 138.4, 132.4, 127.5, 120.4, 119.0, 116.4, 49.1",
  "smiles": "Brc1ccc(-n2cc(C3=NCCN3)cn2)cc1",
  "inchikey": "ILJNJJNKEOAREX-UHFFFAOYSA-N",
  "has_structure": true,
  "license": "CC-BY",
  "license_pool": "commercial"
}
```

Canonical copy: `docs/figma-pack/listing1_exact_record.json`.

## Type / spacing

- JSON: 6.2 pt mono; line-height ~9.2 pt
- Frame inset 8 pt; canvas pad 8 pt (no title band)
- Molecule: max square fitting right column with ~8 pt pad; preserve aspect

## What NOT to invent

- Do not drop `h_nmr` / `c_nmr` / band list entries
- Do not revert to NTJIYHYWVZYBEX / the Sci Data urea
- Do not redraw the molecule from memory — regenerate via `drawmol.mol_image`

## Rebuild

```bash
python scripts/make_listing1.py
```

Writes `figures/listing1_irexp_record.{svg,pdf,png}` and
`figures/listing1_mol_rdkit.{png,pdf}`.

## Source provenance

- Hugging Face `ilkhamfy/IRexp` → `data/irexp_resolved_commercial.jsonl.gz`
  (`license_pool=commercial`, CC-BY, F2/F3 flags false)
- Formula: RDKit from the record SMILES (`C12H11BrN4`)
