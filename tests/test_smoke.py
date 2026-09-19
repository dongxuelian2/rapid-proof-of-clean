from pathlib import Path

import rapid_proof_clean


def test_package_imports() -> None:
    assert rapid_proof_clean.__version__ == "0.1.0"


def test_repository_scope_document_exists() -> None:
    repository_root = Path(__file__).resolve().parents[1]
    assert (repository_root / "PROJECT_SCOPE.md").is_file()
