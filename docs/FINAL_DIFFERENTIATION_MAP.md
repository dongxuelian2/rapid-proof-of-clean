# Final differentiation map

Updated 2026-09-20. This is a scoped technical landscape, not legal advice, a
patentability opinion or freedom-to-operate analysis.

## Bottom line

The sensing ingredients are established and crowded. The search does not support
claiming novelty for structured light, modulation/deflectometry, multiple
frequencies, wavelengths, angles or polarization; clean/soiled references;
confidence maps; source normalization; repeated inspection; abstention; or
coverage planning individually.

The only still-plausible differentiation is a narrow **assurance-system
combination**: material-aware multi-reference confidence → model-bounded optical
inference → explicit PASS/FLAG/UNKNOWN → controlled remeasurement → recorded
visible coverage → false-clean adversarial audit. The scoped search did not find
one record containing that complete cleaning-specific sequence. Absence from this
search does not establish novelty, non-obviousness or freedom to operate.

## Element-by-element map

| Element | Closest evidence / prior art | Classification | Safe position |
|---|---|---|---|
| Structured-light contamination imaging | Huang et al. 2019/2020 | Existing technology | Do not claim the physical principle |
| Two perpendicular fringe directions | Huang et al. improved SMAT | Existing technology | Engineering implementation only |
| Multi-frequency fringe/phase measurement | Longstanding phase-measurement literature | Existing technology | Precision/model-checking choice |
| Multi-angle and multi-wavelength cleaning inspection | Mari et al. 2025; Cho et al. 2007 | Existing technology | v2 selection is evidence-based, not novel per se |
| Polarization/specular residue detection | Lin et al. 2006; Fraunhofer 2022 | Existing technology | Established observable; project-specific fusion unvalidated |
| Material/ware-specific clean and stained controls | [US8229204B2](https://patents.google.com/patent/US8229204B2/en) | Close cleaning-specific patent precedent | Strong overlap; claim chart required |
| Reference detector / source normalization | [EP0903572A2](https://patents.google.com/patent/EP0903572A2/en) and related calibration art | Existing technology | Drift control, not differentiation |
| Multiwavelength contamination ratios | [US20090015824A1](https://patents.google.com/patent/US20090015824A1/en) | Existing technology | Do not claim ratio sensing broadly |
| Surface confidence maps / statistical significance | [US7286218B2](https://patents.google.com/patent/US7286218B2/en) | Close inspection precedent | “Confidence” alone is not novel |
| Repeated prescribed cleanliness measurement | [US6378386B1](https://patents.google.com/patent/US6378386B1/en) | Existing workflow precedent | Controlled repeatability is established broadly |
| Optical cleaning recovery / before-after reference | WO2008029946A1; WO2012065952A1 | Close cleaning-specific precedent | Avoid broad remeasurement claims |
| Explicit reject / UNKNOWN | Mature selective-classification concept | Existing general method | Safety behavior, not standalone novelty |
| Coverage planning with uncertainty | Robotics/inspection literature, e.g. [coverage planning with uncertainty](https://arxiv.org/abs/2201.04310) | Existing adjacent method | Application integration only |
| Three-reference majority consistency | Robust statistics plus inspection calibration art | Likely obvious component; no exact cleaning claim established | Treat as reliability engineering unless counsel finds a narrow claim |
| Bound-preserving fusion of references and two controlled states | No exact cleaning-specific record found in scoped search | Combination-innovation candidate | Describe narrowly and conditionally |
| False-clean adversarial registry tied to PASS/UNKNOWN/coverage | No exact product/patent combination found | Combination-innovation candidate | Strong project differentiation as validation discipline, not necessarily patentable |
| 3×2×2 bands/angles/polarizations and numerical thresholds | This repository | Engineering implementation | Not a defensible novelty thesis |

## Closest overlap

**US8229204B2 is closer than the earlier landscape implied.** It covers controlled
camera/lighting environments configured by ware type, digital surface images,
cleanliness values derived from luminosity, and correlations against clean and
stained control wares, including glass and ceramic-tile examples. Material-aware
reference calibration and optical cleanliness scoring therefore cannot anchor a
broad novelty claim.

**US7286218B2 narrows the confidence claim.** It assigns confidence levels to
surface locations based on signal and modeled noise and criticizes binary
thresholding that treats below-threshold points as absence. Statistical
confidence maps and nonbinary evidence handling are established in surface
inspection, even though that patent is not a cleaning workflow.

**EP0903572A2 and US20090015824A1 narrow normalization/diversity claims.** They
teach reference normalization against source intensity and multiwavelength ratios
for optical-window contamination. The v2 diversity cube may be useful, but its
individual optics are not a clean novelty anchor.

## Candidate combination claim — research wording only

The most defensible technical description is:

> A coverage-aware optical cleaning-verification workflow that accepts a clean
> result only when a material-conditioned reference ensemble is consistent,
> bounded inference is decisive across controlled measurement states, and the
> inspected visible area is logged; otherwise it flags or abstains and triggers
> prescribed remeasurement, with false-clean adversaries retained as validation
> tests.

This wording is a differentiation hypothesis, not proposed patent language. Each
clause has prior-art neighbors, and the combination may still be obvious or
claimed in dependent/non-English/unpublished records.

## Product positioning

- ATP/A3 systems remain stronger for biochemical proxy specificity at sampled
  points; this architecture targets non-contact spatial coverage.
- Fluorescent/retroreflective markers verify process execution at marked sites;
  this architecture attempts native-residue optical response.
- Industrial deflectometry already provides full-field pattern projection on
  shiny surfaces; the candidate distinction is the conservative cleaning
  decision and audit workflow, not the camera/projector system.

## Final novelty judgment

- **Existing technology:** all optical observables, clean/reference comparisons,
  confidence concepts, remeasurement, reject options and coverage methods.
- **Combination-innovation candidates:** the complete bounded assurance sequence
  and the false-clean/UNKNOWN/coverage audit discipline in a professional-cleaning
  workflow.
- **Engineering only:** reference count, chosen bands/angles, thresholds, frame
  scheduling, simulator, data schemas and pipeline.
- **Still unverified:** novelty, non-obviousness, patentability, legal status and
  freedom to operate. A professional claim chart remains mandatory.
