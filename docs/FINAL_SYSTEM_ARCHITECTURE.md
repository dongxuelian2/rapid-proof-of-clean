# Final v2.3 computational system architecture

## Decision objective

Screen visible target-surface FOVs for bounded deviations from a qualified clean
optical envelope. Output `PASS`, `FLAG` or `UNKNOWN`. This is not contaminant
identification or microbial/sterility proof.

## Reference gate

Three current references are checked by pairwise graph consensus and leave-one-out
stability, then compared with a dated external material/finish anchor after common
exposure removal. Independent outliers may be trimmed. Missing anchor, insufficient
consensus or common-mode drift forces UNKNOWN.

## Sequential acquisition

| Frames | Cumulative evidence | Terminal action |
|---:|---|---|
| 2 | polarization pair | FLAG only |
| 4 | diversity corners | FLAG only |
| 12 | full 3 wavelength × 2 angle × 2 polarization | FLAG only |
| 28 | controlled structured endpoints | FLAG only |
| 36 | controlled structured `[0,3,5]` frequencies | PASS / FLAG / UNKNOWN |
| 60 | optional primary `[0,3,5]` diagnostic | FLAG / UNKNOWN or confirmed certificate |

## Inference and FOV aggregation

Structured frames use four-phase demodulation, bounded transfer inference and a
gain guard. Diversity uses exposure-centered reference/sample log-signature shape.
Any pixel FLAG makes the FOV FLAG. PASS requires named complete evidence, all
global gates, no FLAG, at least 95% visible pixels PASS and the balanced spatial
certificate: bounded non-PASS density in 8×8 tiles and 4/8/16-pixel windows,
bounded connected-component area/span, and a separate edge-band limit. A local
violation is UNKNOWN at 36 frames. It neither changes pixel evidence nor adds an
optical frame. Missing measurements never shrink the PASS certificate.

## Coverage and logging

The report stores reference/anchor IDs, raw frame completeness, pose/exposure,
stage trace, visible/inaccessible mask, decision/reason, frame count, repeat action
and orthogonal escalation. Coverage is a release predicate, not display metadata.

## Evidence boundary

Implementation and synthetic behavior are reproducible. Hardware timing,
radiometric calibration, surface compatibility, physical contrast, reference aging,
resolution and operator performance are unmeasured.
