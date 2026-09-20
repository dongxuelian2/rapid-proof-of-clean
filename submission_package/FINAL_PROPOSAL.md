# Reference-Guarded Adaptive Reflectance for Rapid, Coverage-Aware Cleaning Screening

## 1. Participation type, solution level and partnering

Participation type: **[PARTICIPANT TO COMPLETE]**. Proposed solution level:
**TRL 2**—a formulated concept with executable analytical and synthetic evidence,
not a validated prototype. Partnering is requested for representative surfaces,
traceable residue coupons, independent ground truth, optical/mechanical engineering
and professional-site validation. The participant must personally confirm
eligibility, the logged-in Challenge Agreement, IP terms and any AI disclosure.

## 2. Problem and proposed value

Professional cleaning teams need rapid feedback over more area than sparse swabs
cover. Visual inspection is broad but subjective; ATP and chemical methods are
valuable but contact-based point samples. We propose a non-contact optical screen
that maps visible target surfaces, flags deviations from a qualified clean envelope
and refuses to release a view when its references, measurements or coverage are
not adequate.

A projector/display sends controlled patterns while a camera records reflected
modulation. Additional wavelength, angle and polarization states challenge optical
degeneracy. Residue, film, roughness, damage, pose and illumination can all change
these signals, so the system does not identify a contaminant. It produces a
bounded optical-proxy decision and routes FLAG or UNKNOWN regions to recleaning,
remeasurement or an approved orthogonal method.

The intended first use is visible work surfaces and high-touch target sets. It is
not whole-room sterility certification, microbial identification or a replacement
for ATP, chemical assays or microbiology.

## 3. Final system architecture

Each supported material/finish has three live clean references plus a dated,
independently qualified historical anchor. Reference qualification requires a
two-of-three graph-consistent cluster, leave-one-out stability and anchor agreement.
An absent or common-mode-drifting anchor makes the view UNKNOWN.

Acquisition is sequential:

1. two polarization-probe frames;
2. four diversity-corner frames;
3. all 12 wavelength × angle × polarization frames;
4. controlled-geometry structured light at two endpoint frequencies (28 cumulative);
5. a middle-frequency model check (36 cumulative);
6. an optional primary-state three-frequency diagnostic (60 maximum).

Early stages may stop on a FLAG, but cannot issue proxy PASS. PASS requires the
complete 36-frame certificate: qualified references, valid coverage and frames,
PASS from all 12 diversity states and controlled three-frequency bounded inference,
at least 95% visible-pixel PASS, no pixel FLAG, and a balanced multiscale spatial
certificate over tiles, sliding windows, connected components and the FOV edge.
A local-certificate failure becomes UNKNOWN at 36 frames and adds no acquisition.

Four-phase demodulation estimates fringe modulation. The structured model bounds
`log(M_reference/M_sample) = a + x(b + q)`, where `x` scales with squared spatial
frequency, `a` is a gain term, `b` is bounded clean geometry variation and `q` is
a nonnegative equivalent transfer-blur proxy. The diversity arm removes per-pixel
common exposure before testing spectral/angular/polarization signature shape.
These proxies have no mass, CFU or hygiene meaning until physically calibrated.

## 4. Why the frame policy changed

The frozen v2.1 policy needed 44 frames for any PASS and used only endpoint
structured frequencies. In the retained simulator, the final v2.2 certificate
preserves v2.1's nonmatched pixel false-clean at 5.568%, with 0.158% UNKNOWN,
96.480% clean PASS and 0% clean false-FLAG. A normal clean FOV now needs 36 frames,
18.2% fewer than v2.1 and 66.7% fewer than the original 108-frame v2 maximum.

Endpoint compression was then attacked with a different response operator. The
old v2.1 policy proxy-PASSed 20/20 midband-only FOVs; v2.2 returned UNKNOWN on
20/20 because the middle frequency violated the clean model. A 20-frame
four-corner/two-frequency candidate was rejected: its observable-dirty false-clean
was 12.222% in the domain-shift audit.

## 5. Computational evidence and limits

The final evaluation starts from clean rendered material backgrounds and applies
arbitrary state-response vectors, alternative stain morphologies, Gaussian and
impulsive noise, exposure/registration changes, missing measurements, coverage
failure and independent/common-mode reference corruption. It does not reuse the
design simulator's residue optical constants. It remains synthetic because clean
backgrounds and inference code are shared and parameter ranges are unmeasured.

At FOV level on this artificial domain-shift suite, fixed v2.1 had 11.667%
observable-dirty false-clean and 12.778% UNKNOWN. Adaptive v2.2 had 1.111%
false-clean (FOV bootstrap 95% interval 0–2.778%) and 22.222% UNKNOWN. Nominal
clean PASS was 100% with 0% false-FLAG. Over the complete stress set, including
deliberate failures, v2.2 used mean 22.70, median 4, p95 60 and maximum 60 frames.
These rates are comparisons on a constructed distribution, not expected field
performance.

A frozen small-support study used disjoint design, validation and held-out seeds.
The balanced certificate reduced held-out `<5%` false-clean from 66.96% to 41.07%
while clean PASS changed from 76.04% to 75.00%, false-FLAG stayed 0%, and UNKNOWN
rose from 23.96% to 25.00%. It reduced the original 400-case replay from 136 to 93
PASS with zero additional frames. This is a partial result: a focused search still
produced 175/400 PASS, especially sub-1% and dispersed cases. An exact
observation-matched residue remains information-theoretically indistinguishable.

Reference stress was fail-safe in the tested constructions: one independent dirty
reference was trimmed; common-mode drift and missing anchors produced UNKNOWN.
Bounded common aging was accepted by the anchor but still produced UNKNOWN in
the evidence layer. If the anchor and all live references share the same change,
clean origin is unidentifiable.

