# Cover letter — IRSpectra-Bench (ICLR 2027)

**Template:** McMaster letterhead LaTeX (same Rodrigo shell as IRexp / ParetoMol): `cover_letter/cover_letter.tex` + `mcm-col_png.png`.
**Manuscript:** Proposal, Not Ranking, Binds Structure Elucidation from Literature Peak Lists
**Venue:** ICLR 2027 (conference paper)
**Signatory (template convention):** Rodrigo A. Vargas-Hernández (vargashr@mcmaster.ca), on behalf of all authors
**Coauthors:** Ilkham Yabbarov; Rudra Sondhi; Rodrigo A. Vargas-Hernández

---

Dear Program Chairs,

We submit our manuscript entitled *Proposal, Not Ranking, Binds Structure Elucidation from Literature Peak Lists* for consideration as a conference paper at *ICLR 2027*.

Frontier models report strong recovery on curated libraries, simulated traces, or single-instrument absorbance. We do not rescore those systems. We ask whether one off-the-shelf closed-book model, given only a molecular formula and literature-reported IR, ¹H and ¹³C NMR peak lists, proposes the correct constitution, and whether ranking is what fails when it does not.

We release **IRSpectra-Bench** as a frozen roster of 500 problems, an RDKit InChIKey-14 contract, and deposits a mechanical scorer can replay. It is a factorised diagnosis, not a populated board.
On one harness, generation top-1 is 45.4% (227/500) and recall is 49.8% (249/500).
The generation wall is 227 exact top-1 / 22 in-pool not top-1 / 251 never proposed.
Corpus-reweighted top-1 on a validate-clean subset is 26.5%.
Forward verification of the same pools lowers top-1 from 227/500 to 204/500.
The recall gap on a 60-compound arm, not on the n=500 cohort, appears across four vendor families.

This work was supported by NSERC funding reference number 596133-2025 (CREATE for Accelerated Discovery, AccelD), delivered through the Acceleration Consortium.

All authors confirm that this manuscript has not been previously published and is not under consideration elsewhere. The authors have approved the submitted version and agree to ICLR 2027's submission policies.

Best regards,  
Rodrigo A. Vargas-Hernández, on behalf of all authors  
email: vargashr@mcmaster.ca
