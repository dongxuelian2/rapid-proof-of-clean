# Workflow differentiation evidence

Updated 2026-09-20. This is a documentary technical comparison, not a legal
novelty, non-obviousness, validity or freedom-to-operate opinion. “Not found”
means absent from the public material inspected here; it does not prove absence
from dependent claims, other family members, manuals, trade secrets or unsearched
records.

## Result

The broad workflow is **not distinct**: controlled imaging, material-specific
clean/soiled baselines, confidence, whole-surface maps, pass/fail limits,
re-cleaning, coverage and audit records all have close patent or product
precedent. The defensible technical distinction is narrower:

> A clean PASS is a conjunction of a mutually consistent reference ensemble,
> decisive model-bounded results across required active optical states, and a
> valid visibility/coverage record. Failure of an assumption cannot be converted
> to clean; it becomes UNKNOWN and prescribes the missing controlled
> remeasurement. Release testing is explicitly optimized and audited against
> false-clean, UNKNOWN and usable coverage.

This sequence is implemented in the repository. The scoped records below did not
disclose the complete conjunction. That is evidence of a public-document
difference, not proof that the combination is legally novel or patentable.

## Element proof in this implementation

| Required element | Repository evidence | Decision semantics |
|---|---|---|
| Multiple references with corruption confidence | `reference_consensus` in `src/rapid_proof_clean/phase1.py` | No qualifying majority → all pixels UNKNOWN |
| Model-bounded active response | `infer_reference_ensemble`; retained bounded core | PASS is allowed only inside declared error/geometry bounds |
| Independent optical signature shape | `infer_diversity_features` in `advanced.py` | Common exposure is removed; diversity must agree for PASS |
| Controlled second state | v2.1 44-frame schedule | Primary ambiguity cannot silently PASS; controlled state is required |
| Three-way fusion | `combine_measurement_states` / `fuse_v2` | Any FLAG wins; PASS requires every required arm; otherwise UNKNOWN |
| Coverage validity | visibility masks and coverage reports | Occluded/invalid area is not credited as clean |
| False-clean release audit | fixed failure registry plus realistic held-out audit | Reports false-clean and UNKNOWN, not accuracy alone |

## Closest patent and product chart

| Record | What it publicly discloses that overlaps | Difference found in inspected disclosure | Consequence |
|---|---|---|---|
| [US8229204B2](https://patents.google.com/patent/US8229204B2/en) | Ware-type identification; automatically configured lighting/camera environment; luminosity-derived cleanliness; same-type control surfaces; threshold pixel counts; glass, stainless and ceramic examples | Claims reviewed do not require multi-reference corruption consensus, deterministic bounded PASS, explicit UNKNOWN, or bound-failure-triggered acquisition | Very close imaging/reference precedent; material-aware cleanliness scoring is not a novelty anchor |
| [WO2012065952A1](https://patents.google.com/patent/WO2012065952A1/en) | IR chemical image; algorithmic residue amount; comparison with a standard; threshold that directs repeat cleaning/no further cleaning | Chemical-specific threshold workflow, not the implemented active-transfer conjunction or abstaining assumption audit | Re-cleaning and standard comparison are already claimed concepts |
| [US9839712B2](https://patents.google.com/patent/US9839712B2/en) | Applied retroreflective microsphere marker, post-clean illumination and detection | Tests removal of a deliberately applied marker at discrete sites, not native-residue response or full-area bounded evidence | Native sensing is a real modality difference, not proof of broader workflow novelty |
| [US8519360B2](https://patents.google.com/patent/US8519360B2/en) | Invisible dried marking ink made visible under UV to verify cleaning/disinfection | Applied process marker, not the native residue/material interaction | Same distinction as retroreflective marker systems |
| [Fraunhofer F-Camera](https://www.ipm.fraunhofer.de/en/bu/production-control-inline-measurement-techniques/systems/f-camera.html) | Noncontact imaging of contamination; UV fluorescence plus bright/dark field; quantitative maps; product claims for film/area sensitivity | Public page does not state a multi-reference bounded PASS/UNKNOWN proof obligation or failure-triggered state acquisition | Stronger physical product comparator; fluorescence sensitivity may exceed this concept for responsive organics |
| [SITA FluoSpection Qube](https://www.sita-messtechnik.de/en/products/sita-fluospection-qube) | Calibrated normalized RFU maps; full-surface and zone limits; before/after comparison; alignment; reports; planned pass/fail reference patterns | Public page does not disclose reference-corruption consensus, deterministic uncertainty bounds or explicit UNKNOWN that blocks release | Full-surface normalized mapping/reporting is not distinctive |
| [Evident CIX100](https://evidentscientific.com/en/products/cleanliness-and-particle-analysis/cix100) | Polarization-based particle classification, calibration-slide self-check, filter coverage, OK/NOK limits, early rejection, traceable reports | Extracted-particle/filter microscopy; public page does not disclose the project’s native-film multi-state bound conjunction | Calibration, coverage, early fail and audit records are all established product features |
| [iFactory AI Vision](https://ifactoryapp.com/ai-vision-camera/ai-vision-surface-cleanliness-residue-inspection) | Vendor-described controlled lighting, surface/material clean and contaminated baselines, zone maps, pass/fail, coverage completeness, re-cleaning alerts and timestamped records | The inspected marketing page does not disclose multi-reference corruption confidence, deterministic physical bounds, explicit UNKNOWN, or remeasurement selected by the failed bound | Broad end-to-end workflow overlap is extensive; vendor performance/regulatory statements were not independently validated |

## What is and is not established

Established from the inspected documents:

- The project cannot honestly differentiate on imaging, calibration, material
  baselines, maps, pass/fail, re-cleaning, coverage or reporting in isolation.
- Marker products measure removal of an applied surrogate; this project attempts
  native optical response.
- Fluorescence, IR chemical imaging and filter microscopy use different physical
  observables and may be superior for their target residues.
- None of the inspected public disclosures states the complete PASS conjunction
  above.

Not established:

- that no patent/product contains that sequence;
- patentability, non-obviousness, claim scope, legal status or freedom to operate;
- a physical performance advantage over any listed product;
- that UNKNOWN alone is novel—reject-option classification is established art.

## Safe differentiation statement

Use: “Unlike the binary threshold workflows in the public records reviewed, this
research prototype treats clean release as a conjunction of reference integrity,
bounded multi-state optical evidence and coverage validity; unmet assumptions are
logged as UNKNOWN and select a prescribed remeasurement. Its validation target is
false-clean at stated coverage.”

Do not use: “first,” “unique,” “patented/patentable,” “no prior art,” “proves all
residue is absent,” or “freedom to operate.”
