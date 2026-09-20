# Rapid Proof of Clean — research handoff

Updated 2026-09-20. Current classification:
`SIMULATION_V2_CANDIDATE_WITH_MAJOR_UNVALIDATED_PHYSICAL_ASSUMPTION`.

## Do not repeat

- v0 is frozen at `933c82d51b9de0b5ee8609d3bcf05772348cd8a5` with tag
  `v0-baseline`.
- v1 is complete: three-reference consensus, gain guard, primary plus
  controlled-geometry states, conservative PASS/FLAG/UNKNOWN fusion, and fixed
  adversarial/72-scene benchmarks.
- The submission package and proposal audits were already complete before this
  research round. This round did not add or rewrite final submission text.
- A scoped literature/patent/product landscape, coverage/time model, robustness
  sweep, coupon protocol and preregistration already exist.

## New in this research round

- `docs/PHYSICAL_EVIDENCE_MATRIX.md`: residue × material × optical-observable
  evidence, quantitative anchors and easy/hard-class conclusions.
- `src/rapid_proof_clean/realistic.py`: assumption-driven joint material,
  residue, Fresnel thin-film, structured-light, noise, geometry and registration
  simulator.
- `src/rapid_proof_clean/advanced.py`: exposure-invariant diversity inference
  with three-reference confidence and PASS/FLAG/UNKNOWN bounds.
- `scripts/run_v2_study.py`, `experiments/v2_config.json` and generated v2 result
  files: four materials × eight conditions × six replicates, with explicit
  false-clean, UNKNOWN and coverage reporting.
- `docs/ADVANCED_SENSING_STUDY.md`: implemented angle, polarization, wavelength
  and combined arms; rejected phase-only, threshold-only and reference-free
  observability claims.
- `docs/REALISTIC_SIMULATION_REPORT.md`: assumptions, adversaries and quantitative
  v1→v2 results.
- `docs/FINAL_DIFFERENTIATION_MAP.md`: closer patent mapping and final separation
  of existing technology, combination candidates and engineering details.
- `docs/FRAME_BUDGET_OPTIMIZATION.md`: held-out frame Pareto, retained 44-frame
  v2.1 schedule, staged early-FLAG semantics and legacy-failure parity audit.
- `docs/WORKFLOW_DIFFERENTIATION_EVIDENCE.md`: element-level comparison against
  the closest inspected cleanliness patents and commercial product disclosures.
- Source/claim ledgers and the prior-art matrix now include the new evidence and
  close patent records.

## Physical evidence now established from literature

The best direct quantitative support for diversity is Cho et al. (2007): on
stainless steel, a 469/895-nm reflectance ratio separated wet poultry residues
diluted 1:100 from water/background at 94.0% accuracy; 527/580-nm bands separated
dry residues at 99.7% in that dataset. Food-residue response also changes with
surface material and wavelength. Polarization/specular imaging can recover latent
fingerprint residue and has been investigated for transparent water contamination.

The most important negative evidence is NASA TN D-6585: for tested molecular
films on reflective stainless, visible scatter changed little below about 2 µm
and rose rapidly beyond 2–3 µm. A clear thin film can therefore evade the v1
scatter/modulation channel. Thin-film interference can make oil on glass either
increase or suppress reflectance depending on state.

No published dataset found in this round provides the joint residue mass or
thickness × stain size × surface finish × angle × wavelength × polarization ×
field-noise distribution needed to calibrate this system. Glazed ceramic remains
especially weakly supported by matched quantitative evidence.

## Retained v2.1 candidate

The active-reflectance / structured-light main line remains intact. The candidate
v2 adds 470/550/850 nm × 15°/55° × s/p reference-relative intensity to v1. The
diversity score removes common exposure, so it responds only to signature shape.
Any channel FLAG wins; PASS requires both; ambiguity becomes UNKNOWN.

Frame ablation now retains only the 2 and 48 cycles/screen endpoints in both
structured states: 32 structured frames plus 12 diversity states = **44 maximum
sample frames/FOV**, down 59.3% from 108. A diversity-first schedule can issue an
FOV-level early FLAG at 12 frames, or after primary at 28, but every clean PASS
and complete pixel map requires all 44. Hardware timing, polarization registration
and radiometric bounds have not been established.

