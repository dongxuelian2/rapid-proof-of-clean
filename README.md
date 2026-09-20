# Rapid Proof of Clean

Research and submission workspace for the Rapid Proof of Clean innovation challenge.

## Current phase

```text
Phase 0 complete — infrastructure plus an existing computational proof-of-concept handoff
No new technical direction is selected in this consolidation pass.
```

This repository is intentionally limited to project infrastructure, challenge intake, research bookkeeping, reproducibility, and later submission preparation. It does not choose or endorse a technical approach.

## Continuation entry

The existing computational work is preserved as a self-contained subproject. Start the next session with [`PROJECT_HANDOFF.md`](PROJECT_HANDOFF.md); it is the single handoff entry for the imported implementation, evidence, baseline results, and open items.

## Repository policy

- The GitHub repository is private by policy and is initialized at `https://github.com/dongxuelian2/rapid-proof-of-clean`.
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

This consolidation pass does not add a technical direction or solve any failure mode. Continue only from `PROJECT_HANDOFF.md` after reviewing the existing evidence and its limits.
