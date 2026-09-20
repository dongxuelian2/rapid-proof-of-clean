"""Diversity-channel inference layered conservatively on retained v1."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN

from rapid_proof_clean.phase1 import combine_measurement_states


@dataclass(frozen=True)
class DiversityConfig:
    """Bounds for reference-relative, exposure-invariant signature shape."""

    reference_consistency_log: float = 0.045
    pass_bound_log: float = 0.040
    flag_bound_log: float = 0.095
    minimum_reference_consensus: int = 2


def collapse_signature(cube: np.ndarray, arm: str) -> np.ndarray:
    """Select independent observables; result ends in ``(feature,H,W)``."""

    if cube.shape[-5:-2] != (3, 2, 2):
        raise ValueError("cube must end in (3 wavelengths,2 angles,2 polarizations,H,W)")
    if arm == "angle":
        return cube[..., 1, :, :, :, :].mean(axis=-3)
    if arm == "polarization":
        return cube[..., 1, 1, :, :, :]
    if arm == "wavelength":
        return cube[..., :, 0, :, :, :].mean(axis=-3)
    if arm == "combined":
        leading = cube.shape[:-5]
        return cube.reshape(*leading, 12, *cube.shape[-2:])
    raise ValueError(f"unsupported arm: {arm}")


def select_signature_features(
    cube: np.ndarray, indices: tuple[int, ...] | list[int]
) -> np.ndarray:
    """Select flattened wavelength/angle/polarization states by index."""

    if cube.shape[-5:-2] != (3, 2, 2):
        raise ValueError("cube must end in (3 wavelengths,2 angles,2 polarizations,H,W)")
    if len(indices) < 2 or len(set(indices)) != len(indices):
        raise ValueError("at least two distinct feature indices are required")
    if min(indices) < 0 or max(indices) >= 12:
        raise ValueError("feature indices must be in [0, 11]")
    leading = cube.shape[:-5]
    flattened = cube.reshape(*leading, 12, *cube.shape[-2:])
    return flattened[..., list(indices), :, :]


def _reference_consensus(features: np.ndarray, cfg: DiversityConfig) -> tuple[np.ndarray, float]:
    count = len(features)
    log_features = np.log(np.maximum(features, 1e-9))
    distances = np.zeros((count, count))
    for left in range(count):
        for right in range(left):
            delta = log_features[left] - log_features[right]
            delta -= np.median(delta, axis=-3, keepdims=True)
            distance = float(np.median(np.max(np.abs(delta), axis=-3)))
            distances[left, right] = distances[right, left] = distance
    adjacency = distances <= cfg.reference_consistency_log
    medoid = int(np.argmax(adjacency.sum(axis=1)))
    selected = np.flatnonzero(adjacency[medoid])
    confidence = float(len(selected) / count)
    if len(selected) < cfg.minimum_reference_consensus:
        selected = np.array([], dtype=int)
    return selected, confidence


def infer_diversity(
    references: np.ndarray,
    sample: np.ndarray,
    arm: str,
    cfg: DiversityConfig | None = None,
) -> dict:
    """Bounded three-way inference from relative signature *shape*.

    The per-pixel median log ratio is removed, so this channel cannot merely
    repeat the v1 uniform-gain threshold.  It can only react to changes across
    wavelength, angle, or polarization states.
    """

    if cfg is None:
        cfg = DiversityConfig()
    reference_features = collapse_signature(references, arm)
    sample_features = collapse_signature(sample, arm)
    return _infer_features(reference_features, sample_features, cfg)


def infer_diversity_features(
    references: np.ndarray,
    sample: np.ndarray,
    indices: tuple[int, ...] | list[int],
    cfg: DiversityConfig | None = None,
) -> dict:
    """Infer from an explicit compact subset of the 12 raw diversity states."""

    if cfg is None:
        cfg = DiversityConfig()
    reference_features = select_signature_features(references, indices)
    sample_features = select_signature_features(sample, indices)
    return _infer_features(reference_features, sample_features, cfg)


def _infer_features(
    reference_features: np.ndarray,
    sample_features: np.ndarray,
    cfg: DiversityConfig,
) -> dict:
    if reference_features.ndim != 4 or sample_features.ndim != 3:
        raise ValueError("unexpected feature shapes")
    selected, confidence = _reference_consensus(reference_features, cfg)
    shape = sample_features.shape[-2:]
    if not len(selected):
        return {
            "status": np.full(shape, UNKNOWN, dtype=np.uint8),
            "score": np.full(shape, np.nan),
            "reference_confidence": confidence,
        }
    reference = np.median(reference_features[selected], axis=0)
    log_ratio = np.log(np.maximum(reference, 1e-9) / np.maximum(sample_features, 1e-9))
    centered = log_ratio - np.median(log_ratio, axis=0, keepdims=True)
    score = np.max(np.abs(centered), axis=0)
    status = np.full(shape, UNKNOWN, dtype=np.uint8)
    status[score <= cfg.pass_bound_log] = PASS
    status[score >= cfg.flag_bound_log] = FLAG
    return {"status": status, "score": score, "reference_confidence": confidence}


def fuse_v2(v1_status: np.ndarray, diversity_status: np.ndarray) -> np.ndarray:
    """Any positive optical evidence flags; PASS requires both channels."""

    return combine_measurement_states(v1_status, diversity_status)