No project hardware experiment, real sensitivity, specificity, LOD, repeatability,
professional-room scan or operator validation has been completed.

## 6. Physical feasibility

Published studies show that some residues alter spectral reflectance, polarization,
specular return, scatter and thin-film interference. On stainless steel, published
multispectral studies separated prepared organic residues, including a reported
0.94 validation result for diluted spinach/potato juice and 94.0%/99.7% results for
selected wet/dry poultry-residue ratios in their source datasets. These classifier
results do not transfer to this system.

Negative evidence is central. NASA measurements on reflective stainless found
little visible-scatter change below roughly 2 µm for tested contaminant films and
rapid growth beyond 2–3 µm. A fluorescence study reported material-dependent
minimum blob diameters (0.13 mm steel, 0.21 mm plastic) in a different modality.
Clear sub-micron/index-matched films, stains below the optical/spatial support
boundary and strongly textured plastic remain expected hard cases.

## 7. Differentiation and prior art

Structured-light contamination inspection, deflectometry, multi-frequency,
multi-angle, multi-wavelength and polarization imaging are established. Patents
and products disclose controlled illumination, material-specific clean/soiled
references, optical cleanliness values, confidence/maps, coverage thresholds,
before/after comparison, re-cleaning and records. A pending 2025 ASML PCT
application also describes an optical cleanliness measurement, clean-reference
ratio and iterative measurement/cleaning for sensor surfaces.

The proposal therefore does not claim those ingredients as novel. The narrow
candidate distinction is the implemented clean-release obligation: dated-anchor
reference qualification ∧ bounded required-state evidence ∧ valid coverage ∧
mandatory abstention for any failed premise, combined with asymmetric sequential
acquisition and a false-clean adversarial registry. The scoped search did not find
that exact conjunction. Novelty, non-obviousness and freedom to operate are
**unverified**; professional multi-jurisdiction claim charting is required.

## 8. Coverage, workflow and economics

The field concept is a cleanable camera/projector fixture with controlled
illumination, local compute and a guided tablet workflow. A prior planning BOM of
$2,100–$9,200 remains an unquoted range. References need controlled preparation,
storage and replacement even though routine imaging uses no single-use reagent.

Under conservative, unmeasured timing assumptions, the 36-frame clean certificate
models 3.47, 8.24, 15.95 and 27.05 minutes for 1, 5, 12 and 25 m² target sets. The
60-frame p95/worst budget models 3.70, 9.20, 18.10 and 30.90 minutes. Switching,
readout, motion, processing and operator performance have not been measured; the
25 m² worst case misses the 30-minute objective.

Operators receive a registered map:

- **Proxy PASS:** every stated optical and coverage premise passed; not a claim of
  sterility, microbial safety or absence of all residue.
- **FLAG:** positive optical anomaly; reclean/repeat and investigate persistent flags.
- **UNKNOWN:** inadequate reference, evidence, registration, support or coverage;
  correct setup, reacquire or use an approved orthogonal test.

## 9. Validation plan, risks and desired role

Gate 1 is a calibrated bench rig and preregistered coupon study across glass,
stainless steel, HDPE and glazed ceramic; named water/oil/protein/detergent/particle
surrogates; loading, thickness and stain-size levels; finish, day and operator;
reference aging; and independent ground truth. Primary endpoints are coupon/FOV
false-clean, false-FLAG, UNKNOWN, coverage and time with intervals. Exact/near-
matched and small-support controls are mandatory. The spatial limits must be
recalibrated against measured PSF, pixel footprint, registration and clean texture;
the synthetic thresholds are not deployment specifications.

Gate 2 is blinded multi-day replication with frozen code/config. Gate 3 is a
cleanable prototype at two relevant sites, compared with each site's approved
visual, ATP, chemical or microbiological process as appropriate. Failure to find
repeatable contrast, unacceptable false-clean, uncontrolled common-mode reference
drift or excessive timing narrows or stops the claim.

The three largest risks are: (1) important residues are optically equivalent or
below noise; (2) stain size, PSF/registration and inaccessible area permit false
release; and (3) prior-art overlap, reference lifecycle and field workflow make the
system impractical even if contrast exists.

Existing assets are the reproducible inference, sequential controller, synthetic
domain-shift/adversarial suite, audit trail, coverage model and preregistered study
design. Needed partners provide representative residues/surfaces, independent
ground truth, field access, optics/mechanics, human factors and legal/FTO review.

Relevant experience: **[PARTICIPANT TO COMPLETE WITH VERIFIABLE FACTS ONLY]**.

## 10. Selected references

1. Huang et al., structured-light contamination analysis: https://pubmed.ncbi.nlm.nih.gov/31878549/
2. Jespersen et al., wavelength × residue × material: https://pmc.ncbi.nlm.nih.gov/articles/PMC4252410/
3. Aboonajmi et al., VNIR residue imaging: https://pmc.ncbi.nlm.nih.gov/articles/PMC8122335/
4. NASA TN D-6585, film thickness and scatter: https://ntrs.nasa.gov/citations/19720007973
5. Ecolab US8229204B2: https://patents.google.com/patent/US8229204B2/en
6. Cleaning validation WO2012065952A1: https://patents.google.com/patent/WO2012065952A1/en
7. ASML WO2025261682A1: https://patents.google.com/patent/WO2025261682A1/en
8. Fraunhofer F-Camera: https://www.ipm.fraunhofer.de/en/bu/production-control-inline-measurement-techniques/systems/f-camera.html
9. SITA FluoSpection Qube: https://www.sita-messtechnik.de/en/products/sita-fluospection-qube
