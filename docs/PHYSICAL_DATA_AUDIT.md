# Physical-data audit

Audit date: 2026-09-20.

The repository file inventory was searched for camera images, videos, sensor RAW
files, measurement arrays, calibration captures and user-provided experimental
tables outside generated/reference outputs. No physical experiment dataset was
found. `proof_clean_local_plan/reference_run/example_map.npz` and all current
metrics are synthetic reference/generated artifacts.

**Conclusion: the physical experiment was not executed.** There is no real LOD,
sensitivity, specificity, repeatability, material compatibility, hardware timing,
professional-environment performance or operator evidence to analyze.

The proposed first data collection is defined in `MINIMUM_COUPON_PROTOCOL.md` and
`PREREGISTRATION.md`. Any future physical files should be stored with raw immutable
data, checksums, preparation labels, calibration, environment, hardware/software
versions and a clear license/privacy decision; large or restricted raw data should
remain outside Git with a manifest.

