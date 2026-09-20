# Advanced sensing study

Updated 2026-09-20. All implementation results are simulation-only. The active-
reflectance / structured-light main line is unchanged.

## Retained v2 candidate

v2 keeps the full v1 path and adds one reference-relative diversity cube:

1. v1: two orientations × six spatial frequencies × four phase steps × primary
   and controlled-geometry states = 96 sample frames per field of view;
2. v2 auxiliary: 470/550/850 nm × 15°/55° × s/p polarization = 12 intensity
   states per field of view (hardware scheduling is not validated);
3. three clean references are checked for consensus in each path;
4. the diversity score uses the **shape** of log reflectance ratios after removing
   the median common exposure term, so it cannot merely repeat the v1 gain guard;
5. any channel FLAG wins; PASS requires v1 and diversity PASS; otherwise UNKNOWN.

The auxiliary cube was implemented in
`src/rapid_proof_clean/realistic.py` and bounded three-way inference in
`src/rapid_proof_clean/advanced.py`. Configuration is frozen in
`experiments/v2_config.json`; `scripts/run_v2_study.py` regenerates the benchmark.

## Architecture comparison

| Candidate | Independent physical variable? | Implemented in unified benchmark? | Result / decision |
|---|---:|---:|---|
| More structured-light frequencies | No new residue interaction; improves transfer-curve sampling | v1 baseline is already six-frequency | Retain v1, but do not call this an observable-set expansion |
| Multi-angle intensity | Yes: samples angular BRDF and film interference | Yes, 2 angles | Reduced nonmatched false-clean, but UNKNOWN rose strongly; not selected alone |
| Polarization diversity | Yes: samples Fresnel s/p and depolarization response | Yes, s/p | Strongest single diversity arm in this model; retained inside combined v2 |
| Wavelength diversity | Yes: samples absorption, dispersion and interference | Yes, 3 bands | Strong single arm and directly supported by steel residue literature; retained |
| Angle × polarization × wavelength | Yes, joint signature | Yes, 12 features | Selected v2 candidate: lowest nonmatched false-clean with zero clean false-FLAG in the benchmark |
| Phase + amplitude | For flat films, projected fringe phase is unchanged; phase mainly senses geometry/slope | Forward-model negative result recorded | Not promoted. It helps raised defects/wrinkles, not the flat-film boundary being attacked |
| Reference-free sanity checks | No residue information; only validity/closure information | Existing closure/visibility checks plus documented comparison | Retain as UNKNOWN guard, never as proof of clean |
| Threshold-only retuning | No | Deliberately excluded | Rejected: changes operating point without changing identifiability |

## Why the combined arm can add information

A film can match clean reflectance at one wavelength and angle because of Fresnel
interference while differing at another angle, polarization or wavelength. The
new `primary_degenerate_film` adversary searches for precisely this condition:
near-match at unpolarized 550 nm / 15°, contrast elsewhere. v1 false-cleans
86.2% of contaminated pixels across materials; combined v2 reduces this to 5.7%
and flags 94.2% under the frozen simulation assumptions.

That is an observable-set gain, unlike a tighter threshold. It is still not a
physical sensitivity result: the optical constants, film morphology, pose error
and noise distributions have not been calibrated to hardware.

## Reference and bound semantics

The diversity channel uses a three-reference medoid neighborhood. If fewer than
two references are mutually consistent, every pixel is UNKNOWN. The reference
signature is the median of the accepted references. For each pixel, it computes
the reference/sample log ratio across selected features and removes its median;
the maximum absolute residual is the bounded score.

- score ≤ 0.040 log units: auxiliary PASS;
- score ≥ 0.095 log units: auxiliary FLAG;
- between bounds: UNKNOWN.

The gap is intentional abstention. The constants are frozen simulation settings,
not statistically calibrated real error bounds. Common-mode corruption of all
three references still defeats consensus.

## Negative results and non-promotions

**Phase is not a universal extra observable.** Deflectometry phase is valuable for
surface slope/topography, and a raised or wrinkled contaminant may shift it. A
planar thin film can change amplitude, spectrum and polarization without changing
projected phase. Adding phase to the decision would mostly import geometry error
for the present hard case. The deflectometry literature likewise distinguishes
phase/gradient defect response from modulation/reflectivity changes
([review](https://www.frontiersin.org/journals/advanced-optical-technologies/articles/10.3389/aot.2023.1237687/full)).

**More frequencies cannot solve a modulation-identical residue.** They narrow the
same transfer-function estimate. They help model checking and q precision, but
do not distinguish equal observation distributions.

**Reference-free checks cannot certify cleanliness.** Phase closure, saturation,
low signal, exposure consistency and repeated acquisition can invalidate a PASS
and produce UNKNOWN. They cannot turn a clean-equivalent observation into residue
evidence.

## Physical implementation implications

The simulation-retained candidate adds 12 sample intensity states, increasing the
per-view sample count from 96 to 108 before retries. Three reference cubes add 36
reference images but may be amortized only if reference stability is demonstrated.
A division-of-focal-plane polarization camera could reduce sequential captures,
but spatial interpolation and channel imbalance would need new bounds. No hardware
BOM, timing, registration or radiometric calibration claim is updated yet.

## Promotion gate

v2 is promoted only as a **candidate architecture in code**. Physical promotion
requires blinded coupons on glass, stainless steel, HDPE and glazed ceramic with
measured clean repeats, residue mass/thickness proxies, stain size, pose/exposure
perturbations, and preregistered false-clean / UNKNOWN / coverage reporting. Until
then v1 remains the physically unvalidated base and v2 remains a stronger research
hypothesis.
