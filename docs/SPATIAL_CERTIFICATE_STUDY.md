# Multiscale spatial clean-certificate study

Updated 2026-09-20. Final classification: **PARTIAL**. This is a fixed-seed
synthetic aggregation study, not physical validation or a resolution claim.

## Frozen baseline

The baseline is commit `d9651deab163e0bbd651bbe2326d4d613d2a6e29`, v2.2
`adaptive_standard`. Its sensing states, pixel evidence, 2→4→12→28→36 acquisition
and optional 60-frame diagnostic were frozen. Baseline facts retained unchanged:

- original-model nonmatched pixel false-clean 5.568%, UNKNOWN 0.158%;
- clean PASS 96.480%, false-FLAG 0%, UNKNOWN 3.520%;
- domain-shift observable-dirty FOV false-clean 1.111%, UNKNOWN 22.222%;
- the original 400-case search produced 136 PASS.

The old FOV rule allowed PASS with at least 95% visible pixels PASS and no FLAG.
Every one of the 136 replayed adversarial PASS cases contained local non-PASS
evidence at the constructed residue support: they were class A, observable but
spatially diluted. None was class B in that replay. This does not imply that class
B is absent physically; the focused search retained one locally unobservable PASS.

## Benchmark protocol

Design, validation and frozen held-out splits use disjoint seed ranges. Each split
contains 160 contaminated FOVs: ten support levels (0.1%, 0.25%, 0.5%, 1%, 2%,
3%, 4%, 5%, 7.5%, 10%) × eight morphologies × two replicates. Morphologies are
compact blob, elongated streak, edge blob, corner blob, multiple droplets,
dispersed sparse pixels, PSF-blurred residue and registration-shifted residue.
Each split also contains 96 clean FOVs spanning nominal, texture, roughness,
illumination gain, edge artifact and registration nuisance.

Candidate forms and thresholds were fixed before held-out reporting. Validation
selected among aggressive, balanced and conservative policies subject to no more
than a five-percentage-point clean-PASS loss and no increase in false-FLAG. The
held-out split was report-only. The full per-case table is
`experiments/small_support_benchmark.csv`.

## Candidate comparison

On validation, aggressive reduced `<5%` false-clean to 12.50% but cut clean PASS
from 73.96% to 59.38%; it was rejected. Balanced reduced it to 35.71% with clean
PASS unchanged at 73.96%. Conservative reached 38.39%, also with unchanged clean
PASS. Balanced dominated conservative on the primary safety endpoint and was
frozen.

Frozen held-out results:

| Metric | global 95% baseline | balanced spatial certificate |
| --- | ---: | ---: |
| `<5%` support false-clean | 66.96% | 41.07% |
| all contaminated false-clean | 50.63% | 30.00% |
| contaminated FLAG | 29.38% | 29.38% |
| contaminated UNKNOWN | 20.00% | 40.63% |
| clean PASS | 76.04% | 75.00% |
| clean false-FLAG | 0% | 0% |
| clean UNKNOWN | 23.96% | 25.00% |

This is a 25.89 percentage-point, 38.7% relative reduction in `<5%` false-clean
for a 1.04 percentage-point clean-PASS cost. It moves suspicious cases to UNKNOWN;
it does not manufacture new positive evidence or convert them to FLAG.

On the pre-existing domain-shift suite, the spatial rule leaves the selected-policy
result unchanged: observable-dirty false-clean 1.111%, FLAG 76.667%, UNKNOWN
22.222%; clean PASS 100%, false-FLAG 0% and UNKNOWN 0%. It therefore does not buy
the small-support result by degrading that earlier robustness benchmark.

## Final rule

The retained balanced certificate requires the existing global 95% rule plus:

- 8×8 tiles contain at most 24% non-PASS;
- fully visible sliding windows contain at most 80%, 24% and 8% non-PASS at
  4×4, 8×8 and 16×16 scales;
- an 8-connected non-PASS component has area at most 15 pixels and longest span
  at most 20 pixels;
- a four-pixel edge band contains at most 10% non-PASS.

Any pixel FLAG still makes the FOV FLAG. A local-rule violation returns UNKNOWN at
the existing 36-frame certificate; it does not trigger more acquisition. The
certificate performs fixed tiles, three local convolutions, one component-labeling
pass and one edge reduction on the existing 32×32 status map. Additional optical
states and measurement frames are both zero.

## Morphology and support boundary

Held-out false-clean improved most for PSF-blurred cases (40%→0%), compact blobs
(65%→35%), corner blobs (60%→25%) and registration-shifted blobs (60%→30%). It
improved less for dispersed sparse pixels (50%→50%), edge blobs (55%→40%), streaks
(40%→30%) and multiple droplets (35%→30%). By support, false-clean changed from
75.0%→66.7% below 1%, 62.5%→50.0% at 1–2%, and 54.7%→12.5% at 2–5%.

The original 400-case replay changed from 136 to 93 PASS. Its 136 baseline PASS
cases comprised 81 below 1%, 22 at 1–2% and 33 at 2–5%; by morphology they were
37 droplets, 36 particle fields, 35 patchy/diffuse cases and 28 streaks. All 136
were class A observable-but-diluted in this construction. A new focused 400-case
search changed from 233 baseline PASS to 175 balanced PASS; 174 survivors had
local evidence below the frozen spatial limits and one was locally unobservable.
Thus the main residual boundary is sub-1% and dispersed evidence, not an excuse to
lower every threshold or make every isolated UNKNOWN fatal.

## Decision

**PARTIAL.** The certificate materially reduces the repairable spatial-dilution
failure without false-FLAG or large clean-usability loss, but it does not remove
small-support false-clean. Aggressive thresholds would buy more synthetic safety
only by rejecting too many clean nuisance FOVs. Real PSF, pixel footprint,
registration, material response and clean-texture distributions must now set the
spatial limits. Further synthetic tuning is frozen.
