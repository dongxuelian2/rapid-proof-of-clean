# Preregistration for the first coupon study

## Final v2.2 amendment (before any physical data collection)

The frozen acquisition candidate is `experiments/final_model_config.json`. Proxy
PASS requires a qualified dated anchor, valid visible coverage, all 12 diversity
states and controlled structured light at spatial-frequency indices `[0,3,5]`.
The normal clean certificate is 36 sample frames. Two/four/twelve/twenty-eight
frame stages may stop only for FLAG. A primary three-frequency diagnostic may
extend a view to 60 frames; missing required evidence forces UNKNOWN.

Primary analysis units are coupons/FOVs, not pixels. Report false-clean,
false-FLAG, UNKNOWN, usable coverage and frame/time distributions with FOV-level
intervals. Mandatory strata include exact/near optical matching, middle-frequency-
only response controls, stain-size/support sweeps, independent/common-mode
reference corruption, aged anchors, registration and raw sensor noise. Thresholds
may not be changed after unblinding without declaring a new study.

Version: 1.0, 2026-09-20. **Not yet executed or registered externally.** Amendments
must be dated before data collection.

## Hypotheses

H1: for at least one named material/residue pair, the locked v1 produces FLAG at
higher prepared deposit levels more often than on blanks without converting
invalid measurements to PASS. H2: majority-clean reference consensus prevents a
single corrupted reference from creating PASS. H3: controlled-state acquisition
reduces modeled geometry cancellation while maintaining acceptable clean-coupon
false flags. H4: no response will be assumed for optically invisible residues.

## Experimental unit and sample size

The independent unit is a separately prepared coupon on a preparation day, not a
pixel. Minimum: five materials × four residues × five levels (including blank) ×
three coupons × three days = 900 coupon-condition acquisitions, with two states
each. This is a screening design; precision intervals, not significance alone,
drive interpretation.

## Locked analysis

- Code: commit recorded immediately before collection; config and reference hashes archived.
- Primary endpoints: coupon-level false-clean, false-flag, UNKNOWN, and usable-coverage proportions.
- Coupon aggregation: any valid FLAG → FLAG; PASS requires ≥95% visible pixels PASS
  and no FLAG; otherwise UNKNOWN. This rule is prospective and separate from pixel inference.
- Confidence intervals: Wilson 95% intervals by independent coupon; stratify all
  results by material/residue/level/day/operator.
- No threshold tuning on the blinded test split. Calibration split 40%, locked test 60%.
- Missing or corrupt frames → UNKNOWN; no imputation.

## Acceptance criteria

For a named supported pair on the locked test set: upper 95% bound on false-clean
≤5% at the declared action level; upper bound on blank false-flag ≤10%; UNKNOWN
≤20%; ≥80% visible coverage; and median end-to-end time within the declared target.
All must pass. Failure narrows the claim or stops development; it is not repaired by
post-hoc exclusion.

## Deviations and reporting

Publish/archive all exclusions, deviations, raw frames, labels, environment logs,
software versions and negative results. Report common-mode reference corruption
and optically invisible controls prominently.
