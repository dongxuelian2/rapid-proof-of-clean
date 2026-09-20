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

The search did **not confirm** one source that combines all of the following for
professional cleaning verification: multiple controlled references with corruption
confidence, model-bounded intervals, an explicit reject/UNKNOWN class, controlled
remeasurement for ambiguity, visible-coverage accounting, and a false-clean
adversarial registry. This may be a workflow-level distinction. It is not proven
novelty, and it does not create a new physical observable.

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

These records are close enough that professional claim charting is mandatory
before commercialization. Legal status shown by Google Patents was not independently
verified.

## Commercial alternatives

- Hygiena EnSURE Touch, Neogen/3M Clean-Trace and Kikkoman Lumitester provide
  rapid ATP/A3 point sampling, consumables and reporting.
- Ecolab DAZO verifies wiping through an applied fluorescent marker and digital
  monitoring.
- Micro-Epsilon reflectCONTROL applies phase-measuring deflectometry to full-field
  shiny-surface defect inspection, including robotic/multi-position systems.

The proposal is complementary rather than a universal replacement: it trades
chemical/biological specificity for non-contact area coverage and explicit
uncertainty. Any comparison must acknowledge that ATP is also not sterility or
species identification.

## Safe statements

Use: “a research candidate that combines established active optical measurement
with reference-confidence, bounded decisions, explicit abstention, coverage logs
and remeasurement for cleaning workflows.”

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
