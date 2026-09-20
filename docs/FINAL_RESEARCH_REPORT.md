# Final computational research report

Updated 2026-09-20. Status: computational package complete; physical validation
not started.

## Decision

Retain **v2.2 adaptive reference-guarded active reflectance** as the final research
candidate. It keeps the active-reflectance/structured-light main line, adds no
biochemical claim, and changes the release logic more than the sensor inventory:
cheap states can FLAG early, but only a complete 36-frame evidence certificate can
proxy-PASS. A 60-frame primary state is reserved for diagnostic escalation.

## Quantitative result

- Original retained simulator: v2.1 and v2.2 both have 5.568% nonmatched pixel
  false-clean, 0.158% UNKNOWN, 96.480% clean PASS and 0% clean false-FLAG.
- Normal clean FOV certificate: 44 → 36 frames; original v2 maximum 108 → 36.
- Independent-response domain shift: fixed v2.1 11.667% vs adaptive v2.2 1.111%
  observable-dirty FOV false-clean; v2.2 UNKNOWN 22.222% vs 12.778%.
- Selected full stress-set frames: mean 22.70, median 4, p95 60, max 60. These
  values include deliberate failure/reference cases; nominal clean is 36 frames.
- Exact matched-invisible control: 100% false-clean under all policies.
- Random adversarial search: 136/400 PASS, predominantly below the 5% spatial-
  support rule.

The improvement is real within the synthetic test suites but not a physical
performance claim. It trades more abstention and a 60-frame tail for a large
reduction in model-mismatch false-clean.

## Major assumption compression

The work removed three avoidable assumptions:

1. endpoint frequencies were not treated as universally sufficient; a middle
   frequency is now required for PASS;
2. agreement among live references was not treated as proof of clean origin; a
   dated external anchor is required;
3. missing/failed states cannot silently shrink the model; they force UNKNOWN.

The remaining major physical assumption cannot be compressed computationally:
important real residue/material/finish strata must change at least one retained
observable by more than field noise and drift.

## Physical evidence synthesis

Published work establishes that some residues change wavelength ratios,
polarization, reflectance, scatter and thin-film interference. The most relevant
quantitative examples remain stainless-steel food-residue spectral classification,
NASA film-thickness/scatter measurements and fluorescence/HSI studies with
material-dependent small-object limits. None transfers a detection boundary to
this architecture. Clear sub-micron/index-matched films, small-support stains and
strongly textured backgrounds remain hardest.

## Differentiation conclusion

The optics are crowded prior art. Clean references, controlled illumination,
multi-state imaging, repeated cleaning measurement, coverage thresholds,
confidence and reports are also individually known. A 2025 ASML PCT application
further discloses optical cleanliness measurement, a clean-reference ratio and
iterative measure/clean control for sensor surfaces. The defensible technical
position is therefore narrow: a cleaning-screening **release obligation** that
conjoins dated-anchor reference qualification, bounded multi-state evidence,
explicit coverage, abstention and false-clean audit. The scoped search did not
locate that exact conjunction, but novelty and FTO remain unverified.

## Stop condition reached

Further simulated threshold tuning would overfit chosen generators. The unresolved
questions are now physical: contrast magnitude, noise/drift bounds, resolution,
reference lifecycle, operator timing and linkage to accepted cleanliness ground
truth. The repository therefore stops at TRL 2 and hands off to the preregistered
coupon study.
