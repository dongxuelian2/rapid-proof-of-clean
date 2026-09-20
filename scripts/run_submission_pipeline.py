"""Run the complete reproducible submission-artifact pipeline."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*command: str) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    run(sys.executable, "scripts/run_phase1.py")
    run(sys.executable, "scripts/run_final_research.py")
    run(sys.executable, "scripts/run_final_validation.py")
    run(sys.executable, "scripts/run_v2_study.py")
    run(sys.executable, "scripts/run_frame_optimization.py")
    run(sys.executable, "scripts/audit_proposal.py")
    run(sys.executable, "scripts/generate_proposal_figures.py")
    run(sys.executable, "scripts/build_submission_package.py")
    run(sys.executable, "scripts/verify_repo.py")
    run(sys.executable, "-m", "ruff", "check", ".")
    run(sys.executable, "-m", "pytest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
