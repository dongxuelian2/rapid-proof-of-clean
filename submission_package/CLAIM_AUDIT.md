# Claim Audit for the InnoCentive Form Text

This audit maps the participant-facing proposal to its evidence and records
supporting figures that are deliberately absent from the main narrative. Every
computational result below is synthetic. None is a measured physical error rate
or a forecast of field performance.

## Form claim audit

| Form field | Proposal claim | Evidence type and source | Allowed interpretation | Prohibited inference |
| --- | --- | --- | --- | --- |
| Problem & Opportunity | Non-contact optical screening may provide a mapped, broad-area complement to point tests and visual inspection | Intended workflow; `FINAL_CHALLENGE_FIT.md`; coverage model | Proposed value for visible, registered target surfaces | Proven speed, whole-room coverage, replacement for ATP or other tests |
| Solution Overview | Concept is TRL 2, using controlled optical states and qualified material/finish references | Reasoned maturity assessment; `experiments/final_model_config.json`; `src/rapid_proof_clean/reference_integrity.py`; `src/rapid_proof_clean/sequential.py` | Analytical and synthetic concept with executable decision logic | Validated physical prototype or externally certified TRL |
| Solution Overview | Reference qualification, bounded multi-state evidence and coverage gate the PASS outcome | Implemented software behavior; final configuration and tests | Software enforces the stated prerequisites on constructed data | Physically valid thresholds or guaranteed reference cleanliness |
| Solution Overview | Outcomes are PASS, FLAG and UNKNOWN; failed premises trigger controlled remeasurement or escalation | Workflow design and implementation | Proposed operator decision path | Validated usability, operator accuracy or site workflow |
| Solution Overview | Release logic accounts for false-clean risk | Synthetic domain-shift and spatial studies | Conservative gating reduced some constructed false-clean outcomes while preserving known limitations | Elimination of false-clean results or a real-world false-clean rate |
| Solution Feasibility/Scientific Basis | Some prepared residues can alter optical response | Huang; Jespersen; Aboonajmi; NASA TN D-6585 | Physical plausibility for selected materials and constructions | This device detects all residues or transfers published classifier scores |
| Performance Expectations | Synthetic stress testing supports implementation behavior and identifies remaining boundaries | Final benchmark; `experiments/small_support_benchmark.json`; `experiments/spatial_adversarial_results.json` | Evidence about tested synthetic constructions only | Sensitivity, specificity, LOD or expected field performance |
| Performance Expectations | Residues with limited spatial support and observation-matched residues remain limitations | Spatial study and observability control | A signal can be diluted below spatial support or be indistinguishable from the clean observation | Prevalence of these residues in actual facilities |
| Performance Expectations | No physical experiment, real LOD, sensitivity, specificity, repeatability or site performance has been established | Project evidence inventory | Accurate statement of current evidence | Any measured physical detection capability |
| Performance Expectations | No microbial, sterility or hygienic-safety claim is made | Modality scope and claim ladder | Optical proxy only | Microbial absence, sterility or regulatory compliance |
| Performance Expectations | The most conservative 25 m² timing scenario is about 31 minutes | Assumption-driven `experiments/results/adaptive_coverage_time_model.csv` | Planning estimate; its upper scenario exceeds a 30-minute target | Measured scan time, guaranteed 25 m² coverage or operator throughput |
| Experience | Participant must supply their own verifiable experience | Explicit human-completion placeholder | No personal experience is asserted | Invented qualifications or facilities |
| Solution Risks | Shared reference drift can make clean origin unidentifiable; prior-art/FTO is unverified | Synthetic reference stress; scoped patent search including WO2025261682A1 | Known design and legal uncertainty | Independent clean-anchor guarantee, novelty opinion or FTO |
| Development Timeline and Capability | Four proposed stages depend on partner access and physical validation | Future work plan and identified asset/partner needs | Planning estimate only; participant's role must be confirmed; no physical stage is complete | Committed dates, invented experience or current prototype/field status |
| Online References | Selected literature, patent and product sources provide context | Linked sources in proposal | Background and prior-art context | Legal analysis or transfer of another system's performance |

