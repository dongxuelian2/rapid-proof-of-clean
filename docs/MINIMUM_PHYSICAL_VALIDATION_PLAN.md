# Minimum physical validation plan

Status: **DESIGN ONLY — NOT PERFORMED**. This plan must not be described as data.

## Question

Can a low-cost camera/display active-reflectance setup distinguish controlled
clean and residue conditions on selected smooth surfaces, while detecting a
corrupt reference and avoiding false-clean decisions under pose/gain nuisance?

## Minimum hardware

- existing RAW-capable camera or manually controlled webcam;
- existing LCD/tablet/monitor capable of full-screen phase patterns;
- rigid stands, ruler, angle guide, and non-gloss black shroud;
- three clean reference coupons stored separately;
- optional inexpensive linear polarizer pair only after primary measurements;
- no biological culture, pathogen, unsafe chemical, or laboratory claim.

Exact device models, cost, linearity, bit depth, spectral response, and timing
must be recorded when selected; none is currently selected.

## Surfaces and safe contamination surrogates

Use at least glass, stainless steel, and smooth laminate coupons. Include a rough
or matte surface as an out-of-scope control. Candidate safe surrogates are
measured deposits of food-grade oil and dried sugar/protein-free solution; exact
materials require a participant safety review. Use volume/mass preparation notes,
not microbial labels. Include permanent scratch/tape-edge controls to test anomaly
versus removable residue ambiguity.

## Reference procedure

1. Define and document a repeatable clean/rinse/dry protocol.
2. Capture three independently prepared reference acquisitions per material.
3. Seal/date references and repeat them at session start/end.
4. Deliberately contaminate one reference in a blinded challenge while retaining
   two clean references; later challenge two-of-three to demonstrate the limit.
5. Track pairwise reference distance and confidence; do not infer “clean” from
   agreement alone without the preparation record.

## Acquisition protocol

For each material × residue level × nuisance condition:

1. capture dark/flat controls and verify no clipping;
2. capture two orientations × six frequencies × four phases at the primary state;
3. recapture at the registered high-SNR state without cleaning the coupon;
4. record distance, angle, focus, exposure, ambient light, temperature, and time;
5. repeat after randomized removal/repositioning;
6. optionally add angle or polarization only as a separately labeled experiment.

## Controls and repetitions

- negative clean controls and sham handling;
- positive visible residue controls;
- blinded labels during algorithm execution;
- dirty-reference, gain-change, pose/focus, scratch, occlusion, saturation, and
  deliberately optically low-contrast controls;
- minimum 5 independently prepared coupons or preparations per material/level,
  with 3 repositioned captures each; pixels are not independent replicates;
- fixed algorithm/configuration before opening blinded results.

## Endpoints

Primary: scene-level false-clean rate with exact binomial interval, UNKNOWN rate,
usable coverage, and zero-residue PASS/FLAG rates. Secondary: reference-corruption
detection, repeatability of fitted `q`, material/angle stratification, capture
time, compute time, and visible-area fraction. Report FLAG as optical anomaly,
not confirmed residue.

## Decision criteria

Proceed only if (a) no blinded positive preparation is PASS in the pilot, (b)
UNKNOWN is not used for nearly all positives, (c) at least 90% of eligible clean
control scenes remain PASS, (d) the one-of-three dirty reference is rejected, and
(e) repeatability supports predeclared bounds. These are pilot gates, not product
specifications. Any false clean triggers root-cause review before scale-up.

Fail or rescope if real residues do not reproducibly affect a measured channel,
surface nuisance overwhelms response, two-of-three reference corruption is
plausible operationally, coverage/time is incompatible with the challenge, or
the required contrast needs a challenge-excluded modality.
