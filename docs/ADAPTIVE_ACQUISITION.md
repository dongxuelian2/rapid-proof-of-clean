# Adaptive acquisition study

Updated 2026-09-20. All results are deterministic synthetic audits at the FOV
level. Frame counts exclude amortized reference-coupon acquisition and do not
measure hardware time.

## Retained v2.2 policy

The controller acquires evidence in this order:

| Cumulative frames | Evidence | Allowed terminal action |
|---:|---|---|
| 2 | polarization probe | FLAG only |
| 4 | diversity corners | FLAG only |
| 12 | full wavelength × angle × polarization diversity | FLAG only |
| 28 | controlled endpoint structured light | FLAG only |
| 36 | controlled three-frequency structured light | proxy PASS, FLAG or UNKNOWN |
| 60 | optional primary three-frequency diagnostic | FLAG or UNKNOWN; may confirm PASS only with the full certificate |

Early exit is deliberately asymmetric: weak evidence may stop on a positive
optical anomaly, but it cannot release a surface. A proxy PASS requires the full
12-state diversity plus controlled three-frequency certificate at 36 frames.
The 60-frame state is a diagnostic escalation, not the normal clean path.

## Policy comparison

The independent-response domain-shift benchmark contains 420 FOV-policy records
per policy (four clean-background material models, 21 scenarios and five repeats).

| Policy | Max frames | Observable-dirty false-clean | Dirty UNKNOWN | Nominal clean PASS | Mean / median / p95 frames over full stress set |
|---|---:|---:|---:|---:|---:|
| Fast 20 | 20 | 12.222% | 16.111% | 100% | 11.20 / 4 / 20 |
| Fixed v2.1 | 44 | 11.667% | 12.778% | 100% | 24.53 / 12 / 44 |
| Adaptive v2.2 | 60 diagnostic; 36 clean certificate | **1.111%** (95% bootstrap CI 0–2.778%) | 22.222% | 100% | **22.70 / 4 / 60** |
| Conservative | 60 | 0.556% | 23.889% | 100% | 48.57 / 60 / 60 |

The denominator excludes the exact observation-matched impossibility control but
includes weak, cancellation, sparse and midband challenges. The test distribution
is artificial; rates are architecture-comparison diagnostics, not field prevalence.

## Why 20 frames was rejected

The 20-frame certificate uses four diversity corners and two controlled spatial
frequencies. It saved frames by deleting the two evidence dimensions attacked by
the domain-shift suite. Its 12.222% observable-dirty false-clean rate was not a
threshold problem: the missing midband and non-corner states were never observed.
It is archived as a negative result.

## Preservation of v2.1 behavior

On the original retained simulator, the v2.2 pixel certificate and fixed v2.1
both produced 5.568% nonmatched-residue false-clean, 0.158% UNKNOWN, 96.480%
clean PASS and 0% clean false-FLAG. Thus the new certificate preserves the frozen
v2.1 result in-model. At FOV level, normal clean and the matched-invisible control
need 36 rather than 44 frames (18.2% fewer); nonmatched FOVs stop after a mean of
2.14 frames in that simulator. Relative to the original 108-frame v2 maximum,
the normal clean certificate is reduced by 66.7%.

## Coverage-time implication

With the old conservative, unmeasured timing inputs, the 36-frame clean
certificate models 3.47, 8.24, 15.95 and 27.05 minutes for 1, 5, 12 and 25 m²
target sets. The 60-frame p95/worst budget models 3.70, 9.20, 18.10 and 30.90
minutes. These are planning outputs; repositioning, switching and processing have
not been measured.

## Selection rule

No weighted accuracy score was used. A candidate was retained only if it did not
increase original-model false-clean, repaired a named out-of-model failure and
made measurement failure abstain. The adaptive standard order dominated the
risk-targeted order on mean frames with identical decisions, so the latter was
not selected.
