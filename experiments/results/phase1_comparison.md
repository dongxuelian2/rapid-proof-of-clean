# Phase 1 synthetic benchmark comparison

**Evidence type: SYNTHETIC_ONLY. Rates below are descriptive pixel fractions from fixed-seed synthetic scenes, not independent physical trials.**

| Failure mode | v0 false clean | v1 false clean | v1 UNKNOWN | v1 FLAG |
| --- | ---: | ---: | ---: | ---: |
| dirty_reference | 100.00% | 0.00% | 0.00% | 100.00% |
| uniform_absorber | 100.00% | 0.00% | 0.00% | 100.00% |
| optically_invisible_residue | 100.00% | 100.00% | 0.00% | 0.00% |
| negative_blur_cancellation | 100.00% | 0.00% | 0.00% | 100.00% |
| **ALL** | **100.00%** | **25.00%** | **0.00%** | **75.00%** |

The retained v1 does not use the hypothetical secondary-optical result. That candidate is kept as a sensitivity result only because no physical evidence supports its assumed contrast.

## Standard synthetic regression

| Metric | frozen v0 | retained v1 |
| --- | ---: | ---: |
| Proxy-positive false clean | 0.0000% | 0.0000% |
| Zero-proxy PASS | 100.00% | 100.00% |
| UNKNOWN | 18.43% | 17.54% |
| Proxy-positive FLAG | 69.23% | 69.23% |
