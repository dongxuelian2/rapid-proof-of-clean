# Phase 1 de-risking report

Date: 2026-09-20

Scope: active-reflectance / structured-light Rapid Proof of Clean

Evidence ceiling: **SYNTHETIC_ONLY; no physical validation was performed**

Labels used throughout:

- **OBSERVED FACT** — directly read from source, code, or executed output.
- **SIMULATION RESULT** — result of the fixed synthetic generator; not a physical rate.
- **INFERENCE** — reasoned interpretation that remains conditional.
- **HYPOTHESIS** — proposed physical behavior that needs measurement.

## 1. Executive summary

**OBSERVED FACT.** v0 was frozen at commit
`933c82d51b9de0b5ee8609d3bcf05772348cd8a5` and tagged `v0-baseline` before
core changes. Its 8 original tests, 2 root tests, reference metrics, and 12-class
stress summary reproduced.

**SIMULATION RESULT.** In a unified benchmark containing eight fixed-seed scenes
for each prioritized failure, v0 gave 100% false-clean for all four classes. The
retained v1 reduced dirty-reference, uniform-absorber, and negative-cancellation
false-clean to 0%, leaving optically invisible residue at 100%. Aggregate false-clean
fell from 100% to 25%, with 0% UNKNOWN and 75% FLAG. Standard 72-scene regression
kept proxy false-clean at 0% and zero-proxy PASS at 100%; UNKNOWN changed from
18.43% to 17.54%.

**INFERENCE.** v1 is a stronger research candidate because complementary controls
attack three distinct ambiguity mechanisms without an always-FLAG/UNKNOWN rule.
It is not a real cleanliness detector: each gain depends on strong, unvalidated
reference, registration, radiometry, and response assumptions.

## 2. Frozen v0 baseline

The canonical artifacts remain unmodified in
`proof_clean_local_plan/reference_run/`; hashes and commands are recorded in
`experiments/v0_baseline/FROZEN_BASELINE.md`.

| v0 method | Proxy-positive PASS | Zero-proxy PASS | UNKNOWN | Proxy-positive FLAG |
| --- | ---: | ---: | ---: | ---: |
| bounded interval, six frequencies | 0.0000% | 100.00% | 18.43% | 69.23% |

**MODEL-CONDITIONAL.** The 0% row expresses containment under the generator and
declared bounds. It is not measured detection performance and does not imply a
real zero-error rate.

## 3. Challenge/rules implications

**OBSERVED FACT.** The official public page gives a deadline of 2026-09-21 23:59
US Eastern Time, asks for an English written proposal, targets results within 30
minutes, and invites early TRL 2–4 concepts. It excludes ATP, culture alone,
standard fluorescence, undifferentiated commercial monitoring, and hyperspectral
or PCR approaches below TRL 6. A solely generative-AI submission is not of interest.

**OBSERVED FACT.** The public prize terms require a non-exclusive IP license for
an award; non-awarded proposals remain with the Solver and there is no assignment.

**OPEN.** Geographic/payment/tax details, confidentiality, exact license scope,
and post-award obligations require human review of the logged-in agreement. The
complete audit is in `CHALLENGE_RULES.md`.

**INFERENCE.** The project fits only the large-area optical-screening objective
and still lacks evidence for “credible verification of cleanliness” or the
30-minute professional workflow. Species/strain claims remain outside scope.

## 4. Prior-art findings

**OBSERVED FACT.** S3/S6/S7 establish close precedent for structured-light
modulation contamination/defect imaging, mathematical modeling, perpendicular
fringes, and direct binary inspection. S8 establishes the mature deflectometry
field and contamination/defect ambiguity. S4 and S10 establish polarization,
large-area soiling, multi-angle, and multi-wavelength precedents. S5 establishes
uncontaminated references, reflectance/color difference, and cleaning-recovery
measurement. S9 establishes professional-environment optical cleanliness imaging.

**INFERENCE.** The optical components are not credible novelty claims. A possible
distinction is the combined assurance workflow—reference confidence, bounded
feasible proxy, explicit abstention, controlled ambiguity-breaking repeat, and
false-clean/coverage registry—but novelty remains `UNVERIFIED`. See
`docs/PRIOR_ART_AUDIT.md`.

## 5. Failure-mode taxonomy

| Failure | Root cause | Classification |
| --- | --- | --- |
| dirty reference | relative signal erased by reference corruption | `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT`, but fundamental without an external clean-anchor assumption |
| uniform absorber | attenuation confounded with frequency-independent gain | `PARTIALLY_MITIGABLE` |
| optically invisible residue | identical retained observations for clean and contaminated state | `FUNDAMENTAL_LIMITATION` |
| negative blur cancellation | single slope observes only `b+q` | `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT` |

Detailed rationale is in `docs/FAILURE_MODE_ANALYSIS.md`.

## 6. Enhancement candidates tested

Each candidate was run against the same 32 failure scenes (4 classes × 8), with
fixed seeds and per-case machine-readable records.

