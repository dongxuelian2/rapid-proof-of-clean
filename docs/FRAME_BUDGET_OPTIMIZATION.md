# Frame-budget optimization

> Final update: v2.1 below is the frozen fixed-budget baseline. The selected
> v2.2 policy is documented in `ADAPTIVE_ACQUISITION.md`: a 36-frame clean-PASS
> certificate, 2/4/12/28-frame early FLAG exits and optional 60-frame diagnostic.
> It preserves v2.1's 5.568% in-model pixel false-clean and repairs the endpoint-
> only midband domain-shift failure by returning UNKNOWN.

Updated 2026-09-20. All numbers in this document are assumption-driven
simulation results, not camera timing or physical sensitivity measurements.

## Decision

Promote the 44-frame schedule as candidate **v2.1**:

1. 12 raw intensity states: 470/550/850 nm × 15°/55° × s/p;
2. 16 primary structured frames: two orientations × endpoint spatial
   frequencies 2 and 48 cycles/screen × four phases;
3. 16 controlled-geometry structured frames with the same endpoint design.

The maximum is therefore 44 sequential sample exposures/FOV, down from 108
(`−59.3%`). Clean PASS and a complete pixel map always require all 44. If the
12-state diversity stage already produces any FLAG, the system may stop at 12
frames and reject the FOV; after diversity plus primary it may similarly stop at
28. These early exits prove only an FOV-level FLAG and do not produce a complete
map of every pixel.

Clean-reference acquisitions are excluded from both the old and new sample-frame
counts. No claim is made about exposure time, polarization simultaneity, camera
readout overlap, switching latency or motion tolerance.

## Selection method

`scripts/run_frame_optimization.py` evaluates the same four materials, eight
conditions and six replicates used by the realistic v2 benchmark. Replicates 0–2
form a design split; replicates 3–5 are a held-out audit split. Candidate
schedules vary structured states/frequencies and explicit subsets of the 12
diversity states. They use unchanged inference bounds.

The 44-frame schedule was selected instead of the numerically identical 28-frame
controlled-only schedule because it preserves the primary→controlled
remeasurement and the cancellation defense. The 28-frame row remains a negative
engineering result: it looks equally good in the current realistic simulator,
but removes an independently motivated failure-control state.

## Held-out audit

| Schedule | Frames/FOV | Nonmatched false-clean | Nonmatched UNKNOWN | Clean PASS | Clean false-FLAG | Matched-invisible false-clean |
|---|---:|---:|---:|---:|---:|---:|
| v2, 6 frequencies + both states + 12 diversity | 108 | 5.531% | 0.137% | 96.330% | 0% | 96.519% |
| **v2.1, 2 endpoint frequencies + both states + 12 diversity** | **44** | **5.531%** | **0.137%** | **96.330%** | **0%** | **96.519%** |
| Controlled only + 2 frequencies + 12 diversity | 28 | 5.531% | 0.137% | 96.330% | 0% | 96.519% |
| Controlled only + 2 frequencies + 4 corner diversity states | 20 | 6.132% | 4.961% | 98.763% | 0% | 98.767% |
| Controlled only + 2 frequencies + s/p pair | 18 | 7.409% | 3.689% | 100% | 0% | 100% |

The equality of the 108- and 44-frame rows is exact for this fixed audit, not a
statistical non-inferiority claim. It reveals model redundancy: the simulated
structured transfer response is sufficiently described by its two frequency
endpoints, while most v2 false-clean improvement comes from the diversity cube.
Real optics may have mid-band structure, flare or frequency-dependent error not
represented here.

## Original failure-mode audit

The fixed eight-scene-per-class v1 constructions were rerun with all six
frequencies and with only the two endpoints. Both schedules produced the same
result: dirty-reference, uniform-absorber and negative-blur-cancellation cases
had 0% false-clean and 100% FLAG; the intentionally observation-matched residue
remained 100% false-clean. Compression therefore retains the three modeled v1
defenses without pretending to solve the identifiability boundary.

## Adaptive acquisition result

In the 192 realistic simulated FOVs, the staged schedule stopped at 12 frames for
all 144 nonmatched-residue FOVs because at least one pixel was already FLAG; all
24 clean and 24 matched-invisible FOVs required 44 frames. The overall simulated
mean was 20 frames/FOV. This is a triage result, not the cost of issuing PASS:
every clean decision still has a 44-frame ceiling, and physical false triggers
could change the distribution.

## Reproduce

```powershell
& .\.venv\Scripts\python.exe scripts\run_frame_optimization.py
```

Generated evidence is in `experiments/results/frame_optimization_benchmark.csv`
and `experiments/results/frame_optimization_results.json`.