## Supporting numerical evidence

These details support internal review. Keep them out of the main proposal narrative
unless the form specifically requests supporting metrics and the synthetic caveat
can be displayed with the number.

| Synthetic result | Recorded value | Source and boundary |
| --- | --- | --- |
| Nonmatched pixel benchmark for the spatial certificate | 5.568% false-clean; 0.158% UNKNOWN; clean PASS 96.480%; clean false-FLAG 0% | `experiments/results/final_research_results.json`; constructed simulator cases, not physical pixels or sites |
| Observable-dirty domain-shift FOV comparison | Fixed policy: 11.667% false-clean and 12.778% UNKNOWN. Adaptive policy: 1.111% false-clean (FOV bootstrap 95% interval 0–2.778%) and 22.222% UNKNOWN. Nominal clean PASS was 100%, with 0% false-FLAG. | Final synthetic benchmark; the changed response operator is artificial and rates are distribution-dependent |
| Held-out `<5%` spatial-support stratum | False-clean fell from 66.96% to 41.07%; clean PASS changed from 76.04% to 75.00%; clean UNKNOWN changed from 23.96% to 25.00%; clean false-FLAG remained 0%. | `experiments/small_support_benchmark.json`; `<5%` describes the fraction of constructed FOV area occupied by residue, not residue concentration or a field-population rate |
| Original 400-case adversarial replay | PASS cases changed from 136/400 to 93/400 with no added measurement frames. | `experiments/spatial_adversarial_results.json`; constructed cases, not a random sample of real cleaning outcomes |
| Focused 400-case adversarial search | The balanced rule still returned PASS for 175/400 cases, concentrated in sub-1% and dispersed constructions. | `experiments/spatial_adversarial_results.json`; a separate synthetic search set; confirms the partial result and surviving boundary |
| Exact observation-matched control | 100% false-clean by construction | Final benchmark / observability control; identical measured evidence is not separable by this modality, and this does not estimate prevalence |
| Sequential acquisition implementation | A nominal clean certificate uses 36 frames; optional diagnostics reach 60 frames | `experiments/final_model_config.json`; frame counts are code behavior, not measured scan time |
| 25 m² time scenarios | 27.05 minutes for the nominal 36-frame certificate and 30.90 minutes for the 60-frame budget | `experiments/results/adaptive_coverage_time_model.csv`; unmeasured assumptions for switching, readout, motion and processing |
| Planning hardware range | USD 2,100–9,200 | `docs/HARDWARE_BOM.md`; unquoted estimate, not a supplier quote or validated field build |

The original replay and focused search are separate constructed sets and must not
be merged into one denominator. The small-support percentages describe synthetic
strata. No denominator in this section represents independent physical samples.

## Language and submission check

- The proposal headings map to the current form's Problem & Opportunity,
  Solution Overview, Solution Feasibility/Scientific Basis, Performance
  Expectations, Experience, Solution Risks, Development Timeline and Capability,
  and Online References fields.
- The main narrative describes adversarial findings qualitatively; detailed
  adversarial counts and rates remain in supporting evidence above.
- PASS is an optical-proxy result. FLAG indicates an optical anomaly. UNKNOWN
  means the available reference, measurement or coverage evidence is inadequate.
- The proposal explicitly states that no physical experiment has been conducted,
  no real LOD or sensitivity/specificity is known, no microbial or sterility claim
  is made, physical validation remains required, and observation-matched residues
  cannot be distinguished.
- The Experience placeholder is participant-only and must be completed with
  verifiable facts before submission.
- Participation type, eligibility, agreement acceptance, IP terms and any
  required AI disclosure also remain human-only checks in
  `HUMAN_FINAL_CHECKLIST.md`.
