# Red-team review

## Round 1 — challenge-fit and scientific attack on proposal v1

1. **Where is the physical evidence?** None. Make “not executed” prominent and
   keep the solution at TRL 2.
2. **Does PASS mean clean?** No. Rename it operationally as “proxy PASS” and state
   its narrow meaning every time metrics appear.
3. **Why would residue change modulation transfer?** Literature supports the
   mechanism for some contamination/defect classes, but each surface/residue pair
   requires a coupon dose-response study.
4. **Can invisible residue pass?** Yes; the synthetic adversarial case passes 100%.
   Preserve this result and require orthogonal testing.
5. **Can three dirty references agree?** Yes. Consensus protects against one
   discordant reference, not common-mode corruption.
6. **Is the gain guard a residue detector?** No. It flags attenuation outside a
   bounded acquisition-gain assumption and can false-flag exposure drift.
7. **Is the second state real?** It is implemented in simulation only. Hardware
   registration and the `|b|≤0.01` bound are major unvalidated assumptions.
8. **Are pixels independent trials?** No. Report scene/coupon units and avoid
   binomial claims from pixel counts.
9. **Is 0% false-clean a performance claim?** Only within the standard toy-model
   benchmark; pair it with the invisible-case failure and no real sensitivity.
10. **Is under 30 minutes demonstrated?** No. It is a transparent input model.
11. **Does 12 m² mean full-room coverage?** No. It is visible target-surface area;
    inaccessible fractions are explicitly excluded.
12. **Why not ATP?** The proposal offers non-contact area screening; it does not
    provide ATP's biochemical proxy and should complement rather than “replace.”
13. **Is the solution differentiated from known structured light?** Only at the
    assurance-workflow combination level; the optical principle is prior art.
14. **Is novelty established?** No. Use “candidate differentiation,” keep FTO
    unverified, and recommend counsel.
15. **Does the minimal BOM satisfy v1 assumptions?** Not necessarily. Label it a
    concept rig and separate the field-grade 12-bit configuration.
16. **What happens with missing frames?** Entire view becomes UNKNOWN and is
    reacquired; never silently fit fewer frequencies without revalidation.
17. **What about scratches and wear?** They can flag like residue. The system is an
    anomaly screen and cannot identify cause.
18. **What about transparent, matte, curved or textured surfaces?** Unsupported
    until separately calibrated; material-class refusal is required.
19. **Could UNKNOWN make the system unusable?** Yes. Report coverage and UNKNOWN
    rate as primary operational endpoints.
20. **What is the action threshold?** A synthetic `q=0.5 pixel²`; it has no
    physical meaning until calibrated and must not be converted to mass/CFU.
21. **Could AI-policy wording disqualify the entry?** Human authorship, technical
    decisions, source review and agreement acceptance must be documented.
22. **Who owns background IP?** Unknown from the public page; the participant must
    review the logged-in agreement and obtain advice if needed.
23. **What is the comparator?** Use ATP/chemical/visual/microbiology according to
    the decision, but do not treat any single proxy as universal ground truth.
24. **What would falsify the project?** No reproducible physical response, excessive
    false-clean, common-mode reference failure, or measured timing beyond scope.
25. **What should the final pitch emphasize?** Honest bounded decision control,
    area workflow and a concrete validation plan—not a breakthrough sensor claim.

Round-1 revisions: narrowed PASS language; elevated invisibility and reference
failure; separated modeled time from measured performance; replaced novelty and
ATP-replacement language; added stop criteria and human-only fields.

## Round 2 — final-draft verification

1. Every performance number is labeled synthetic or assumption-driven: **pass**.
2. No microbial, sterility, species, strain or real LOD claim: **pass**.
3. Physical experiment status is explicit: **pass**.
4. Closest structured-light, patent, product and industrial precedents disclosed:
   **pass**, with FTO still open.
5. 30-minute claim is conditional and includes failing scenarios: **pass**.
6. UNKNOWN and inaccessible coverage are first-class outputs: **pass**.
7. Hardware cost is a range/assumption, not a quote: **pass**.
8. Experience and participation are not invented: **pass; human completion needed**.
9. Logged-in agreement/eligibility/IP/AI decisions are not automated: **pass;
   human completion needed**.
10. Proposal can stand without attachments: **pass**, while attachments supply
    audit detail.

## Non-expert read

A cleaning manager should understand the concept as a camera-and-pattern scanner
that finds some surface changes, refuses uncertain views, and creates a coverage
record. Potentially confusing terms (`q`, BRDF, interval propagation) were kept in
the scientific section and translated elsewhere. The most important plain-language
warning is repeated: a green optical result is not proof of microbial safety.
