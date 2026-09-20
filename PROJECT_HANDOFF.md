# Rapid Proof of Clean — Phase 1 handoff

Updated: 2026-09-20. This is the continuation entry. The project remains an
active-reflectance / structured-light research candidate with **synthetic-only**
evidence. No physical experiment, microbial detection, real LOD, professional
room scan, novelty opinion, or final InnoCentive proposal exists.

## Current state

v0 was frozen before changes at
`933c82d51b9de0b5ee8609d3bcf05772348cd8a5` with annotated tag `v0-baseline`.
The canonical `proof_clean_local_plan/reference_run/` artifacts were not edited.
The working branch after Phase 1 contains a retained v1, unified adversarial
registry, challenge/prior-art/claims audits, and physical-validation design.

## Architecture

### v0

- two orientations × six spatial frequencies × four phases;
- four-phase amplitude demodulation;
- model `log(M_ref/M_sample)=a+x(b+q)`;
- deterministic amplitude/log interval propagation;
- `PASS` only when both directional q upper bounds are below threshold;
- `FLAG` when any directional lower bound reaches threshold;
- `UNKNOWN` on ambiguity, low signal, saturation, closure failure, invisibility,
  infeasible intervals, or external visibility failure.

`q` is equivalent Gaussian transfer-blur variance in screen-pixel². It is not
residue mass, thickness, CFU, organism load, or a cleanliness standard.

### retained v1

v1 keeps v0 inference and adds:

1. three-reference self-consistency with minimum 2-of-3 consensus;
2. absolute log-gain guard `0.36` after consensus;
3. a registered high-SNR second state modeled with `|b|<=0.01 pixel²`, additive
   error `0.0002`, and 12-bit quantization;
4. fusion where any FLAG wins and PASS requires both states to PASS.

Implementation: `src/rapid_proof_clean/phase1.py`; synthetic extra states:
`proof_clean_local_plan/src/simulation.py`; orchestration:
`scripts/run_phase1.py`; configuration: `experiments/v1_config.json`.

Cost in the implemented model: live sample frames 48→96; reference library
frames 48→288; six bounded inferences plus consistency checks per field. These
are frame counts, not measured acquisition time.

## Frozen baseline metrics

72 scenes, 32×32, six conditions, 12 scenes/condition:

| Method | Proxy-positive PASS | q=0 PASS | UNKNOWN | Proxy-positive FLAG |
| --- | ---: | ---: | ---: | ---: |
| uniform DC | 99.1111% | 99.07% | 0.00% | 0.89% |
| single-frequency modulation | 8.2833% | 100.00% | 0.00% | 91.72% |
| multi-frequency point estimate | 6.4879% | 100.00% | 0.00% | 93.51% |
| bounded interval, six frequencies | 0.0000% | 100.00% | 18.43% | 69.23% |
| interval, two frequencies | 0.0000% | 100.00% | 19.15% | 69.23% |
| interval, three frequencies | 0.0000% | 100.00% | 19.14% | 69.23% |

Frozen validation: original 8/8 tests, root 2/2 tests, ruff, full pipeline, and
integrity check passed; fresh metrics/stress/tests exactly matched reference.
Hashes are in `experiments/v0_baseline/FROZEN_BASELINE.md`.

## Phase 1 results

Unified prioritized benchmark: 4 failure classes × 8 fixed-seed scenes × 1024
pixels. Pixels are descriptive, not independent trials.

| Failure | v0 false-clean | v1 false-clean | v1 UNKNOWN | v1 FLAG |
| --- | ---: | ---: | ---: | ---: |
| dirty reference | 100% | 0% | 0% | 100% |
| uniform absorber | 100% | 0% | 0% | 100% |
| optically invisible residue | 100% | 100% | 0% | 0% |
| negative blur cancellation | 100% | 0% | 0% | 100% |
| **all** | **100%** | **25%** | **0%** | **75%** |

Standard 72-scene v1 regression: proxy-positive false-clean 0%; q=0 PASS 100%;
UNKNOWN 17.54% (v0 18.43%); proxy-positive FLAG 69.23%. The improvement is not
an always-FLAG or always-UNKNOWN policy.

Candidate results:

- E1 gain guard: overall false-clean 84.38%; uniform absorber 37.5%; retained as a layer.
- E2 consensus: overall 75%; dirty reference 0%; retained.
- E3 controlled geometry: overall 75%; cancellation 0%; retained.
- E4 hypothetical extra optical state: overall 50%; rejected because its
  invisible-residue contrast was assumed, not measured.

