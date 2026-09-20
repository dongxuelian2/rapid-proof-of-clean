# ruff: noqa: E402
"""Run the final sequential, reference, domain-shift and adversarial benchmark.

The evaluation perturbations operate on clean rendered observations and do not
reuse the retained simulator's residue parameterization.  Results remain
synthetic, conditional and unsuitable as a physical detection-limit claim.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof_clean_local_plan.src.core import demodulate

from rapid_proof_clean.advanced import DiversityConfig, infer_diversity_features
from rapid_proof_clean.domain_shift import (
    add_evaluation_noise,
    apply_diversity_response,
    apply_structured_response,
    morphology_mask,
)
from rapid_proof_clean.phase1 import V1Config, infer_reference_ensemble
from rapid_proof_clean.realistic import (
    MATERIALS,
    RESIDUES,
    make_latents,
    simulate_diversity_observation,
    simulate_structured_scene,
)
from rapid_proof_clean.reference_integrity import qualify_reference_features
from rapid_proof_clean.sequential import combine_evidence, retained_policies, run_policy

RESULTS = ROOT / "experiments" / "results"
FREQUENCY_INDICES = {"2": [0, 5], "3": [0, 3, 5]}
DIVERSITY_INDICES = {"d2": [6, 7], "d4": [0, 1, 10, 11], "d12": list(range(12))}


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


def subset_structured(values: np.ndarray, cfg: dict, indices: list[int]) -> tuple:
    selected = dict(cfg)
    selected["frequencies_cycles_per_screen"] = [
        cfg["frequencies_cycles_per_screen"][index] for index in indices
    ]
    if values.ndim == 6:
        return values[:, :, indices], selected
    return values[:, indices], selected


def flatten_demodulated(references: np.ndarray) -> np.ndarray:
    modulated = demodulate(references)
    return modulated.reshape(len(references), -1, *references.shape[-2:])


def _scenario_catalog() -> list[dict]:
    z6 = [0.0] * 6
    z12 = [0.0] * 12
    return [
        {"name": "clean_easy", "group": "clean", "morphology": "uniform", "support": 1.0},
        {
            "name": "clean_exposure_drift",
            "group": "clean",
            "morphology": "uniform",
            "support": 1.0,
            "sample_gain": 0.93,
        },
        {
            "name": "clean_registration_error",
            "group": "clean",
            "morphology": "uniform",
            "support": 1.0,
            "registration": [1, -1],
        },
        {
            "name": "clean_impulsive_noise",
            "group": "nuisance",
            "morphology": "uniform",
            "support": 1.0,
            "noise": [0.0012, 0.002, 0.035],
        },
        {
            "name": "high_contrast_smear",
            "group": "contaminated",
            "morphology": "patchy",
            "support": 0.35,
            "primary": [0.02, 0.05, 0.10, 0.20, 0.34, 0.48],
            "controlled": [0.03, 0.07, 0.14, 0.27, 0.42, 0.58],
            "diversity": [0.00, 0.06, 0.12, 0.20, 0.03, 0.13, 0.22, 0.32, 0.05, 0.15, 0.28, 0.42],
        },
        {
            "name": "low_contrast_film",
            "group": "contaminated",
            "morphology": "droplet",
            "support": 0.42,
            "primary": [0.00, 0.012, 0.025, 0.040, 0.060, 0.080],
            "controlled": [0.00, 0.018, 0.038, 0.060, 0.082, 0.105],
            "diversity": [
                0.00, 0.018, 0.038, 0.062, 0.01, 0.03,
                0.055, 0.08, 0.02, 0.04, 0.07, 0.10,
            ],
        },
        {
            "name": "primary_cancellation",
            "group": "contaminated",
            "morphology": "patchy",
            "support": 0.40,
            "primary": z6,
            "controlled": [0.00, 0.05, 0.12, 0.24, 0.40, 0.60],
            "diversity": [0.00, 0.03, 0.08, 0.14, 0.02, 0.07, 0.15, 0.24, 0.04, 0.10, 0.21, 0.34],
        },
        {
            "name": "midband_only",
            "group": "contaminated",
            "morphology": "droplet",
            "support": 0.45,
            "primary": [0.0, 0.10, 0.19, 0.28, 0.12, 0.0],
            "controlled": [0.0, 0.12, 0.22, 0.34, 0.14, 0.0],
            "diversity": z12,
        },
        {
            "name": "diversity_only",
            "group": "contaminated",
            "morphology": "patchy",
            "support": 0.32,
            "primary": z6,
            "controlled": z6,
            "diversity": [0.00, 0.12, 0.03, 0.22, 0.04, 0.30, 0.08, 0.39, 0.02, 0.19, 0.07, 0.34],
        },
        {
            "name": "uniform_absorber",
            "group": "contaminated",
            "morphology": "uniform",
            "support": 1.0,
            "primary": [0.42] * 6,
            "controlled": [0.42] * 6,
            "diversity": [0.28] * 12,
        },
        {
            "name": "near_threshold",
            "group": "contaminated",
            "morphology": "patchy",
            "support": 0.48,
            "primary": [0.0, 0.01, 0.025, 0.045, 0.07, 0.10],
            "controlled": [0.0, 0.015, 0.035, 0.060, 0.09, 0.125],
            "diversity": [
                0.00, 0.02, 0.04, 0.065, 0.01, 0.03,
                0.055, 0.085, 0.02, 0.045, 0.07, 0.105,
            ],
        },
        {
            "name": "thin_streak",
            "group": "contaminated",
            "morphology": "streak",
            "support": 0.025,
            "primary": [0.0, 0.04, 0.10, 0.20, 0.34, 0.52],
            "controlled": [0.0, 0.05, 0.13, 0.25, 0.42, 0.62],
            "diversity": [0.0, 0.04, 0.10, 0.18, 0.03, 0.10, 0.20, 0.32, 0.05, 0.14, 0.28, 0.44],
        },
        {
            "name": "sparse_particles",
            "group": "contaminated",
            "morphology": "particles",
            "support": 0.008,
            "primary": [0.0, 0.05, 0.14, 0.28, 0.46, 0.68],
            "controlled": [0.0, 0.07, 0.18, 0.34, 0.54, 0.76],
            "diversity": [0.0, 0.07, 0.14, 0.24, 0.05, 0.14, 0.28, 0.43, 0.08, 0.19, 0.36, 0.55],
        },
        {
            "name": "observation_matched",
            "group": "contaminated",
            "morphology": "uniform",
            "support": 1.0,
            "primary": z6,
            "controlled": z6,
            "diversity": z12,
        },
        {
            "name": "independent_dirty_reference",
            "group": "reference",
            "morphology": "uniform",
            "support": 1.0,
            "reference_mode": "independent",
        },
        {
            "name": "common_mode_dirty_reference",
            "group": "reference",
            "morphology": "uniform",
            "support": 1.0,
            "reference_mode": "common",
        },
        {
            "name": "bounded_reference_aging",
            "group": "reference",
            "morphology": "uniform",
            "support": 1.0,
            "reference_mode": "aging_small",
        },
        {
            "name": "excess_reference_aging",
            "group": "reference",
            "morphology": "uniform",
            "support": 1.0,
            "reference_mode": "aging_large",
        },
        {
            "name": "missing_diversity_state",
            "group": "failure",
            "morphology": "uniform",
            "support": 1.0,
            "failed_states": ["d12"],
        },
        {
            "name": "invalid_coverage",
            "group": "failure",
            "morphology": "uniform",
            "support": 1.0,
            "coverage_valid": False,
        },
        {
            "name": "missing_historical_anchor",
            "group": "failure",
            "morphology": "uniform",
            "support": 1.0,
            "anchor_missing": True,
        },
    ]


def _apply_reference_mode(
    structured: dict[str, np.ndarray],
    diversity: np.ndarray,
    mask: np.ndarray,
    mode: str | None,
) -> tuple[dict[str, np.ndarray], np.ndarray]:
    if mode is None:
        return structured, diversity
    if mode == "independent":
        indices = [0]
        scale = 1.0
    elif mode == "aging_small":
        indices = list(range(len(diversity)))
        scale = 0.10
    else:
        indices = list(range(len(diversity)))
        scale = 1.0
    s_profile = np.asarray([0.0, 0.04, 0.08, 0.14, 0.21, 0.30]) * scale
    d_profile = np.asarray(
        [0.0, 0.03, 0.07, 0.12, 0.02, 0.08, 0.15, 0.23, 0.04, 0.11, 0.20, 0.31]
    ) * scale
    for state in structured:
        for index in indices:
            structured[state][index] = apply_structured_response(
                structured[state][index], mask, s_profile
            )
    for index in indices:
        diversity[index] = apply_diversity_response(diversity[index], mask, d_profile)
    return structured, diversity


def _make_evidence(
    cfg: dict,
    controlled: dict,
    v1: V1Config,
    dcfg: DiversityConfig,
    material_name: str,
    scenario: dict,
    seed: int,
) -> tuple[dict, np.ndarray, bool, bool, frozenset[str], dict]:
    material = MATERIALS[material_name]
    clean = RESIDUES["clean"]
    latents = make_latents(cfg["image_size"], clean, seed)
    structured: dict[str, np.ndarray] = {}
    samples: dict[str, np.ndarray] = {}
    visible = np.ones((cfg["image_size"], cfg["image_size"]), dtype=bool)
    for state, state_cfg, is_controlled in (
        ("p", cfg, False),
        ("c", controlled, True),
    ):
        references, sample, visible, _ = simulate_structured_scene(
            state_cfg, material, clean, latents, seed, controlled=is_controlled
        )
        structured[state] = references
        samples[state] = sample
    drefs, dsample = simulate_diversity_observation(
        material,
        clean,
        latents,
        seed,
        reference_noise_log=0.006,
        sample_noise_log=0.009,
    )
    anchors = {
        state: np.median(flatten_demodulated(refs), axis=0)
        for state, refs in structured.items()
    }
    danchor = np.median(drefs.reshape(3, 12, *drefs.shape[-2:]), axis=0)
    mask = morphology_mask(
        cfg["image_size"], scenario["morphology"], scenario["support"], seed + 91
    )

    for state, key in (("p", "primary"), ("c", "controlled")):
        profile = np.asarray(scenario.get(key, [0.0] * 6), dtype=float)
        samples[state] = apply_structured_response(
            samples[state], mask, profile, gain=float(scenario.get("sample_gain", 1.0))
        )
    dsample = apply_diversity_response(
        dsample, mask, np.asarray(scenario.get("diversity", [0.0] * 12), dtype=float)
    )
    if "registration" in scenario:
        shift = tuple(scenario["registration"])
        samples = {key: np.roll(value, shift, axis=(-2, -1)) for key, value in samples.items()}
        dsample = np.roll(dsample, shift, axis=(-2, -1))
    if "noise" in scenario:
        sigma, probability, scale = scenario["noise"]
        samples = {
            key: add_evaluation_noise(
                value,
                seed + offset,
                gaussian_sigma=sigma,
                outlier_probability=probability,
                outlier_scale=scale,
            )
            for offset, (key, value) in enumerate(samples.items())
        }
        dsample = add_evaluation_noise(
            dsample,
            seed + 17,
            gaussian_sigma=sigma,
            outlier_probability=probability,
            outlier_scale=scale,
        )

    structured, drefs = _apply_reference_mode(
        structured, drefs, mask, scenario.get("reference_mode")
    )
    anchor_missing = scenario.get("anchor_missing", False)
    integrity = {}
    for state, refs in structured.items():
        integrity[state] = qualify_reference_features(
            flatten_demodulated(refs), anchor=None if anchor_missing else anchors[state]
        )
    integrity["d"] = qualify_reference_features(
        drefs.reshape(3, 12, *drefs.shape[-2:]), anchor=None if anchor_missing else danchor
    )
    reference_valid = all(item["valid"] for item in integrity.values())

    evidence = {}
    for name, indices in DIVERSITY_INDICES.items():
        evidence[name] = infer_diversity_features(drefs, dsample, indices, dcfg)["status"]
    for state, state_cfg in (("p", cfg), ("c", controlled)):
        for label, indices in FREQUENCY_INDICES.items():
            refs, selected_cfg = subset_structured(structured[state], state_cfg, indices)
            sample, _ = subset_structured(samples[state], state_cfg, indices)
            evidence[f"{state}{label}"] = infer_reference_ensemble(
                refs, sample, selected_cfg, visible, v1, use_gain_guard=True
            )["status"]
    diagnostics = {
        "reference_reasons": {key: item["reason"] for key, item in integrity.items()},
        "reference_valid": reference_valid,
        "support_pixels": int(mask.sum()),
    }
    return (
        evidence,
        visible,
        reference_valid,
        bool(scenario.get("coverage_valid", True)),
        frozenset(scenario.get("failed_states", [])),
        diagnostics,
    )


def _bootstrap_interval(values: list[float], seed: int) -> list[float]:
    if not values:
        return [float("nan"), float("nan")]
    array = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    draws = rng.choice(array, size=(1000, len(array)), replace=True).mean(axis=1)
    return [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))]


def _summarize(records: list[dict]) -> list[dict]:
    rows = []
    for policy in sorted({row["policy"] for row in records}):
        selected = [row for row in records if row["policy"] == policy]
        dirty = [row for row in selected if row["group"] == "contaminated"]
        observable = [row for row in dirty if row["scenario"] != "observation_matched"]
        clean = [row for row in selected if row["group"] == "clean"]
        frames = np.asarray([row["frames"] for row in selected], dtype=float)
        false_clean = [float(row["decision"] == "PASS") for row in observable]
        rows.append(
            {
                "policy": policy,
                "fov_count": len(selected),
                "observable_dirty_false_clean_rate": float(np.mean(false_clean)),
                "observable_dirty_false_clean_ci95": _bootstrap_interval(false_clean, 17),
                "observable_dirty_unknown_rate": float(
                    np.mean([row["decision"] == "UNKNOWN" for row in observable])
                ),
                "matched_invisible_false_clean_rate": float(
                    np.mean(
                        [
                            row["decision"] == "PASS"
                            for row in dirty
                            if row["scenario"] == "observation_matched"
                        ]
                    )
                ),
                "clean_pass_rate": float(np.mean([row["decision"] == "PASS" for row in clean])),
                "clean_false_flag_rate": float(
                    np.mean([row["decision"] == "FLAG" for row in clean])
                ),
                "clean_unknown_rate": float(
                    np.mean([row["decision"] == "UNKNOWN" for row in clean])
                ),
                "usable_coverage": float(
                    np.mean([row["decision"] != "UNKNOWN" for row in selected])
                ),
                "mean_frames": float(np.mean(frames)),
                "median_frames": float(np.median(frames)),
                "p75_frames": float(np.quantile(frames, 0.75)),
                "p90_frames": float(np.quantile(frames, 0.90)),
                "p95_frames": float(np.quantile(frames, 0.95)),
                "maximum_frames": int(np.max(frames)),
                "frame_histogram": dict(sorted(Counter(map(int, frames)).items())),
            }
        )
    return rows


def _group_summary(records: list[dict]) -> list[dict]:
    rows = []
    for policy in sorted({row["policy"] for row in records}):
        for group in sorted({row["group"] for row in records}):
            selected = [
                row for row in records if row["policy"] == policy and row["group"] == group
            ]
            frames = np.asarray([row["frames"] for row in selected], dtype=float)
            rows.append(
                {
                    "policy": policy,
                    "group": group,
                    "fov_count": len(selected),
                    "pass_rate": float(np.mean([row["decision"] == "PASS" for row in selected])),
                    "flag_rate": float(np.mean([row["decision"] == "FLAG" for row in selected])),
                    "unknown_rate": float(
                        np.mean([row["decision"] == "UNKNOWN" for row in selected])
                    ),
                    "mean_frames": float(np.mean(frames)),
                    "median_frames": float(np.median(frames)),
                    "p95_frames": float(np.quantile(frames, 0.95)),
                    "maximum_frames": int(np.max(frames)),
                }
            )
    return rows


def _reference_summary(records: list[dict]) -> list[dict]:
    rows = []
    scenarios = sorted({row["scenario"] for row in records if row["group"] == "reference"})
    for scenario in scenarios:
        selected = [
            row
            for row in records
            if row["scenario"] == scenario and row["policy"] == "adaptive_risk_targeted"
        ]
        rows.append(
            {
                "scenario": scenario,
                "fov_count": len(selected),
                "reference_rejection_rate": float(
                    np.mean([not row["reference_valid"] for row in selected])
                ),
                "pass_rate": float(np.mean([row["decision"] == "PASS" for row in selected])),
                "unknown_rate": float(np.mean([row["decision"] == "UNKNOWN" for row in selected])),
                "flag_rate": float(np.mean([row["decision"] == "FLAG" for row in selected])),
            }
        )
    return rows


def _make_id_evidence(cfg, controlled, v1, dcfg, material, residue, seed):
    latents = make_latents(cfg["image_size"], residue, seed)
    evidence = {}
    visible = np.ones((cfg["image_size"], cfg["image_size"]), dtype=bool)
    mask = latents.residue_mask
    for state, state_cfg, is_controlled in (
        ("p", cfg, False),
        ("c", controlled, True),
    ):
        references, sample, visible, mask = simulate_structured_scene(
            state_cfg,
            material,
            residue,
            latents,
            seed,
            controlled=is_controlled,
        )
        for label, indices in FREQUENCY_INDICES.items():
            refs, selected_cfg = subset_structured(references, state_cfg, indices)
            selected_sample, _ = subset_structured(sample, state_cfg, indices)
            evidence[f"{state}{label}"] = infer_reference_ensemble(
                refs,
                selected_sample,
                selected_cfg,
                visible,
                v1,
                use_gain_guard=True,
            )["status"]
    drefs, dsample = simulate_diversity_observation(
        material,
        residue,
        latents,
        seed,
        reference_noise_log=0.008,
        sample_noise_log=0.012,
    )
    for name, indices in DIVERSITY_INDICES.items():
        evidence[name] = infer_diversity_features(drefs, dsample, indices, dcfg)["status"]
    return evidence, visible, mask


def _in_model_audit(cfg, controlled, v1, dcfg, policies) -> dict:
    methods = {
        "fixed_v2_1": ("d12", "p2", "c2"),
        "adaptive_v2_2_certificate": ("d12", "c3"),
    }
    counts = defaultdict(Counter)
    fov_counts = defaultdict(Counter)
    frame_records = defaultdict(list)
    for material_index, material in enumerate(MATERIALS.values()):
        for residue_index, residue in enumerate(RESIDUES.values()):
            for replicate in range(6):
                seed = 20260920 + material_index * 100_000 + residue_index * 1_000 + replicate
                evidence, visible, mask = _make_id_evidence(
                    cfg, controlled, v1, dcfg, material, residue, seed
                )
                evaluation = visible if residue.name == "clean" else mask
                group = (
                    "clean"
                    if residue.name == "clean"
                    else "matched_invisible"
                    if residue.name == "matched_invisible"
                    else "nonmatched"
                )
                for method, keys in methods.items():
                    status = combine_evidence([evidence[key] for key in keys])
                    values = status[evaluation]
                    counts[(method, group)]["PASS"] += int(np.sum(values == 1))
                    counts[(method, group)]["FLAG"] += int(np.sum(values == 2))
                    counts[(method, group)]["UNKNOWN"] += int(np.sum(values == 0))
                    counts[(method, group)]["pixels"] += int(values.size)
                for policy_name in ("fixed_v2_1", "adaptive_standard"):
                    result = run_policy(
                        policies[policy_name],
                        evidence,
                        visible,
                        reference_valid=True,
                        coverage_valid=True,
                    )
                    fov_counts[(policy_name, group)][result["decision"]] += 1
                    frame_records[(policy_name, group)].append(result["frames"])
    pixel_rows = []
    for (method, group), item in sorted(counts.items()):
        total = item["pixels"]
        pixel_rows.append(
            {
                "method": method,
                "group": group,
                "pixels": total,
                "pass_rate": item["PASS"] / total,
                "flag_rate": item["FLAG"] / total,
                "unknown_rate": item["UNKNOWN"] / total,
            }
        )
    fov_rows = []
    for (policy, group), item in sorted(fov_counts.items()):
        total = sum(item.values())
        frames = np.asarray(frame_records[(policy, group)])
        fov_rows.append(
            {
                "policy": policy,
                "group": group,
                "fovs": total,
                "pass_rate": item["PASS"] / total,
                "flag_rate": item["FLAG"] / total,
                "unknown_rate": item["UNKNOWN"] / total,
                "mean_frames": float(np.mean(frames)),
                "p95_frames": float(np.quantile(frames, 0.95)),
                "maximum_frames": int(np.max(frames)),
            }
        )
    return {
        "pixel_metrics": pixel_rows,
        "fov_metrics": fov_rows,
        "warning": (
            "This audit reuses the retained forward model and is an internal regression only; "
            "the domain-shift audit is the stronger synthetic challenge."
        ),
    }


def _adversarial_search(cfg, controlled, v1, dcfg, policy) -> dict:
    rng = np.random.default_rng(20260922)
    passes = []
    attempts = 400
    for index in range(attempts):
        shape = rng.choice(["droplet", "streak", "particles", "patchy"])
        support = float(10 ** rng.uniform(-2.7, -0.12))
        structured = rng.uniform(0.0, 0.16, size=6)
        diversity = rng.uniform(0.0, 0.13, size=12)
        if rng.random() < 0.25:
            structured[[0, 5]] = 0.0
        scenario = {
            "name": f"search_{index}",
            "group": "contaminated",
            "morphology": shape,
            "support": min(support, 0.75),
            "primary": structured.tolist(),
            "controlled": (structured * rng.uniform(0.8, 1.3)).tolist(),
            "diversity": diversity.tolist(),
        }
        evidence, visible, ref_valid, coverage_valid, failed, diag = _make_evidence(
            cfg,
            controlled,
            v1,
            dcfg,
            "stainless_steel",
            scenario,
            20270000 + index,
        )
        result = run_policy(
            policy,
            evidence,
            visible,
            reference_valid=ref_valid,
            coverage_valid=coverage_valid,
            failed_states=failed,
        )
        if result["decision"] == "PASS":
            passes.append(
                {
                    "case": scenario["name"],
                    "morphology": shape,
                    "requested_support_fraction": scenario["support"],
                    "realized_support_pixels": diag["support_pixels"],
                    "structured_max_log_attenuation": float(np.max(structured)),
                    "diversity_span_log": float(np.ptp(diversity)),
                    "frames": result["frames"],
                    "classification": (
                        "SPATIAL_SUPPORT_LIMIT"
                        if diag["support_pixels"] / cfg["image_size"] ** 2 < 0.05
                        else "BELOW_RETAINED_DECISION_BOUNDS"
                    ),
                    "parameters": scenario,
                }
            )
    passes.sort(
        key=lambda row: (
            row["realized_support_pixels"],
            row["structured_max_log_attenuation"] + row["diversity_span_log"],
        ),
        reverse=True,
    )
    return {
        "attempts": attempts,
        "passing_adversarial_cases": len(passes),
        "passing_fraction": len(passes) / attempts,
        "top_regressions": passes[:20],
        "interpretation": (
            "Search distribution is deliberately artificial; this is a boundary attack, "
            "not a prevalence or physical limit-of-detection estimate."
        ),
    }


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
    dcfg = DiversityConfig(
        v2_file["reference_consistency_log"],
        v2_file["pass_bound_log"],
        v2_file["flag_bound_log"],
        v1_file["minimum_reference_consensus"],
    )
    policies = retained_policies()
    records = []
    scenarios = _scenario_catalog()
    for material_index, material in enumerate(MATERIALS):
        for scenario_index, scenario in enumerate(scenarios):
            for replicate in range(5):
                seed = 20260921 + material_index * 100_000 + scenario_index * 1_000 + replicate
                evidence, visible, ref_valid, coverage_valid, failed, diagnostics = _make_evidence(
                    cfg, controlled, v1, dcfg, material, scenario, seed
                )
                for policy_name, policy in policies.items():
                    result = run_policy(
                        policy,
                        evidence,
                        visible,
                        reference_valid=ref_valid,
                        coverage_valid=coverage_valid,
                        failed_states=failed,
                    )
                    records.append(
                        {
                            "material": material,
                            "scenario": scenario["name"],
                            "group": scenario["group"],
                            "replicate": replicate,
                            "policy": policy_name,
                            "decision": result["decision"],
                            "frames": result["frames"],
                            "reason": result["reason"],
                            **diagnostics,
                        }
                    )
    summary = _summarize(records)
    selected = next(row for row in summary if row["policy"] == "adaptive_standard")
    adversarial = _adversarial_search(
        cfg, controlled, v1, dcfg, policies["adaptive_standard"]
    )
    return {
        "evidence_type": "SYNTHETIC_DOMAIN_SHIFT_AND_ADVERSARIAL_AUDIT_ONLY",
        "physical_experiment_executed": False,
        "independent_evaluation_model": {
            "description": (
                "Clean rendered observations are perturbed by arbitrary state-response vectors, "
                "alternative morphologies, Gaussian/impulsive noise, registration, missing-state, "
                "coverage and reference-anchor failures. Residue optical constants are not reused."
            ),
            "remaining_coupling": (
                "Clean backgrounds and inference code are shared; this is stronger than an "
                "in-model split but is not independent hardware data."
            ),
        },
        "policy_definitions": {
            name: {"name": policy.name, "stages": [asdict(stage) for stage in policy.stages]}
            for name, policy in policies.items()
        },
        "scenario_definitions": scenarios,
        "summary": summary,
        "selected_policy": {"name": "adaptive_standard", **selected},
        "group_summary": _group_summary(records),
        "reference_robustness": _reference_summary(records),
        "in_model_regression": _in_model_audit(cfg, controlled, v1, dcfg, policies),
        "records": records,
        "adversarial_search": adversarial,
        "pre_registered_decision_rule": (
            "At each acquired stage any pixel FLAG makes the FOV FLAG. PASS requires a named "
            "complete certificate, valid dated reference anchors, valid coverage, no failed "
            "required state, and at least 95% visible pixels PASS; otherwise UNKNOWN."
        ),
    }


def main() -> int:
    result = run()
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "final_research_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    rows = result["summary"]
    with (RESULTS / "final_policy_benchmark.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    regressions = {
        "evidence_type": result["evidence_type"],
        **result["adversarial_search"],
    }
    (ROOT / "experiments" / "adversarial_regressions.json").write_text(
        json.dumps(regressions, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result["summary"], indent=2))
    print(json.dumps(result["reference_robustness"], indent=2))
    print(json.dumps(result["adversarial_search"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
