"""Reference qualification beyond majority self-consistency.

Self-consistency can reject an independent outlier but cannot identify a
consistent common-mode shift.  An optional dated anchor adds that information;
without it, common-mode cleanliness remains unidentifiable by construction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ReferenceIntegrityConfig:
    pairwise_bound_log: float = 0.045
    anchor_bound_log: float = 0.070
    minimum_consensus: int = 2
    maximum_leave_one_out_log: float = 0.060


def centered_log_shape(features: np.ndarray) -> np.ndarray:
    """Remove per-pixel common exposure while preserving feature shape."""

    logged = np.log(np.maximum(features, 1e-9))
    return logged - np.median(logged, axis=-3, keepdims=True)


def shape_distance(left: np.ndarray, right: np.ndarray) -> float:
    """Robust scalar distance between two feature images."""

    delta = centered_log_shape(left) - centered_log_shape(right)
    return float(np.median(np.max(np.abs(delta), axis=-3)))


def qualify_reference_features(
    references: np.ndarray,
    *,
    anchor: np.ndarray | None,
    config: ReferenceIntegrityConfig | None = None,
) -> dict:
    """Qualify a reference set using graph, leave-one-out and anchor checks.

    ``references`` has shape ``(reference, feature, height, width)``.  ``anchor``
    is a dated/certified feature image.  When it is absent the result explicitly
    reports that common-mode integrity was not established.
    """

    if config is None:
        config = ReferenceIntegrityConfig()
    if references.ndim != 4 or len(references) < 2:
        raise ValueError("references must have shape (R,F,H,W), R>=2")
    count = len(references)
    distances = np.zeros((count, count), dtype=float)
    for left in range(count):
        for right in range(left):
            distance = shape_distance(references[left], references[right])
            distances[left, right] = distances[right, left] = distance
    adjacency = distances <= config.pairwise_bound_log
    medoid = int(np.argmax(adjacency.sum(axis=1)))
    selected = np.flatnonzero(adjacency[medoid])
    pairwise_valid = len(selected) >= config.minimum_consensus

    loo_distances = []
    if pairwise_valid:
        for index in selected:
            others = selected[selected != index]
            if len(others):
                loo_distances.append(
                    shape_distance(references[index], np.median(references[others], axis=0))
                )
    leave_one_out_max = max(loo_distances, default=0.0)
    leave_one_out_valid = leave_one_out_max <= config.maximum_leave_one_out_log

    common_mode_identifiable = anchor is not None
    anchor_distance = None
    anchor_valid = False
    if anchor is not None and pairwise_valid:
        consensus = np.median(references[selected], axis=0)
        anchor_distance = shape_distance(consensus, anchor)
        anchor_valid = anchor_distance <= config.anchor_bound_log

    valid = pairwise_valid and leave_one_out_valid and anchor_valid
    if not pairwise_valid:
        reason = "insufficient_pairwise_consensus"
    elif not leave_one_out_valid:
        reason = "leave_one_out_instability"
    elif anchor is None:
        reason = "common_mode_unidentified_no_anchor"
    elif not anchor_valid:
        reason = "common_mode_anchor_drift"
    else:
        reason = "qualified"
    return {
        "valid": valid,
        "reason": reason,
        "selected": selected,
        "pairwise_confidence": float(len(selected) / count),
        "pairwise_distances": distances,
        "leave_one_out_max_log": float(leave_one_out_max),
        "anchor_distance_log": anchor_distance,
        "common_mode_identifiable": common_mode_identifiable,
    }
