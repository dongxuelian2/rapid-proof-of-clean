# Domain shift and adversarial audit

Updated 2026-09-20. No physical experiment was performed.

## Evaluation generator

The design simulator uses Fresnel film optics plus a structured-light blur proxy.
The final evaluation instead begins with clean rendered backgrounds and applies
arbitrary per-state log-response vectors, different morphologies, Gaussian plus
impulsive noise, registration shifts, exposure changes, missing measurements,
coverage failures and independent/common-mode reference corruption. It therefore
does not reuse residue optical constants or the design residue families.

The evaluation is still not fully independent: clean backgrounds and inference
code are shared, and parameter ranges are chosen rather than measured. Results
are labeled `SYNTHETIC_DOMAIN_SHIFT_AND_ADVERSARIAL_AUDIT_ONLY`.

## Named attacks

- high/low contrast films and smears;
- primary-state cancellation;
- diversity-only and frequency-only signatures;
- midband-only response invisible to endpoint compression;
- uniform attenuation, near-threshold response, thin streaks and sparse particles;
- exact observation matching;
- registration, impulsive noise, missing states and invalid coverage;
- independent reference dirt, common-mode drift, aging and missing anchor.

The old fixed v2.1 policy proxy-PASSed 20/20 midband-only FOVs. Adaptive v2.2
returned UNKNOWN for 20/20. Exact observation matching passed 20/20 under every
policy, as required by the observability theorem.

## Random adversarial search

A deterministic 400-case search varied morphology, support from roughly 0.2% to
75%, arbitrary six-frequency responses, 12-state diversity response and
controlled-state mismatch. It found 136 proxy-PASS cases (34%). This is not a
prevalence estimate. The strongest retained examples were concentrated below the
5% FOV PASS-tolerance boundary; the top passing example affected 50/1024 pixels
with maximum structured attenuation 0.146 log units and diversity span 0.120 log
units. The search therefore exposed spatial support—not another threshold—as the
dominant remaining computational failure family.

The exact cases and parameters are frozen in
`experiments/adversarial_regressions.json`. They are retained as negative results
for future physical and higher-resolution tests.

## Failure semantics

Reference-anchor failure and coverage invalidity terminate UNKNOWN at zero sample
frames. Missing required evidence cannot form a PASS certificate. Impulsive-noise
stress false-FLAGed clean FOVs and is reported as a nuisance failure, not hidden in
nominal-clean accuracy. Registration stress in the tested one-pixel construction
passed, but the shared clean renderer makes that result non-probative.

## Remaining domain gaps

The audit lacks measured BRDFs, projector/camera spectra, RAW sensor noise,
polarizer leakage, surface curvature, motion, ambient flicker, real stain edges,
subpixel PSF mixing and real reference aging. These are coupon/rig tasks, not
parameters that another synthetic sweep can resolve.
