"""Check final proposal section word counts and placeholder state."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "proposal" / "FINAL_PROPOSAL.md"


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w’'-]+\b", text))


def main() -> int:
    text = PROPOSAL.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)[1:]
    failed = False
    total = 0
    for part in parts:
        heading, _, body = part.partition("\n")
        words = count_words(body)
        total += words
        print(f"{heading}: {words} words")
        if words > 500:
            failed = True
    print(f"Total substantive field words: {total}")
    print(f"Human placeholders present: {'[PARTICIPANT TO COMPLETE]' in text}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
