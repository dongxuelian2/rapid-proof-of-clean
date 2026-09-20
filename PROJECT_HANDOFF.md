# Rapid Proof of Clean — final handoff

Updated 2026-09-20. Final classification:
`SUBMISSION_READY_WITH_MAJOR_UNVALIDATED_PHYSICAL_ASSUMPTION`.

## What is complete

- v0 frozen at `933c82d51b9de0b5ee8609d3bcf05772348cd8a5` with tag `v0-baseline`;
- retained v1 with three-reference consensus, gain guard, controlled second state,
  conservative state fusion and explicit PASS/FLAG/UNKNOWN;
- fixed-seed Phase 1 benchmark and adversarial registry;
- executable coverage/time model and synthetic nuisance envelope;
- final challenge fit, architecture, detection scope, BOM, synthetic-to-physical
  map, coupon protocol, preregistration, claim ladder, risk register, TRL roadmap,
  workflow and competitive positioning;
- literature/patent/product audit with structured matrix;
- English form-aligned proposal, claim audit, two red-team rounds, nonexpert review,
  three labeled figures and curated `submission_package/`.

## Evidence summary

Evidence remains **synthetic and assumption-driven only**. No physical experiment,
sensor capture, calibration dataset or professional-site trial was found or
performed.

In the four prioritized synthetic false-clean constructions, v0 proxy-PASSed all
four; v1 FLAGS dirty-reference, uniform-absorber and geometry-cancellation cases,
but proxy-PASSes the deliberately optically invisible case. Aggregate false-clean
falls from 100% to 25% only within this synthetic set. In the separate 72-scene
toy regression, v1 proxy-positive PASS is 0%, zero-proxy PASS 100%, UNKNOWN 17.54%
and proxy-positive FLAG 69.23%.

The time model predicts 21.3 minutes for 12 m² of visible target surfaces in a
conservative profile and 36.7 minutes for 25 m². Stress cases exceed 30 minutes
from 4 m². These are unmeasured inputs, not hardware claims.

## Architecture and limits

Per view: two states × two orientations × six frequencies × four phases = 96
sample frames. `q` is an equivalent Gaussian transfer-blur variance in screen-
pixel², not residue mass, thickness, CFU or hygiene. PASS requires both states;
any FLAG wins; failures of signal, bounds, reference confidence, frame completeness
or visibility return UNKNOWN.

Fundamental/open failures:

- retained optics cannot detect residue with a clean-equivalent response;
- all references can share common-mode contamination;
- the controlled-state geometry/noise bounds are not physically established;
- material/BRDF diversity, roughness, illumination and pose may violate the model;
- inaccessible areas are not assessed;
- scratches, wear, moisture and residue can be confounded;
- no microbial, species, strain, sterility, regulatory, real LOD, field error,
  whole-room, novelty or FTO claim is supported.

## Prior art and positioning

Structured-light contamination inspection, perpendicular fringes, deflectometry,
clean references, optical markers, multi-angle/multi-wavelength imaging and
industrial full-field inspection all have precedent. The only candidate
differentiation is the combined assurance workflow: reference-confidence → bounded
decision → explicit abstention → controlled remeasurement → coverage/action log.
Novelty and freedom to operate remain `UNVERIFIED`.

## Reproduce

```powershell
& .\.venv\Scripts\python.exe scripts\run_submission_pipeline.py
& .\.venv\Scripts\ruff.exe check .
```

The pipeline runs the frozen v0 regression, Phase 1, final models, proposal field
word-count audit, figures, package build, repository checks and root tests. The
original pipeline's eight tests are also run inside Phase 1.

## Human actions before submission

1. Complete the participation type and truthful experience fields in
   `proposal/FINAL_PROPOSAL.md`.
2. Personally read/accept the logged-in Challenge Agreement and confirm eligibility,
   IP/license, AI, confidentiality, tax and payment terms.
3. Review every claim and figure; obtain optical/cleaning-domain review if possible.
4. Paste fields into the live form, recheck word limits/URLs, then archive the exact
   submitted text and confirmation.

The next scientific action after submission is Gate 1 of
`experiments/MINIMUM_COUPON_PROTOCOL.md`: establish whether any named residue/material
pair is physically observable before adding modalities or features.
