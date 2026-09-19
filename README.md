# Rapid Proof of Clean

Research and submission workspace for the Rapid Proof of Clean innovation challenge.

## Current phase

```text
Phase 0 — Infrastructure / challenge intake
No technical solution direction has been selected.
```

This repository is intentionally limited to project infrastructure, challenge intake, research bookkeeping, reproducibility, and later submission preparation. It does not choose or endorse a technical approach.

## Repository policy

- GitHub visibility is private by policy. The remote repository remains pending until GitHub CLI authentication is repaired.
- Original challenge materials with unclear redistribution, copyright, confidentiality, or download terms stay outside version control.
- Secrets, credentials, cookies, tokens, and API keys never belong in this repository.
- No technical route has been selected during Phase 0.
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
- `challenge/` — challenge intake metadata and rights-cleared material references.
- `research/` — source and claim ledgers; no solution literature is added in Phase 0.
- `proposal/` — later proposal drafts and review notes.
- `scripts/` — environment and repository checks.
- `private_data/` — local-only material, ignored by Git.

## Scope guard

The current task stops after infrastructure initialization. Phase 1 is reserved for challenge intake, rules/IP audit, and broad technology landscape scouting.
