# Rapid Proof of Clean — final research handoff

Updated 2026-09-20. Classification:
`FINAL_V2_3_COMPUTATIONAL_CANDIDATE_PARTIAL_SPATIAL_IMPROVEMENT`.

## Do not repeat

- v0 (`933c82d`, tag `v0-baseline`), v1 and fixed v2.1 are frozen historical
  baselines. v2.1's pre-final commit is tagged `v2.1-fixed-budget`.
- Physical/literature, realistic-simulator, sensing-diversity, frame-ablation,
  prior-art/product, coverage and proposal work are complete and retained.
- The final run already implemented sequential acquisition, dated-anchor reference
  qualification, an independent-response domain-shift suite, adversarial search,
  observability proof, final proposal and three-round red team.
- The multiscale study already compared global, tile, multiscale-window,
  connected-component, local-density, edge-aware and combined certificates on
  disjoint design/validation/held-out splits. Do not retune on held-out data.
- Do not run another synthetic threshold search and call it physical validation.

## Final candidate

v2.3 keeps the v2.2 active reflectance / structured-light sensing unchanged.
Acquisition is
2→4→12→28→36 frames, with a 60-frame optional diagnostic. Early stages may issue
only FLAG. Proxy PASS requires full 12-state wavelength × angle × polarization
evidence, controlled structured light at frequency indices `[0,3,5]`, qualified
three-reference consensus against a dated external anchor, valid coverage, at
least 95% visible-pixel PASS, no pixel FLAG and the balanced multiscale spatial
certificate. Missing global or local premises force UNKNOWN.

The spatial certificate checks 8×8 tiles; 4×4, 8×8 and 16×16 fully visible
windows; 8-connected component area/span; and a four-pixel edge band. A violation
returns UNKNOWN at 36 frames. Pixel evidence is unchanged and added frames are zero.

Primary implementation:

- `src/rapid_proof_clean/sequential.py`
- `src/rapid_proof_clean/reference_integrity.py`
- `src/rapid_proof_clean/domain_shift.py`
- `src/rapid_proof_clean/spatial_certificate.py`
- `scripts/run_final_research.py`
- `scripts/run_spatial_certificate_study.py`
- `experiments/final_model_config.json`

## Frozen quantitative findings

On the original realistic simulator, fixed v2.1 and v2.2 both produce 5.568%
nonmatched pixel false-clean, 0.158% UNKNOWN, 96.480% clean PASS and 0% clean
false-FLAG. Clean FOVs require 36 rather than 44 frames; this is 66.7% below the
original 108-frame v2 maximum. Nonmatched FOVs stop after a 2.14-frame mean in that
same simulator.

On the different response/morphology/noise domain-shift suite, fixed v2.1 has
11.667% observable-dirty FOV false-clean and 12.778% UNKNOWN. Adaptive v2.2 has
1.111% false-clean (FOV bootstrap 95% interval 0–2.778%) and 22.222% UNKNOWN.
Nominal clean PASS is 100% with 0% false-FLAG. Full stress-set frames are mean
22.70, median 4, p95 60 and max 60. The constructed distribution is not prevalence.

The frozen small-support held-out split gives `<5%` false-clean 66.96%→41.07%,
clean PASS 76.04%→75.00%, false-FLAG 0%→0% and UNKNOWN 23.96%→25.00%. The original
400-case replay gives PASS 136→93; a focused search gives 233→175. This is PARTIAL,
not success: sub-1% and dispersed cases remain weak.

The 20-frame candidate was rejected at 12.222% domain false-clean. The 44-frame
endpoint policy passed 20/20 midband-only attacks; v2.2 returned UNKNOWN on 20/20.
Exact observation matching still passes 100% under every policy.

## Reference conclusion

One independent dirty reference is trimmed in the synthetic audit. Common-mode
dirty live references and missing anchors become UNKNOWN. A dated anchor reduces,
but cannot eliminate, common-mode risk: if anchor, live references and sample share
the same change, clean origin is unidentifiable. Anchor certification and lifecycle
therefore require independent physical evidence.

## Physical conclusion

Literature supports real spectral, angular, polarization, reflectance, scatter and
thin-film responses for some residue/material pairs. It also shows hard boundaries:
tested clear films below roughly 2 µm changed visible scatter little on reflective
stainless, and reported small-object limits vary by material/modality. No source
or project dataset supplies the joint signal/noise distribution needed to calibrate
this architecture. The remaining major assumption is physical, not computational.

## Differentiation conclusion

The optics and broad workflow are crowded. US8229204B2, WO2012065952,
US9839712B2, US11615694B2 and pending WO2025261682A1 collectively cover controlled
optical cleanliness, material-aware references, thresholds/reclean, coverage and
clean-reference iterative measurement. The only candidate distinction is the
narrow clean-release obligation combining dated-anchor qualification, bounded
required-state evidence, coverage, mandatory abstention and false-clean audit.
Novelty, non-obviousness and FTO are unverified.

## Canonical reproduction

```powershell
& .\.venv\Scripts\python.exe scripts\run_submission_pipeline.py
```

This regenerates all synthetic outputs, including the frozen spatial study,
proposal figures/package, repository verification, ruff and pytest.

## Only meaningful next work

Computational research is frozen; next meaningful step is physical coupon
validation. Execute the preregistered blinded protocol with raw data and independent
ground truth. Highest-priority factors are real contrast/noise, sub-1% and dispersed
stains, PSF/pixel scale, registration, clean texture, finish/material transfer,
reference aging/common mode, operator coverage and measured timing. No new
technology main line is authorized by this handoff.

## Three largest remaining risks

1. Important real residues are observation-matched or below field noise.
2. Sub-1%/dispersed stains, real PSF/registration and inaccessible area allow false release.
3. Reference lifecycle, workflow/timing and crowded IP make the concept impractical.
