# Optical observability limit

Updated 2026-09-20. This note states what the system can and cannot establish. It
is a mathematical scope statement, not a physical validation result.

## Formal boundary

Let `O` be every recorded value in the retained acquisition: selected structured-
light frames, wavelength/angle/polarization intensities, validity metadata and the
coverage mask. Let `C` denote a clean surface and `R` a residue state. If

`P(O | C) = P(O | R)`

for the deployed nuisance distribution, then every deterministic or randomized
decision rule using only `O` has the same output distribution under `C` and `R`.
In particular, raising sensitivity to `R` necessarily raises the corresponding
false-alarm probability on `C`. More thresholds, confidence scores, reference
votes or model complexity cannot change this result. A new measurement state
helps only if it changes the conditional observation distribution.

The benchmark's `observation_matched` construction is the exact equality case.
It proxy-PASSed 100% of FOVs for every policy, including the 60-frame policy. This
is an intended impossibility control, not a bug to tune away.

## Three distinct claims

1. **Model-observable:** under the retained forward model, a residue changes at
   least one required state outside the declared error bounds.
2. **Experimentally observable:** blinded physical data show a repeatable change
   on a named residue × material × finish × loading stratum.
3. **Cleanliness-relevant:** the observed change is linked to an accepted
   cleanliness criterion and external ground truth.

Only the first has computational evidence. The second and third are unverified.

## What changed from v2.1

The two-frequency endpoint certificate was model-redundant in the original
simulator, but it was not robustly redundant. A deliberately different response
operator placed signal only at intermediate spatial frequencies. The 44-frame
v2.1 endpoint policy proxy-PASSed all 20 midband-only FOVs; the three-frequency
controlled state in v2.2 returned UNKNOWN for all 20. The added frequency therefore
adds adversarial information under model mismatch. It does not prove that a real
residue has that response.

The retained observable classes are:

| Class | Retained response | Expected result |
|---|---|---|
| Frequency-shaped blur/scatter | non-linear modulation loss over three frequencies | FLAG or UNKNOWN |
| Spectral/angular/polarization shape change | centered 12-state log signature | FLAG or UNKNOWN |
| Uniform modulation loss | bounded structured-light gain guard | FLAG outside the acquisition envelope |
| Midband-only response | controlled three-frequency model check | UNKNOWN in the domain-shift audit |
| Small-support response | may affect fewer than the 5% PASS tolerance | unresolved spatial-support risk |
| Response matched across all retained states | none | information-theoretically indistinguishable |

## Clean-PASS obligation

The final synthetic policy permits proxy PASS only when all of the following hold:

`dated anchor valid ∧ multi-reference set qualified ∧ coverage valid ∧`
`all required frames valid ∧ diversity certificate PASS ∧ controlled f3 PASS ∧`
`at least 95% of visible pixels PASS ∧ no pixel FLAG`.

Failure of a premise produces UNKNOWN, never PASS. This is a conditional proof
obligation about the acquired optical proxy. It is not proof of sterility, species,
viability, ATP, a chemical identity or absence of all residue.

## Irreducible next evidence

Only physical coupons can determine whether important residue/material strata
move the retained observables by more than field noise and reference drift. The
minimum study must include response-matched negative controls, loading/thickness,
stain size, finish, day/operator, reference aging and an independent comparator.
No further synthetic sweep can close that gap.
