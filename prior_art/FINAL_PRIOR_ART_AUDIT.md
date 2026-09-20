# Final prior-art, patent and product audit

Audit date: 2026-09-20. This is a technical landscape screen, **not** legal
advice, a novelty opinion, patentability analysis, validity analysis or freedom-
to-operate opinion. Search coverage is necessarily incomplete. The structured
matrix is `prior_art_matrix.csv`.

## Bottom line

The physical sensing ingredients are crowded. Structured-light modulation for
contaminant/defect inspection, perpendicular fringes, phase-measuring
deflectometry, clean references, before/after cleaning comparison, multi-angle,
multi-wavelength and polarization inspection all have clear precedent. Cleaning
verification products already use ATP swabs, fluorescent/retroreflective markers
and digital workflows. Industrial systems already project patterns and inspect
large shiny surfaces.

The new product review removes the broad workflow as a plausible novelty claim:
commercial pages already describe baselines, maps, limits/pass-fail, coverage,
re-cleaning guidance and records. The search did **not confirm** one source that
requires, jointly for a clean PASS, multiple controlled references with corruption
confidence, model-bounded evidence across required states and valid coverage,
forcing any failed premise to UNKNOWN and selecting remeasurement. This narrower
assurance conjunction may be a technical distinction. It is not proven novelty,
and it does not create a new physical observable.

The final search found an additional close 2025 disclosure. Pending PCT
[WO2025261682A1](https://patents.google.com/patent/WO2025261682A1/en)
claims a gas/liquid sensor-surface cleaning device; dependent claims 7–8 add a
cleanliness measurement and control of cleaning, and claim 11 adds an optical
sensor/camera/chemical analyzer. Its description expressly includes a ratio to a
clean reference patterned structure and iterative measurement/cleaning. This
further removes “reference + measure + reclean” as a safe broad distinction.

## Closest technical literature

- Huang et al. (2019/2020) are the closest optical precedent: sinusoidal or binary
  structured light, contamination/defect imaging, models and experiments on
  specular/transparent surfaces. Perpendicular fusion is already disclosed.
- Deflectometry reviews establish fast, full-field, non-contact inspection and
  also the calibration/uncertainty burden and the ambiguity between contamination
  and unresolved defects.
- Hospital hyperspectral imaging and automotive multi-angle/IR studies show that
  optical cleaning assessment in professional contexts is not new.
- Selective classification provides general precedent for abstaining when a
  prediction is not trustworthy; it is not cleaning-specific.

## Patent landscape highlights

- WO2008029946A1 uses uncontaminated references and optical comparison for
  contamination/cleaning recovery.
- WO2011001380A2/A3 is assigned to Ecolab and explicitly concerns optical
  processing of surfaces to determine cleanliness.
- WO2012065952A1 covers in-situ IR chemical imaging, comparison to a standard and
  a repeat-cleaning threshold.
- US9839712B2/3M determines cleaning effectiveness from residual retroreflection
  at marked sites; US10369243B2/Diversey uses a photochromic indicator.
- US8949043B2 and EP0180756A1 show reference/calibration standards and drift
  management in surface inspection.
- WO2025261682A1 (ASML, 2025) discloses optical cleanliness measurement, a clean-
  reference ratio and iterative control of cleaning for sensor surfaces. The
  independent claims center on the gas/liquid cleaning apparatus; the optical
  measurement is dependent-claim/specification subject matter.

These records are close enough that professional claim charting is mandatory
before commercialization. Legal status shown by Google Patents was not independently
verified. The scoped family/status audit found: US8229204B2 shown active with a
2030 adjusted expiry; US9839712B2 shown active with US, EP, JP, CN, BR and WO
family members; WO2012065952A1 shown ceased, with US9692989B2 shown expired for
fees and its EP member withdrawn; and WO2025261682A1 shown pending with only a
PCT publication at the audit date. These database labels are leads for counsel,
not legal conclusions.

## Independent-claim comparison

| Family | Independent-claim center | Overlap | Difference from final v2.2 |
|---|---|---|---|
| US8229204B2 | ware type, configured imaging, luminosity and cleanliness value | controlled material-aware cleanliness | no located bounded multi-state certificate or mandatory UNKNOWN |
| WO2012065952 / US9692989 | IR chemical image, named chemical, threshold and repeat cleaning | spatial threshold/reclean workflow | chemical concentration rather than active-reflectance proxy |
| US9839712B2 | retroreflective marker, post-clean illumination and detection | optical cleaning effectiveness | deliberately applied surrogate at sites |
| US11615694B2 | camera tracks surface state and cleaning behavior | coverage/state/reporting | process observation rather than native residue evidence |
| WO2025261682A1 | gas/liquid cleaning apparatus; dependent cleanliness measurement | clean-reference ratio and iterative cleaning | sensor-cleaning apparatus; no located assurance conjunction |

No claim chart was performed for dependent claims, equivalents, prosecution
history or national-phase variations. Professional counsel must do that work.

## Commercial alternatives

- Hygiena EnSURE Touch, Neogen/3M Clean-Trace and Kikkoman Lumitester provide
  rapid ATP/A3 point sampling, consumables and reporting.
- Ecolab DAZO verifies wiping through an applied fluorescent marker and digital
  monitoring.
- Micro-Epsilon reflectCONTROL applies phase-measuring deflectometry to full-field
  shiny-surface defect inspection, including robotic/multi-position systems.
- Fraunhofer F-Camera and SITA FluoSpection perform native full-field fluorescence
  contamination imaging; SITA includes normalized maps, zone limits,
  before/after comparison and reports.
- Evident CIX100 combines calibration-device checks, polarization-based particle
  imaging, coverage, OK/NOK, early rejection and traceable reports on extracted
  filter samples.
- iFactory's vendor page describes controlled lighting, material/surface
  baselines, zone pass/fail maps, coverage, re-clean alerts and logged evidence.
  Its performance and regulatory statements were not independently validated.

The proposal is complementary rather than a universal replacement: it trades
chemical/biological specificity for non-contact area coverage and explicit
uncertainty. Any comparison must acknowledge that ATP is also not sterility or
species identification.

## Safe statements

Use: “a research candidate that permits clean release only when reference
integrity, bounded evidence across required active states and coverage validity
all hold; failed premises become UNKNOWN and select remeasurement.”

Do not use: “novel structured-light contamination detector,” “first optical proof
of clean,” “detects all residues,” “replaces ATP,” or “freedom to operate.”

## Unsafe novelty statements

- Do not claim structured light, fringe projection, phase shifting, multiple
  frequencies/directions, polarization, before/after comparison, clean references,
  contamination imaging or deflectometry as individually novel.
- Do not claim “no prior art exists,” “first,” “patentable,” “non-infringing,” or
  “freedom to operate.”
- Do not imply that explicit UNKNOWN alone is novel; reject-option classification
  is a mature general concept.

## Unresolved novelty

We did not identify, in this scoped search, one record with the entire cleaning-
specific assurance sequence of multi-reference corruption confidence, deterministic
bounds, explicit abstention, controlled remeasurement, coverage accounting and a
false-clean audit. Whether that combination is new, non-obvious, claimable or free
to operate requires a professional multi-jurisdiction search and claim chart.

## Remaining search gaps

Non-English patent families, unpublished applications, dependent claims,
prosecution histories, product manuals, quote-only industrial systems and
jurisdiction-specific legal status were not exhaustively reviewed. No search can
prove absence. Novelty and FTO therefore remain `UNVERIFIED`.
