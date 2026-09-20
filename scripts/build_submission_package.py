"""Build the curated, reviewer-facing submission package."""

from __future__ import annotations

import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "submission_package"

COPIES = {
    ROOT / "proposal" / "FINAL_PROPOSAL.md": PACKAGE / "FINAL_PROPOSAL.md",
    ROOT / "proposal" / "CLAIM_AUDIT.md": PACKAGE / "CLAIM_AUDIT.md",
    ROOT / "docs" / "FINAL_CHALLENGE_FIT.md": PACKAGE / "FINAL_CHALLENGE_FIT.md",
    ROOT / "docs" / "FINAL_STATUS.md": PACKAGE / "FINAL_STATUS.md",
    ROOT / "docs" / "SPATIAL_CERTIFICATE_STUDY.md": PACKAGE / "SPATIAL_CERTIFICATE_STUDY.md",
    ROOT / "prior_art" / "FINAL_PRIOR_ART_AUDIT.md": PACKAGE / "REFERENCES_AND_PRIOR_ART.md",
}


def copy_with_retry(source: Path, destination: Path) -> None:
    """Tolerate brief Windows scanner/indexer locks on generated package files."""

    for attempt in range(3):
        try:
            shutil.copyfile(source, destination)
            return
        except OSError:
            if attempt == 2:
                raise
            time.sleep(0.1 * (attempt + 1))


def main() -> int:
    PACKAGE.mkdir(parents=True, exist_ok=True)
    for source, destination in COPIES.items():
        copy_with_retry(source, destination)
    for source in sorted((ROOT / "figures").glob("figure*.*")):
        copy_with_retry(source, PACKAGE / source.name)
    print(f"Built curated package with {len(list(PACKAGE.iterdir()))} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
