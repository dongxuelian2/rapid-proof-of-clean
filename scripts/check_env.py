"""Print the local tools and package versions used by this repository."""

from __future__ import annotations

import importlib.metadata
import platform
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAMES = (
    "matplotlib",
    "numpy",
    "pandas",
    "pydantic",
    "pytest",
    "rich",
    "ruff",
    "scipy",
)


def command_version(command: str) -> str:
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError:
        return "not found"

    output = (result.stdout or result.stderr).strip().splitlines()
    if result.returncode != 0:
        return f"unavailable (exit {result.returncode})"
    return output[0] if output else "available (no version text)"


def package_version(package_name: str) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


def virtualenv_status() -> str:
    expected = (PROJECT_ROOT / ".venv").resolve()
    current = Path(sys.prefix).resolve()
    if current == expected:
        return f"active ({expected})"
    if expected.is_dir():
        return f"present but not active ({expected})"
    return "missing"


def main() -> int:
    print(f"Python version: {platform.python_version()} ({sys.executable})")
    print(f"Platform: {platform.platform()}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Virtualenv status: {virtualenv_status()}")
    print("Important package versions:")
    for package_name in PACKAGE_NAMES:
        print(f"  {package_name}: {package_version(package_name)}")
    print(f"Git version: {command_version('git')}")
    print(f"gh version: {command_version('gh')}")
    print(f"uv version: {command_version('uv')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
