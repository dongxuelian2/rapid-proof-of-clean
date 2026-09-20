import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN

from rapid_proof_clean.sequential import retained_policies, run_policy


def evidence(value: int) -> np.ndarray:
    return np.full((4, 4), value, dtype=np.uint8)


def test_pass_requires_complete_certificate() -> None:
    policy = retained_policies()["adaptive_standard"]
    result = run_policy(
        policy,
        {"d2": evidence(PASS), "d4": evidence(PASS), "d12": evidence(PASS)},
        np.ones((4, 4), dtype=bool),
        reference_valid=True,
        coverage_valid=True,
    )
    assert result["decision"] == "UNKNOWN"
    assert result["frames"] == 60


def test_invalid_reference_or_coverage_never_passes() -> None:
    policy = retained_policies()["fast_20"]
    complete = {"d4": evidence(PASS), "c2": evidence(PASS)}
    visible = np.ones((4, 4), dtype=bool)
    for reference_valid, coverage_valid in ((False, True), (True, False)):
        result = run_policy(
            policy,
            complete,
            visible,
            reference_valid=reference_valid,
            coverage_valid=coverage_valid,
        )
        assert result["decision"] == "UNKNOWN"
        assert result["frames"] == 0


def test_flag_stops_before_pass_certificate() -> None:
    policy = retained_policies()["adaptive_standard"]
    result = run_policy(
        policy,
        {"d2": evidence(FLAG)},
        np.ones((4, 4), dtype=bool),
        reference_valid=True,
        coverage_valid=True,
    )
    assert result["decision"] == "FLAG"
    assert result["frames"] == 2


def test_failed_required_state_becomes_unknown() -> None:
    policy = retained_policies()["fast_20"]
    result = run_policy(
        policy,
        {"d4": evidence(PASS), "c2": evidence(PASS)},
        np.ones((4, 4), dtype=bool),
        reference_valid=True,
        coverage_valid=True,
        failed_states=frozenset({"c2"}),
    )
    assert result["decision"] == "UNKNOWN"


def test_unknown_pixels_cannot_be_hidden_by_invisible_area() -> None:
    policy = retained_policies()["fast_20"]
    status = evidence(PASS)
    status[0, 0] = UNKNOWN
    result = run_policy(
        policy,
        {"d4": status, "c2": evidence(PASS)},
        np.ones((4, 4), dtype=bool),
        reference_valid=True,
        coverage_valid=True,
    )
    assert result["decision"] == "UNKNOWN"
