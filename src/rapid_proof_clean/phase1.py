"""Phase-1 adversarial benchmark and v1 inference helpers.

All results are synthetic and model-conditional.  The retained v1 adds three
explicit assumptions: a majority-clean reference ensemble, bounded gain drift,
and a second acquisition with controlled geometry.  It does not create
observability for residue that affects neither retained optical state.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN, demodulate, infer


@dataclass(frozen=True)
class V1Config:
    """Configuration separated from the frozen v0 ``config.json``."""

    reference_consistency_bound_pixel2: float = 0.25
    minimum_reference_consensus: int = 2
    gain_log_ratio_bound: float = 0.36


def signed_slope_and_intercept(
    reference: np.ndarray, sample: np.ndarray, cfg: dict
) -> tuple[np.ndarray, np.ndarray]:
    """Return unconstrained signed slope/intercept for diagnostics.

    Arrays have shape ``(2, H, W)``.  These point estimates do not replace the
    bounded v0 inference; they are used only for reference clustering and the
    explicitly bounded gain-drift guard.
    """

    frequencies = np.asarray(cfg["frequencies_cycles_per_screen"], dtype=float)
    frequencies /= cfg["screen_coordinate_width"]
    x = 2 * np.pi**2 * frequencies**2
    centered = x - x.mean()
    mref = demodulate(reference)
    msam = demodulate(sample)
    tiny = np.finfo(float).tiny
    z = np.log(np.maximum(mref, tiny) / np.maximum(msam, tiny))
    slope = np.einsum("f,ofhw->ohw", centered, z) / np.sum(centered * centered)
    intercept = np.mean(z - x[None, :, None, None] * slope[:, None], axis=1)
    return slope, intercept


def reference_consensus(
    references: np.ndarray, cfg: dict, v1_cfg: V1Config
) -> tuple[np.ndarray, float, np.ndarray]:
    """Select the largest self-consistent reference neighborhood.

    The guarantee is conditional on at least ``minimum_reference_consensus``
    mutually consistent references and fewer corrupt references than the
    selected cluster.  With no majority-clean anchor, reference cleanliness is
    not identifiable from self-consistency alone.
    """

    if references.ndim != 6 or references.shape[1] != 2:
        raise ValueError("references must have shape (R,2,F,4,H,W)")
    count = len(references)
    distances = np.zeros((count, count), dtype=float)
    for left in range(count):
        for right in range(left):
            slope, _ = signed_slope_and_intercept(references[left], references[right], cfg)
            distance = float(np.median(np.max(np.abs(slope), axis=0)))
            distances[left, right] = distances[right, left] = distance
    adjacency = distances <= v1_cfg.reference_consistency_bound_pixel2
    degrees = adjacency.sum(axis=1)
    medoid = int(np.argmax(degrees))
    selected = np.flatnonzero(adjacency[medoid])
    confidence = float(len(selected) / count)
    if len(selected) < v1_cfg.minimum_reference_consensus:
        selected = np.array([], dtype=int)
    return selected, confidence, distances


def infer_reference_ensemble(
    references: np.ndarray,
    sample: np.ndarray,
    cfg: dict,
    visible: np.ndarray,
    v1_cfg: V1Config,
    *,
    use_gain_guard: bool,
) -> dict:
    """Run bounded inference against the consensus reference cluster."""

    selected, confidence, distances = reference_consensus(references, cfg, v1_cfg)
    shape = sample.shape[-2:]
    if not len(selected):
        return {
            "status": np.full(shape, UNKNOWN, dtype=np.uint8),
            "reference_confidence": confidence,
            "selected_references": selected,
            "reference_distances": distances,
        }

    statuses = []
    intercepts = []
    validities = []
    for index in selected:
        result = infer(references[index], sample, cfg, visible)
        statuses.append(result["status"])
        validities.append(result["valid"])
        _, intercept = signed_slope_and_intercept(references[index], sample, cfg)
        intercepts.append(intercept)
    stack = np.asarray(statuses)
    valid = np.logical_and.reduce(validities)
    majority = len(selected) // 2 + 1
    status = np.full(shape, UNKNOWN, dtype=np.uint8)
    status[valid & ((stack == PASS).sum(axis=0) == len(selected))] = PASS
    status[valid & ((stack == FLAG).sum(axis=0) >= majority)] = FLAG

    if use_gain_guard:
        median_intercept = np.median(np.asarray(intercepts), axis=(0, 1))
        gain_anomaly = valid & (np.abs(median_intercept) > v1_cfg.gain_log_ratio_bound)
        status[gain_anomaly] = FLAG

    return {
        "status": status,
        "reference_confidence": confidence,
        "selected_references": selected,
        "reference_distances": distances,
    }


def combine_measurement_states(primary: np.ndarray, secondary: np.ndarray) -> np.ndarray:
    """Conservative two-state decision: any FLAG wins; PASS requires both."""

    if primary.shape != secondary.shape:
        raise ValueError("measurement states must have matching shapes")
    status = np.full(primary.shape, UNKNOWN, dtype=np.uint8)
    status[(primary == PASS) & (secondary == PASS)] = PASS
    status[(primary == FLAG) | (secondary == FLAG)] = FLAG
    return status


def summarize_status(status: np.ndarray) -> dict[str, float | str | bool]:
    """Summarize a physically-positive failure case without hiding abstention."""

    total = status.size
    pass_rate = float(np.sum(status == PASS) / total)
    flag_rate = float(np.sum(status == FLAG) / total)
    unknown_rate = float(np.sum(status == UNKNOWN) / total)
    counts = {
        "PASS": int(np.sum(status == PASS)),
        "FLAG": int(np.sum(status == FLAG)),
        "UNKNOWN": int(np.sum(status == UNKNOWN)),
    }
    actual = max(counts, key=counts.get)
    return {
        "actual_behavior": actual,
        "false_clean_indicator": bool(pass_rate > 0),
        "false_clean_rate": pass_rate,
        "flag_rate": flag_rate,
        "unknown_rate": unknown_rate,
        "usable_coverage": 1.0 - unknown_rate,
    }


def timed(callable_):
    """Return ``(value, elapsed_seconds)`` for benchmark bookkeeping."""

    start = perf_counter()
    value = callable_()
    return value, perf_counter() - start
