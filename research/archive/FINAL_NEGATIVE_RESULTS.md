# Final negative-result archive

Updated 2026-09-20. These results are retained to prevent future work from
quietly repeating or tuning away failed ideas.

| Candidate / claim | Result | Disposition |
|---|---|---|
| 20-frame `d4+c2` clean certificate | 12.222% observable-dirty FOV false-clean in the domain-shift suite | Rejected; missing evidence dimensions cannot be repaired by threshold tuning |
| Fixed v2.1 endpoint-only structured certificate | PASS on 20/20 midband-only FOVs | Superseded by required third controlled frequency |
| 60-frame conservative always-on acquisition | slightly lower synthetic false-clean but median 60 frames and no new physical observable | Retained only as diagnostic comparator |
| Risk-targeted 4→28→36 order | identical decisions but higher mean frames than 2→4→12→28→36 | Rejected as dominated on the tested distribution |
| Phase/amplitude joint inference for planar film | no independent phase response in retained planar model; geometry confounds phase | Not promoted without physical evidence |
| Reference-free sanity check as cleanliness evidence | cannot distinguish identical observations | Validity guard only; not an observability channel |
| Live multi-reference agreement proves clean origin | common-mode dirty references can agree | Rejected; dated independent anchor required |
| Threshold adjustment solves matched invisibility | exact observation match passes every retained policy | Impossible within retained observations |
| Broad workflow novelty | contradicted by patent/product combinations, strengthened by WO2025261682A1 | Do not claim |

Machine-readable adversarial counterexamples are in
`experiments/adversarial_regressions.json`. Historical v0/v1/v2.1 artifacts remain
in their original paths and tags.
