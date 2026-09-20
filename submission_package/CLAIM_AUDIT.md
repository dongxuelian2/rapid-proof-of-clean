# Final proposal claim audit

| Proposal statement | Evidence type | Source / artifact | Allowed wording | Prohibited inference |
| --- | --- | --- | --- | --- |
| Structured light can reveal some contamination/defect responses | published external evidence | Huang 2019/2020 | establishes mechanism plausibility | validates this device or all residues |
| Deflectometry is fast, non-contact and full-field | published review/product evidence | Burke 2023; Micro-Epsilon | adjacent technical foundation | low-cost cleaning performance |
| v0 false-cleaned four constructed cases | synthetic run | `phase1_results.json` | true for fixed toy-model scenes | real false-clean rate |
| v1 flags three of four constructed cases | synthetic run | `failure_mode_registry.csv` | model-conditional improvement | 75% real detection sensitivity |
| optically invisible construction still passes | synthetic impossibility control | Phase 1 results | retained modality limitation | all real residues are invisible |
| standard synthetic proxy-positive PASS is 0% | synthetic run | Phase 1 results | fixed benchmark only | zero real error or proof of safety |
| standard synthetic UNKNOWN is 17.54% | synthetic run | Phase 1 results | fixed benchmark only | expected field availability |
| 12 m² conservative scenario is 21.3 min | assumption model | `coverage_time_model.csv` | planning scenario | measured hardware speed |
| 25 m² conservative scenario is 36.7 min | assumption model | coverage model | transparent limit | whole-room under 30 minutes |
| field BOM $2,100–$9,200 | planning estimate | `HARDWARE_BOM.md` | indicative, unquoted range | purchase price or field readiness |
| routine imaging has no reagent consumable | design fact | architecture/BOM | true for imaging step | zero maintenance/consumable cost |
| PASS requires two states and validity | implemented code | `phase1.py` | software behavior | scientifically valid physical threshold |
| UNKNOWN routes to reacquire/escalate | workflow design | architecture/workflow | proposed safety behavior | validated usability |
| current maturity is TRL 2 | reasoned self-assessment | NASA terminology; evidence ledger | concept-stage estimate | external certification |
| no exact full workflow match found | scoped search result | prior-art matrix | “not confirmed in this search” | novelty or freedom to operate |
| v2.2 preserves v2.1 in-model nonmatched false-clean | retained simulator regression | `final_research_results.json` | both 5.568% pixel false-clean; synthetic only | physical non-inferiority |
| v2.2 lowers domain-shift FOV false-clean | different synthetic response operator | final benchmark | 11.667% fixed vs 1.111% adaptive on constructed suite | expected field performance |
| normal proxy PASS uses 36 frames | implemented sequential policy | `final_model_config.json`; tests | sample-frame certificate behavior | measured acquisition time |
| matched-invisible remains 100% false-clean | information-theoretic control | final benchmark; observability note | fundamental retained-state limit | prevalence of invisible residue |
| balanced spatial release reduces `<5%` false-clean | frozen synthetic held-out split | `small_support_benchmark.json` | 66.96%→41.07%; clean PASS 76.04%→75.00%; synthetic only | physical resolution or field detection limit |
| original 400-case PASS falls 136→93 | deterministic replay | `spatial_adversarial_results.json` | aggregation-only comparison; zero added frames | expected field error rate |
| common-mode live-reference drift becomes UNKNOWN when anchor differs | synthetic reference stress | final benchmark | tested construction only | independently clean anchor guarantee |
| recent art discloses clean-reference optical measurement and iterative cleaning | scoped patent review | WO2025261682A1 | removes broad differentiation claim | legal claim interpretation or FTO |

## Language check

- “clean,” when used as an outcome, was replaced by “proxy PASS” or by a statement
  about the accepted optical-transfer envelope.
- No species, strain, microbial-load, sterility, regulatory, real LOD,
  sensitivity/specificity, or whole-room performance claim is made.
- Every reported number is paired with `synthetic`, `assumption-driven`, or
  `unquoted estimate` as appropriate.
- Participant experience, participation category, eligibility and agreement
  acceptance remain human-only fields.
