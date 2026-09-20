# Reference-Guarded Active Reflectance for Rapid, Coverage-Aware Cleaning Screening

## 1. Participation type, solution level and partnering

Participation type: **[PARTICIPANT TO COMPLETE]**. Proposed solution level:
**TRL 2**—a formulated concept with executable analytical/synthetic proof, not a
validated hardware prototype. Partnering is desired for representative surfaces,
independent residue ground truth, optical/mechanical engineering and professional-
site validation. The participant must personally confirm eligibility, the logged-in
Challenge Agreement, IP terms and any generative-AI disclosure.

## 2. Problem / opportunity and differentiation

Professional teams need rapid feedback over more surface area than a small set of
swabs can cover. Visual inspection is broad but subjective; ATP is fast and useful
but is a contact biochemical proxy at sampled points. The opportunity is a
non-contact screen that maps visible target surfaces, reports where an optical
state differs from a controlled clean envelope, and refuses to call uncertain or
unseen regions acceptable.

We propose reference-guarded active reflectance. A display/projector sends known
phase-shifted patterns to a surface while a camera records their reflected
modulation. Residue, film, roughness, damage, pose and illumination can all change
that transfer. The method therefore does not identify a contaminant; it detects a
bounded optical anomaly and routes it for recleaning, remeasurement or an
orthogonal test.

Structured-light contamination inspection and industrial deflectometry are prior
art. The candidate differentiation is the combined assurance workflow: three
controlled references with corruption confidence; deterministic measurement-error
intervals; `PASS / FLAG / UNKNOWN` rather than a forced binary answer; a registered
second measurement state to challenge geometry ambiguity; explicit visible-
coverage accounting; and a remeasurement/escalation route. This combination has
not been confirmed as novel and freedom to operate remains unverified.

Unlike ATP, the proposal uses no routine contact reagent and can screen an area.
Unlike a fluorescent marker, it does not require pre-marking each site. Those
methods remain complementary when biochemical, biological or process-specific
evidence is required.

## 3. Solution overview against requirements

For each material class, an operator inserts or images three dated clean-reference
coupons. The instrument projects two orientations, six spatial frequencies and
four phase steps. It records a primary state and a rigidly controlled, higher-SNR
repeat: 96 live frames per field of view. It logs reference IDs, pose, exposure,
frame completeness, visible mask and spatial coverage.

Four-step demodulation estimates modulation amplitude. The software compares
sample and reference transfer across frequency. Two of three mutually consistent
references are required. A gain check detects modeled frequency-independent
attenuation outside the accepted acquisition envelope. Bounded inference returns:

- **Proxy PASS:** both states are valid and the modeled optical-transfer proxy is
  below threshold. This is not a statement of hygiene, sterility or microbial safety.
- **FLAG:** at least one state is inconsistent with the accepted clean envelope;
  reclean and repeat, then investigate persistent flags.
- **UNKNOWN:** signal, references, registration, coverage or assumptions are
  inadequate; correct the setup, reacquire or use an approved orthogonal assay.

The field concept is a cleanable camera/projector fixture with local compute and a
guided tablet workflow. An indicative field BOM is $2,100–$9,200, an unquoted
planning range. Routine imaging uses no consumable reagent, although references
require controlled preparation and replacement.

The intended first use is targeted visible work surfaces and high-touch sets, not
one-shot whole-room certification. Unsupported materials and inaccessible regions
remain UNKNOWN. Reports preserve coverage, repeats and deviations rather than
displaying a single universal “clean” score.

## 4. Feasibility and scientific basis

For each orientation and spatial frequency, four phase-shifted frames recover
modulation. The implemented model is
`log(M_reference/M_sample) = a + x(b + q)`, where `x` is proportional to squared
spatial frequency, `a` captures frequency-independent gain, `b` is bounded clean
geometry variation, and nonnegative `q` is an equivalent Gaussian transfer-blur
proxy in screen-pixel². Quantization and declared additive error are propagated to
feasible intervals. A result is accepted only when the interval and acquisition
validity checks support it.

The mechanism is grounded in published structured-light modulation analysis for
contamination/defect detection and in the larger phase-measuring deflectometry
literature. Those sources establish plausibility, not this system's performance.
Patents and products also show long-standing clean-reference, optical-marker,
before/after and calibration concepts.

The executable repository freezes v0 and tests v1 against four deliberately hard
synthetic constructions. V0 proxy-PASSed all four. V1 FLAGS a single dirty
reference, modeled uniform attenuation and modeled geometry cancellation, but
still proxy-PASSes a residue constructed to be optically invisible. In a separate
72-scene toy-model regression, v1 has 0% proxy-positive PASS, 100% zero-proxy PASS
and 17.54% UNKNOWN. These are fixed-seed synthetic results; pixels are not
independent experiments and no physical sensitivity follows from them.

The next falsifiable step is a preregistered blinded coupon study across named
materials, residue surrogates, levels, days and operators. It measures noise,
reference aging, pose, illumination, coverage and coupon-level error/UNKNOWN
intervals before any field claim is made.

## 5. Performance expectations and limitations

The target is an actionable visible-surface map within 30 minutes. An executable
assumption model includes field of view, overlap, inaccessible area, 96 frames,
frame period, processing, repositioning and reference overhead. Under its
conservative—not measured—profile, 1 m² requires 4.0 minutes, a 4 m² high-touch
set 9.3 minutes, a 5 m² preparation zone 10.6 minutes, and 12 m² of small-room
target surfaces 21.3 minutes. A 25 m² target set requires 36.7 minutes and fails
the objective. Stress assumptions exceed 30 minutes from 4 m² upward. Hardware
timing and operator studies are therefore gating evidence.

