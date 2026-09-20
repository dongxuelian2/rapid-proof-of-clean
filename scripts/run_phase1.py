# ruff: noqa: E402, E501
"""Reproduce the frozen v0 regression, Phase-1 candidates, and retained v1.

This script writes deterministic synthetic results only.  It does not alter
``proof_clean_local_plan/reference_run`` and performs no physical experiment.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN, infer
from proof_clean_local_plan.src.simulation import CONDITIONS, make_scene

from rapid_proof_clean.phase1 import (
    V1Config,
    combine_measurement_states,
    infer_reference_ensemble,
    summarize_status,
    timed,
)

PLAN = ROOT / "proof_clean_local_plan"
EXPERIMENTS = ROOT / "experiments"
RESULTS = EXPERIMENTS / "results"
FAILURES = (
    "dirty_reference",
    "uniform_absorber",
    "optically_invisible_residue",
    "negative_blur_cancellation",
)
METHODS = (
    "v0_single_reference",
    "E1_gain_guard",
    "E2_reference_consensus",
    "E3_controlled_geometry",
    "E4_secondary_optical_hypothesis",
    "v1_retained",
)
OBSERVATIONS = {
    "v0_single_reference": "primary state; one reference; 48 reference + 48 sample frames",
    "E1_gain_guard": "primary state; one reference; bounded absolute gain ratio",
    "E2_reference_consensus": "primary state; three references; majority self-consistency",
    "E3_controlled_geometry": "primary plus registered high-SNR geometry state; one reference each",
    "E4_secondary_optical_hypothesis": "primary plus hypothetical residue-sensitive optical state",
    "v1_retained": "three-reference consensus and gain guard in primary + registered high-SNR state",
}
NOTES = {
    "dirty_reference": "Relative comparison is unidentifiable when reference and sample share the change; consensus adds an external majority-clean anchor assumption.",
    "uniform_absorber": "Frequency-independent attenuation is confounded with acquisition gain; the guard helps only under a calibrated gain-drift bound.",
    "optically_invisible_residue": "Primary and retained secondary measurements are identical to clean by construction; only E4 injects an unvalidated new contrast.",
    "negative_blur_cancellation": "A single relative slope observes b+q, so b=-q cancels; registered geometry narrows the allowed b interval.",
}
GROUND_TRUTH = {
    "dirty_reference": "sample q=1.2 and reference q=1.2; contaminated by construction",
    "uniform_absorber": "frequency-independent 0.65 modulation attenuation; contaminated by construction",
    "optically_invisible_residue": "no retained-channel optical effect; contaminated by construction",
    "negative_blur_cancellation": "sample q=0.6 and geometry b=-0.6 in the primary state",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def controlled_config(cfg: dict, experiment_cfg: dict) -> dict:
    result = dict(cfg)
    result["clean_variation_bound_pixel2"] = experiment_cfg[
        "controlled_geometry_clean_variation_bound_pixel2"
    ]
    result["additive_noise_bound"] = experiment_cfg["controlled_geometry_additive_noise_bound"]
    result["quantization_levels"] = experiment_cfg["controlled_geometry_quantization_levels"]
    return result


def clean_reference(cfg: dict, rng: np.random.Generator, state: str) -> np.ndarray:
    return make_scene(cfg, rng, "clean", measurement_state=state)[0]


def pool(first: np.ndarray, cfg: dict, rng: np.random.Generator, state: str) -> np.ndarray:
    return np.stack([first, clean_reference(cfg, rng, state), clean_reference(cfg, rng, state)])


def ensemble_status(
    references: np.ndarray,
    sample: np.ndarray,
    cfg: dict,
    visible: np.ndarray,
    v1_cfg: V1Config,
    gain_guard: bool,
) -> np.ndarray:
    return infer_reference_ensemble(
        references, sample, cfg, visible, v1_cfg, use_gain_guard=gain_guard
    )["status"]


def candidate_statuses(
    cfg: dict, cfg_controlled: dict, v1_cfg: V1Config, kind: str, seed: int
) -> dict[str, tuple[np.ndarray, float]]:
    rng = np.random.default_rng(seed)
    primary = make_scene(cfg, rng, kind, measurement_state="primary")
    primary_pool = pool(primary[0], cfg, rng, "primary")

    controlled_rng = np.random.default_rng(seed + 10_000)
    controlled = make_scene(
        cfg_controlled,
        controlled_rng,
        kind,
        measurement_state="controlled_geometry",
    )
    controlled_pool = pool(controlled[0], cfg_controlled, controlled_rng, "controlled_geometry")

    optical_rng = np.random.default_rng(seed + 20_000)
    optical = make_scene(cfg, optical_rng, kind, measurement_state="secondary_optical")

    single_cfg = replace(v1_cfg, minimum_reference_consensus=1)
    output: dict[str, tuple[np.ndarray, float]] = {}
    output["v0_single_reference"] = timed(
        lambda: infer(primary[0], primary[1], cfg, primary[3])["status"]
    )
    output["E1_gain_guard"] = timed(
        lambda: ensemble_status(primary_pool[:1], primary[1], cfg, primary[3], single_cfg, True)
    )
    output["E2_reference_consensus"] = timed(
        lambda: ensemble_status(primary_pool, primary[1], cfg, primary[3], v1_cfg, False)
    )

    def geometry_candidate() -> np.ndarray:
        first = infer(primary[0], primary[1], cfg, primary[3])["status"]
        second = infer(controlled[0], controlled[1], cfg_controlled, controlled[3])["status"]
        return combine_measurement_states(first, second)

    output["E3_controlled_geometry"] = timed(geometry_candidate)

    def optical_candidate() -> np.ndarray:
        first = infer(primary[0], primary[1], cfg, primary[3])["status"]
        second = infer(optical[0], optical[1], cfg, optical[3])["status"]
        return combine_measurement_states(first, second)

    output["E4_secondary_optical_hypothesis"] = timed(optical_candidate)

    def retained() -> np.ndarray:
        first = ensemble_status(primary_pool, primary[1], cfg, primary[3], v1_cfg, True)
        second = ensemble_status(
            controlled_pool,
            controlled[1],
            cfg_controlled,
            controlled[3],
            v1_cfg,
            True,
        )
        return combine_measurement_states(first, second)

    output["v1_retained"] = timed(retained)
    return output


def run_failure_registry(
    cfg: dict, cfg_controlled: dict, experiment_cfg: dict, v1_cfg: V1Config
) -> list[dict]:
    rows: list[dict] = []
    count = int(experiment_cfg["failure_scenes_per_class"])
    for failure_index, kind in enumerate(FAILURES):
        for replicate in range(count):
            seed = int(experiment_cfg["fixed_seed"]) + failure_index * 100 + replicate
            for method, (status, _runtime) in candidate_statuses(
                cfg, cfg_controlled, v1_cfg, kind, seed
            ).items():
                row = {
                    "case_id": f"{kind}-{replicate:02d}-{method}",
                    "failure_mode_class": kind,
                    "synthetic_ground_truth": GROUND_TRUTH[kind],
                    "observation_configuration": OBSERVATIONS[method],
                    "expected_behavior": "FLAG",
                    **summarize_status(status),
                    # Wall-clock microbenchmarks are machine/load dependent and
                    # made an otherwise fixed-seed artifact non-reproducible.
                    # Keep the schema while declining to present them as evidence.
                    "runtime_seconds": None,
                    "nuisance_seed": seed,
                    "nuisance_parameters": (
                        "scene gain U(0.85,1.15); random phase; declared bounded noise; "
                        "failure-specific reference/gain/geometry state"
                    ),
                    "notes": NOTES[kind],
                }
                rows.append(row)
    path = EXPERIMENTS / "failure_mode_registry.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def aggregate_registry(rows: list[dict]) -> list[dict]:
    aggregates = []
    for method in METHODS:
        for kind in (*FAILURES, "ALL_FAILURES"):
            selected = [
                row
                for row in rows
                if method in row["case_id"]
                and (kind == "ALL_FAILURES" or row["failure_mode_class"] == kind)
            ]
            aggregates.append(
                {
                    "method": method,
                    "failure_mode": kind,
                    "scene_count": len(selected),
                    "false_clean_rate": float(
                        np.mean([row["false_clean_rate"] for row in selected])
                    ),
                    "flag_rate": float(np.mean([row["flag_rate"] for row in selected])),
                    "unknown_rate": float(np.mean([row["unknown_rate"] for row in selected])),
                    "usable_coverage": float(np.mean([row["usable_coverage"] for row in selected])),
                    "mean_runtime_seconds": None,
                }
            )
    return aggregates


def run_v1_standard_benchmark(cfg: dict, cfg_controlled: dict, v1_cfg: V1Config) -> dict:
    counts = {
        "pixels": 0,
        "proxy_positive_pixels": 0,
        "exact_zero_proxy_pixels": 0,
        "proxy_positive_called_pass": 0,
        "proxy_positive_flagged": 0,
        "exact_zero_proxy_called_pass": 0,
        "unknown_pixels": 0,
    }
    start_seed = int(cfg["seed"]) + 404
    scene_number = 0
    for kind in CONDITIONS:
        for _ in range(int(cfg["scenes_per_condition"])):
            seed = start_seed + scene_number
            scene_number += 1
            rng = np.random.default_rng(seed)
            primary = make_scene(cfg, rng, kind, measurement_state="primary")
            primary_pool = pool(primary[0], cfg, rng, "primary")
            rng2 = np.random.default_rng(seed + 10_000)
            secondary = make_scene(
                cfg_controlled,
                rng2,
                kind,
                measurement_state="controlled_geometry",
            )
            secondary_pool = pool(secondary[0], cfg_controlled, rng2, "controlled_geometry")
            first = ensemble_status(primary_pool, primary[1], cfg, primary[3], v1_cfg, True)
            second = ensemble_status(
                secondary_pool,
                secondary[1],
                cfg_controlled,
                secondary[3],
                v1_cfg,
                True,
            )
            status = combine_measurement_states(first, second)
            q = primary[2]
            positive = q.max(axis=0) >= cfg["proxy_threshold_pixel2"]
            zero = (q == 0).all(axis=0)
            counts["pixels"] += status.size
            counts["proxy_positive_pixels"] += int(positive.sum())
            counts["exact_zero_proxy_pixels"] += int(zero.sum())
            counts["proxy_positive_called_pass"] += int(((status == PASS) & positive).sum())
            counts["proxy_positive_flagged"] += int(((status == FLAG) & positive).sum())
            counts["exact_zero_proxy_called_pass"] += int(((status == PASS) & zero).sum())
            counts["unknown_pixels"] += int((status == UNKNOWN).sum())
    return {
        **counts,
        "false_clean_rate": counts["proxy_positive_called_pass"] / counts["proxy_positive_pixels"],
        "zero_proxy_pass_rate": counts["exact_zero_proxy_called_pass"]
        / counts["exact_zero_proxy_pixels"],
        "unknown_rate": counts["unknown_pixels"] / counts["pixels"],
        "proxy_positive_flag_rate": counts["proxy_positive_flagged"]
        / counts["proxy_positive_pixels"],
        "scene_count": scene_number,
        "evidence_type": "SYNTHETIC_ONLY",
    }


def frozen_baseline_regression() -> tuple[dict, str]:
    process = subprocess.run(
        [sys.executable, "run_pipeline.py", "all"],
        cwd=PLAN,
        check=True,
        capture_output=True,
        text=True,
    )
    reference = read_json(PLAN / "reference_run" / "summary.json")
    current = read_json(PLAN / "outputs" / "summary.json")
    reference_tests = read_json(PLAN / "reference_run" / "test_results.json")
    current_tests = read_json(PLAN / "outputs" / "test_results.json")
    result = {
        "frozen_head": "933c82d51b9de0b5ee8609d3bcf05772348cd8a5",
        "tag": "v0-baseline",
        "metrics_equal": reference["metrics"] == current["metrics"],
        "stress_equal": reference["stress"] == current["stress"],
        "original_tests_equal": reference_tests == current_tests,
        "original_tests": current_tests,
    }
    if not all(result[key] for key in ("metrics_equal", "stress_equal", "original_tests_equal")):
        raise RuntimeError("Frozen v0 regression differs from reference_run")
    stable_stdout = re.sub(
        r"Ran (\d+) tests in [0-9.]+s",
        r"Ran \1 tests in <elapsed-not-recorded>",
        process.stdout,
    )
    return result, stable_stdout


def comparison_markdown(results: dict) -> str:
    aggregate = results["failure_aggregate"]

    def lookup(method: str, failure: str) -> dict:
        return next(
            item
            for item in aggregate
            if item["method"] == method and item["failure_mode"] == failure
        )

    lines = [
        "# Phase 1 synthetic benchmark comparison",
        "",
        "**Evidence type: SYNTHETIC_ONLY. Rates below are descriptive pixel fractions from fixed-seed synthetic scenes, not independent physical trials.**",
        "",
        "| Failure mode | v0 false clean | v1 false clean | v1 UNKNOWN | v1 FLAG |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for failure in FAILURES:
        v0 = lookup("v0_single_reference", failure)
        v1 = lookup("v1_retained", failure)
        lines.append(
            f"| {failure} | {v0['false_clean_rate']:.2%} | {v1['false_clean_rate']:.2%} | "
            f"{v1['unknown_rate']:.2%} | {v1['flag_rate']:.2%} |"
        )
    v0_all = lookup("v0_single_reference", "ALL_FAILURES")
    v1_all = lookup("v1_retained", "ALL_FAILURES")
    lines += [
        f"| **ALL** | **{v0_all['false_clean_rate']:.2%}** | **{v1_all['false_clean_rate']:.2%}** | **{v1_all['unknown_rate']:.2%}** | **{v1_all['flag_rate']:.2%}** |",
        "",
        "The retained v1 does not use the hypothetical secondary-optical result. That candidate is kept as a sensitivity result only because no physical evidence supports its assumed contrast.",
        "",
        "## Standard synthetic regression",
        "",
        "| Metric | frozen v0 | retained v1 |",
        "| --- | ---: | ---: |",
    ]
    v0_metric = results["v0_bounded_interval"]
    v1_metric = results["v1_standard_benchmark"]
    lines += [
        f"| Proxy-positive false clean | {v0_metric['false_pass_fraction']:.4%} | {v1_metric['false_clean_rate']:.4%} |",
        f"| Zero-proxy PASS | {v0_metric['zero_proxy_pass_fraction']:.2%} | {v1_metric['zero_proxy_pass_rate']:.2%} |",
        f"| UNKNOWN | {v0_metric['unknown_fraction']:.2%} | {v1_metric['unknown_rate']:.2%} |",
        f"| Proxy-positive FLAG | {v0_metric['proxy_positive_flag_fraction']:.2%} | {v1_metric['proxy_positive_flag_rate']:.2%} |",
    ]
    return "\n".join(lines)


def main() -> int:
    cfg = read_json(PLAN / "config.json")
    experiment_cfg = read_json(EXPERIMENTS / "v1_config.json")
    v1_cfg = V1Config(
        reference_consistency_bound_pixel2=experiment_cfg["reference_consistency_bound_pixel2"],
        minimum_reference_consensus=experiment_cfg["minimum_reference_consensus"],
        gain_log_ratio_bound=experiment_cfg["gain_log_ratio_bound"],
    )
    cfg_controlled = controlled_config(cfg, experiment_cfg)
    baseline, baseline_stdout = frozen_baseline_regression()
    registry = run_failure_registry(cfg, cfg_controlled, experiment_cfg, v1_cfg)
    aggregate = aggregate_registry(registry)
    standard = run_v1_standard_benchmark(cfg, cfg_controlled, v1_cfg)
    reference = read_json(PLAN / "reference_run" / "summary.json")
    v0_bounded = next(
        metric for metric in reference["metrics"] if metric["method"] == "bounded_interval"
    )
    output = {
        "evidence_type": "SYNTHETIC_ONLY",
        "physical_validation_performed": False,
        "baseline_regression": baseline,
        "v0_bounded_interval": v0_bounded,
        "failure_aggregate": aggregate,
        "v1_standard_benchmark": standard,
        "candidate_decisions": {
            "E1_gain_guard": "RETAIN; improves modeled uniform absorption under an explicit gain bound.",
            "E2_reference_consensus": "RETAIN; breaks one-corrupt-of-three dirty-reference failure.",
            "E3_controlled_geometry": "RETAIN; breaks cancellation under registered high-SNR assumptions.",
            "E4_secondary_optical_hypothesis": "REJECT FOR V1; apparent invisible-residue gain is assumption-driven and physically unvalidated.",
        },
        "candidate_costs": {
            "E1_gain_guard": {
                "extra_live_frames": 0,
                "acquisition_complexity": "unchanged",
                "computation": "signed slope/intercept fit",
                "calibration": "radiometric gain-drift bound",
            },
            "E2_reference_consensus": {
                "extra_live_frames": 0,
                "acquisition_complexity": "three stored references instead of one",
                "computation": "pairwise reference distances plus three bounded inferences",
                "calibration": "reference preparation, dating, drift, and replacement",
            },
            "E3_controlled_geometry": {
                "extra_live_frames": 48,
                "acquisition_complexity": "registered high-SNR repeat",
                "computation": "one additional bounded inference",
                "calibration": "pose bound, registration, linearity, and high-SNR error bound",
            },
            "E4_secondary_optical_hypothesis": {
                "extra_live_frames": 48,
                "acquisition_complexity": "new wavelength/polarization/angle state",
                "computation": "one additional bounded inference",
                "calibration": "material-specific contrast; not established",
            },
        },
        "measurement_cost": {
            "v0_live_sample_frames": 48,
            "v1_live_sample_frames": 96,
            "v0_reference_frames": 48,
            "v1_reference_library_frames": 288,
            "computation": "Six bounded inferences plus reference-consistency checks per field of view.",
            "calibration_burden": "Maintain majority-clean references, gain bound, registration, and high-SNR secondary state.",
        },
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS / "phase1_results.json", output)
    (RESULTS / "v0_pipeline_stdout.txt").write_text(baseline_stdout, encoding="utf-8")
    (RESULTS / "phase1_comparison.md").write_text(
        comparison_markdown(output) + "\n", encoding="utf-8"
    )
    print("Phase 1 complete: baseline regression, failure registry, v1 benchmark, comparison")
    print(RESULTS / "phase1_results.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
