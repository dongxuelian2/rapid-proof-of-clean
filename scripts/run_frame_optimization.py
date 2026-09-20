# ruff: noqa: E402
"""Compare compressed acquisition schedules on the frozen realistic scenes."""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN
from proof_clean_local_plan.src.simulation import make_scene

from rapid_proof_clean.advanced import (
    DiversityConfig,
    fuse_v2,
    infer_diversity_features,
)
from rapid_proof_clean.phase1 import V1Config, combine_measurement_states, infer_reference_ensemble
from rapid_proof_clean.realistic import (
    MATERIALS,
    RESIDUES,
    make_latents,
    simulate_diversity_observation,
    simulate_structured_scene,
)

RESULTS = ROOT / "experiments" / "results"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def controlled_config(cfg: dict, v1_cfg: dict) -> dict:
    result = dict(cfg)
    result["clean_variation_bound_pixel2"] = v1_cfg[
        "controlled_geometry_clean_variation_bound_pixel2"
    ]
    result["additive_noise_bound"] = v1_cfg["controlled_geometry_additive_noise_bound"]
    result["quantization_levels"] = v1_cfg["controlled_geometry_quantization_levels"]
    return result


def subset_acquisition(
    references: np.ndarray,
    sample: np.ndarray,
    cfg: dict,
    frequency_indices: list[int],
) -> tuple[np.ndarray, np.ndarray, dict]:
    selected_cfg = dict(cfg)
    selected_cfg["frequencies_cycles_per_screen"] = [
        cfg["frequencies_cycles_per_screen"][index] for index in frequency_indices
    ]
    return references[:, :, frequency_indices], sample[:, frequency_indices], selected_cfg


def structured_status(
    state_data: dict,
    candidate: dict,
    v1: V1Config,
) -> np.ndarray:
    statuses = []
    for state in candidate["states"]:
        references, sample, visible, cfg = state_data[state]
        references, sample, selected_cfg = subset_acquisition(
            references, sample, cfg, candidate["frequency_indices"]
        )
        statuses.append(
            infer_reference_ensemble(
                references, sample, selected_cfg, visible, v1, use_gain_guard=True
            )["status"]
        )
    if len(statuses) == 1:
        return statuses[0]
    return combine_measurement_states(*statuses)


def frame_count(structured: dict, diversity: dict | None) -> int:
    structured_frames = 2 * len(structured["frequency_indices"]) * 4 * len(
        structured["states"]
    )
    return structured_frames + (0 if diversity is None else len(diversity["feature_indices"]))


def accumulate(
    counts: dict,
    method: str,
    status: np.ndarray,
    evaluation_mask: np.ndarray,
    residue_name: str,
    split: str,
) -> None:
    values = status[evaluation_mask]
    key = (method, residue_name, split)
    counts[key]["PASS"] += int(np.sum(values == PASS))
    counts[key]["FLAG"] += int(np.sum(values == FLAG))
    counts[key]["UNKNOWN"] += int(np.sum(values == UNKNOWN))
    counts[key]["pixels"] += int(values.size)


def summarize(counts: dict, methods: dict[str, int]) -> list[dict]:
    rows = []
    for split in ("design", "audit", "all"):
        for method, frames in methods.items():
            residue_counts = {
                residue: counts[(method, residue, split)]
                for residue in RESIDUES
                if counts[(method, residue, split)]["pixels"]
            }
            nonmatched = [
                values
                for residue, values in residue_counts.items()
                if residue not in ("clean", "matched_invisible")
            ]
            clean = residue_counts["clean"]
            invisible = residue_counts["matched_invisible"]
            dirty_pixels = sum(item["pixels"] for item in nonmatched)
            rows.append(
                {
                    "split": split,
                    "method": method,
                    "sample_frames_per_fov": frames,
                    "frame_reduction_vs_108": 1.0 - frames / 108,
                    "nonmatched_false_clean_rate": sum(item["PASS"] for item in nonmatched)
                    / dirty_pixels,
                    "nonmatched_flag_rate": sum(item["FLAG"] for item in nonmatched)
                    / dirty_pixels,
                    "nonmatched_unknown_rate": sum(item["UNKNOWN"] for item in nonmatched)
                    / dirty_pixels,
                    "clean_pass_rate": clean["PASS"] / clean["pixels"],
                    "clean_false_flag_rate": clean["FLAG"] / clean["pixels"],
                    "clean_unknown_rate": clean["UNKNOWN"] / clean["pixels"],
                    "matched_invisible_false_clean_rate": invisible["PASS"]
                    / invisible["pixels"],
                    "matched_invisible_flag_rate": invisible["FLAG"] / invisible["pixels"],
                    "evidence_type": "ASSUMPTION_DRIVEN_SIMULATION_ONLY",
                }
            )
    return rows


