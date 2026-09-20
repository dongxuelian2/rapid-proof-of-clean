# Final three-round red-team review

Updated 2026-09-20. Each round contains at least 20 hard objections. “Change”
records the resulting proposal or implementation action; it is not a rebuttal by
assertion.

## Round 1 — skeptical optical scientist

1. **No physical signal exists.** Evidence: none in-project. Change: TRL 2 and
   “no physical experiment” are explicit.
2. **The design and test simulators share assumptions.** Evidence: earlier tests
   reused residue optics. Change: added arbitrary observation-space response,
   morphology and noise operators; remaining clean-background coupling is stated.
3. **Endpoint frequencies can miss a curved response.** Evidence: 20/20
   midband-only FOVs passed v2.1. Change: middle frequency required for PASS.
4. **Twenty frames delete information.** Evidence: 12.222% domain false-clean.
   Change: fast-20 rejected and archived.
5. **More frames can merely retune thresholds.** Evidence: middle frequency sees
   an otherwise unobserved dimension. Change: retain only this information-adding
   state; label other threshold-only ideas negative.
6. **Pixel counts inflate confidence.** Evidence: pixels share FOV nuisances.
   Change: FOV is the bootstrap/resampling unit.
7. **The reported CI is distribution-specific.** Evidence: constructed scenarios.
   Change: call it a benchmark interval, never field uncertainty.
8. **Clean false-FLAG is cherry-picked.** Evidence: impulsive-noise clean stress
   false-FLAGed. Change: report nuisance group separately instead of folding it
   into nominal-clean results.
9. **Uniform attenuation is confounded with exposure.** Evidence: gain guard uses
   a bounded acquisition assumption. Change: keep it as a guarded anomaly, not a
   residue identifier.
10. **Registration test is unrealistic.** Evidence: shared clean renderer and
    integer roll. Change: mark its pass non-probative and require physical texture.
11. **A clear film can be below scatter sensitivity.** Evidence: NASA thin-film
    data. Change: elevate sub-2 µm clear film as a primary negative control.
12. **Polarization depends strongly on angle.** Evidence: oil DOLP varies with
    viewing geometry. Change: require locked pose and angle sweep in coupons.
13. **Material transfer is unsupported.** Evidence: steel/plastic response and
    blob-size differences. Change: claims are stratified by material and finish.
14. **Three agreeing references may all be dirty.** Evidence: common-mode
    construction. Change: require dated external anchor.
15. **The anchor can also be dirty.** Evidence: identifiability theorem. Change:
    require independent certification and state this residual failure explicitly.
16. **Reference thresholds are arbitrary.** Evidence: synthetic values only.
    Change: label them preregistered starting values requiring measured calibration.
17. **Matched residue remains invisible.** Evidence: 100% PASS control. Change:
    formal observability theorem and mandatory orthogonal route.
18. **Small stains exploit FOV aggregation.** Evidence: adversarial search found
    strong cases below 5% support. Change: expose spatial support as top risk and
    freeze regression cases.
19. **The optional 60-frame state can rescue a bad model by chance.** Evidence:
    it slightly changes synthetic false-clean. Change: treat it as diagnostic;
    clean release already requires the 36-frame certificate.
20. **No more simulation will prove feasibility.** Evidence: main uncertainty is
    real contrast/noise. Change: stop computational tuning and hand off to coupons.

## Round 2 — industrial cleaning / operations reviewer

1. **PASS will be read as hygienically clean.** Change: every operator-facing
   definition says “optical proxy PASS,” not sterility or microbial safety.
2. **ATP comparison is misleading.** Change: describe complementary area screen
   versus biochemical point proxy; no replacement claim.
3. **References create hidden consumables.** Change: disclose preparation,
   storage, lifecycle and replacement burden.
4. **Anchor setup could dominate field time.** Change: frame counts explicitly
   exclude amortized reference acquisition; timing study must include it.
5. **Frame count is not elapsed time.** Change: all time figures remain unmeasured
   input models with switching/readout caveat.
6. **The average frame count is prevalence-sensitive.** Change: report nominal
   clean 36, artificial-mix mean, p95 and max separately.
7. **The 60-frame tail misses the target.** Evidence: 25 m² models 30.90 min.
   Change: disclose failure rather than headline only the mean.