| Candidate | Hypothesis | Aggregate false-clean | UNKNOWN | Added burden | Decision |
| --- | --- | ---: | ---: | --- | --- |
| E1 gain guard | bound absolute gain to expose uniform attenuation | 84.38% | 0% | radiometric calibration | retain as layer |
| E2 reference consensus | two clean references reject one corrupt reference | 75.00% | 0% | three-reference library | retain |
| E3 controlled geometry | registered high-SNR repeat breaks `b=-q` | 75.00% | 0% | 2× live frames; registration | retain |
| E4 secondary optical | a responsive extra state exposes invisible residue | 50.00% | 25.15% | new optical state | reject: effect was assumed |
| combined v1 | complementary controls cover different ambiguities | 25.00% | 0% | all retained burdens | retain |

**NEGATIVE RESULT.** E1 alone missed 37.5% of uniform-absorber pixels/scenes in
the tested construction. E2 and E3 each solve only their targeted ambiguity.
E4 produced apparent detection for the invisible case only because the simulator
was explicitly given contrast; this is not evidence and the feature is excluded.

## 7. v1 implementation

v1 keeps the v0 bounded interval as its decision core and adds:

1. three-reference pairwise slope self-consistency and a minimum two-reference cluster;
2. an absolute log-gain guard at 0.36 after consensus;
3. a second registered state with modeled `|b|<=0.01 pixel²`, additive error
   0.0002, and 12-bit quantization;
4. conservative fusion: any FLAG wins; PASS requires both states to PASS.

**MATHEMATICAL RATIONALE.** The reference graph adds information not present in
a single comparison; the gain guard constrains the intercept previously free in
`z=a+xt`; and the registered state narrows the geometry nuisance so `q` cannot be
cancelled by `b=-q` within its declared bound.

**COST.** Live sample frames rise from 48 to 96. Stored/calibration reference
frames rise from 48 to 288 (3 references × 2 states × 48 frames). Compute changes
from one to six bounded inferences plus reference consistency. Physical acquisition
time and calibration feasibility remain unmeasured.

## 8. Benchmark comparison

| Failure mode | v0 false-clean | v1 false-clean | v1 UNKNOWN | v1 FLAG |
| --- | ---: | ---: | ---: | ---: |
| dirty reference | 100% | 0% | 0% | 100% |
| uniform absorber | 100% | 0% | 0% | 100% |
| optically invisible residue | 100% | 100% | 0% | 0% |
| negative blur cancellation | 100% | 0% | 0% | 100% |
| **all four** | **100%** | **25%** | **0%** | **75%** |

| Standard 72-scene metric | v0 | v1 |
| --- | ---: | ---: |
| proxy-positive false-clean | 0.0000% | 0.0000% |
| zero-proxy PASS | 100.00% | 100.00% |
| UNKNOWN | 18.43% | 17.54% |
| proxy-positive FLAG | 69.23% | 69.23% |

Raw registry: `experiments/failure_mode_registry.csv`. Aggregate JSON:
`experiments/results/phase1_results.json`.

## 9. Negative results

- More frequencies did not materially outperform the two/three-frequency
  interval baselines in v0 and cannot repair wrong physics.
- Self-consistency cannot prove references clean; three equally dirty references
  can agree perfectly.
- A gain guard trades absorber sensitivity against exposure/BRDF false alarms.
- Controlled geometry works only because its much tighter error/pose assumptions
  were supplied to the model; hardware may not achieve them.
- Invisible residue remains false-clean in retained v1. No algorithm can recover
  a label absent from every observation.
- Optical anomaly remains unable to distinguish removable residue from scratch.

## 10. Remaining limitations

The model lacks real materials, roughness/BRDF diversity, projector-camera
calibration, motion, ambient light, exposure control, independent contamination
ground truth, surface registration, reference aging, and room coverage. `q` has no
mapping to mass, thickness, CFU, organisms, or cleaning standards. Common-mode
reference corruption and all-channel invisibility remain structural failures.

## 11. Real-world validation gap

**OBSERVED FACT.** No physical experiment was performed. Every camera, distance,
field-of-view, contrast, noise, timing, and material value without data is marked
`UNVALIDATED RANGE` in `docs/REAL_WORLD_PARAMETER_MAP.md`.

**HYPOTHESIS.** Some real residues may change modulation, gain, angle, polarization,
or wavelength response enough for v1. This must be tested rather than asserted.
The smallest safe pilot, controls, repetitions, endpoints, and stop criteria are
specified in `docs/MINIMUM_PHYSICAL_VALIDATION_PLAN.md`.

## 12. Recommended next phase

1. Human-review the logged-in agreement and document eligibility, AI contribution,
   and IP acceptance before any submission work.
2. Run the pre-registered coupon pilot, first validating reference corruption,
   radiometric drift, registration, and the controlled-state error bound.
3. Search patents/products specifically for multi-reference optical inspection,
   confidence/abstention workflows, and controlled dual-state deflectometry.
4. Measure field-of-view and full acquisition time; rescope if 30 minutes is not credible.
5. Only after positive physical evidence, calibrate residue/material response and
   decide whether an angle, polarization, or wavelength channel merits retention.

No final InnoCentive proposal was written in this phase.
