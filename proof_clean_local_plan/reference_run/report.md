# Local synthetic feasibility report

**Evidence: synthetic model only. No oil, microorganism, professional room, camera or screen has been experimentally validated by this run.**

## Definitions

The proxy q is an excess Gaussian reflection-transfer blur variance in screen-coordinate pixels squared. It is not film thickness, CFU, protein mass, pathogen concentration, or a cleanliness standard. PASS is restricted to this proxy, the supplied reference and the assumed model.

## Benchmark

| Method | Proxy-positive called PASS | Zero-proxy PASS | UNKNOWN | Proxy-positive FLAG |
|---|---:|---:|---:|---:|
| uniform_DC | 99.1111% | 99.07% | 0.00% | 0.89% |
| single_frequency_modulation | 8.2833% | 100.00% | 0.00% | 91.72% |
| multi_frequency_point_estimate | 6.4879% | 100.00% | 0.00% | 93.51% |
| bounded_interval | 0.0000% | 100.00% | 18.43% | 69.23% |
| interval_two_frequencies | 0.0000% | 100.00% | 19.15% | 69.23% |
| interval_three_frequencies | 0.0000% | 100.00% | 19.14% | 69.23% |

These are descriptive synthetic pixel ratios; scenes share nuisance parameters, so pixels are not independent experimental samples. A zero count is not proof of zero real-world error. The bounded-error statement is an algebraic, model-conditional result.

## Stress tests and failure modes

| Condition | PASS | UNKNOWN | FLAG |
|---|---:|---:|---:|
| low_signal | 0.00% | 100.00% | 0.00% |
| occluded | 50.00% | 50.00% | 0.00% |
| clipped | 0.00% | 100.00% | 0.00% |
| noise_bound_violated | 0.00% | 100.00% | 0.00% |
| defocus_bound_violated | 0.00% | 0.00% | 100.00% |
| dirty_reference | 100.00% | 0.00% | 0.00% |
| uniform_absorber | 100.00% | 0.00% | 0.00% |
| optically_invisible_residue | 100.00% | 0.00% | 0.00% |
| scratch_like_response | 0.00% | 0.00% | 100.00% |
| phase_motion | 0.00% | 100.00% | 0.00% |
| frequency_dependent_gain | 0.00% | 0.22% | 99.78% |
| negative_blur_cancellation | 100.00% | 0.00% | 0.00% |

The uniform-absorber, optically-invisible-residue and dirty-reference cases may PASS even though the scene construction labels physical residue present. This is a limitation of the sensing model or reference, not a success. A scratch-like response can FLAG a clean but damaged surface.

## Interpretation and next evidence required

This prototype checks demodulation, error propagation, feasible-set inference, abstention and synthetic failure cases. It does not establish that actual residues obey the Gaussian model, that the reference is clean, that a room can be covered within 30 minutes, that equipment costs are acceptable, or that the proposed combination is novel. These require human assessment and physical/source evidence.

The uniform-DC baseline is intentionally weak for this response model because the primary modeled effect changes modulation rather than mean intensity. It is a sanity baseline, not evidence of superiority over all conventional optical inspection.

No autonomous submission is performed. Human-authored contribution, verified sources and review of the current challenge agreement are required before any proposal.
