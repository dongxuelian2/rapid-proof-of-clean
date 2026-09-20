# Reference-Qualified Optical Screening for Professional Cleaning

## Problem & Opportunity

Professional cleaning teams need timely, consistent feedback across visible work
surfaces and high-touch areas. Visual inspection covers broad areas but depends on
the observer. Contact swabs and many chemical tests provide useful point
measurements, but sample only selected locations.

This proposal is for non-contact, large-area optical screening of registered,
visible target surfaces. Its intended value is a mapped screen that
helps teams locate optical anomalies, identify areas that need another measurement
and direct approved confirmatory testing. It is designed to complement a site's
cleaning and verification process, not to certify an entire room or replace
biological or chemical methods.

## Solution Overview

The concept uses a camera and controlled projected illumination to measure how a
surface returns light. It combines multiple wavelength, illumination-angle and
polarization states to challenge cases that look alike in a single image. It is a
**TRL 2** concept with executable analytical and synthetic evidence; no validated
physical prototype has been built.

For each supported material and finish, the workflow qualifies multiple clean
references against a separate, dated and independently prepared anchor. It checks
reference agreement, measurement quality, registration and surface coverage before
interpreting a scan. It then evaluates bounded evidence across the required optical
states. A missing, drifting or inconsistent reference, state or coverage condition
cannot support PASS.

The operator receives a registered surface map with three outcomes:

- **PASS:** the measured optical proxy and coverage satisfy the qualified release
  criteria for this scan. PASS is not proof that all residue is absent.
- **FLAG:** an optical anomaly was measured; reclean the area and investigate a
  persistent result.
- **UNKNOWN:** the references, measurements, registration, spatial support or
  coverage are inadequate. Correct the setup and use controlled remeasurement;
  escalate to an approved orthogonal test when the result remains unresolved.

This clean-release logic accounts for false-clean risk by requiring qualified
references, valid coverage and acceptable bounded evidence in every required
state. Any failed premise leads to FLAG or UNKNOWN rather than automatic release.
These safeguards are design behavior and still require physical validation.

## Solution Feasibility / Scientific Basis

Residues, films, surface texture and damage can alter reflected intensity,
polarization, angular response, scatter and the modulation of projected patterns.
Comparing controlled measurements with qualified references may therefore reveal
some residue-related optical changes. Multiple states provide more evidence than
a single brightness or color threshold, while bounded inference makes the accepted
range explicit.

Published work supports the plausibility of optical response to selected prepared
residues and surfaces. It does not establish this system's performance. Different
residues can be optically similar to a clean surface, and some thin, transparent,
index-matched or spatially sparse residues may produce no distinguishable signal.
The measurements are optical proxies; without physical calibration they have no
validated mass, microbial-load or hygiene interpretation.

## Performance Expectations

The current evidence is computational. Synthetic stress testing exercises
alternative optical responses, noise, registration and exposure changes, missing
measurements, coverage failure and reference corruption. It supports the
implementation of conservative reference, evidence and abstention rules. It does
not estimate field error rates. Adversarial testing identified residues with small
spatial support and observation-matched residues as remaining boundaries;
supporting numerical results are recorded in the claim audit.

**No physical experiment has been conducted.** No real limit of detection (LOD),
sensitivity, specificity, repeatability, scan time or professional-site
performance has been measured. The current timing model is assumption-driven; its
most conservative 25 m² planning case is about 31 minutes, so a 30-minute target
for that area has not been demonstrated. PASS is an optical-proxy decision only:
there is no microbial, sterility or hygienic-safety claim.

Physical validation must establish false-clean, false-FLAG and UNKNOWN rates,
coverage, repeatability and time across named materials, finishes, residues,
residue loads and sizes, operators and days. Testing must include residues with
limited spatial support, dispersed deposits, closely matched cases and
observation-matched cases, with independent ground truth. A residue that produces
the same measurements as an accepted clean surface
cannot be distinguished by this measurement system; that limitation must remain
in any release claim.

## Experience

I am an undergraduate student in Automation at Hebei University of Technology,
with experience in mathematical modeling, control systems, computational research,
reproducible Python development, and AI-assisted technical investigation.

For this project, I developed and iteratively audited the proposed concept through
a reproducible computational research pipeline. My work included active-optical
measurement modeling, reference-integrity logic, bounded PASS/FLAG/UNKNOWN
decision rules, sequential acquisition, multiscale spatial release criteria,
domain-shift simulation, adversarial false-clean testing, prior-art analysis, and
automated regression testing.

