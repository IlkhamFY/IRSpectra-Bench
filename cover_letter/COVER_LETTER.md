# Cover letter — IRSpectra-Bench (ICLR 2027)

**Template:** McMaster letterhead LaTeX (same Rodrigo shell as IRexp / ParetoMol): `cover_letter/cover_letter.tex` + `mcm-col_png.png`.
**Manuscript:** Molecular Structure Elucidation with Frontier Models: A Benchmark on Literature-Reported IR, ¹H, and ¹³C NMR Peak Lists
**Venue:** ICLR 2027 (conference paper)
**Signatory (template convention):** Rodrigo A. Vargas-Hernández (vargashr@mcmaster.ca), on behalf of all authors
**Coauthors:** Ilkham Yabbarov; Rudra Sondhi; Rodrigo A. Vargas-Hernández

---

Dear Program Chairs,

We submit our manuscript entitled *Molecular Structure Elucidation with Frontier Models: A Benchmark on Literature-Reported IR, ¹H, and ¹³C NMR Peak Lists* for consideration as a conference paper at *ICLR 2027*.

Frontier models have shown strong performance on molecular structure elucidation, but it is unclear how well those results transfer to heterogeneous experimental reports. We ask an operational question: given only a molecular formula and literature-reported IR, ¹H and ¹³C NMR peak lists—not digitised spectral images—can an off-the-shelf frontier model recover the correct constitution, and which stage fails when it cannot?

We introduce **IRSpectra-Bench**, a blind, mechanically scored peak-list benchmark scored on 500 compounds drawn from redistributable experimental band lists (**IRexp**), with a fixed RDKit InChIKey-connectivity scoring contract and decomposable generation-recall / verification-precision metrics.
On IRSpectra-Bench, a frontier model recovers 45.4% top-1 (227/500) and 49.8% generation recall (249/500).
The bottleneck is candidate proposal, not verification: the n=500 forward-verify wall is 204 verified / 45 misranked / 251 never proposed.
The same recall ≪ precision asymmetry replicates across four vendor families.

This work was supported by NSERC funding reference number 596133-2025 (CREATE for Accelerated Discovery, AccelD), delivered through the Acceleration Consortium.

All authors confirm that this manuscript has not been previously published and is not under consideration elsewhere. The authors have approved the submitted version and agree to ICLR 2027's submission policies.

Best regards,  
Rodrigo A. Vargas-Hernández, on behalf of all authors  
email: vargashr@mcmaster.ca