def _legacy_reference_pool(
    first: np.ndarray,
    cfg: dict,
    rng: np.random.Generator,
    state: str,
) -> np.ndarray:
    clean = [
        make_scene(cfg, rng, "clean", measurement_state=state)[0]
        for _ in range(2)
    ]
    return np.stack([first, *clean])


def legacy_failure_audit(cfg: dict, controlled: dict, v1: V1Config) -> list[dict]:
    """Check that endpoint-frequency compression retains the fixed v1 defenses."""

    failures = (
        "dirty_reference",
        "uniform_absorber",
        "optically_invisible_residue",
        "negative_blur_cancellation",
    )
    schedules = {
        "structured_96_full": list(range(6)),
        "structured_32_endpoint": [0, 5],
    }
    counts: dict = defaultdict(lambda: defaultdict(int))
    for failure_index, failure in enumerate(failures):
        for replicate in range(8):
            seed = 20260920 + failure_index * 100 + replicate
            primary_rng = np.random.default_rng(seed)
            primary = make_scene(cfg, primary_rng, failure, measurement_state="primary")
            primary_references = _legacy_reference_pool(
                primary[0], cfg, primary_rng, "primary"
            )
            controlled_rng = np.random.default_rng(seed + 10_000)
            second = make_scene(
                controlled,
                controlled_rng,
                failure,
                measurement_state="controlled_geometry",
            )
            controlled_references = _legacy_reference_pool(
                second[0], controlled, controlled_rng, "controlled_geometry"
            )
            for schedule, indices in schedules.items():
                p_ref, p_sample, p_cfg = subset_acquisition(
                    primary_references, primary[1], cfg, indices
                )
                c_ref, c_sample, c_cfg = subset_acquisition(
                    controlled_references, second[1], controlled, indices
                )
                p_status = infer_reference_ensemble(
                    p_ref, p_sample, p_cfg, primary[3], v1, use_gain_guard=True
                )["status"]
                c_status = infer_reference_ensemble(
                    c_ref, c_sample, c_cfg, second[3], v1, use_gain_guard=True
                )["status"]
                status = combine_measurement_states(p_status, c_status)
                key = (schedule, failure)
                counts[key]["PASS"] += int(np.sum(status == PASS))
                counts[key]["FLAG"] += int(np.sum(status == FLAG))
                counts[key]["UNKNOWN"] += int(np.sum(status == UNKNOWN))
                counts[key]["pixels"] += int(status.size)
    rows = []
    for schedule in schedules:
        for failure in failures:
            item = counts[(schedule, failure)]
            total = item["pixels"]
            rows.append(
                {
                    "schedule": schedule,
                    "failure_mode": failure,
                    "false_clean_rate": item["PASS"] / total,
                    "flag_rate": item["FLAG"] / total,
                    "unknown_rate": item["UNKNOWN"] / total,
                }
            )
    return rows


def summarize_adaptive_frames(records: list[dict]) -> list[dict]:
    rows = []
    for split in ("design", "audit", "all"):
        for residue_group in ("clean", "nonmatched", "matched_invisible", "all"):
            selected = [
                row
                for row in records
                if (row["split"] == split or split == "all")
                and (residue_group == "all" or row["residue_group"] == residue_group)
            ]
            frames = np.asarray([row["frames"] for row in selected], dtype=float)
            rows.append(
                {
                    "split": split,
                    "residue_group": residue_group,
                    "fov_count": len(selected),
                    "mean_frames": float(np.mean(frames)),
                    "minimum_frames": int(np.min(frames)),
                    "maximum_frames": int(np.max(frames)),
                    "early_flag_fraction": float(np.mean(frames < 44)),
                }
            )
    return rows


