"""Assumption-driven coverage and acquisition-time model.

The model is deliberately simple and auditable.  It predicts workflow time from
declared inputs; it is not a measurement of the current prototype.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil


@dataclass(frozen=True)
class CoverageInputs:
    name: str
    target_area_m2: float
    fov_width_m: float
    fov_height_m: float
    area_overlap_fraction: float
    inaccessible_fraction: float
    measurement_states: int = 2
    orientations: int = 2
    frequencies: int = 6
    phases: int = 4
    frame_period_s: float = 1 / 30
    processing_per_view_s: float = 1.0
    reposition_per_view_s: float = 3.0
    setup_and_reference_s: float = 120.0

    def validate(self) -> None:
        positive = (
            "target_area_m2",
            "fov_width_m",
            "fov_height_m",
            "measurement_states",
            "orientations",
            "frequencies",
            "phases",
            "frame_period_s",
        )
        if any(getattr(self, field) <= 0 for field in positive):
            raise ValueError("area, field of view, frame count, and frame period must be positive")
        if not 0 <= self.area_overlap_fraction < 1:
            raise ValueError("area_overlap_fraction must be in [0, 1)")
        if not 0 <= self.inaccessible_fraction < 1:
            raise ValueError("inaccessible_fraction must be in [0, 1)")
        if (
            min(self.processing_per_view_s, self.reposition_per_view_s, self.setup_and_reference_s)
            < 0
        ):
            raise ValueError("time overheads cannot be negative")


def estimate_coverage(inputs: CoverageInputs) -> dict[str, float | int | str | dict]:
    """Return the deterministic time/coverage breakdown for one scenario."""

    inputs.validate()
    raw_fov_m2 = inputs.fov_width_m * inputs.fov_height_m
    effective_fov_m2 = raw_fov_m2 * (1 - inputs.area_overlap_fraction)
    accessible_area_m2 = inputs.target_area_m2 * (1 - inputs.inaccessible_fraction)
    views = ceil(accessible_area_m2 / effective_fov_m2)
    frames_per_view = (
        inputs.measurement_states * inputs.orientations * inputs.frequencies * inputs.phases
    )
    capture_per_view_s = frames_per_view * inputs.frame_period_s
    per_view_s = capture_per_view_s + inputs.processing_per_view_s + inputs.reposition_per_view_s
    total_s = inputs.setup_and_reference_s + views * per_view_s
    return {
        "name": inputs.name,
        "assumption_status": "UNVALIDATED_MODEL_INPUTS",
        "inputs": asdict(inputs),
        "raw_fov_m2": raw_fov_m2,
        "effective_fov_m2": effective_fov_m2,
        "accessible_area_m2": accessible_area_m2,
        "coverage_fraction": 1 - inputs.inaccessible_fraction,
        "views": views,
        "frames_per_view": frames_per_view,
        "capture_per_view_s": capture_per_view_s,
        "per_view_s": per_view_s,
        "total_s": total_s,
        "total_minutes": total_s / 60,
        "within_30_minutes": total_s <= 30 * 60,
    }


def estimate_coverage_for_frame_budget(
    inputs: CoverageInputs,
    frames_per_view: float,
    *,
    budget_label: str,
) -> dict[str, float | int | str | dict]:
    """Evaluate a measured/modeled sequential frame statistic.

    ``frames_per_view`` may be a mean or percentile and is deliberately separate
    from the integer fixed-grid acquisition fields in :class:`CoverageInputs`.
    All other timing assumptions remain unchanged and unvalidated.
    """

    inputs.validate()
    if frames_per_view <= 0:
        raise ValueError("frames_per_view must be positive")
    raw_fov_m2 = inputs.fov_width_m * inputs.fov_height_m
    effective_fov_m2 = raw_fov_m2 * (1 - inputs.area_overlap_fraction)
    accessible_area_m2 = inputs.target_area_m2 * (1 - inputs.inaccessible_fraction)
    views = ceil(accessible_area_m2 / effective_fov_m2)
    capture_per_view_s = frames_per_view * inputs.frame_period_s
    per_view_s = capture_per_view_s + inputs.processing_per_view_s + inputs.reposition_per_view_s
    total_s = inputs.setup_and_reference_s + views * per_view_s
    return {
        "name": inputs.name,
        "budget_label": budget_label,
        "assumption_status": "SIMULATED_FRAME_DISTRIBUTION_AND_UNVALIDATED_TIMING_INPUTS",
        "inputs": asdict(inputs),
        "raw_fov_m2": raw_fov_m2,
        "effective_fov_m2": effective_fov_m2,
        "accessible_area_m2": accessible_area_m2,
        "coverage_fraction": 1 - inputs.inaccessible_fraction,
        "views": views,
        "frames_per_view": float(frames_per_view),
        "capture_per_view_s": capture_per_view_s,
        "per_view_s": per_view_s,
        "total_s": total_s,
        "total_minutes": total_s / 60,
        "within_30_minutes": total_s <= 30 * 60,
    }
