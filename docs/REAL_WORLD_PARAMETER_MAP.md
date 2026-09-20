# Real-world parameter map

This map translates the toy model into quantities that a physical pilot must
measure. Unless a row cites an actual device result, its range is **UNVALIDATED**.

| Model / workflow quantity | Physical counterpart | Current value or range | Validation needed |
| --- | --- | --- | --- |
| `image_size=32` | analyzed camera samples per field | 32×32 synthetic pixels; **UNVALIDATED RANGE** | Select camera, optics, binning, and verify spatial resolution on each surface. |
| screen coordinate width 256 px | projected-pattern coordinate system | 256 model pixels; **UNVALIDATED RANGE** | Calibrate projector/display pixels to millimetres on surface at working distance. |
| camera resolution | sensor sampling and lens MTF | not selected; **UNVALIDATED RANGE** | Record native resolution, bit depth, lens, focus, linearity, dark/flat fields. |
| working distance | camera/projector-to-surface distance | not selected; **UNVALIDATED RANGE** | Test repeatability, spot size, parallax, occlusion, and operator tolerance. |
| field of view | inspected surface area per pose | not selected; **UNVALIDATED RANGE** | Measure width/height and usable fraction on representative materials. |
| illumination geometry | incidence/viewing angles and baseline | two abstract orthogonal directions; **UNVALIDATED RANGE** | Record angles, polarization, standoff, registration error, BRDF sensitivity. |
| spatial frequencies | projected cycles per physical length | `[2,4,8,16,32,48]` cycles per 256 model px; **UNVALIDATED RANGE** | Convert to cycles/mm and measure delivered contrast at surface. |
| phase states | projected/captured sequence | four per frequency and orientation | Verify phase accuracy, synchronization, motion sensitivity, and closure test. |
| exposure / noise | linear radiometric error bound | v0 `0.0015` + 8-bit quantization; v1 controlled `0.0002` + 12-bit; **UNVALIDATED RANGE** | Measure repeatability and justify deterministic or statistical bounds without test leakage. |
| surface roughness | BRDF/scatter and modulation visibility | absent from material model; **UNVALIDATED RANGE** | Use coupons spanning stainless steel, glass, laminate, and deliberately rough controls. |
| reflectivity / gain | reference/sample modulation intercept | simulator gain 0.85–1.15; v1 log-ratio guard 0.36; **UNVALIDATED RANGE** | Measure across angle, material, exposure, ambient light, and day-to-day drift. |
| residue thickness / optical contrast | response mapped to `q` or added channel | no mapping; **UNVALIDATED RANGE** | Prepare gravimetric or volumetric dilution series and measure independent ground truth. |
| `q` | equivalent added Gaussian transfer variance | threshold 0.5 screen-pixel²; synthetic proxy only | Fit or reject model per residue/material; never convert to mass/thickness without data. |
| geometry term `b` | focus/standoff/pose-induced transfer change | v0 bound 0.08; controlled-state bound 0.01; **UNVALIDATED RANGE** | Perturb pose and focus systematically; verify registration and bound coverage. |
| reference count/confidence | clean historical acquisitions and agreement | 3 refs; 2-of-3 synthetic consensus | Define cleaning, sealing, dating, drift, replacement, and contamination challenge procedure. |
| acquisition count | raw frames per field | v0 96 total; v1 384 including 288 reference-library + 96 live sample frames | Separate one-time reference capture from live scan; measure dropped/misaligned frames. |
| scan time | pattern display + exposure + motion | no measured value; **UNVALIDATED RANGE** | Time end-to-end field coverage, not just inference. |
| computational latency | demodulation/inference time | machine-specific synthetic milliseconds only | Benchmark selected hardware including capture, registration, mapping, and reporting. |
| area coverage | visible in-scope surface fraction | synthetic mask only; **UNVALIDATED RANGE** | Record all target surfaces, occlusions, unusable BRDF, repeat overlap, and blind areas. |

No row establishes a real LOD, professional-environment coverage, or a 30-minute
workflow. The table is an experiment-starting specification, not measured product data.
