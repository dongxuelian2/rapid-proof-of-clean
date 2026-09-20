"""Verify repository structure and safety invariants."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "PROJECT_HANDOFF.md",
    "PROJECT_SCOPE.md",
    "CHALLENGE_RULES.md",
    "DECISION_LOG.md",
    "RESEARCH_LOG.md",
    "SUBMISSION_CHECKLIST.md",
    "pyproject.toml",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".env.example",
    "docs/ENVIRONMENT_REPORT.md",
    "docs/REPRODUCIBILITY.md",
    "docs/IP_AND_DATA_POLICY.md",
    "docs/WORKFLOW.md",
    "docs/FINAL_CHALLENGE_FIT.md",
    "docs/FINAL_SYSTEM_ARCHITECTURE.md",
    "docs/FINAL_STATUS.md",
    "docs/DETECTION_SCOPE.md",
    "docs/COVERAGE_AND_TIME_BUDGET.md",
    "docs/HARDWARE_BOM.md",
    "docs/SYNTHETIC_TO_PHYSICAL_MAP.md",
    "experiments/MINIMUM_COUPON_PROTOCOL.md",
    "experiments/PREREGISTRATION.md",
    "docs/PHYSICAL_DATA_AUDIT.md",
    "experiments/ROBUSTNESS_ENVELOPE.md",
    "docs/CLAIM_LADDER.md",
    "docs/FINAL_RISK_REGISTER.md",
    "docs/TRL_ROADMAP.md",
    "docs/USER_WORKFLOW.md",
    "docs/COMPETITIVE_POSITIONING.md",
    "docs/PHYSICAL_EVIDENCE_MATRIX.md",
    "docs/ADVANCED_SENSING_STUDY.md",
    "docs/REALISTIC_SIMULATION_REPORT.md",
    "docs/FINAL_DIFFERENTIATION_MAP.md",
    "docs/FRAME_BUDGET_OPTIMIZATION.md",
    "docs/ADAPTIVE_ACQUISITION.md",
    "docs/REFERENCE_ROBUSTNESS.md",
    "docs/DOMAIN_SHIFT_AND_ADVERSARIAL.md",
    "docs/OBSERVABILITY_LIMIT.md",
    "docs/FINAL_RESEARCH_REPORT.md",
    "docs/SPATIAL_CERTIFICATE_STUDY.md",
    "docs/WORKFLOW_DIFFERENTIATION_EVIDENCE.md",
    "challenge/README.md",
    "research/source_ledger.csv",
    "research/claims_ledger.csv",
    "research/README.md",
    "proposal/README.md",
    "proposal/FINAL_PROPOSAL.md",
    "proposal/CLAIM_AUDIT.md",
    "proposal/figures/figure1_workflow.png",
    "proposal/figures/figure2_synthetic_failure_comparison.png",
    "proposal/figures/figure3_coverage_time_model.png",
    "proposal/RED_TEAM_REVIEW.md",
    "prior_art/FINAL_PRIOR_ART_AUDIT.md",
    "prior_art/prior_art_matrix.csv",
    "submission_package/FINAL_PROPOSAL.md",
    "submission_package/HUMAN_FINAL_CHECKLIST.md",
    "submission_package/PACKAGE_README.md",
    "submission_package/FINAL_STATUS.md",
    "submission_package/SPATIAL_CERTIFICATE_STUDY.md",
    "figures/figure1_workflow.png",
    "figures/figure2_synthetic_failure_comparison.png",
    "figures/figure3_coverage_time_model.png",
    "notebooks/README.md",
    "src/rapid_proof_clean/__init__.py",
    "src/rapid_proof_clean/realistic.py",
    "src/rapid_proof_clean/advanced.py",
    "experiments/v2_config.json",
    "experiments/results/v2_results.json",
    "experiments/results/v2_benchmark.csv",
    "experiments/frame_optimization_config.json",
    "experiments/final_model_config.json",
    "experiments/adversarial_regressions.json",
    "experiments/small_support_benchmark.json",
    "experiments/small_support_benchmark.csv",
    "experiments/spatial_adversarial_results.json",
    "experiments/spatial_adversarial_results.csv",
    "experiments/results/frame_optimization_results.json",
    "experiments/results/frame_optimization_benchmark.csv",
    "scripts/run_v2_study.py",
    "scripts/run_frame_optimization.py",
    "scripts/run_final_research.py",
    "scripts/run_spatial_certificate_study.py",
    "src/rapid_proof_clean/sequential.py",
    "src/rapid_proof_clean/reference_integrity.py",
    "src/rapid_proof_clean/domain_shift.py",
    "src/rapid_proof_clean/spatial_certificate.py",
    "tests/test_final_research_artifacts.py",
    "tests/test_spatial_certificate.py",
    "tests/test_realistic.py",
    "tests/test_advanced.py",
    "tests/test_smoke.py",
    "scripts/bootstrap.ps1",
    "scripts/check_env.py",
    "scripts/verify_repo.py",
    "prompts/README.md",
    "artifacts/README.md",
    ".github/workflows/ci.yml",
)
LEDGER_HEADERS = {
    "research/source_ledger.csv": (
        "source_id,title,authors,year,source_type,url,doi,date_accessed,relevance,status,notes"
    ),
    "research/claims_ledger.csv": "claim_id,claim,source_ids,evidence_type,status,notes",
}
OBVIOUS_SECRET_NAMES = {
    ".env",
    "credentials.json",
    "secrets.json",
    "service-account.json",
    "id_rsa",
    "id_ed25519",
}
OBVIOUS_SECRET_SUFFIXES = (".pem", ".p12", ".pfx", ".key")
SKIP_DIRECTORIES = {".git", ".venv", ".uv-cache", "__pycache__", ".pytest_cache", ".ruff_cache"}


def git_ignores(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", path],
        cwd=PROJECT_ROOT,
        check=False,
    )
    return result.returncode == 0


def secret_files() -> list[str]:
    findings: list[str] = []
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRECTORIES for part in path.parts):
            continue
        name = path.name.lower()
        if name in OBVIOUS_SECRET_NAMES or name.endswith(OBVIOUS_SECRET_SUFFIXES):
            if name != ".env.example":
                findings.append(path.relative_to(PROJECT_ROOT).as_posix())
    return findings


def main() -> int:
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (PROJECT_ROOT / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    if not git_ignores("private_data/"):
        errors.append("private_data/ is not ignored by Git")
    if not git_ignores(".env"):
        errors.append(".env is not ignored by Git")

    for relative_path in secret_files():
        errors.append(f"obvious secret file present: {relative_path}")

    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    try:
        package = importlib.import_module("rapid_proof_clean")
    except Exception as exc:  # pragma: no cover - diagnostic path
        errors.append(f"package import failed: {exc}")
    else:
        if not getattr(package, "__version__", None):
            errors.append("package has no __version__")

    for relative_path, expected_header in LEDGER_HEADERS.items():
        path = PROJECT_ROOT / relative_path
        if path.is_file():
            first_line = path.read_text(encoding="utf-8-sig").splitlines()[0]
            if first_line != expected_header:
                errors.append(f"ledger header mismatch: {relative_path}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS")
    print(f"Checked {len(REQUIRED_FILES)} required files.")
    print("Checked Git ignore rules, package import, and ledger headers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
