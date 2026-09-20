from __future__ import annotations

import pytest

from rapid_proof_clean.coverage import (
    CoverageInputs,
    estimate_coverage,
    estimate_coverage_for_frame_budget,
)


def test_coverage_breakdown_is_auditable() -> None:
    result = estimate_coverage(
        CoverageInputs(
            name="unit",
            target_area_m2=1.0,
            fov_width_m=0.5,
            fov_height_m=0.5,
            area_overlap_fraction=0.2,
            inaccessible_fraction=0.1,
            measurement_states=2,
            orientations=2,
            frequencies=6,
            phases=4,
            frame_period_s=0.01,
            processing_per_view_s=0.1,
            reposition_per_view_s=0.2,
            setup_and_reference_s=10,
        )
    )
    assert result["effective_fov_m2"] == pytest.approx(0.2)
    assert result["accessible_area_m2"] == pytest.approx(0.9)
    assert result["views"] == 5
    assert result["frames_per_view"] == 96
    assert result["total_s"] == pytest.approx(16.3)


@pytest.mark.parametrize(
    "field,value", [("area_overlap_fraction", 1.0), ("inaccessible_fraction", -0.1)]
)
def test_invalid_fraction_rejected(field: str, value: float) -> None:
    values = {"area_overlap_fraction": 0.1, "inaccessible_fraction": 0.1}
    values[field] = value
    with pytest.raises(ValueError):
        estimate_coverage(
            CoverageInputs(name="bad", target_area_m2=1, fov_width_m=1, fov_height_m=1, **values)
        )


def test_sequential_frame_budget_accepts_percentile_value() -> None:
    inputs = CoverageInputs(
        name="adaptive",
        target_area_m2=1,
        fov_width_m=0.5,
        fov_height_m=0.5,
        area_overlap_fraction=0,
        inaccessible_fraction=0,
        frame_period_s=0.01,
        processing_per_view_s=0,
        reposition_per_view_s=0,
        setup_and_reference_s=0,
    )
    result = estimate_coverage_for_frame_budget(inputs, 17.5, budget_label="mean")
    assert result["views"] == 4
    assert result["frames_per_view"] == 17.5
    assert result["total_s"] == pytest.approx(0.7)
