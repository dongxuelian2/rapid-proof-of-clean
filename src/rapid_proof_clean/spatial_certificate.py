"""Spatial release certificates layered on immutable pixel evidence.

The functions in this module never alter optical evidence.  They only decide
whether a PASS/UNKNOWN/FLAG pixel map is strong enough to release an entire FOV.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS
from scipy import ndimage


@dataclass(frozen=True)
class SpatialCertificate:
    """Local anomaly limits required in addition to the global PASS fraction."""

    name: str
    minimum_pass_fraction: float = 0.95
    tile_size: int | None = None
    tile_max_nonpass_fraction: float | None = None
    window_rules: tuple[tuple[int, float], ...] = ()
    maximum_component_area: int | None = None
    maximum_component_span: int | None = None
    edge_width: int | None = None
    edge_max_nonpass_fraction: float | None = None
    minimum_window_visible_fraction: float = 0.75


def _window_max_fraction(
    anomaly: np.ndarray,
    visible: np.ndarray,
    size: int,
    minimum_visible_fraction: float,
) -> float:
    kernel = np.ones((size, size), dtype=np.int32)
    anomaly_count = ndimage.convolve(anomaly.astype(np.int32), kernel, mode="constant")
    visible_count = ndimage.convolve(visible.astype(np.int32), kernel, mode="constant")
    valid = visible_count >= size * size * minimum_visible_fraction
    if not np.any(valid):
        return 0.0
    return float(np.max(anomaly_count[valid] / visible_count[valid]))


def _tile_max_fraction(
    anomaly: np.ndarray,
    visible: np.ndarray,
    size: int,
    minimum_visible_fraction: float,
) -> float:
    height, width = anomaly.shape
    maximum = 0.0
    for top in range(0, height, size):
        for left in range(0, width, size):
            tile_visible = visible[top : top + size, left : left + size]
            required = tile_visible.size * minimum_visible_fraction
            count = int(tile_visible.sum())
            if count < required:
                continue
            tile_anomaly = anomaly[top : top + size, left : left + size]
            maximum = max(maximum, float(tile_anomaly[tile_visible].mean()))
    return maximum


def _component_metrics(anomaly: np.ndarray) -> tuple[int, int, int]:
    labels, count = ndimage.label(anomaly, structure=np.ones((3, 3), dtype=np.uint8))
    if count == 0:
        return 0, 0, 0
    areas = np.bincount(labels.ravel())[1:]
    maximum_area = int(areas.max())
    maximum_span = 0
    for bounds in ndimage.find_objects(labels):
        if bounds is None:
            continue
        maximum_span = max(
            maximum_span,
            bounds[0].stop - bounds[0].start,
            bounds[1].stop - bounds[1].start,
        )
    return maximum_area, maximum_span, count


def spatial_outcome(
    status: np.ndarray,
    visible: np.ndarray,
    certificate: SpatialCertificate,
) -> dict:
    """Return an auditable FOV decision from an unchanged status map."""

    if status.shape != visible.shape or status.ndim != 2:
        raise ValueError("status and visible must be matching 2-D arrays")
    if not np.any(visible):
        return {"decision": "UNKNOWN", "reason": "no_visible_pixels", "metrics": {}}
    values = status[visible]
    if np.any(values == FLAG):
        return {"decision": "FLAG", "reason": "pixel_flag", "metrics": {}}

    pass_fraction = float(np.mean(values == PASS))
    anomaly = visible & (status != PASS)
    max_area, max_span, component_count = _component_metrics(anomaly)
    metrics: dict[str, float | int] = {
        "pass_fraction": pass_fraction,
        "nonpass_pixels": int(anomaly.sum()),
        "maximum_component_area": max_area,
        "maximum_component_span": max_span,
        "component_count": component_count,
    }
    if pass_fraction < certificate.minimum_pass_fraction:
        return {"decision": "UNKNOWN", "reason": "global_pass_fraction", "metrics": metrics}

    if certificate.tile_size is not None:
        tile_fraction = _tile_max_fraction(
            anomaly,
            visible,
            certificate.tile_size,
            certificate.minimum_window_visible_fraction,
        )
        metrics["maximum_tile_nonpass_fraction"] = tile_fraction
        if tile_fraction > float(certificate.tile_max_nonpass_fraction):
            return {"decision": "UNKNOWN", "reason": "tile_density", "metrics": metrics}

    for size, limit in certificate.window_rules:
        fraction = _window_max_fraction(
            anomaly,
            visible,
            size,
            certificate.minimum_window_visible_fraction,
        )
        metrics[f"maximum_window_{size}_nonpass_fraction"] = fraction
        if fraction > limit:
            return {
                "decision": "UNKNOWN",
                "reason": f"window_{size}_density",
                "metrics": metrics,
            }

    if certificate.maximum_component_area is not None:
        if max_area > certificate.maximum_component_area:
            return {"decision": "UNKNOWN", "reason": "component_area", "metrics": metrics}
    if certificate.maximum_component_span is not None:
        if max_span > certificate.maximum_component_span:
            return {"decision": "UNKNOWN", "reason": "component_span", "metrics": metrics}

    if certificate.edge_width is not None:
        width = certificate.edge_width
        edge = np.zeros_like(visible)
        edge[:width] = True
        edge[-width:] = True
        edge[:, :width] = True
        edge[:, -width:] = True
        edge_visible = edge & visible
        edge_fraction = float(np.mean(anomaly[edge_visible])) if np.any(edge_visible) else 0.0
        metrics["edge_nonpass_fraction"] = edge_fraction
        if edge_fraction > float(certificate.edge_max_nonpass_fraction):
            return {"decision": "UNKNOWN", "reason": "edge_density", "metrics": metrics}

    return {"decision": "PASS", "reason": "spatial_certificate", "metrics": metrics}


def candidate_certificates() -> dict[str, SpatialCertificate]:
    """Frozen candidate family; selection is performed outside held-out data."""

    return {
        "global_baseline": SpatialCertificate("global_baseline"),
        "tile": SpatialCertificate("tile", tile_size=8, tile_max_nonpass_fraction=0.12),
        "multiscale": SpatialCertificate(
            "multiscale", window_rules=((4, 0.25), (8, 0.12), (16, 0.07))
        ),
        "connected_component": SpatialCertificate(
            "connected_component", maximum_component_area=6, maximum_component_span=10
        ),
        "max_local_density": SpatialCertificate(
            "max_local_density", window_rules=((4, 0.19), (8, 0.10))
        ),
        "edge_aware": SpatialCertificate(
            "edge_aware", edge_width=4, edge_max_nonpass_fraction=0.08
        ),
        "aggressive": SpatialCertificate(
            "aggressive",
            tile_size=8,
            tile_max_nonpass_fraction=0.08,
            window_rules=((4, 0.12), (8, 0.08), (16, 0.05)),
            maximum_component_area=3,
            maximum_component_span=5,
            edge_width=4,
            edge_max_nonpass_fraction=0.04,
        ),
        "balanced": SpatialCertificate(
            "balanced",
            tile_size=8,
            tile_max_nonpass_fraction=0.24,
            window_rules=((4, 0.80), (8, 0.24), (16, 0.08)),
            maximum_component_area=15,
            maximum_component_span=20,
            edge_width=4,
            edge_max_nonpass_fraction=0.10,
            minimum_window_visible_fraction=1.0,
        ),
        "conservative": SpatialCertificate(
            "conservative",
            tile_size=8,
            tile_max_nonpass_fraction=0.35,
            window_rules=((4, 0.90), (8, 0.35), (16, 0.12)),
            maximum_component_area=24,
            maximum_component_span=28,
            edge_width=4,
            edge_max_nonpass_fraction=0.14,
            minimum_window_visible_fraction=1.0,
        ),
    }
