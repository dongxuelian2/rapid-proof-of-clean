# ruff: noqa: E402
"""Run the realistic joint-model architecture comparison."""

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

from rapid_proof_clean.advanced import DiversityConfig, fuse_v2, infer_diversity
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


def _v1_status(
    cfg: dict,
    controlled: dict,
    v1: V1Config,
    material_name: str,
    residue_name: str,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    material = MATERIALS[material_name]
    residue = RESIDUES[residue_name]
    latents = make_latents(cfg["image_size"], residue, seed)
    states = []
    for is_controlled, state_cfg in ((False, cfg), (True, controlled)):
        references, sample, visible, mask = simulate_structured_scene(
            state_cfg,
            material,
            residue,
            latents,
            seed,
            controlled=is_controlled,
        )
        states.append(
            infer_reference_ensemble(
                references, sample, state_cfg, visible, v1, use_gain_guard=True
            )["status"]
        )
    return combine_measurement_states(*states), mask


def _accumulate(
    accumulator: dict,
    method: str,
    material: str,
    residue: str,
    status: np.ndarray,
    evaluation_mask: np.ndarray,
) -> None:
    values = status[evaluation_mask]
    key = (method, material, residue)
    accumulator[key]["PASS"] += int(np.sum(values == PASS))
    accumulator[key]["FLAG"] += int(np.sum(values == FLAG))
    accumulator[key]["UNKNOWN"] += int(np.sum(values == UNKNOWN))
    accumulator[key]["pixels"] += int(values.size)


def run() -> dict:
    cfg = read_json(ROOT / "proof_clean_local_plan" / "config.json")
    v1_file = read_json(ROOT / "experiments" / "v1_config.json")
    v2_file = read_json(ROOT / "experiments" / "v2_config.json")
    controlled = controlled_config(cfg, v1_file)
    v1 = V1Config(
        v1_file["reference_consistency_bound_pixel2"],
        v1_file["minimum_reference_consensus"],
        v1_file["gain_log_ratio_bound"],
    )
    diversity = DiversityConfig(
        v2_file["reference_consistency_log"],
        v2_file["pass_bound_log"],
        v2_file["flag_bound_log"],
        v1_file["minimum_reference_consensus"],
    )
    arms = ("angle", "polarization", "wavelength", "combined")
    accumulator: dict = defaultdict(lambda: defaultdict(int))
    for material_index, material_name in enumerate(v2_file["materials"]):
        for residue_index, residue_name in enumerate(v2_file["residues"]):
            for replicate in range(v2_file["replicates"]):
                seed = (
                    v2_file["fixed_seed"]
                    + material_index * 100_000
                    + residue_index * 1_000
                    + replicate
                )
                v1_status, mask = _v1_status(
                    cfg, controlled, v1, material_name, residue_name, seed
                )
                evaluation_mask = np.ones_like(mask) if residue_name == "clean" else mask
                _accumulate(
                    accumulator,
                    "v1_multifrequency",
                    material_name,
                    residue_name,
                    v1_status,
                    evaluation_mask,
                )
                latents = make_latents(cfg["image_size"], RESIDUES[residue_name], seed)
                references, sample = simulate_diversity_observation(
                    MATERIALS[material_name],
                    RESIDUES[residue_name],
                    latents,
                    seed,
                    reference_noise_log=v2_file["reference_noise_log"],
                    sample_noise_log=v2_file["sample_noise_log"],
                )
                for arm in arms:
                    auxiliary = infer_diversity(references, sample, arm, diversity)["status"]
                    fused = fuse_v2(v1_status, auxiliary)
                    _accumulate(
                        accumulator,
                        f"v2_{arm}",
                        material_name,
                        residue_name,
                        fused,
                        evaluation_mask,
                    )

    rows = []
    for (method, material, residue), counts in sorted(accumulator.items()):
        total = counts["pixels"]
        rows.append(
            {
                "method": method,
                "material": material,
                "residue": residue,
                "evaluated_pixels": total,
                "false_clean_rate": counts["PASS"] / total if residue != "clean" else "",
                "clean_pass_rate": counts["PASS"] / total if residue == "clean" else "",
                "flag_rate": counts["FLAG"] / total,
                "unknown_rate": counts["UNKNOWN"] / total,
                "usable_coverage": 1.0 - counts["UNKNOWN"] / total,
                "evidence_type": "ASSUMPTION_DRIVEN_SIMULATION_ONLY",
            }
        )

    aggregate = []
    methods = sorted({row["method"] for row in rows})
    for method in methods:
        selected = [
            row
            for row in rows
            if row["method"] == method and row["residue"] not in ("clean", "matched_invisible")
        ]
        invisible = [
            row
            for row in rows
            if row["method"] == method and row["residue"] == "matched_invisible"
        ]
        clean = [
            row for row in rows if row["method"] == method and row["residue"] == "clean"
        ]
        weights = np.array([row["evaluated_pixels"] for row in selected], dtype=float)
        aggregate.append(
            {
                "method": method,
                "nonmatched_residue_false_clean_rate": float(
                    np.average([row["false_clean_rate"] for row in selected], weights=weights)
                ),
                "nonmatched_residue_unknown_rate": float(
                    np.average([row["unknown_rate"] for row in selected], weights=weights)
                ),
                "nonmatched_residue_usable_coverage": float(
                    np.average([row["usable_coverage"] for row in selected], weights=weights)
                ),
                "matched_invisible_false_clean_rate": float(
                    np.mean([row["false_clean_rate"] for row in invisible])
                ),
                "clean_pass_rate": float(np.mean([row["clean_pass_rate"] for row in clean])),
                "clean_false_flag_rate": float(np.mean([row["flag_rate"] for row in clean])),
                "clean_unknown_rate": float(np.mean([row["unknown_rate"] for row in clean])),
            }
        )
    return {
        "evidence_type": v2_file["evidence_type"],
        "physical_experiment_executed": False,
        "configuration": v2_file,
        "rows": rows,
        "aggregate": aggregate,
        "negative_results": {
            "phase_amplitude_joint": (
                "Not promoted: the planar-film model changes amplitude/signature but not projected "
                "fringe phase; phase adds no information for flat residue and geometry "
                "confounds it."
            ),
            "reference_free_sanity": (
                "Retained only as a validity/UNKNOWN guard; it cannot distinguish two physical "
                "states with identical observations and therefore does not expand observability."
            ),
            "multi_frequency_only": (
                "Already represented by retained v1; more frequencies tighten a blur estimate but "
                "do not expose a residue whose modulation transfer matches clean."
            ),
        },
    }


def main() -> int:
    result = run()
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "v2_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    rows = result["rows"]
    with (RESULTS / "v2_benchmark.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(result["aggregate"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
