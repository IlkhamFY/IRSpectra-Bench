# Cover letter — IRSpectra-Bench (ICLR 2027)

**Template:** McMaster letterhead LaTeX (same Rodrigo shell as IRexp / ParetoMol): `cover_letter/cover_letter.tex` + `mcm-col_png.png`.
**Manuscript:** Generation Recall, Not Verification, Binds LLM Structure Elucidation from Literature Spectra
**Venue:** ICLR 2027 (conference paper)
**Signatory (template convention):** Rodrigo A. Vargas-Hernández (vargashr@mcmaster.ca), on behalf of all authors
**Coauthors:** Ilkham Yabbarov; Rudra Sondhi; Rodrigo A. Vargas-Hernández

---

Dear Program Chairs,

We submit our manuscript entitled *Generation Recall, Not Verification, Binds LLM Structure Elucidation from Literature Spectra* for consideration as a conference paper at *ICLR 2027*.

Frontier LLMs are often presented as near-solved structure elucidators on curated spectra. We ask a harder operational question: given the molecular formula and literature-reported IR / ¹H / ¹³C peak lists—not digitised traces—can an off-the-shelf LLM recover the correct constitution, and which stage fails when it does not?

We introduce **IRSpectra-Bench**, a blind, mechanically scored peak-list benchmark scored on 500 compounds (194 locked + all 106 expansion + 200 validate-clean expand-500; R01–R75 cut) drawn from redistributable experimental band lists (**IRexp**; companion Scientific Data Data Descriptor, in preparation), with a fixed RDKit InChIKey-connectivity scoring contract and decomposable generation-recall / verification-precision metrics.
On IRSpectra-Bench, a frontier LLM recovers the correct constitution for 45.4% top-1 (227/500); generation recall is 49.8% (249/500). No CIs on this pool.
The bottleneck is candidate proposal, not verification: on the instrumented n=194 slice, the true structure enters the pool for only 34% of compounds, and where it does, training-free forward-verification selects it 89% of the time (58/65).
The same recall ≪ precision asymmetry replicates across four vendor families.
Former n=300 and n=524 / n=530 stay appendix; expand-500 fverify is not a pooled wall.
This ICLR paper cites IRexp as infrastructure and does not re-present a Data Descriptor.

This work was supported by NSERC funding reference number 596133-2025 (CREATE for Accelerated Discovery, AccelD), delivered through the Acceleration Consortium.

All authors confirm that this manuscript has not been previously published and is not under consideration elsewhere. The authors have approved the submitted version and agree to ICLR 2027's submission policies.

Best regards,  
Rodrigo A. Vargas-Hernández, on behalf of all authors  
email: vargashr@mcmaster.ca
