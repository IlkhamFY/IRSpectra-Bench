# Morning handoff — ICLR Figma pack (0800 ET)

**Landed:** 2026-09-20 on `cursor/figma-pack-land-440e` (stacked on
`cursor/iclr-night-strengthen-20260920-c33d` / PR #14).
**Built overnight for:** Ilkham Yabbarov — IRSpectra-Bench ICLR figures.
**Do not wait:** files and tex wiring are in-repo.

## Where files landed

### Vectors (`figures/`)

| Asset | Repo paths | Role |
|-------|------------|------|
| **Lead Fig 1** | `figures/fig1_lead_overview.{pdf,svg,png}` | Canonical lead (protocol → equation → wall). Wired as Fig.~1. |
| **Listing 1** | `figures/listing1_irexp_record.{pdf,svg,png}` | IRexp JSON + molecule. Exact record `NTJIYHYWVZYBEX-UHFFFAOYSA-N`. Wired near setup. |
| **Molecule** | `figures/listing1_mol_rdkit.{pdf,png}` | RDKit asset for that record only. |
| **Wall diagnostic** | `figures/fig_wall_diagnostic.{pdf,svg,png}` | 58 verified / 7 mis-ranked / 129 never proposed (n=194). Wired as Fig.~wall. |

Kept, not overwritten (not cited by this stack's `main.tex`):

- `figures/fig1_overview.{pdf,png}` — sibling `bc-201e83c7` a/b/c plate. Same 58/7/129.
- `figures/fig_wall.{pdf,png}` — prior diagnostic; same 58/7/129; different palette.
- `figures/fig_listing_mol.{pdf,png}` — v3-R25 molecule (worked-case / mechanism, not Listing 1).

### Specs / sources (`docs/figma-pack/`)

- `FIG1_BUILD_SPEC.md`, `LISTING1_BUILD_SPEC.md`, `WALL_BUILD_SPEC.md`, `TOKENS.md`
- `listing1_exact_record.json`, `LOCKED_FACTS.md`
- this brief

## Tex wiring — done (`main.tex`)

| Slot | Include | Notes |
|------|---------|-------|
| Fig.~1 (`fig:fig1`) | `fig1_lead_overview.pdf` | Caption is protocol + $30\% \approx 34\% \times 89\%$ + wall 58/7/129. No (a)/(b)/(c). |
| Listing 1 (`lst:payload`) | `listing1_irexp_record.pdf` | Companion IRexp record. Prose still says solvers see only formula + peak lists; SMILES / InChIKey are resource fields. |
| Diagnostic wall (`fig:fig-wall`) | `fig_wall_diagnostic.pdf` | Same 58/7/129. Appendix diagnostic (not the only figure). |

`iclr_paper.tex` remains the `\input{main}` shim.

## Exact numbers used (all from locked sources)

| Claim | Value |
|-------|-------|
| Instrumented wall n | 194 |
| top-1 constitution (locked slice) | 28.4% [22–35]; simple 48.0%; complex 8.3% |
| recovered top-3 | 33.5%; simple 54.1%; complex 12.5% |
| generation recall (locked slice) | 65/194 = 34% |
| Wall | verified **58** \| mis-ranked **7** \| never proposed **129** |
| Bracket | `65 recalled (34%)` |
| precision\|recall (forward-verify) | 58/65 = 89% |
| forward-verified top-1 | 58/194 = 30% |
| Verification alone (diagnostic) | 28% → 30% |
| Formula-only control | 3/60 (5%) vs formula+IR+¹H+¹³C 14/60 (23%) |
| IRexp | 121,233 records; 43,060 structure-linked; 33,201 full quadruples |
| Listing 1 id | `NTJIYHYWVZYBEX-UHFFFAOYSA-N` (full JSON unchanged) |

`LOCKED_FACTS.md` is the **figure-lock** list (n=194 instrumented slice). Paper
headline remains **n=300** generation (118/300; 133/300).
Do not read this pack as a headline rewrite.

## Coordination

- `bc-201e83c7` told not to duplicate. Their `fig1_overview` files remain on disk; tex prefers Figma Bro filenames.
- `bc-fef3e36b` — strengthen PR #14. This stack merges onto that tip.
- No new metrics.
