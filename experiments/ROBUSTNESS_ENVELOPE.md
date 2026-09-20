# Synthetic robustness envelope

`scripts/run_final_validation.py` evaluates 14 nuisance settings over clean and
strong-proxy scenes (four fixed seeds; pixels are descriptive, not independent).
The full table is `experiments/results/robustness_envelope.csv`.

| Nuisance | Clean outcome | Strong-proxy outcome | Interpretation |
| --- | --- | --- | --- |
| nominal | PASS | FLAG | expected synthetic behavior |
| exposure ×0.75 / ×1.25 | FAIL | FLAG | gain guard can false-flag clean under drift |
| multiplicative gain ×0.65 | FAIL | FLAG | independent naming of the same radiometric confounder |
| registration 1 / 3 px | PASS | FLAG | this generator is spatially homogeneous enough that shift is not a hard test |
| extra noise 0.003 | UNKNOWN | mixed FLAG/UNKNOWN | bounds detect degradation |
| extra noise 0.015 | UNKNOWN | UNKNOWN | unusable outside error envelope |
| common reference aging 0.2 | UNKNOWN | FLAG | clean availability collapses |
| common reference aging 0.8 | UNKNOWN | UNKNOWN | reference lifecycle is critical |
| roughness mismatch +0.2 | mostly PASS | FLAG | near modeled envelope |
| roughness mismatch −0.4 | UNKNOWN | FLAG | sign/asymmetry matters |
| illumination gradient 10% | mostly PASS | FLAG | small modeled gradient tolerated |
| illumination gradient 35% | FAIL | FLAG | false flags; shading correction must be validated |
| missing frequency | UNKNOWN | UNKNOWN | deliberate safe abstention |

This sweep identifies bound violations; it does not validate the bounds. The
registration result is specifically non-probative because the synthetic phase
field lacks realistic object texture and parallax. High-priority physical tests
are noise, common reference aging, exposure/illumination drift, pose/registration,
material roughness and optically subtle films.
