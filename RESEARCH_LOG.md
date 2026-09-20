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

## 2026-09-20

### Goal

Consolidate the supplied `proof_clean_local_plan.zip` into a directly usable project state without extending the research.

### Actions

- Extracted and read the archive's code, documents, task cards, evidence files, reference outputs, and manifest.
- Verified the archive manifest and ran its existing tests and integrity pipeline.
- Preserved the implementation as `proof_clean_local_plan/` and created `PROJECT_HANDOFF.md` as the sole continuation entry.

### Findings

- The imported work is a synthetic, model-conditional computational proof of concept; it is not physical validation or a completed submission.
- The reference metrics reproduce under the current project environment.
- The major failure modes are recorded in the handoff and were not addressed in this pass.

### Decisions

- Do not rewrite the imported core implementation.
- Do not import generated validation outputs; keep only the archive's reference run.

### Open questions

- All human, physical, current-rule, novelty, deployment, and submission gates listed in `PROJECT_HANDOFF.md` remain open.

### Next

Read `PROJECT_HANDOFF.md`, then follow the existing task-card order only after explicit authorization.

## 2026-09-19

### Goal

Complete the requested private GitHub initialization after local validation.

### Actions

- Confirmed that the requested repository name was not already in use.
- Created the private GitHub repository with Issues enabled and no license.
- Pushed the initial `main` commit and configured `origin/main` tracking.

### Findings

- Remote settings report private visibility, `main` as the default branch, Issues enabled, Pages disabled, and no license.
- The local worktree is clean after the push.

### Decisions

- Keep the remote private and defer licensing until IP review.

### Open questions

- Official challenge rules, source URL, deadline, eligibility, AI policy, and IP terms remain `TO VERIFY`.

### Next

Phase 1 — Challenge intake, rules/IP audit, and broad technology landscape scouting.