On the held-out simulator split, 108 and 44 frames have identical metrics:
nonmatched false-clean 5.531%, UNKNOWN 0.137%, clean PASS 96.330%, clean
false-FLAG 0%, and matched-invisible false-clean 96.519%. The old fixed failures
also remain identical: the compressed dual-state path flags dirty-reference,
uniform-absorber and cancellation cases and still false-cleans the deliberately
observation-matched case. See `docs/FRAME_BUDGET_OPTIMIZATION.md`.

## Frozen realistic-benchmark result

Across all non-clean, non-matched-invisible residue pixels:

- v1 false-clean 44.37%, UNKNOWN 12.21%, usable coverage 87.79%;
- combined v2 false-clean 5.57%, UNKNOWN 0.16%, usable coverage 99.84%;
- clean: v1 PASS 100%; v2 PASS 96.48%, UNKNOWN 3.52%, false-FLAG 0%;
- v1-degenerate film: false-clean 86.23% → 5.66%;
- matched-invisible: v1 false-clean 100%; v2 false-clean 96.55%, UNKNOWN 3.45%,
  FLAG 0%.

The improvement is substantive **inside the model** because new optical variables,
not a threshold change, expose a one-state-degenerate film. It is not evidence of
real sensitivity or specificity.

## Observable boundary

“Optically invisible” now has two explicit meanings:

1. **v1-degenerate but diversity-visible:** nearly clean-equivalent at the v1
   central reflectance state, different across wavelength/angle/polarization;
   candidate v2 improves this case in simulation.
2. **fully observation-matched:** identical to clean in every retained state;
   neither v1 nor v2 can FLAG it. Noise can only cause abstention. No optical
   decision rule can solve this without adding a physically responsive observable.

## Novelty / differentiation state

US8229204B2 closely covers ware-type-specific optical environments plus clean and
stained control wares; US7286218B2 covers surface confidence maps and statistical
significance; EP0903572A2 covers reference normalization; US20090015824A1 covers
multiwavelength contamination ratios. Together with structured-light,
polarization, remeasurement, reject-option and coverage prior art, no individual
ingredient is a credible novelty anchor.

The broad sequence is no longer a credible distinction: SITA, Evident CIX100 and
iFactory public product material collectively disclose normalized/full-surface
maps, calibration/self-checks, limits or pass/fail, re-cleaning guidance,
coverage and records. The remaining narrow hypothesis is the clean-PASS
conjunction: reference integrity ∧ bounded evidence across required active states
∧ coverage validity, with any failed premise forced to UNKNOWN and used to select
remeasurement, plus a false-clean release audit. No inspected public record stated
the complete conjunction. Novelty, non-obviousness and freedom to operate remain
unverified; see `docs/WORKFLOW_DIFFERENTIATION_EVIDENCE.md`.

## Reproduce

```powershell
& .\.venv\Scripts\python.exe scripts\run_v2_study.py
& .\.venv\Scripts\python.exe scripts\run_frame_optimization.py
& .\.venv\Scripts\python.exe scripts\run_submission_pipeline.py
```

The canonical pipeline now regenerates v0/v1, robustness/coverage, v2 results,
existing proposal artifacts, repository verification, ruff and pytest. Generation
does not change the proposal claims unless source files are deliberately edited.

## Next scientific gate

Run the existing coupon protocol with the diversity states on named glass,
stainless, HDPE and glazed-ceramic finishes. Measure clean-repeat covariance first,
then blinded water/oil/protein/detergent/particle deposits across stain size and a
thickness or mass proxy. Freeze bounds on calibration coupons and report
false-clean, UNKNOWN, false-FLAG and visible coverage on held-out coupons.

## Three largest remaining risks

1. **Uncalibrated physical response:** the impressive v2 reduction may disappear
   when real residue morphology, optical constants and sensor noise replace
   assumptions.
2. **Reference/common-mode and material variation:** three references cannot
   identify shared contamination, and real finishes/aging may exceed the frozen
   bounds or drive excessive UNKNOWN/false-FLAG.
3. **Fundamental and operational coverage:** fully observation-matched thin films,
   small stains at registration boundaries, occluded areas and 44-frame timing
   remain unresolved.
