# Rapid Proof of Clean

Research and submission workspace for the Rapid Proof of Clean innovation challenge.

## Current status

```text
FINAL_V2_3_COMPUTATIONAL_CANDIDATE_PARTIAL_SPATIAL_IMPROVEMENT
TRL 2 — computational candidate frozen; no physical experiment executed.
```

The active direction is reference-guarded multi-frequency active-reflectance
screening with bounded inference, dated-anchor reference qualification, explicit
abstention, coverage accounting and sequential acquisition. Candidate v2.3 keeps
v2.2 sensing and adds a balanced multiscale FOV-release certificate. It uses a
36-frame clean-PASS point and a 60-frame diagnostic tail. All performance evidence
remains synthetic or assumption-driven.

## Continuation entry

Start with [`PROJECT_HANDOFF.md`](PROJECT_HANDOFF.md). The curated reviewer package
is in [`submission_package/`](submission_package/), and the final classification
and open human gates are in [`docs/FINAL_STATUS.md`](docs/FINAL_STATUS.md).

## Repository policy

- The GitHub repository is private by policy and is initialized at `https://github.com/dongxuelian2/rapid-proof-of-clean`.
- Original challenge materials with unclear redistribution, copyright, confidentiality, or download terms stay outside version control.
- Secrets, credentials, cookies, tokens, and API keys never belong in this repository.
- The selected research route is active optical screening; it is not a validated product or hygiene standard.
- Important research claims must later be traceable through `research/claims_ledger.csv` to entries in `research/source_ledger.csv`.
- No open-source license is added before an IP review.

## Quick start — Windows PowerShell

From the repository root:

```powershell
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe scripts\check_env.py
.\.venv\Scripts\python.exe scripts\verify_repo.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

The bootstrap script uses the installed `uv` tool when available, creates `.venv` with CPython 3.12, installs the project and development dependencies, and runs the smoke checks. It does not modify the system-wide Python installation or write secrets.

## Repository map

- `docs/` — environment, reproducibility, policy, and workflow notes.
- `docs/PHYSICAL_EVIDENCE_MATRIX.md` — material/residue/observable evidence and gaps.
- `docs/ADVANCED_SENSING_STUDY.md` — v2 architecture and negative results.
- `docs/REALISTIC_SIMULATION_REPORT.md` — joint-model v1→v2 benchmark.
- `docs/FINAL_DIFFERENTIATION_MAP.md` — final prior-art separation.
- `docs/FINAL_RESEARCH_REPORT.md` — final architecture, benchmark and stop decision.
- `docs/ADAPTIVE_ACQUISITION.md` — selected policy and rejected frame schedules.
- `docs/OBSERVABILITY_LIMIT.md` — formal limit of retained optical evidence.
- `challenge/` — challenge intake metadata and rights-cleared material references.
- `research/` — source and claim ledgers; no solution literature is added in Phase 0.
- `proposal/` — form-aligned final proposal, claim audit and three-round red team.
- `prior_art/` — literature/patent/product audit and structured matrix.
- `figures/` — generated proposal figures in PNG and SVG.
- `submission_package/` — curated files for human review and form submission.
- `scripts/` — environment and repository checks.
- `private_data/` — local-only material, ignored by Git.

## Scope guard

No file supports claims of microbial detection, sterility, real-world LOD, zero
real error, whole-room coverage, novelty or freedom to operate. Reproduce every
generated submission artifact with:

```powershell
& .\.venv\Scripts\python.exe scripts\run_submission_pipeline.py
```

The pipeline reruns the frozen baseline, Phase 1 benchmark, robustness/coverage
models, realistic v2 study, domain-shift/adversarial audit, proposal audit,
figures, curated package, repository verification and tests.
