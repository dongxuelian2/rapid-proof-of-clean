# Minimum physical coupon protocol

**Status: designed, not executed.** No physical images or instrument data were
found in the repository on 2026-09-20.

## Purpose

Determine whether the retained optical states respond reproducibly to selected
surface/residue combinations, and measure nuisance bounds needed for an honest
go/no-go decision. This is not a microbial efficacy or safety study.

## Minimum design

- Materials: stainless steel, glass, glazed ceramic, high-pressure laminate and
  one textured polymer; at least three independently prepared coupons per class.
- Deposits: a transparent oil film, proteinaceous food soil surrogate, detergent
  film and water/mineral residue. Include optically subtle negative controls.
- Levels: blank plus at least four gravimetrically or volumetrically prepared
  areal levels spanning the expected cleaning-residue range.
- Replication: three independent preparation days × three coupons × two operators;
  repeated mounts, randomized order and blinded labels.
- Nuisances: distance/angle, exposure, warm-up, illumination gradient, drying time,
  clean-reference age, roughness, occlusion and one missing-frame condition.
- Ground truth: preparation log and independent mass/volume protocol; optional ATP
  or chemistry is a comparator, not truth for the optical proxy.

## Procedure

1. Lock hardware, firmware, code commit, references, thresholds and exclusions.
2. Capture dark/flat/linearity/MTF checks and three clean references.
3. Randomize blinded coupons; collect primary and controlled states plus metadata.
4. Run the frozen pipeline once. Do not manually relabel `UNKNOWN`.
5. Reclean flagged coupons, repeat once, and log persistent outcomes.
6. Unblind only after hashes and outputs are archived.

## Minimum endpoints

Report per material/residue/level: PASS/FLAG/UNKNOWN counts by independent coupon,
false-clean proportion with interval, false-flag proportion on blanks, repeatability,
coverage, time and invalid/reacquisition rate. Pixels are not independent trials.

## Stop / go criteria

Stop the broad claim if any preregistered high-priority condition yields a
false-clean point estimate above 5%, if common-mode dirty references can pass, or
if conservative 12 m² projected time exceeds 30 minutes after measured inputs.
Proceed only to a larger blinded study when every material-specific acceptance
criterion in the preregistration is met. These thresholds are engineering choices,
not regulatory standards.