8. **Whole-room coverage is implied.** Change: use “visible target-surface set”
   and report inaccessible fraction.
9. **Curved/occluded sites are common.** Change: unsupported or invisible regions
   are UNKNOWN and require another method.
10. **Repeated flags may be scratches.** Change: system is an anomaly screen;
    persistent flags trigger investigation, not a residue diagnosis.
11. **Moist clean surfaces may flag.** Change: include water/cleaning-condition
    strata and workflow-specific acceptance timing in coupon design.
12. **Operator skipping can produce false release.** Change: coverage validity is
    a PASS predicate, not a report-only metric.
13. **Missing frames could be ignored.** Change: failed required evidence cannot
    form a certificate.
14. **Reference mix-up is likely.** Change: immutable IDs, material/finish scope
    and chain-of-custody are specified.
15. **A 95% pixel rule tolerates too much dirt.** Evidence: adversarial support
    failures. Change: call the value provisional and make stain-size sweeps a gate.
16. **False FLAG harms usability.** Evidence: impulsive noise stress. Change:
    false-FLAG and UNKNOWN are primary endpoints, not hidden behind accuracy.
17. **No field-grade enclosure is designed.** Change: BOM remains a planning range;
    cleanability and ingress are Gate 3 work.
18. **No operator study exists.** Change: time and usability are explicit pilot
    endpoints.
19. **Ground truth varies by application.** Change: comparator is chosen per
    decision context, never one universal proxy.
20. **Failure criteria are vague.** Change: no reproducible contrast, excessive
    false-clean, uncontrolled references or excessive time narrows/stops claims.

## Round 3 — competitor / patent and submission reviewer

1. **Structured light is old.** Change: no novelty claim for the sensing principle.
2. **Perpendicular fringes are old.** Change: classify as engineering.
3. **Multi-frequency is old.** Change: justify middle frequency by benchmark only.
4. **Wavelength/angle/polarization diversity is old.** Change: no component claim.
5. **Clean references are old.** Change: differentiation is not “uses a reference.”
6. **Material-aware lighting is patented.** Evidence: US8229204B2. Change: disclose
   direct overlap and require a claim chart.
7. **Threshold/reclean is patented.** Evidence: WO2012065952 family. Change: avoid
   broad workflow novelty.
8. **Optical marker cleaning checks exist.** Evidence: US9839712B2/US8519360B2.
   Change: distinguish native-response scope without disparaging marker systems.
9. **Coverage-based CLEAN exists.** Evidence: US11615694B2 description. Change:
   coverage alone is not differentiated.
10. **Confidence maps exist.** Evidence: US7286218B2. Change: bounded confidence is
    a safety implementation, not a novelty claim.
11. **Reference normalization exists.** Evidence: EP0903572/US7948617. Change:
    do not claim source normalization.
12. **Multiwavelength contamination ratios exist.** Evidence: US7948617. Change:
    do not claim spectral ratios broadly.
13. **Recent ASML art has clean-reference ratio and iterative cleaning.** Evidence:
    WO2025261682A1. Change: remove “reference + remeasure” differentiation.
14. **Commercial full-field fluorescence maps exist.** Evidence: F-Camera/SITA.
    Change: position as elastic-reflectance research alternative, not first imaging.
15. **Commercial technical-cleanliness audit trails exist.** Evidence: CIX100.
    Change: records/OK-NOK are not differentiators.
16. **Vendor vision pages claim baselines and reclean alerts.** Evidence: iFactory.
    Change: broad end-to-end workflow novelty is contradicted.
17. **UNKNOWN is standard selective classification.** Change: do not claim reject
    option alone.
18. **The residual conjunction may be obvious.** Change: label it a candidate
    technical distinction, not patentability.
19. **Legal status data are unreliable.** Change: database statuses are explicitly
    unverified leads; counsel must check registers and prosecution histories.
20. **The submission can overstate generated work.** Change: participant identity,
    experience, eligibility, agreement and AI disclosure remain human-only fields.

## Final disposition

The review changed the architecture (middle-frequency PASS requirement and dated
anchor), rejected the 20-frame candidate, changed metrics to FOV-level intervals,
created permanent adversarial regressions, rewrote the proposal around conditional
evidence, and narrowed differentiation after the 2025 patent find. No objection
was answered by asserting real performance.
