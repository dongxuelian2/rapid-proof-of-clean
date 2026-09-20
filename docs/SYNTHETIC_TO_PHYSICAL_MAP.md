# Synthetic-to-physical assumption map

| Synthetic parameter | Mathematical role | Possible physical counterpart | Expected measurable quantity | Calibration experiment | Current status |
| --- | --- | --- | --- | --- | --- |
| `additive_noise_bound` | intensity interval width | dark/read/shot noise after normalization | residual intensity distribution by exposure | dark, flat and static-repeat captures | assumed; not measured |
| `quantization_levels` | digitization interval | effective camera ADC/RAW pipeline | code levels, linearity, clipping | RAW ramp and linearity test | 8-bit primary / 12-bit controlled assumed |
| `clean_variation_bound_pixel2` | allowed nuisance slope `b` | pose/BRDF/reference variability | fitted clean transfer-slope distribution | repeated mounts, operators, distances and angles | proxy assumption only |
| controlled `|b|≤0.01` | narrows cancellation ambiguity | residual geometry after registered repeat | repeat-state slope error | metrology target plus repeated positioning | major unvalidated assumption |
| gain bound `0.36` | constrains intercept `a` | sample/reference radiometric drift | absolute log modulation-gain ratio | exposure, warm-up, distance and gradient sweep | assumed; stress-sensitive |
| reference distance `0.25` | consensus neighborhood | between-reference transfer drift | pairwise median slope distance | three clean coupons over age/cleaning cycles | synthetic only |
| `q` and threshold `0.5` | nonnegative equivalent blur proxy / action rule | material-specific optical transfer change | frequency-dependent modulation loss | blinded deposit ladder with independent mass/area | not mass, thickness, CFU or hygiene; uncalibrated |
| visible mask | domain of possible decision | optical accessibility | visible/registered area fraction | annotated occlusion/curvature study | modeled only |
| frequency transfer | x-axis and signal availability | projector-camera MTF plus surface response | modulation vs frequency/material/pose | edge/pattern sweep | not measured |
| 96 frames/view | observation count | triggered acquisition sequence | capture/drop/registration time | hardware timing and completeness log | implemented count; timing assumed |

Acceptance actions are prospective: violations produce UNKNOWN/reacquisition,
reference replacement, wider bounds with lower usable coverage, or removal of the
unsupported material class.

No mapping is considered established until the corresponding raw data, protocol,
analysis and deviations are archived. Calibration may invalidate the current
synthetic bounds; that is an expected outcome, not a reason to alter data.