def run() -> dict:
    cfg = read_json(ROOT / "proof_clean_local_plan" / "config.json")
    v1_file = read_json(ROOT / "experiments" / "v1_config.json")
    v2_file = read_json(ROOT / "experiments" / "v2_config.json")
    study = read_json(ROOT / "experiments" / "frame_optimization_config.json")
    controlled = controlled_config(cfg, v1_file)
    v1 = V1Config(
        v1_file["reference_consistency_bound_pixel2"],
        v1_file["minimum_reference_consensus"],
        v1_file["gain_log_ratio_bound"],
    )
    diversity_cfg = DiversityConfig(
        v2_file["reference_consistency_log"],
        v2_file["pass_bound_log"],
        v2_file["flag_bound_log"],
        v1_file["minimum_reference_consensus"],
    )
    methods = {}
    for structured in study["structured_candidates"]:
        methods[structured["name"]] = frame_count(structured, None)
        for diversity in study["diversity_candidates"]:
            name = f"{structured['name']}+{diversity['name']}"
            methods[name] = frame_count(structured, diversity)

    counts: dict = defaultdict(lambda: defaultdict(int))
    adaptive_records = []
    for material_index, (_material_name, material) in enumerate(MATERIALS.items()):
        for residue_index, (residue_name, residue) in enumerate(RESIDUES.items()):
            for replicate in range(study["replicates"]):
                seed = (
                    study["fixed_seed"]
                    + material_index * 100_000
                    + residue_index * 1_000
                    + replicate
                )
                split = "design" if replicate < study["replicates"] // 2 else "audit"
                latents = make_latents(cfg["image_size"], residue, seed)
                state_data = {}
                for state, state_cfg, is_controlled in (
                    ("primary", cfg, False),
                    ("controlled", controlled, True),
                ):
                    references, sample, visible, mask = simulate_structured_scene(
                        state_cfg,
                        material,
                        residue,
                        latents,
                        seed,
                        controlled=is_controlled,
                    )
                    state_data[state] = (references, sample, visible, state_cfg)
                diversity_references, diversity_sample = simulate_diversity_observation(
                    material,
                    residue,
                    latents,
                    seed,
                    reference_noise_log=v2_file["reference_noise_log"],
                    sample_noise_log=v2_file["sample_noise_log"],
                )
                full_diversity = infer_diversity_features(
                    diversity_references,
                    diversity_sample,
                    list(range(12)),
                    diversity_cfg,
                )["status"]
                endpoint_primary = structured_status(
                    state_data,
                    {"states": ["primary"], "frequency_indices": [0, 5]},
                    v1,
                )
                if np.any(full_diversity == FLAG):
                    adaptive_frames = 12
                elif np.any(endpoint_primary == FLAG):
                    adaptive_frames = 28
                else:
                    adaptive_frames = 44
                if residue_name == "clean":
                    residue_group = "clean"
                elif residue_name == "matched_invisible":
                    residue_group = "matched_invisible"
                else:
                    residue_group = "nonmatched"
                adaptive_records.append(
                    {
                        "split": split,
                        "residue_group": residue_group,
                        "frames": adaptive_frames,
                    }
                )
                evaluation_mask = np.ones_like(mask) if residue_name == "clean" else mask
                for structured in study["structured_candidates"]:
                    base_status = structured_status(state_data, structured, v1)
                    accumulate(
                        counts,
                        structured["name"],
                        base_status,
                        evaluation_mask,
                        residue_name,
                        split,
                    )
                    accumulate(
                        counts,
                        structured["name"],
                        base_status,
                        evaluation_mask,
                        residue_name,
                        "all",
                    )
                    for diversity in study["diversity_candidates"]:
                        auxiliary = infer_diversity_features(
                            diversity_references,
                            diversity_sample,
                            diversity["feature_indices"],
                            diversity_cfg,
                        )["status"]
                        fused = fuse_v2(base_status, auxiliary)
                        name = f"{structured['name']}+{diversity['name']}"
                        accumulate(
                            counts, name, fused, evaluation_mask, residue_name, split
                        )
                        accumulate(
                            counts, name, fused, evaluation_mask, residue_name, "all"
                        )
    rows = summarize(counts, methods)
    all_rows = [row for row in rows if row["split"] == "all"]
    pareto = []
    for row in sorted(all_rows, key=lambda item: item["sample_frames_per_fov"]):
        dominated = any(
            other["sample_frames_per_fov"] <= row["sample_frames_per_fov"]
            and other["nonmatched_false_clean_rate"] <= row["nonmatched_false_clean_rate"]
            and other["clean_pass_rate"] >= row["clean_pass_rate"]
            and (
                other["sample_frames_per_fov"] < row["sample_frames_per_fov"]
                or other["nonmatched_false_clean_rate"] < row["nonmatched_false_clean_rate"]
                or other["clean_pass_rate"] > row["clean_pass_rate"]
            )
            for other in all_rows
        )
        if not dominated:
            pareto.append(row)
    return {
        "evidence_type": study["evidence_type"],
        "physical_experiment_executed": False,
        "configuration": study,
        "rows": rows,
        "pareto_all_split": pareto,
        "selected_v2_1": {
            "method": "s32_both_f2+d12_full",
            "maximum_sample_frames_per_fov": 44,
            "schedule": (
                "12 diversity -> 16 primary endpoint-frequency -> "
                "16 controlled endpoint-frequency"
            ),
            "early_exit_semantics": (
                "Early exit is valid only for an FOV-level FLAG; a complete "
                "pixel map and every PASS require all 44 frames."
            ),
        },
        "adaptive_frame_summary": summarize_adaptive_frames(adaptive_records),
        "legacy_failure_audit": legacy_failure_audit(cfg, controlled, v1),
    }


def main() -> int:
    result = run()
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "frame_optimization_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    rows = result["rows"]
    with (RESULTS / "frame_optimization_benchmark.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(result["pareto_all_split"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
