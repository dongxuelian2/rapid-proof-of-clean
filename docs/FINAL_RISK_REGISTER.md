# Final risk register

Probability estimates are engineering judgments, not measured frequencies.

| Risk | Probability | Consequence | Mitigation | Residual risk | Proposal-critical? |
| --- | --- | --- | --- | --- | --- |
| Optically invisible residue | HIGH | false-clean within retained channels | explicit scope, negative controls, orthogonal assay | HIGH; fundamental | YES |
| Small-support residue below FOV tolerance/PSF | HIGH | false-clean despite strong local response | preregister size sweep; revise aggregation only on held-out physical data | HIGH | YES |
| All references share contamination/aging | MEDIUM | common-mode false-clean or loss of confidence | dated external anchor, independently prepared references, blanks, lifecycle study | HIGH; anchor can share error | YES |
| Material/BRDF variability | HIGH | invalid threshold or large UNKNOWN | material-specific classes/references; refuse unsupported surfaces | HIGH | YES |
| Controlled-state registration fails | HIGH | cancellation mitigation invalid | rigid fixture, fiducials, registration QA, disable PASS on failure | HIGH | YES |
| Exposure/lighting drift | HIGH | false flag or biased proxy | RAW lock, warm-up, flat-field, gain check, reacquire | MEDIUM | YES |
| Sensor noise exceeds bound | HIGH | UNKNOWN or uncontained inference | dark/flat repeats, exposure control, measured bounds | MEDIUM | YES |
| Hardware synchronization/dropout | MEDIUM | corrupt phase sequence | trigger/log frames; missing frame makes view UNKNOWN | LOW–MEDIUM | YES |
| Reference logistics | MEDIUM | stale/wrong material reference | keyed cassette, IDs, expiry/replacement criteria | MEDIUM | YES |
| Occlusion/curvature/inaccessible area | HIGH | unassessed surface is mistaken for coverage | visible mask, multi-view plan, explicit inaccessible fraction | HIGH | YES |
| Operator skips/mispositions a view | MEDIUM | coverage gap or bad geometry | guided sequence, completeness check, training study | MEDIUM | YES |
| Cleaning-agent/residue variation | HIGH | response absent or interference false-flags | safe-surrogate matrix; named supported strata only | HIGH | YES |
| Scratch/wear/moisture confounding | HIGH | false flags and unnecessary recleaning | reclean/repeat; inspect persistent flags; no causal label | MEDIUM | NO |
| Under-30-minute target fails | MEDIUM | misses core challenge requirement for broad areas | adaptive 36-frame clean certificate; measured timing; restrict target set | MEDIUM–HIGH | YES |
| Field-grade hardware costs exceed estimate | MEDIUM | weak affordability case | vendor quotes and acceptance tests | MEDIUM | NO |
| Prior-art overlap | HIGH | differentiation or patentability weakened | precise workflow positioning; professional search/claim chart | HIGH | YES |
| IP/license terms unacceptable | UNKNOWN | cannot submit/commercialize as planned | human agreement review and counsel | UNKNOWN | YES |
| Cannot establish hygienic LOD | HIGH | cannot translate proxy to hygiene threshold | do not claim one; use orthogonal approved endpoints | HIGH | YES |
| AI/authorship terms not satisfied | LOW–MEDIUM | submission ineligible | substantive human review/contribution and required disclosure | LOW after human check | YES |

The proposal does not represent these mitigations as validated. The first physical
go/no-go questions are observability, common-mode reference integrity, material
envelope and measured acquisition time.
