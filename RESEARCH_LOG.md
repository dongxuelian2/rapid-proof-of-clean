# Research log

Append-only project log. Add new dated entries; do not rewrite earlier findings to make later work look more certain than it was.

## 2026-09-19

### Goal

Initialize a clean, reproducible research workspace for Rapid Proof of Clean.

### Actions

- Created the repository structure, project metadata, research ledgers, policy documents, scripts, tests, and CI workflow.
- Recorded the detected local development environment.
- Created a project virtual environment with `uv` and CPython 3.12.

### Findings

- No technical solution direction was selected.
- The local `gh` installation is present, but its current GitHub authentication token is invalid.
- The system `python` command is not usable; the project environment is managed through `uv`.

### Decisions

- Keep the repository private by policy.
- Keep restricted challenge material, credentials, and other sensitive data outside Git.
- Defer technical direction and open-source licensing.

### Open questions

- Official challenge rules, source URL, deadline, eligibility, AI policy, and IP terms remain `TO VERIFY`.
- GitHub remote creation requires a fresh `gh auth login` session.

### Next

Verify challenge intake and rules/IP terms in the next explicitly authorized phase.
