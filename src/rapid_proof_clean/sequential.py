"""Sequential evidence acquisition with explicit clean certificates.

The controller is intentionally policy-agnostic.  A stage may stop early for a
FLAG, but PASS is available only when the stage names a complete certificate and
all reference/coverage predicates hold.  Missing evidence never defaults to PASS.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN

CONTINUE = "CONTINUE"


@dataclass(frozen=True)
class AcquisitionStage:
    """One cumulative point in a sequential policy."""

    name: str
    evidence_keys: tuple[str, ...]
    cumulative_frames: int
    pass_certificate: tuple[str, ...] = ()


@dataclass(frozen=True)
class SequentialPolicy:
    """Ordered stages and FOV aggregation rule."""

    name: str
    stages: tuple[AcquisitionStage, ...]
    minimum_pass_fraction: float = 0.95


def combine_evidence(statuses: list[np.ndarray]) -> np.ndarray:
    """Conservative conjunction: any FLAG wins and PASS requires every arm."""

    if not statuses:
        raise ValueError("at least one evidence status is required")
    shape = statuses[0].shape
    if any(status.shape != shape for status in statuses):
        raise ValueError("evidence maps must have matching shapes")
    stack = np.asarray(statuses)
    result = np.full(shape, UNKNOWN, dtype=np.uint8)
    result[np.any(stack == FLAG, axis=0)] = FLAG
    result[np.all(stack == PASS, axis=0)] = PASS
    return result


def fov_outcome(
    status: np.ndarray,
    visible: np.ndarray,
    *,
    minimum_pass_fraction: float,
) -> str:
    """Aggregate a pixel map without crediting invisible pixels as clean."""

    if status.shape != visible.shape:
        raise ValueError("status and visible mask must match")
    if not 0 < minimum_pass_fraction <= 1:
        raise ValueError("minimum_pass_fraction must be in (0, 1]")
    if not np.any(visible):
        return "UNKNOWN"
    values = status[visible]
    if np.any(values == FLAG):
        return "FLAG"
    if np.mean(values == PASS) >= minimum_pass_fraction:
        return "PASS"
    return "UNKNOWN"


def run_policy(
    policy: SequentialPolicy,
    evidence: dict[str, np.ndarray],
    visible: np.ndarray,
    *,
    reference_valid: bool,
    coverage_valid: bool,
    failed_states: frozenset[str] = frozenset(),
) -> dict:
    """Run a policy and return its auditable state trace.

    A global reference or coverage failure is terminal UNKNOWN because additional
    optical states cannot repair the missing clean anchor or inaccessible area.
    A failed measurement state remains CONTINUE while a later stage can add useful
    evidence, and becomes UNKNOWN if no complete certificate is obtained.
    """

    if not policy.stages:
        raise ValueError("policy must contain at least one stage")
    if not reference_valid or not coverage_valid:
        reason = "reference_integrity" if not reference_valid else "coverage"
        return {
            "decision": "UNKNOWN",
            "frames": 0,
            "reason": reason,
            "trace": [],
        }

    trace = []
    acquired: set[str] = set()
    for stage in policy.stages:
        acquired.update(stage.evidence_keys)
        available = [
            evidence[key]
            for key in stage.evidence_keys
            if key in evidence and key not in failed_states
        ]
        if available:
            combined = combine_evidence(available)
            outcome = fov_outcome(
                combined,
                visible,
                minimum_pass_fraction=policy.minimum_pass_fraction,
            )
        else:
            outcome = "UNKNOWN"
        trace.append(
            {
                "stage": stage.name,
                "frames": stage.cumulative_frames,
                "outcome": outcome,
                "available_evidence": len(available),
            }
        )
        if outcome == "FLAG":
            return {
                "decision": "FLAG",
                "frames": stage.cumulative_frames,
                "reason": "positive_contamination_evidence",
                "trace": trace,
            }
        certificate = stage.pass_certificate
        certificate_available = bool(certificate) and all(
            key in acquired and key in evidence and key not in failed_states
            for key in certificate
        )
        if certificate_available:
            certificate_status = combine_evidence([evidence[key] for key in certificate])
            certificate_outcome = fov_outcome(
                certificate_status,
                visible,
                minimum_pass_fraction=policy.minimum_pass_fraction,
            )
            if certificate_outcome == "PASS":
                return {
                    "decision": "PASS",
                    "frames": stage.cumulative_frames,
                    "reason": "complete_clean_certificate",
                    "trace": trace,
                }
            if certificate_outcome == "FLAG":
                return {
                    "decision": "FLAG",
                    "frames": stage.cumulative_frames,
                    "reason": "positive_contamination_evidence",
                    "trace": trace,
                }
    return {
        "decision": "UNKNOWN",
        "frames": policy.stages[-1].cumulative_frames,
        "reason": "insufficient_or_incompatible_evidence",
        "trace": trace,
    }


def retained_policies() -> dict[str, SequentialPolicy]:
    """Return fixed and adaptive candidates with explicit frame accounting."""

    return {
        "fixed_v2_1": SequentialPolicy(
            "fixed_v2_1",
            (
                AcquisitionStage("diversity_full", ("d12",), 12),
                AcquisitionStage("primary_endpoints", ("d12", "p2"), 28),
                AcquisitionStage(
                    "controlled_endpoints",
                    ("d12", "p2", "c2"),
                    44,
                    ("d12", "p2", "c2"),
                ),
            ),
        ),
        "fast_20": SequentialPolicy(
            "fast_20",
            (
                AcquisitionStage("diversity_corners", ("d4",), 4),
                AcquisitionStage(
                    "controlled_endpoints",
                    ("d4", "c2"),
                    20,
                    ("d4", "c2"),
                ),
            ),
        ),
        "adaptive_standard": SequentialPolicy(
            "adaptive_standard",
            (
                AcquisitionStage("polarization_probe", ("d2",), 2),
                AcquisitionStage("diversity_corners", ("d4",), 4),
                AcquisitionStage("diversity_full", ("d12",), 12),
                AcquisitionStage("controlled_endpoints", ("d12", "c2"), 28),
                AcquisitionStage(
                    "controlled_midband_check",
                    ("d12", "c3"),
                    36,
                    ("d12", "c3"),
                ),
                AcquisitionStage(
                    "primary_diagnostic",
                    ("d12", "c3", "p3"),
                    60,
                    ("d12", "c3", "p3"),
                ),
            ),
        ),
        "adaptive_risk_targeted": SequentialPolicy(
            "adaptive_risk_targeted",
            (
                AcquisitionStage("diversity_corners", ("d4",), 4),
                AcquisitionStage("controlled_three_frequency", ("d4", "c3"), 28),
                AcquisitionStage(
                    "diversity_full",
                    ("d12", "c3"),
                    36,
                    ("d12", "c3"),
                ),
                AcquisitionStage(
                    "primary_diagnostic",
                    ("d12", "c3", "p3"),
                    60,
                    ("d12", "c3", "p3"),
                ),
            ),
        ),
        "conservative_60": SequentialPolicy(
            "conservative_60",
            (
                AcquisitionStage(
                    "all_required_states",
                    ("d12", "c3", "p3"),
                    60,
                    ("d12", "c3", "p3"),
                ),
            ),
        ),
    }