The current evidence is analytical and synthetic only. No physical experiment,
real sensitivity, specificity, limit of detection, repeatability, professional-
room scan or operator validation has been completed. The method does not detect
ATP, organisms, species/strain, viability, sterility or a named chemical. It can
confuse residue with scratches, wear, moisture or geometry; it cannot detect a
material whose retained optical response equals clean; and it cannot assess
occluded or unsupported surfaces.

Synthetic nuisance sweeps intentionally show non-ideal behavior. Added noise and
common reference aging can drive UNKNOWN; large illumination/exposure changes can
false-FLAG clean scenes; missing frequencies become UNKNOWN. The synthetic
registration test is non-probative because it lacks realistic texture/parallax.
These results define experiments, not product specifications.

Success will be declared only by material/residue stratum after blinded coupon
criteria are met. Persistent UNKNOWN or absence of physical contrast narrows or
stops the claim; an added wavelength or polarization state will not be retained
without measured incremental value.

## 6. Relevant experience

**[PARTICIPANT TO COMPLETE: provide only verifiable personal/team experience,
facilities, prior projects and intended role. Do not attribute generated text,
software or literature review to credentials that the participant does not have.]**

The current project package contains reproducible Python code, 13 root tests plus
the frozen eight-test baseline, deterministic synthetic benchmarks, an adversarial
failure registry, a source/claim ledger, an executable coverage model, a hardware
assumption map, and a preregistered coupon-study design. These artifacts demonstrate
the proposal's computational and experimental-planning foundation; they do not
demonstrate laboratory experience or field performance.

Desired collaborators include a professional-cleaning domain owner, optical and
mechanical engineers, a statistician/metrologist, and laboratories able to prepare
traceable residue coupons and run appropriate independent comparators. The
participant should state which of those capabilities are actually available.

## 7. Solution risks and mitigations

The highest scientific risk is non-observability: some hazardous residues may not
change the retained optical channels. This cannot be solved by confidence scoring.
Mitigation is explicit scope, optically subtle negative controls and orthogonal
testing; failure stops the affected claim.

Reference consensus defeats one discordant reference, not three references aged or
soiled together. References therefore require independent preparation, IDs,
lifecycle monitoring, blanks and replacement triggers. Exposure, projector
nonlinearity, ambient light and surface BRDF may exceed modeled bounds; locked RAW
settings, warm-up, flat-field checks, rigid geometry and mandatory UNKNOWN behavior
contain—but do not eliminate—this risk.

Scratches, wear or water may look like residue, causing false flags. Reclean-and-
repeat plus inspection of persistent flags separates workflow actions without
claiming cause. Curvature, texture and occlusion reduce coverage; unsupported
material classes are refused and inaccessible area is reported.

Operational risks include slow repositioning, skipped views and misreading proxy
PASS as hygienic clearance. A guided sequence, frame-completeness checks, coverage
maps, operator training and carefully limited report language address these risks.

Commercial risks include field-grade hardware cost, reference maintenance and
substantial prior-art overlap. Vendor quotes, design-for-cleanability work and a
professional patent claim chart/FTO review are required before productization.

## 8. Development timeline, capabilities, deliverables and desired role

Development is evidence-gated rather than performance-promised.

**Gate 1—bench observability (approximately 6–10 weeks after resources):** assemble
and calibrate a triggerable camera/projector rig; measure noise, linearity, MTF,
pose and reference drift; test named coupons including invisible controls.
Deliverables: raw frames, calibration report, locked code/config and go/no-go memo.

**Gate 2—blinded coupon validation (8–12 weeks):** run the preregistered material ×
residue × level × day × operator design. Deliverables: coupon-level false-clean,
false-flag, UNKNOWN, coverage and timing intervals; supported-stratum statement;
negative results and deviations.

**Gate 3—relevant-environment pilot (12–20 weeks):** build a cleanable field
prototype, validate the guided workflow at two professional sites, and compare
against the site's approved visual/ATP/chemical/microbiological processes.
Deliverables: usability, coverage, time, maintenance and failure reports.

**Gate 4—multi-site demonstration:** only after prior gates pass, freeze the product
claim, safety/data architecture, manufacturing BOM, training and prospective study.

Existing capabilities are the executable inference, simulation, audit trail,
coverage model and study design. Needed partner capabilities are representative
surfaces/residues, independent ground truth, field access, optical/mechanical
engineering, product safety and legal/FTO review. The desired role is joint
technical development with transparent negative-result gates, not transfer of an
already validated product.

## 9. Online references

1. Challenge requirements: https://www.innocentive.com/challenges/novel-technologies-for-rapid-proof-of-clean-in-professional-environments/
2. Huang et al., structured-light modulation analysis, Optics Express (2019): https://pubmed.ncbi.nlm.nih.gov/31878549/
3. Huang, direct structured-light inspection (2020): https://arxiv.org/abs/2006.12186
4. Burke et al., deflectometry overview (2023): https://www.frontiersin.org/journals/advanced-optical-technologies/articles/10.3389/aot.2023.1237687/full
5. Pavliček and Paličková, PMD uncertainty (2023): https://pubmed.ncbi.nlm.nih.gov/37132924/
6. Ecolab optical cleanliness patent WO2011001380: https://patents.google.com/patent/WO2011001380A3/en
7. 3M surface-cleanliness patent US9839712: https://patents.google.com/patent/US9839712B2/en
8. Micro-Epsilon reflectCONTROL: https://www.micro-epsilon.com/2d-3d-measurement/reflectcontrol/
9. Hygiena EnSURE Touch: https://store.hygiena.com/monitoring-systems/ensure-touch-asy0460
10. Kikkoman Lumitester Smart: https://biochemifa.kikkoman.com/e/kit/product/atp-test/lumitester-smart/
