# ruff: noqa: E402
"""Run assumption-driven coverage and synthetic nuisance sweeps."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN
from proof_clean_local_plan.src.simulation import make_scene

from rapid_proof_clean.coverage import (
    CoverageInputs,
    estimate_coverage,
    estimate_coverage_for_frame_budget,
)
from rapid_proof_clean.phase1 import V1Config, combine_measurement_states, infer_reference_ensemble
from rapid_proof_clean.robustness import Nuisance, perturb_frames

RESULTS = ROOT / "experiments" / "results"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def controlled_config(cfg: dict, experiment_cfg: dict) -> dict:
    result = dict(cfg)
    result["clean_variation_bound_pixel2"] = experiment_cfg[
        "controlled_geometry_clean_variation_bound_pixel2"
    ]
    result["additive_noise_bound"] = experiment_cfg["controlled_geometry_additive_noise_bound"]
    result["quantization_levels"] = experiment_cfg["controlled_geometry_quantization_levels"]
    return result


def make_pool(first: np.ndarray, cfg: dict, rng: np.random.Generator, state: str) -> np.ndarray:
    extra = [make_scene(cfg, rng, "clean", measurement_state=state)[0] for _ in range(2)]
    return np.stack([first, *extra])


def status_for(
    kind: str, seed: int, nuisance: Nuisance, cfg: dict, controlled: dict, v1: V1Config
) -> np.ndarray:
    statuses = []
    for offset, (state, state_cfg) in enumerate(
        (("primary", cfg), ("controlled_geometry", controlled))
    ):
        rng = np.random.default_rng(seed + offset * 10_000)
        ref, sample, _, visible, _ = make_scene(state_cfg, rng, kind, measurement_state=state)
        refs = make_pool(ref, state_cfg, rng, state)
        if nuisance.missing_frequency:
            statuses.append(np.full(visible.shape, UNKNOWN, dtype=np.uint8))
            continue
        refs, sample = perturb_frames(refs, sample, state_cfg, nuisance, rng)
        statuses.append(
            infer_reference_ensemble(refs, sample, state_cfg, visible, v1, use_gain_guard=True)[
                "status"
            ]
        )
    return combine_measurement_states(*statuses)


def run_robustness(cfg: dict, experiment_cfg: dict) -> list[dict]:
    controlled = controlled_config(cfg, experiment_cfg)
    v1 = V1Config(
        experiment_cfg["reference_consistency_bound_pixel2"],
        experiment_cfg["minimum_reference_consensus"],
        experiment_cfg["gain_log_ratio_bound"],
    )
    nuisances = [
        Nuisance("nominal"),
        Nuisance("exposure_drift_low", exposure_scale=0.75),
        Nuisance("exposure_drift_high", exposure_scale=1.25),
        Nuisance("multiplicative_gain_0.65", exposure_scale=0.65),
        Nuisance("registration_1px", registration_shift_px=1),
        Nuisance("registration_3px", registration_shift_px=3),
        Nuisance("additive_noise_0.003", additive_noise=0.003),
        Nuisance("additive_noise_0.015", additive_noise=0.015),
        Nuisance("reference_aging_0.2", reference_aging=0.2),
        Nuisance("reference_aging_0.8", reference_aging=0.8),
        Nuisance("roughness_mismatch_0.2", roughness_mismatch=0.2),
        Nuisance("roughness_mismatch_-0.4", roughness_mismatch=-0.4),
        Nuisance("illumination_gradient_10pct", illumination_gradient=0.10),
        Nuisance("illumination_gradient_35pct", illumination_gradient=0.35),
        Nuisance("missing_frequency", missing_frequency=True),
    ]
    rows = []
    for nuisance in nuisances:
        for kind in ("clean", "strong"):
            accum = {"PASS": 0, "FLAG": 0, "UNKNOWN": 0, "pixels": 0}
            for replicate in range(4):
                status = status_for(kind, 7000 + replicate, nuisance, cfg, controlled, v1)
                accum["PASS"] += int(np.sum(status == PASS))
                accum["FLAG"] += int(np.sum(status == FLAG))
                accum["UNKNOWN"] += int(np.sum(status == UNKNOWN))
                accum["pixels"] += status.size
            expected_name = "PASS" if kind == "clean" else "FLAG"
            expected_rate = accum[expected_name] / accum["pixels"]
            outcome = (
                "PASS"
                if expected_rate >= 0.95
                else ("UNKNOWN" if accum["UNKNOWN"] / accum["pixels"] >= 0.05 else "FAIL")
            )
            rows.append(
                {
                    "nuisance": nuisance.name,
                    "ground_truth_proxy": kind,
                    "expected": expected_name,
                    "outcome": outcome,
                    "pass_rate": accum["PASS"] / accum["pixels"],
                    "flag_rate": accum["FLAG"] / accum["pixels"],
                    "unknown_rate": accum["UNKNOWN"] / accum["pixels"],
                    "evidence_type": "SYNTHETIC_ONLY",
                }
            )
    return rows


def coverage_scenarios() -> list[dict]:
    profiles = {
        "optimistic": dict(
            fov_width_m=0.50,
            fov_height_m=0.40,
            area_overlap_fraction=0.15,
            frame_period_s=1 / 60,
            processing_per_view_s=0.4,
            reposition_per_view_s=1.0,
            setup_and_reference_s=90,
        ),
        "conservative": dict(
            fov_width_m=0.30,
            fov_height_m=0.25,
            area_overlap_fraction=0.25,
            frame_period_s=1 / 30,
            processing_per_view_s=1.0,
            reposition_per_view_s=3.0,
            setup_and_reference_s=120,
        ),
        "stress": dict(
            fov_width_m=0.20,
            fov_height_m=0.15,
            area_overlap_fraction=0.35,
            frame_period_s=1 / 20,
            processing_per_view_s=2.0,
            reposition_per_view_s=6.0,
            setup_and_reference_s=180,
        ),
    }
    targets = [
        ("work_surface_1m2", 1.0, 0.05),
        ("high_touch_set_4m2", 4.0, 0.15),
        ("prep_zone_5m2", 5.0, 0.20),
        ("small_room_targets_12m2", 12.0, 0.25),
        ("large_room_targets_25m2", 25.0, 0.35),
    ]
    results = []
    for profile, assumptions in profiles.items():
        for target, area, inaccessible in targets:
            item = estimate_coverage(
                CoverageInputs(
                    name=f"{profile}:{target}",
                    target_area_m2=area,
                    inaccessible_fraction=inaccessible,
                    **assumptions,
                )
            )
            item["profile"] = profile
            item["target"] = target
            results.append(item)
    return results


def adaptive_coverage_scenarios() -> list[dict]:
    benchmark = read_json(RESULTS / "final_research_results.json")
    records = [
        row
        for row in benchmark["records"]
        if row["policy"] == "adaptive_standard"
        and row["group"] in ("clean", "contaminated", "nuisance")
        and row["reference_valid"]
    ]
    frames = np.asarray([row["frames"] for row in records], dtype=float)
    budgets = {
        "expected_valid_synthetic_mix": float(np.mean(frames)),
        "p95_valid_synthetic_mix": float(np.quantile(frames, 0.95)),
        "worst_case_diagnostic": 60.0,
        "clean_pass_certificate": 36.0,
    }
    profiles = {
        "optimistic": dict(
            fov_width_m=0.50,
            fov_height_m=0.40,
            area_overlap_fraction=0.15,
            frame_period_s=1 / 60,
            processing_per_view_s=0.4,
            reposition_per_view_s=1.0,
            setup_and_reference_s=90,
        ),
        "conservative": dict(
            fov_width_m=0.30,
            fov_height_m=0.25,
            area_overlap_fraction=0.25,
            frame_period_s=1 / 30,
            processing_per_view_s=1.0,
            reposition_per_view_s=3.0,
            setup_and_reference_s=120,
        ),
        "stress": dict(
            fov_width_m=0.20,
            fov_height_m=0.15,
            area_overlap_fraction=0.35,
            frame_period_s=1 / 20,
            processing_per_view_s=2.0,
            reposition_per_view_s=6.0,
            setup_and_reference_s=180,
        ),
    }
    targets = [("1m2", 1.0, 0.05), ("5m2", 5.0, 0.20), ("12m2", 12.0, 0.25), ("25m2", 25.0, 0.35)]
    results = []
    for profile, assumptions in profiles.items():
        for target, area, inaccessible in targets:
            inputs = CoverageInputs(
                name=f"{profile}:{target}",
                target_area_m2=area,
                inaccessible_fraction=inaccessible,
                **assumptions,
            )
            for label, frame_budget in budgets.items():
                item = estimate_coverage_for_frame_budget(
                    inputs, frame_budget, budget_label=label
                )
                item["profile"] = profile
                item["target"] = target
                results.append(item)
    return results


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    cfg = read_json(ROOT / "proof_clean_local_plan" / "config.json")
    experiment_cfg = read_json(ROOT / "experiments" / "v1_config.json")
    robustness = run_robustness(cfg, experiment_cfg)
    coverage = coverage_scenarios()
    adaptive_coverage = adaptive_coverage_scenarios()
    RESULTS.mkdir(parents=True, exist_ok=True)
    write_csv(RESULTS / "robustness_envelope.csv", robustness)
    write_csv(
        RESULTS / "coverage_time_model.csv",
        [{key: value for key, value in item.items() if key != "inputs"} for item in coverage],
    )
    write_csv(
        RESULTS / "adaptive_coverage_time_model.csv",
        [
            {key: value for key, value in item.items() if key != "inputs"}
            for item in adaptive_coverage
        ],
    )
    (RESULTS / "final_validation_results.json").write_text(
        json.dumps(
            {
                "evidence_type": "SYNTHETIC_AND_ASSUMPTION_DRIVEN_ONLY",
                "physical_experiment_executed": False,
                "robustness": robustness,
                "coverage": coverage,
                "adaptive_coverage": adaptive_coverage,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {len(robustness)} robustness rows, {len(coverage)} fixed coverage "
        f"scenarios and {len(adaptive_coverage)} adaptive scenarios"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