The current solution is intentionally submitted as a TRL 2 concept rather than a
validated physical prototype. I do not currently have dedicated optical
laboratory facilities or physical validation data for this system. If partnering
with Diversey, I would contribute the computational model, decision architecture,
software implementation, failure-mode analysis, reproducible evaluation
framework, and validation protocol, while working with relevant partners on
optical hardware, representative surfaces and residues, independent ground truth,
and field validation.

## Solution Risks

- Some important residues may be optically equivalent to a clean surface, below
  the system's spatial support or outside the selected wavelengths and geometries.
- Residue with limited spatial support can be diluted within a measurement area. An
  observation-matched residue can pass because the measured evidence contains no
  distinguishing signal.
- Surface finish, aging, pose, lighting, registration error, occlusion and
  inaccessible areas can weaken the evidence or leave parts of a target unobserved.
- If the dated anchor and all live references change together, the original clean
  state may be unidentifiable. Reference preparation, qualification and lifecycle
  need physical controls.
- Conservative release rules can increase UNKNOWN outcomes and remeasurement.
  Their field usability and impact on workflow time are unknown.
- Prior-art overlap and freedom to operate remain unverified and require
  professional claim review.

The system cannot claim microbial absence, sterility or compliance with a
hygiene standard. FLAG and UNKNOWN results should be handled through each site's
approved cleaning and verification procedures.

## Development Timeline and Capability

The following is a partner-dependent planning estimate from project start; these
stages have not been completed.

1. **Months 0–2 — Bench setup and preregistration.** Build and calibrate a
   non-contact bench rig; select supported surfaces and reference materials;
   define residue panels, independent ground truth, coverage rules and acceptance
   endpoints before collecting data.
2. **Months 2–5 — Physical coupon study.** Test representative water, oil,
   protein, detergent and particle residues on glass, stainless steel, HDPE and
   glazed ceramic across measured loads, sizes, finishes, days and operators.
   Quantify false-clean, false-FLAG, UNKNOWN, repeatability, spatial support and
   time. Narrow or stop the concept if repeatable contrast or acceptable
   false-clean performance cannot be established.
3. **Months 5–8 — Blinded replication.** Freeze the configuration and thresholds,
   then repeat the preregistered study across days and operators. Calibrate
   reference qualification, registration, spatial support and remeasurement
   rules against the physical measurements.
4. **Months 9–12 — Field prototype and pilot.** Develop a cleanable prototype and
   evaluate it at two relevant professional sites. Compare results with each
   site's approved visual, ATP, chemical or microbiological process as
   appropriate; assess coverage, usability, workflow time and failure handling.

Progress beyond each stage depends on the preceding physical evidence. No field
deployment or performance claim is justified before independent validation.

Current project assets are the analytical decision logic, synthetic stress suite,
audit trail, coverage model and preregistered validation plan. Delivery also needs
optical and mechanical engineering, surface metrology, residue preparation,
independent ground-truth methods, professional-site access and human-factors
review. If partnering, the proposed technical contribution is to carry the
reference and release logic into the validation workflow.

## Online References

1. Huang et al., structured-light contamination analysis. [PubMed](https://pubmed.ncbi.nlm.nih.gov/31878549/)
2. Jespersen et al., wavelength, residue and material responses. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4252410/)
3. Aboonajmi et al., visible/near-infrared residue imaging. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8122335/)
4. NASA TN D-6585, contaminant-film thickness and visible scatter. [NASA Technical Reports Server](https://ntrs.nasa.gov/citations/19720007973)
5. Ecolab patent US8229204B2, optical cleanliness measurement. [Google Patents](https://patents.google.com/patent/US8229204B2/en)
6. Cleaning validation patent WO2012065952A1. [Google Patents](https://patents.google.com/patent/WO2012065952A1/en)
7. ASML patent application WO2025261682A1. [Google Patents](https://patents.google.com/patent/WO2025261682A1/en)
8. Fraunhofer F-Camera. [Product information](https://www.ipm.fraunhofer.de/en/bu/production-control-inline-measurement-techniques/systems/f-camera.html)
9. SITA FluoSpection Qube. [Product information](https://www.sita-messtechnik.de/en/products/sita-fluospection-qube)
