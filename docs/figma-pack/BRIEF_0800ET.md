# Morning handoff — ICLR Figma pack (0800 ET)

**Landed:** 2026-09-20 on `cursor/figma-pack-land-440e` (stacked on
`cursor/iclr-night-strengthen-20260920-c33d` / PR #14).
**Built overnight for:** Ilkham Yabbarov — IRSpectra-Bench ICLR figures.
**Do not wait:** files are in-repo; no human action required to receive them.

## Where files landed

### Vectors (`figures/`)

| Asset | Repo paths | Role |
|-------|------------|------|
| **Lead Fig 1** | `figures/fig1_lead_overview.{pdf,svg,png}` | Canonical new lead (protocol → equation → wall). Prefer PDF for `\includegraphics`. |
| **Listing 1** | `figures/listing1_irexp_record.{pdf,svg,png}` | IRexp JSON + molecule. Exact record `NTJIYHYWVZYBEX-UHFFFAOYSA-N`. |
| **Molecule** | `figures/listing1_mol_rdkit.{pdf,png}` | RDKit asset for that record only. |
| **Wall diagnostic** | `figures/fig_wall_diagnostic.{pdf,svg,png}` | 58 verified / 7 mis-ranked / 129 never proposed (n=194). |

Existing overnight plates were **kept**, not overwritten:

- `figures/fig1_overview.{pdf,png}` — sibling `bc-201e83c7` protocol plate (a/b/c + v3-R25). Same locked 58/7/129. Stronger multi-panel visual; different composition than the Figma lead.
- `figures/fig_wall.{pdf,png}` — paper diagnostic already cited by `main.tex`. Same 58/7/129 semantics; different palette (blue vs teal/vermil/grey).
- `figures/fig_listing_mol.{pdf,png}` — solver-facing v3-R25 molecule (gold held out). **Not** the IRexp commercial DoR record.

### Specs / sources (`docs/figma-pack/`)

- `FIG1_BUILD_SPEC.md`, `LISTING1_BUILD_SPEC.md`, `WALL_BUILD_SPEC.md`, `TOKENS.md`
- `listing1_exact_record.json`, `LOCKED_FACTS.md`
- this brief

## Tex wiring — skipped

`main.tex` (source of truth; `iclr_paper.tex` is a shim) was **not** edited.

Sibling `bc-fef3e36b` / `bc-201e83c7` already wired PR #14 to `fig1_overview.pdf`
with panel (a)/(b)/(c) captions and several `Figure~\ref{fig:fig1}c` callouts, plus
a solver-facing Listing 1 (`v3-R25`, gold held out). Switching the lead include to
`fig1_lead_overview` would require rewriting those panel refs while those agents
are still running — messy conflict, so files-only this pass.

**When night edits settle**, a one-line swap is:

```latex
\includegraphics[width=\linewidth]{fig1_lead_overview.pdf}
```

Caption should then describe the blind peak-list protocol + recall-bound diagnosis
(equation `30% ≈ 34% × 89%`; wall 58/7/129). Do **not** keep “(a)/(b)/(c)” language
unless the included plate still has those panels.

Do **not** replace the solver-facing Listing 1 (`lst:payload` / v3-R25) with
`listing1_irexp_record`. That PDF is the companion IRexp example record
(`NTJIYHYWVZYBEX-UHFFFAOYSA-N`) and **includes** SMILES / InChIKey. Fit it near
the dataset pointer / Appendix A if a second listing is wanted. Do not invent
claims.

Wall in the paper stays diagnostic (`fig_wall` or `fig_wall_diagnostic`). Same
locked counts. Chem partner: wall is not the only figure.

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
headline on the night branch remains **n=300** generation (118/300; 133/300).
Do not read this pack as a headline rewrite.

## Coordination

- `bc-201e83c7` — Fig1 + Listing1 overnight plate (`fig1_overview`, v3-R25 listing). Still running at land time. Kept their vectors.
- `bc-fef3e36b` — strengthen PR #14. Still running at land time. Tex left to them.
- This land: Figma Bro pack only. No new metrics.

## Recommendation (morning)

1. **Lead** with `figures/fig1_lead_overview.pdf` once tex is free.
2. Keep `fig_wall` / `fig_wall_diagnostic` as **diagnostic** (not sole lead).
3. Keep solver Listing 1 as v3-R25; IRexp record is a companion example only.
4. Prefer locked counts above if any later vector drifts.
