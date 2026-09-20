# Failure-mode analysis and enhancement decisions

All observations below are synthetic. `FALSE_CLEAN` means a construction labeled
contaminated/proxy-positive was output as PASS; it is not a clinical error rate.

| Failure | Root cause | Solvability | Retained mitigation | Remaining risk |
| --- | --- | --- | --- | --- |
| `dirty_reference` | Reference corruption; equal reference/sample response removes the relative signal. With no external anchor it is unidentifiable. | `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT` under a majority-clean-reference assumption; otherwise `FUNDAMENTAL_LIMITATION`. | Three-reference self-consistency, minimum two-reference consensus, confidence 2/3 or higher. | Common-mode contamination of all references still passes; “consistent” is not “clean.” |
| `uniform_absorber` | Frequency-independent amplitude change is absorbed by the unknown intercept/gain: a single-channel ambiguity. | `PARTIALLY_MITIGABLE`. | Absolute gain guard after reference consensus, with calibrated `|log gain ratio| <= 0.36`. | Real auto-exposure, BRDF, distance, and illumination drift may violate the bound; weak absorbers remain ambiguous. |
| `optically_invisible_residue` | The contaminated and clean states generate exactly the same retained observations. This is information-theoretic unobservability. | `FUNDAMENTAL_LIMITATION` of the retained modality; `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT` only if that measurement physically responds. | None. v1 keeps the false-clean result visible. | The synthetic extra-channel candidate only assumed contrast; it was rejected because no physical evidence establishes wavelength/polarization response. |
| `negative_blur_cancellation` | Relative slope observes `t=b+q`; a geometry term `b=-q` cancels residue blur. | `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT` if geometry can be independently constrained. | Registered high-SNR second state with `|b|<=0.01 pixel²`, noise `0.0002`, and 12-bit quantization in the synthetic model. | Those bounds are unvalidated and impose registration, exposure, and calibration burden. |

## Candidate experiments

| ID | Hypothesis | Added cost | Four-mode false-clean | Decision |
| --- | --- | --- | ---: | --- |
| E1 gain guard | Frequency-independent absorption becomes visible when acquisition gain is bounded. | No extra frames; gain calibration. | 84.38% overall; uniform absorber 37.5%. | Retain as one layer, not sufficient alone. |
| E2 reference consensus | One corrupt reference can be rejected by two consistent clean references. | Reference library grows from 1 to 3. | 75%; dirty reference 0%. | Retain. |
| E3 controlled geometry | Repeating at known geometry separates `q` from cancelling `b`. | Sample frames 48→96; registration/high-SNR calibration. | 75%; cancellation 0%. | Retain. |
| E4 secondary optical | An additional responsive state expands the observable set. | Another 48 sample frames plus new optics/calibration. | 50%; invisible case ~0% PASS but assumption-injected. | Reject from v1; sensitivity result only. |
| v1 combined | Independent controls cover complementary ambiguity classes. | 96 live sample frames, 288 stored reference-library frames, six bounded inferences. | 25%; 0% UNKNOWN. | Retain as research candidate. |

The fixed-seed per-case records are in `experiments/failure_mode_registry.csv`.
v1 does not “solve” invisible residue and does not turn every difficult case into
UNKNOWN. Standard benchmark zero-proxy PASS remains 100%, so the improvement is
not an always-FLAG rule.
