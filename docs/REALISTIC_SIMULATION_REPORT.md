# Realistic simulation report

Updated 2026-09-20. Evidence class:
`ASSUMPTION_DRIVEN_PHYSICALLY_MOTIVATED_SIMULATION_ONLY`. No physical experiment
was executed.

## What changed from the toy proxy

The new model jointly varies:

- four surfaces: glass, stainless steel, HDPE and glazed ceramic;
- clean, water film, oil film, protein smear, detergent crystals, particles,
  a single-state-degenerate film and a fully matched invisible residue;
- complex-index Fresnel reflection and coherent single-film interference over
  three wavelengths, two angles and s/p polarization;
- structured-light modulation loss, roughness/defocus, mixed specular/diffuse
  response, finite nonuniform stains and film-thickness variation;
- exposure drift, illumination gradient, multiplicative sensor noise,
  quantization and ±1-pixel registration error;
- three-reference consensus and primary/controlled-geometry state fusion.

This is closer to reality than the original q-only proxy, but it is not a digital
twin. Optical constants are coarse constants, morphology is synthetic, coherent
film assumptions fail for many rough/discontinuous residues, and no parameter is
fit to project sensor data.

## Frozen benchmark

Configuration: four materials × eight residue conditions × six scene replicates,
32×32 pixels, fixed seed 20260920. Positive metrics are evaluated only within the
constructed stain support; clean metrics use the full image. Files:

- `experiments/results/v2_results.json`
- `experiments/results/v2_benchmark.csv`
- `experiments/v2_config.json`

### Aggregate architecture comparison

| Method | Nonmatched residue false-clean | UNKNOWN | Usable coverage | Matched-invisible false-clean | Clean PASS | Clean false-FLAG |
|---|---:|---:|---:|---:|---:|---:|
| v1 multi-frequency | 44.37% | 12.21% | 87.79% | 100.00% | 100.00% | 0.00% |
| v2 angle | 21.20% | 26.70% | 73.30% | 100.00% | 100.00% | 0.00% |
| v2 polarization | 8.93% | 2.18% | 97.82% | 100.00% | 100.00% | 0.00% |
| v2 wavelength | 7.66% | 9.16% | 90.84% | 99.94% | 99.97% | 0.00% |
| **v2 combined** | **5.57%** | **0.16%** | **99.84%** | **96.56%** | **96.48%** | **0.00%** |

The matched-invisible construction receives no FLAG from any arm. Its combined-v2
false-clean is below 100% only because 3.45% becomes UNKNOWN under noise; that is
not detection.

### v1 → combined-v2 by residue

| Residue | v1 false-clean | v2 false-clean | v2 FLAG | v2 UNKNOWN | Interpretation |
|---|---:|---:|---:|---:|---|
| Water film | 38.35% | 5.37% | 94.45% | 0.18% | angular/polarization/interference signature adds information |
| Oil film | 75.99% | 4.54% | 95.38% | 0.08% | strongest benefit over v1 film weakness |
| Protein smear | 4.66% | 4.48% | 95.34% | 0.18% | v2 converts most v1 ambiguity to FLAG |
| Detergent crystals | 7.56% | 7.35% | 92.44% | 0.21% | already easy via modulation blur; little new gain |
| Particles | 8.20% | 7.98% | 91.80% | 0.22% | already easy; registration-edge misses dominate |
| Primary-degenerate film | 86.23% | 5.66% | 94.20% | 0.14% | direct demonstration of observable-set expansion |
| Matched invisible | 100.00% | 96.55% | 0.00% | 3.45% | unchanged identifiability boundary |

## What drives the remaining false-clean

Most nonmatched v2 false-clean pixels occur at stain boundaries after the sample
is shifted by up to one pixel relative to the truth mask. Particulate/crystal
classes also retain the v1 blur model’s finite threshold. These are useful
adversaries: a strong per-pixel optical signature does not guarantee geometric
coverage when stain size approaches registration/PSF error.

The combined arm’s 3.52% clean UNKNOWN is the cost of taking the maximum residual
over 12 noisy features. It creates no clean false-FLAG in this run, but this result
is conditional on the frozen noise distribution and cannot be extrapolated.

## Adversarial benchmark cases

1. **Single-state degeneracy:** a thin film is selected to nearly match clean at
   the v1 central state while retaining contrast across the diversity cube.
2. **Full observational equivalence:** the residue returns the exact clean
   signature and zero extra modulation blur in every retained state.
3. **Common exposure drift:** diversity inference removes a median log gain so it
   cannot win by duplicating the v1 gain threshold.
4. **Finite stain + registration:** sample images shift independently of the
   ground-truth support, exposing boundary false-cleans.
5. **Material BRDF diversity:** dielectric, metallic and mixed diffuse/specular
   bases are evaluated separately.
6. **Reference ensemble:** every scene uses three noisy clean references; no
   benchmark grants a perfect noiseless reference to the inference code.

## Interpretation

Within this model, v2 is a substantive architecture improvement, not a threshold
change: it adds independent angular, spectral and polarization measurements and
dramatically improves the deliberately v1-degenerate film. The result reduces the
scope of the unvalidated assumption from “will any real residue produce v1 blur?”
to “will named real residue/material pairs produce a stable diversity signature
above field nuisance?” It does not answer that question experimentally.

## Reproduce

```powershell
& .\.venv\Scripts\python.exe scripts\run_v2_study.py
```

The canonical pipeline also runs this command before repository verification,
ruff and pytest.
