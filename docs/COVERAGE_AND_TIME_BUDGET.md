# Coverage and time budget

The executable model is `src/rapid_proof_clean/coverage.py`; the scenario runner
is `scripts/run_final_validation.py`. Results are in
`experiments/results/coverage_time_model.csv`. Every input is an **unvalidated
assumption**, not measured hardware performance.

For target area `A`, inaccessible fraction `u`, field of view `w×h`, and declared
area-overlap fraction `o`:

`views = ceil(A(1-u) / (w h (1-o)))`

`frames/view = states × orientations × frequencies × phases = 2×2×6×4 = 96`

This remains the conservative v1 timing model. The v2.1 sample schedule is 44
frames/FOV, but the table is not rescaled because wavelength/polarization
switching, exposure and readout timing have not been measured; fewer frames do
not by themselves establish a proportional field-time reduction.

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
