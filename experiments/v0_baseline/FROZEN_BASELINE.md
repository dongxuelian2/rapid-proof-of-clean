# Frozen v0 baseline

- Frozen UTC+8 date: 2026-09-20
- Git commit: `933c82d51b9de0b5ee8609d3bcf05772348cd8a5`
- Annotated tag: `v0-baseline`
- Branch state before changes: `main...origin/main`, clean
- Evidence: synthetic/model-conditional only

The existing `proof_clean_local_plan/reference_run/` directory is the canonical
immutable baseline artifact. It was not edited. Fresh `run_pipeline.py all`
results matched the reference `metrics`, `stress`, and `test_results` structures
exactly before v1 work began.

## Artifact hashes

| Artifact | SHA-256 |
| --- | --- |
| `reference_run/summary.json` | `1801BB77A2CD788970AF70E6633E369196D375BE9D0DB0B9C3406AE0DD233313` |
| `reference_run/stress.csv` | `2C4FCE55B7FAFF091FCD145F87D44A9CD3F5713CBF2B572B0EB8883960C8B327` |
| `reference_run/tests.txt` | `289F72475F72E0548A0CD8B21F8032F6306462568985DA6347169A76A01B8375` |
| `reference_run/test_results.json` | `8E36E183722A0DAE9385470032C71175CF70E3E1A21355E9CE6E58A2A55754C0` |

## Frozen verification

- Original tests: 8 run, 0 failures, 0 errors.
- Root tests: 2 passed.
- Root ruff: passed.
- Integrity checker: `pipeline_integrity_passed=true`.
- 72-scene v0 bounded interval: proxy-positive false clean 0%; zero-proxy
  PASS 100%; UNKNOWN 18.4339735%; proxy-positive FLAG 69.2307692%.
- Four prioritized v0 stress cases: 100% PASS each (`dirty_reference`,
  `uniform_absorber`, `optically_invisible_residue`, `negative_blur_cancellation`).

The root-test count belongs to the pre-v1 commit. Later test growth is reported
separately and does not rewrite this frozen record.
