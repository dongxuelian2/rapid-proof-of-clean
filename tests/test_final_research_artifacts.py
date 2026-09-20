import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_results() -> dict:
    return json.loads(
        (ROOT / "experiments" / "results" / "final_research_results.json").read_text(
            encoding="utf-8"
        )
    )


def test_selected_policy_beats_fixed_on_domain_shift_false_clean():
    result = load_results()
    summary = {row["policy"]: row for row in result["summary"]}
    assert result["selected_policy"]["name"] == "adaptive_standard"
    assert (
        summary["adaptive_standard"]["observable_dirty_false_clean_rate"]
        < summary["fixed_v2_1"]["observable_dirty_false_clean_rate"]
    )


def test_original_model_false_clean_is_not_worsened():
    rows = load_results()["in_model_regression"]["pixel_metrics"]
    dirty = {
        row["method"]: row
        for row in rows
        if row["group"] == "nonmatched"
    }
    assert dirty["adaptive_v2_2_certificate"]["pass_rate"] <= dirty["fixed_v2_1"]["pass_rate"]


def test_common_mode_reference_and_missing_anchor_never_pass():
    records = [
        row
        for row in load_results()["records"]
        if row["policy"] == "adaptive_standard"
        and row["scenario"] in ("common_mode_dirty_reference", "missing_historical_anchor")
    ]
    assert records
    assert all(row["decision"] == "UNKNOWN" for row in records)
