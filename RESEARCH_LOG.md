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

## 2026-09-20 — Phase 1 de-risking

### Goal

Advance the active-reflectance synthetic baseline into an audited v1 research
candidate without overstating physical evidence.

### Actions

- Froze clean `main` commit `933c82d5...` as annotated tag `v0-baseline` and
  verified the reference metrics, 12 stress classes, 8 original tests, 2 root
  tests, ruff, and integrity checker before core changes.
- Audited the official public challenge page and recorded logged-in agreement,
  geographic, payment, tax, confidentiality, and detailed license items as `TO VERIFY`.
- Expanded the source and claim ledgers and completed a focused prior-art screen.
- Built a fixed-seed failure registry centered on false clean, abstention, usable
  coverage, nuisance seed, and runtime.
- Tested gain guard, reference consensus, controlled geometry, and a hypothetical
  secondary optical state; rejected the unvalidated optical-state result.
- Implemented retained v1 and a single-command reproducibility pipeline.
- Added real-world parameter mapping and a not-performed physical pilot plan.

### Findings

- v0 false-clean was 100% for each prioritized failure construction.
- v1 reduced dirty-reference, uniform-absorber, and cancellation false-clean to
  0% in the fixed synthetic benchmark; invisible residue stayed at 100%.
- Standard synthetic regression stayed at 0% proxy false-clean and 100% q=0 PASS.
- Major optical components have clear precedent; only a combined assurance
  workflow remains a possible, unverified distinction.

### Decisions

- Keep invisible residue as a fundamental retained-modality limitation.
- Retain reference consensus, bounded gain, and controlled second-state logic.
- Do not retain the hypothetical extra-channel response without physical data.
- Keep all claims explicitly synthetic/model-conditional until physical validation.

### Next

Human agreement review, then the pre-registered coupon pilot and focused
multi-reference/abstention patent-product search. Do not write a final proposal yet.
