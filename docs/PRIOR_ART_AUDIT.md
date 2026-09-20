# Prior-art audit — active reflectance / structured light

Audit date: 2026-09-20. This is a technical landscape screen, not a legal
novelty, patentability, validity, or freedom-to-operate opinion. Source IDs map
to `research/source_ledger.csv`. Abstract-level records are identified as such;
absence from the reviewed material means only **not confirmed in this search**.

## What has clearly been done

1. **Structured-light contamination/defect imaging is direct precedent.** S3
   reports reflection and transmission SMAT, mathematical models, simulation,
   physical experiments, reduced modulation at contaminated/defective regions,
   and comparison with uniform illumination. S6 extends modeling and merges
   mutually perpendicular fringe directions. S7 uses two binary structured-light
   patterns for direct contaminant/defect distributions.
2. **Deflectometry and fringe inspection of specular surfaces are established.**
   S8 surveys a broad field, including qualitative defect inspection. It also
   warns that unresolved contamination and actual defects can be observationally
   inseparable, matching this project's scratch/residue ambiguity.
3. **Polarization, multiple angles, multiple wavelengths, and large-area optical
   soiling inspection all have precedent.** S4 proposes DoLP-based UAV mirror
   soiling assessment. S10 evaluates cleaning with natural and 850/940-nm light
   at different incidence angles. These are candidate measurements, not novelty.
4. **Clean references and before/after cleaning comparisons are old.** S5 uses
   an uncontaminated reference, spectral diffuse reflectance/color difference,
   and quantitative recovery after cleaning. S10 likewise compares pre/post wash.
5. **Optical cleanliness imaging in professional settings exists.** S9 reports a
   hospital touch-surface optical study. Its hyperspectral route is additionally
   disfavored by this challenge below TRL 6 (S1).
6. **Multiple-frequency phase measurement predates this work.** S11 analyzes
   two-frequency phase measurement and temporal-noise tradeoffs. Frequency
   diversity cannot be presented as an invention here.

## Baseline elements that are not plausible novelty claims

- screen/projector plus camera;
- sinusoidal structured light and four-phase demodulation;
- two perpendicular orientations;
- modulation loss as a contamination/defect cue;
- multi-frequency acquisition;
- clean-versus-sample comparison;
- optical maps of anomalous regions;
- polarization, angle, wavelength, or before/after cleaning in isolation;
- fast or low-cost implementation without comparative evidence.

## Remaining candidate differentiation

The search did not confirm an exact match for the full assurance workflow:

> multiple-reference confidence and corruption detection → bounded feasible
> proxy intervals → explicit PASS/FLAG/UNKNOWN → controlled repeat for a known
> ambiguity → coverage accounting → adversarial false-clean registry.

That is a **candidate combination/workflow distinction**, not established
novelty. Each optical component has close precedent, and a deeper patent/product
search could invalidate the distinction. The strongest research contribution at
present is transparent handling of assumptions and failure modes, not a new
physical sensing principle.

## Claims that must shrink

- Replace “novel structured-light contamination detector” with “research
  candidate combining established active optical measurements with explicit
  reference-confidence and model-bound decision controls.”
- Replace “proof of clean” with “model-conditional optical proxy screen for
  selected surfaces.”
- Replace “detects residue” with “flags modeled optical responses; real residue
  sensitivity remains unvalidated.”
- Never claim species/strain, microbial load, sterility, real LOD, whole-room
  coverage, or zero real-world false-clean rate.
- Do not describe the v1 invisible-residue sensitivity experiment as evidence:
  the added contrast was a hypothesis, not a measurement, and was rejected from v1.

## Search gaps

Full-text claim-charting remains incomplete for several papers; non-English
patents, commercial inspection systems, unpublished applications, and the
logged-in challenge agreement were not exhaustively reviewed. Novelty and FTO
therefore remain `UNVERIFIED`.