Machine-readable results: `experiments/results/phase1_results.json` and
`experiments/failure_mode_registry.csv`.

## Failure-mode status

### dirty reference

- Root cause: equal corrupt reference/sample responses erase relative contrast.
- Classification: `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT` only under an external
  majority-clean anchor; otherwise fundamental.
- Current mitigation: 2-of-3 self-consistent reference cluster and confidence.
- Risk: common-mode dirty references agree and can still false-clean.

### uniform absorber

- Root cause: frequency-independent attenuation is confounded with free gain/intercept.
- Classification: `PARTIALLY_MITIGABLE`.
- Current mitigation: bounded absolute log-gain check after reference consensus.
- Risk: real exposure/BRDF drift can exceed the bound; weak absorption remains ambiguous.

### optically invisible residue

- Root cause: observations are identical by construction.
- Classification: `FUNDAMENTAL_LIMITATION OF THE MEASUREMENT MODALITY`.
- Current mitigation: none; failure remains visible in the benchmark.
- Risk: only a physically responsive wavelength, polarization, angle, or other
  state can expand the observable set. The synthetic extra-channel result is not evidence.

### negative blur cancellation

- Root cause: single-state slope sees only `b+q` and `b=-q` cancels.
- Classification: `SOLVABLE_WITH_ADDITIONAL_MEASUREMENT`.
- Current mitigation: registered high-SNR state with a narrower geometry bound.
- Risk: the registration/noise bounds are unvalidated and may be impractical.

## Claims boundary

Can say:

- the code implements the stated model, intervals, abstention, reference
  consensus, gain guard, controlled-state fusion, and fixed-seed benchmarks;
- the reported v0/v1 metrics are synthetic results;
- the interval containment is model-conditional;
- v1 improves three named synthetic failures while leaving invisibility unresolved.

Cannot say:

- proof of real cleanliness, real sensitivity/specificity/LOD, zero real error,
  microbial/species/strain detection, sterility, regulatory compliance, whole-room
  coverage, under-30-minute operation, experimental TRL, novelty, or patentability.

The formal ledger is `research/claims_ledger.csv`.

## Challenge and prior-art status

The official public challenge page was checked on 2026-09-20. Deadline is
2026-09-21 23:59 US Eastern. Public requirements, exclusions, form fields, AI
language, and non-exclusive award license are recorded in `CHALLENGE_RULES.md`.
Logged-in agreement, geography, tax/payment, confidentiality, and detailed
post-award terms remain `TO VERIFY` by the participant.

Clear precedent exists for structured-light modulation contamination/defect
inspection, perpendicular fringes, deflectometry, polarization soiling, multi-angle
and multi-wavelength cleaning QC, clean-reference reflectance, and before/after
cleaning evaluation. Only the combined assurance workflow remains a possible
distinction, with novelty `UNVERIFIED`. See `docs/PRIOR_ART_AUDIT.md`.

## Reproduce

From repository root:

```powershell
& .\.venv\Scripts\python.exe scripts\run_phase1.py
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\ruff.exe check .
& .\.venv\Scripts\python.exe scripts\verify_repo.py
```

`run_phase1.py` performs v0 regression, the failure registry, v1 standard
benchmark, and comparison report without altering `reference_run/`.

Final Phase 1 verification: root pytest 8/8, original tests 8/8, ruff pass,
pipeline integrity pass, repository verification pass, and 192 registry rows.

## Next critical experiments

1. Human review of the logged-in Challenge Agreement, eligibility, IP, AI, tax,
   payment, and substantive-contribution record before any submission.
2. Pre-registered physical coupon pilot in
   `docs/MINIMUM_PHYSICAL_VALIDATION_PLAN.md`, prioritizing reference corruption,
   gain drift, registration, and controlled-state error bounds.
3. Measure camera/projector mapping, BRDF/material envelope, field of view,
   coverage, and end-to-end acquisition time using
   `docs/REAL_WORLD_PARAMETER_MAP.md`.
4. Focused patent/product search for multi-reference confidence, abstaining
   reflectance inspection, and controlled dual-state deflectometry.
5. Only after physical response evidence, evaluate a minimal additional angle,
   polarization, or wavelength channel for the invisible set.

Do not begin proposal writing by treating synthetic metrics as field evidence.
