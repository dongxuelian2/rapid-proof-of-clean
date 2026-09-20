import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN

from rapid_proof_clean.sequential import retained_policies, run_policy
from rapid_proof_clean.spatial_certificate import candidate_certificates, spatial_outcome


def _map(value: int) -> np.ndarray:
    return np.full((32, 32), value, dtype=np.uint8)


def _complete_evidence() -> dict[str, np.ndarray]:
    clean = _map(PASS)
    return {key: clean.copy() for key in ("d2", "d4", "d12", "c2", "c3", "p3")}


def test_any_pixel_flag_prevents_pass() -> None:
    status = _map(PASS)
    status[7, 9] = FLAG
    result = spatial_outcome(
        status,
        np.ones_like(status, dtype=bool),
        candidate_certificates()["balanced"],
    )
    assert result["decision"] == "FLAG"


def test_invalid_local_certificate_stops_without_extra_frames() -> None:
    evidence = _complete_evidence()
    evidence["d12"][8:12, 8:12] = UNKNOWN
    evidence["c3"][8:12, 8:12] = UNKNOWN
    result = run_policy(
        retained_policies()["adaptive_standard"],
        evidence,
        np.ones((32, 32), dtype=bool),
        reference_valid=True,
        coverage_valid=True,
        spatial_certificate=candidate_certificates()["balanced"],
    )
    assert result["decision"] == "UNKNOWN"
    assert result["reason"] == "spatial_certificate_failed"
    assert result["frames"] == 36


def test_invalid_coverage_cannot_pass() -> None:
    result = run_policy(
        retained_policies()["adaptive_standard"],
        _complete_evidence(),
        np.ones((32, 32), dtype=bool),
        reference_valid=True,
        coverage_valid=False,
        spatial_certificate=candidate_certificates()["balanced"],
    )
    assert result["decision"] == "UNKNOWN"
    assert result["frames"] == 0


def test_nominal_homogeneous_clean_remains_pass() -> None:
    result = run_policy(
        retained_policies()["adaptive_standard"],
        _complete_evidence(),
        np.ones((32, 32), dtype=bool),
        reference_valid=True,
        coverage_valid=True,
        spatial_certificate=candidate_certificates()["balanced"],
    )
    assert result["decision"] == "PASS"
    assert result["frames"] == 36


def test_deterministic_and_evidence_preserving() -> None:
    status = _map(PASS)
    status[2:5, 3:6] = UNKNOWN
    original = status.copy()
    visible = np.ones_like(status, dtype=bool)
    certificate = candidate_certificates()["balanced"]
    first = spatial_outcome(status, visible, certificate)
    second = spatial_outcome(status, visible, certificate)
    assert first == second
    assert np.array_equal(status, original)
