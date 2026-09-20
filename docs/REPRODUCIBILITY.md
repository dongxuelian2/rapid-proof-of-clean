# Reproducibility

The repository is designed to make later research work inspectable and repeatable without bundling restricted challenge material.

## Environment

- Use the Python version selected in `pyproject.toml`.
- Use `scripts/bootstrap.ps1` on Windows PowerShell. It creates or reuses `.venv`, installs the project and the declared `dev` extra, and runs the smoke checks.
- `uv.lock` records the resolved dependency graph after the first successful sync. Future bootstrap runs use the lock file in locked mode.
- The project-local `.uv-cache/` is ignored and is only a download/build cache; it is not an input to the research record.

## Verification commands

```powershell
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe scripts\check_env.py
.\.venv\Scripts\python.exe scripts\verify_repo.py
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts\run_submission_pipeline.py
```

## Evidence discipline

- Public sources are recorded in `research/source_ledger.csv`.
- Important claims are recorded in `research/claims_ledger.csv` and reference source IDs.
- Challenge originals, confidential documents, account exports, and raw proprietary data stay outside Git unless redistribution rights are separately verified and documented.
- Generated plots and computational outputs should record the source commit, environment, inputs, and command used.
- The final pipeline regenerates `experiments/results`, figures and curated package
  copies. Small runtime fields in Phase 1 JSON/CSV are machine-dependent; scientific
  rates and fixed-seed outcomes are deterministic.
