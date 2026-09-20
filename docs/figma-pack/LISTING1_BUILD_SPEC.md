# LISTING1_BUILD_SPEC — `listing1_irexp_record`

Adapted from IRexp Scientific Data `lst:example` for ICLR handoff.

## Frame

| | Print (pt) | @2x px |
|--|------------|--------|
| Width | 504 (7.0 in) | 1008 |
| Height | 280 (~3.89 in) | 560 |

## Layout

- **Title line** above frame: `Listing 1. Example IRexp JSON record (commercial DoR).`
- **Framed two-column** (rounded rect, fill `#F7F7F5`, stroke `#E5E5E0`):
  - Left **~62%**: monospace JSON (exact fields; wrap long NMR — do not truncate values)
  - Gap **~4%**
  - Right **~34%**: molecule image centered (`listing1_mol_rdkit.pdf` / `.png`)

## Exact JSON (verbatim field values)

```json
{
  "id": "NTJIYHYWVZYBEX-UHFFFAOYSA-N",
  "ir_bands_cm-1": [3337.0, 2969.0, 1633.0, 1556.0, 1505.0, 1240.0, 1181.0, 1071.0, 826.0],
  "ir_source": "experimental",
  "source_doi": "PMC:13029360",
  "pmcid": "PMC13029360",
  "h_nmr": "8.07 (brs, 1H, NH), 7.25 (d, J = 7.3 Hz, 2H, Ar), 6.78 (d, J = 7.3 Hz, 2H, Ar), 6.25 (d, J = 8.1 Hz, 1H, NH), 4.10 (hex, J = 8.1 Hz, 1H, CH), 3.66 (s, 3H, OCH3), 2.23-2.09 (m, 2H, CH2), 1.90-1.71 (m, 2H, CH2), 1.64-1.51 (m, 2H, CH2)",
  "c_nmr": "154.8, 154.4, 134.0, 119.9, 114.3, 55.5, 45.0, 31.8, 14.8",
  "smiles": "COc1ccc(NC(=O)NC2CCC2)cc1",
  "inchikey": "NTJIYHYWVZYBEX-UHFFFAOYSA-N",
  "has_structure": true,
  "license": "CC-BY",
  "license_pool": "commercial"
}
```

Canonical copy: `sources/listing1_exact_record.json`.

## Type / spacing

- Title: 10 pt bold sans (`TOKENS.md` `listing-title`)
- JSON: 6.2 pt mono; line-height ~9.2 pt
- Left column pad: 8 pt from frame edge
- Molecule: max square fitting right column with ~8 pt pad; preserve aspect

## What NOT to invent

- Do not drop `h_nmr` / `c_nmr` / band list entries
- Do not substitute a different InChIKey or SMILES
- Do not redraw the molecule from memory — use shipped `listing1_mol_rdkit.*`

## Figma paste handoff

1. Place `vectors/listing1_irexp_record.svg` or rebuild two-column frame.
2. Paste JSON from `sources/listing1_exact_record.json` into a mono text layer; enable wrapping.
3. Place `vectors/listing1_mol_rdkit.png` (or PDF) in right column.
4. Export SVG + PDF + PNG @2x.

## Source provenance

- `/workspace/IRexp_fresh/scientific_data.tex` (`lst:example`)
- Molecule: `/workspace/IRexp_fresh/figures/fig_example_mol_rdkit.{pdf,png}`
