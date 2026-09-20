# Coverage and time budget

The executable model is `src/rapid_proof_clean/coverage.py`; the scenario runner
is `scripts/run_final_validation.py`. Results are in
`experiments/results/coverage_time_model.csv`. Every input is an **unvalidated
assumption**, not measured hardware performance.

For target area `A`, inaccessible fraction `u`, field of view `w×h`, and declared
area-overlap fraction `o`:

`views = ceil(A(1-u) / (w h (1-o)))`

`frames/view = states × orientations × frequencies × phases = 2×2×6×4 = 96`

This remains the frozen conservative v1 timing model. The final v2.2 schedule is
also evaluated explicitly in `adaptive_coverage_time_model.csv`, while preserving
the warning that switching, exposure, readout and operator timing are unmeasured.
Fewer simulated frames do not establish a proportional field-time reduction.

`total time = setup/reference + views × (frames×frame period + processing + reposition)`

| Profile | FOV | Frame period | Process + move / view | Setup/reference |
| --- | --- | ---: | ---: | ---: |
| optimistic | 0.50×0.40 m | 16.7 ms | 1.4 s | 90 s |
| conservative | 0.30×0.25 m | 33.3 ms | 4.0 s | 120 s |
| stress | 0.20×0.15 m | 50 ms | 8.0 s | 180 s |

| Target | Accessible fraction | Optimistic | Conservative | Stress |
| --- | ---: | ---: | ---: | ---: |
| 1 m² work surface | 95% | 1.8 min | 4.0 min | 13.5 min |
| 4 m² high-touch set | 85% | 2.5 min | 9.3 min | 40.3 min |
| 5 m² preparation zone | 80% | 2.7 min | 10.6 min | 46.9 min |
| 12 m² small-room targets | 75% | 4.2 min | 21.3 min | 101.6 min |
| 25 m² large-room targets | 65% | 6.3 min | 36.7 min | 180.9 min |

The 30-minute objective is plausible for a bounded target set under the
conservative assumptions, but not for the 25 m² case and not under stress. The
model excludes rescans, cleaning time, operator interruptions, network transfer
and orthogonal testing. A full-room “single pass” is not demonstrated.

## Final adaptive budget

The final policy has a 36-frame normal clean-PASS certificate, early FLAG exits
and a 60-frame diagnostic tail. In the artificial valid-case mix its mean was
22.9 frames and p95 was 60. Applying those statistics to the same conservative
timing assumptions gives:

| Target | Expected synthetic mix | Clean PASS (36) | p95 / worst (60) |
|---|---:|---:|---:|
| 1 m² | 3.35 min | 3.47 min | 3.70 min |
| 5 m² | 7.72 min | 8.24 min | 9.20 min |
| 12 m² | 14.78 min | 15.95 min | 18.10 min |
| 25 m² | 24.94 min | 27.05 min | 30.90 min |

“Expected” reflects the constructed benchmark mix, not field prevalence. The
25 m² p95/worst case still misses 30 minutes. Physical timing and operator
coverage studies remain gating evidence.
