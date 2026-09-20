# ruff: noqa: E402
"""Frozen multiscale spatial-certificate benchmark.

This study changes only FOV release aggregation.  Pixel evidence, references,
optical states and frame counts are inherited unchanged from v2.2.
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

from rapid_proof_clean.advanced import DiversityConfig
from rapid_proof_clean.phase1 import V1Config
from rapid_proof_clean.sequential import combine_evidence, retained_policies, run_policy
from rapid_proof_clean.spatial_certificate import candidate_certificates, spatial_outcome
from run_final_research import _make_evidence, _scenario_catalog, controlled_config, read_json

SUPPORTS = (0.001, 0.0025, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.10)
MORPHOLOGIES = (
    "compact_blob",
    "elongated_streak",
    "edge_blob",
    "corner_blob",
    "multiple_droplets",
    "dispersed_sparse",
    "psf_blurred",
    "registration_shifted",
)
SPLITS = {"design": 20300000, "validation": 20400000, "heldout": 20500000}


def _configs() -> tuple[dict, dict, V1Config, DiversityConfig]:
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
    return cfg, controlled, v1, dcfg


def _support_bin(value: float) -> str:
    if value < 0.01:
        return "<1%"
    if value < 0.02:
        return "1-2%"
    if value <= 0.05:
        return "2-5%"
    return ">5%"


def _profiles(rng: np.random.Generator) -> tuple[list[float], list[float], list[float]]:
    strength = float(rng.uniform(0.055, 0.22))
    shape = np.asarray([0.08, 0.20, 0.38, 0.62, 0.82, 1.0])
    structured = strength * shape * rng.uniform(0.85, 1.15, size=6)
    controlled = structured * rng.uniform(0.90, 1.25)
    diversity_shape = np.linspace(0.05, 1.0, 12)
    rng.shuffle(diversity_shape)
    diversity = strength * 0.85 * diversity_shape * rng.uniform(0.85, 1.15, size=12)
    return structured.tolist(), controlled.tolist(), diversity.tolist()


def _contaminated_scenario(
    morphology: str, support: float, rng: np.random.Generator, name: str
) -> dict:
    primary, controlled, diversity = _profiles(rng)
    base_morphology = morphology
    extra: dict = {}
    if morphology == "psf_blurred":
        base_morphology = "compact_blob"
        extra["psf_sigma"] = float(rng.uniform(0.7, 1.8))
    elif morphology == "registration_shifted":
        base_morphology = "compact_blob"
        extra["registration"] = [int(rng.choice([-1, 1])), int(rng.choice([-1, 0, 1]))]
    return {
        "name": name,
        "group": "contaminated",
        "morphology": base_morphology,
        "reported_morphology": morphology,
        "support": support,
        "primary": primary,
        "controlled": controlled,
        "diversity": diversity,
        **extra,
    }


def _clean_scenario(kind: str, rng: np.random.Generator, name: str) -> dict:
    zero6 = [0.0] * 6
    zero12 = [0.0] * 12
    scenario = {
        "name": name,
        "group": "clean",
        "morphology": "uniform",
        "reported_morphology": kind,
        "support": 1.0,
        "primary": zero6,
        "controlled": zero6,
        "diversity": zero12,
    }
    if kind == "texture":
        scenario.update(
            morphology="patchy",
            support=0.08,
            primary=(
                np.asarray([0, 0.006, 0.012, 0.020, 0.028, 0.036])
                * rng.uniform(0.7, 1.2)
            ).tolist(),
            controlled=(
                np.asarray([0, 0.006, 0.013, 0.021, 0.030, 0.038])
                * rng.uniform(0.7, 1.2)
            ).tolist(),
            diversity=(rng.uniform(0.0, 0.025, size=12)).tolist(),
        )
    elif kind == "roughness":
        scenario.update(
            morphology="dispersed_sparse",
            support=0.05,
            primary=rng.uniform(0.0, 0.035, size=6).tolist(),
            controlled=rng.uniform(0.0, 0.040, size=6).tolist(),
            diversity=rng.uniform(0.0, 0.028, size=12).tolist(),
        )
    elif kind == "illumination_gradient":
        scenario["illumination_gradient"] = float(rng.uniform(0.01, 0.05))
    elif kind == "edge_artifact":
        scenario.update(
            morphology="edge_blob",
            support=0.012,
            primary=rng.uniform(0.0, 0.040, size=6).tolist(),
            controlled=rng.uniform(0.0, 0.045, size=6).tolist(),
            diversity=rng.uniform(0.0, 0.030, size=12).tolist(),
        )
    elif kind == "registration_noise":
        scenario["registration"] = [int(rng.choice([-1, 1])), 0]
    return scenario


def _case_status(cfg, controlled, v1, dcfg, scenario: dict, seed: int) -> tuple:
    evidence, visible, ref_valid, coverage_valid, failed, diagnostics = _make_evidence(
        cfg, controlled, v1, dcfg, "stainless_steel", scenario, seed
    )
    if not ref_valid or not coverage_valid or failed:
        raise RuntimeError("small-support benchmark unexpectedly invalidated a global premise")
    status = combine_evidence([evidence["d12"], evidence["c3"]])
    return status, visible, diagnostics, evidence


def _benchmark_records() -> list[dict]:
    cfg, controlled, v1, dcfg = _configs()
    certificates = candidate_certificates()
    records = []
    for split, base_seed in SPLITS.items():
        case_index = 0
        for support in SUPPORTS:
            for morphology in MORPHOLOGIES:
                for replicate in range(2):
                    seed = base_seed + case_index
                    rng = np.random.default_rng(seed)
                    scenario = _contaminated_scenario(
                        morphology, support, rng, f"{split}_dirty_{case_index:03d}"
                    )
                    status, visible, diagnostics, _evidence = _case_status(
                        cfg, controlled, v1, dcfg, scenario, seed
                    )
                    truth = morphology_mask_for_truth(cfg["image_size"], scenario, seed)
                    baseline = spatial_outcome(status, visible, certificates["global_baseline"])
                    local_observable = bool(np.any(status[truth] != 1))
                    failure_class = (
                        "A_OBSERVABLE_SPATIALLY_DILUTED"
                        if baseline["decision"] == "PASS" and local_observable
                        else "B_LOCALLY_UNOBSERVABLE"
                        if baseline["decision"] == "PASS"
                        else "NOT_FALSE_CLEAN"
                    )
                    for name, certificate in certificates.items():
                        outcome = spatial_outcome(status, visible, certificate)
                        records.append(
                            {
                                "split": split,
                                "case": scenario["name"],
                                "group": "contaminated",
                                "support": support,
                                "support_bin": _support_bin(support),
                                "morphology": morphology,
                                "replicate": replicate,
                                "certificate": name,
                                "decision": outcome["decision"],
                                "reason": outcome["reason"],
                                "failure_class": failure_class,
                                "local_observable": local_observable,
                                "nonpass_pixels": int(np.sum((status != 1) & visible)),
                                "support_pixels": diagnostics["support_pixels"],
                                "maximum_component_area": baseline["metrics"].get(
                                    "maximum_component_area", -1
                                ),
                                "maximum_component_span": baseline["metrics"].get(
                                    "maximum_component_span", -1
                                ),
                            }
                        )
                    case_index += 1
        for nuisance in (
            "nominal",
            "texture",
            "roughness",
            "illumination_gradient",
            "edge_artifact",
            "registration_noise",
        ):
            for replicate in range(16):
                seed = base_seed + 10000 + case_index
                rng = np.random.default_rng(seed)
                scenario = _clean_scenario(nuisance, rng, f"{split}_clean_{case_index:03d}")
                status, visible, diagnostics, _evidence = _case_status(
                    cfg, controlled, v1, dcfg, scenario, seed
                )
                for name, certificate in certificates.items():
                    outcome = spatial_outcome(status, visible, certificate)
                    records.append(
                        {
                            "split": split,
                            "case": scenario["name"],
                            "group": "clean",
                            "support": 0.0,
                            "support_bin": "clean",
                            "morphology": nuisance,
                            "replicate": replicate,
                            "certificate": name,
                            "decision": outcome["decision"],
                            "reason": outcome["reason"],
                            "failure_class": "CLEAN_NUISANCE",
                            "local_observable": False,
                            "nonpass_pixels": int(np.sum((status != 1) & visible)),
                            "support_pixels": diagnostics["support_pixels"],
                            "maximum_component_area": spatial_outcome(
                                status, visible, certificates["global_baseline"]
                            )["metrics"]["maximum_component_area"],
                            "maximum_component_span": spatial_outcome(
                                status, visible, certificates["global_baseline"]
                            )["metrics"]["maximum_component_span"],
                        }
                    )
                case_index += 1
    return records


def morphology_mask_for_truth(size: int, scenario: dict, seed: int) -> np.ndarray:
    from rapid_proof_clean.domain_shift import morphology_mask

    mask = morphology_mask(size, scenario["morphology"], scenario["support"], seed + 91)
    if "psf_sigma" in scenario:
        from scipy import ndimage

        mask = ndimage.gaussian_filter(mask.astype(float), scenario["psf_sigma"])
        mask /= max(float(mask.max()), 1e-12)
        return mask >= 0.10
    if "registration" in scenario:
        return np.roll(mask, tuple(scenario["registration"]), axis=(-2, -1))
    return mask.astype(bool)


def _summaries(records: list[dict]) -> list[dict]:
    rows = []
    for split in SPLITS:
        for certificate in candidate_certificates():
            selected = [
                row
                for row in records
                if row["split"] == split and row["certificate"] == certificate
            ]
            dirty = [row for row in selected if row["group"] == "contaminated"]
            below = [row for row in dirty if row["support"] < 0.05]
            clean = [row for row in selected if row["group"] == "clean"]
            rows.append(
                {
                    "split": split,
                    "certificate": certificate,
                    "dirty_fovs": len(dirty),
                    "below_5pct_fovs": len(below),
                    "below_5pct_false_clean_rate": float(
                        np.mean([row["decision"] == "PASS" for row in below])
                    ),
                    "dirty_false_clean_rate": float(
                        np.mean([row["decision"] == "PASS" for row in dirty])
                    ),
                    "dirty_flag_rate": float(
                        np.mean([row["decision"] == "FLAG" for row in dirty])
                    ),
                    "dirty_unknown_rate": float(
                        np.mean([row["decision"] == "UNKNOWN" for row in dirty])
                    ),
                    "clean_fovs": len(clean),
                    "clean_pass_rate": float(
                        np.mean([row["decision"] == "PASS" for row in clean])
                    ),
                    "clean_false_flag_rate": float(
                        np.mean([row["decision"] == "FLAG" for row in clean])
                    ),
                    "clean_unknown_rate": float(
                        np.mean([row["decision"] == "UNKNOWN" for row in clean])
                    ),
                    "usable_coverage": float(
                        np.mean([row["decision"] != "UNKNOWN" for row in selected])
                    ),
                }
            )
    return rows


def _stratified(records: list[dict], split: str, certificate: str) -> list[dict]:
    selected = [
        row
        for row in records
        if row["split"] == split
        and row["certificate"] == certificate
        and row["group"] == "contaminated"
    ]
    output = []
    for dimension in ("support_bin", "morphology", "failure_class"):
        for value in sorted({row[dimension] for row in selected}):
            group = [row for row in selected if row[dimension] == value]
            output.append(
                {
                    "dimension": dimension,
                    "value": value,
                    "fovs": len(group),
                    "false_clean_rate": float(
                        np.mean([row["decision"] == "PASS" for row in group])
                    ),
                    "flag_rate": float(np.mean([row["decision"] == "FLAG" for row in group])),
                    "unknown_rate": float(
                        np.mean([row["decision"] == "UNKNOWN" for row in group])
                    ),
                }
            )
    return output


def _select_policy(summaries: list[dict]) -> tuple[str, list[dict]]:
    validation = {
        row["certificate"]: row for row in summaries if row["split"] == "validation"
    }
    baseline = validation["global_baseline"]
    profiles = ["aggressive", "balanced", "conservative"]
    pareto = []
    for name in profiles:
        row = validation[name]
        dominated = any(
            other != name
            and validation[other]["below_5pct_false_clean_rate"]
            <= row["below_5pct_false_clean_rate"]
            and validation[other]["clean_unknown_rate"] <= row["clean_unknown_rate"]
            and (
                validation[other]["below_5pct_false_clean_rate"]
                < row["below_5pct_false_clean_rate"]
                or validation[other]["clean_unknown_rate"] < row["clean_unknown_rate"]
            )
            for other in profiles
        )
        pareto.append({"certificate": name, "dominated": dominated, **row})
    eligible = [
        name
        for name in profiles
        if validation[name]["clean_pass_rate"] >= baseline["clean_pass_rate"] - 0.05
        and validation[name]["clean_false_flag_rate"] <= baseline["clean_false_flag_rate"]
    ]
    if not eligible:
        return "global_baseline", pareto
    selected = min(
        eligible,
        key=lambda name: (
            validation[name]["below_5pct_false_clean_rate"],
            validation[name]["dirty_false_clean_rate"],
            validation[name]["clean_unknown_rate"],
        ),
    )
    return selected, pareto


def _old_adversarial(selected_name: str) -> dict:
    cfg, controlled, v1, dcfg = _configs()
    certificates = candidate_certificates()
    rng = np.random.default_rng(20260922)
    counts = Counter()
    classifications = Counter()
    pass_support = Counter()
    pass_morphology = Counter()
    records = []
    for index in range(400):
        shape = str(rng.choice(["droplet", "streak", "particles", "patchy"]))
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
        status, visible, _, evidence = _case_status(
            cfg, controlled, v1, dcfg, scenario, 20270000 + index
        )
        truth = morphology_mask_for_truth(cfg["image_size"], scenario, 20270000 + index)
        policy = retained_policies()["adaptive_standard"]
        baseline = run_policy(
            policy,
            evidence,
            visible,
            reference_valid=True,
            coverage_valid=True,
        )
        selected = run_policy(
            policy,
            evidence,
            visible,
            reference_valid=True,
            coverage_valid=True,
            spatial_certificate=certificates[selected_name],
        )
        counts[f"baseline_{baseline['decision'].lower()}"] += 1
        counts[f"selected_{selected['decision'].lower()}"] += 1
        if baseline["decision"] == "PASS":
            classification = (
                "A_OBSERVABLE_SPATIALLY_DILUTED"
                if np.any(status[truth] != 1)
                else "B_LOCALLY_UNOBSERVABLE"
            )
            classifications[classification] += 1
            pass_support[_support_bin(scenario["support"])] += 1
            pass_morphology[shape] += 1
        records.append(
            {
                "search": "original_400_replay",
                "case": scenario["name"],
                "support": scenario["support"],
                "support_bin": _support_bin(scenario["support"]),
                "morphology": shape,
                "baseline_decision": baseline["decision"],
                "selected_decision": selected["decision"],
                "selected_reason": selected["reason"],
            }
        )
    return {
        "counts": dict(counts),
        "baseline_pass_classification": dict(classifications),
        "baseline_pass_by_support_bin": dict(pass_support),
        "baseline_pass_by_morphology": dict(pass_morphology),
        "truly_observation_matched": (
            "Excluded from this search by scope; the frozen separate impossibility "
            "control remains 100% PASS."
        ),
        "records": records,
    }


def _focused_adversarial(selected_name: str) -> dict:
    cfg, controlled, v1, dcfg = _configs()
    certificates = candidate_certificates()
    rng = np.random.default_rng(20600000)
    records = []
    reasons = Counter()
    selected_pass_support = Counter()
    selected_pass_morphology = Counter()
    for index in range(400):
        morphology = str(rng.choice(MORPHOLOGIES))
        support = float(10 ** rng.uniform(-3.1, -0.92))
        scenario = _contaminated_scenario(
            morphology,
            min(support, 0.12),
            rng,
            f"focused_{index}",
        )
        status, visible, _, evidence = _case_status(
            cfg, controlled, v1, dcfg, scenario, 20600000 + index
        )
        truth = morphology_mask_for_truth(cfg["image_size"], scenario, 20600000 + index)
        policy = retained_policies()["adaptive_standard"]
        baseline = run_policy(
            policy,
            evidence,
            visible,
            reference_valid=True,
            coverage_valid=True,
        )
        selected = run_policy(
            policy,
            evidence,
            visible,
            reference_valid=True,
            coverage_valid=True,
            spatial_certificate=certificates[selected_name],
        )
        if selected["decision"] == "PASS":
            reason = (
                "LOCALLY_UNOBSERVABLE"
                if np.all(status[truth] == 1)
                else "BELOW_SPATIAL_LIMITS"
            )
            reasons[reason] += 1
            selected_pass_support[_support_bin(scenario["support"])] += 1
            selected_pass_morphology[morphology] += 1
        records.append(
            {
                "search": "focused_heldout_400",
                "case": scenario["name"],
                "support": scenario["support"],
                "support_bin": _support_bin(scenario["support"]),
                "morphology": morphology,
                "baseline_decision": baseline["decision"],
                "selected_decision": selected["decision"],
                "selected_reason": selected["reason"],
            }
        )
    return {
        "attempts": 400,
        "baseline_passes": sum(row["baseline_decision"] == "PASS" for row in records),
        "selected_passes": sum(row["selected_decision"] == "PASS" for row in records),
        "selected_pass_reasons": dict(reasons),
        "selected_pass_by_support_bin": dict(selected_pass_support),
        "selected_pass_by_morphology": dict(selected_pass_morphology),
        "records": records,
    }


def _domain_shift_regression(selected_name: str) -> dict:
    cfg, controlled, v1, dcfg = _configs()
    certificate = candidate_certificates()[selected_name]
    policies = retained_policies()
    counts = defaultdict(Counter)
    materials = ("glass", "stainless_steel", "hdpe", "glazed_ceramic")
    for material_index, material in enumerate(materials):
        for scenario_index, scenario in enumerate(_scenario_catalog()):
            if scenario["group"] not in {"clean", "contaminated"}:
                continue
            if scenario["name"] == "observation_matched":
                continue
            for replicate in range(5):
                seed = 20260921 + material_index * 100_000 + scenario_index * 1_000 + replicate
                evidence, visible, ref_valid, coverage_valid, failed, _ = _make_evidence(
                    cfg, controlled, v1, dcfg, material, scenario, seed
                )
                for label, spatial in (("baseline", None), ("selected", certificate)):
                    result = run_policy(
                        policies["adaptive_standard"],
                        evidence,
                        visible,
                        reference_valid=ref_valid,
                        coverage_valid=coverage_valid,
                        failed_states=failed,
                        spatial_certificate=spatial,
                    )
                    counts[(label, scenario["group"])][result["decision"]] += 1
    output = {}
    for (label, group), values in sorted(counts.items()):
        total = sum(values.values())
        output[f"{label}_{group}"] = {
            "fovs": total,
            "pass_rate": values["PASS"] / total,
            "flag_rate": values["FLAG"] / total,
            "unknown_rate": values["UNKNOWN"] / total,
        }
    return output


def run() -> dict:
    records = _benchmark_records()
    summaries = _summaries(records)
    selected, pareto = _select_policy(summaries)
    old = _old_adversarial(selected)
    focused = _focused_adversarial(selected)
    domain_shift = _domain_shift_regression(selected)
    heldout = {
        row["certificate"]: row for row in summaries if row["split"] == "heldout"
    }
    baseline = heldout["global_baseline"]
    final = heldout[selected]
    conclusion = (
        "SUCCESS"
        if final["below_5pct_false_clean_rate"] <= baseline["below_5pct_false_clean_rate"] * 0.5
        and final["clean_pass_rate"] >= baseline["clean_pass_rate"] - 0.05
        else "PARTIAL"
        if final["below_5pct_false_clean_rate"] < baseline["below_5pct_false_clean_rate"]
        else "NEGATIVE_RESULT"
    )
    return {
        "evidence_type": "SYNTHETIC_SPATIAL_AGGREGATION_AUDIT_ONLY",
        "physical_experiment_executed": False,
        "baseline_head": "d9651deab163e0bbd651bbe2326d4d613d2a6e29",
        "baseline_v2_2": {
            "original_adversarial_passes": 136,
            "minimum_visible_pixel_pass_fraction": 0.95,
            "additional_measurement_frames": 0,
        },
        "split_protocol": {
            "design_seed": SPLITS["design"],
            "validation_seed": SPLITS["validation"],
            "frozen_heldout_seed": SPLITS["heldout"],
            "selection": (
                "Candidate forms are frozen; validation selects among aggressive/balanced/"
                "conservative under <=5 percentage-point clean-PASS loss. Held-out is report-only."
            ),
        },
        "candidate_definitions": {
            name: asdict(value) for name, value in candidate_certificates().items()
        },
        "selected_certificate": selected,
        "conclusion": conclusion,
        "summary": summaries,
        "pareto_validation": pareto,
        "heldout_stratified_baseline": _stratified(records, "heldout", "global_baseline"),
        "heldout_stratified_selected": _stratified(records, "heldout", selected),
        "heldout_comparison": {"baseline": baseline, "selected": final},
        "original_400_replay": {key: value for key, value in old.items() if key != "records"},
        "focused_adversarial": {key: value for key, value in focused.items() if key != "records"},
        "domain_shift_regression": domain_shift,
        "operational": {
            "additional_measurement_frames": 0,
            "evidence_maps_modified": False,
            "compute": (
                "Per 32x32 certificate: fixed tiles, three local convolutions, one 8-connected "
                "component labeling pass, and one edge-band reduction; O(pixels × scales)."
            ),
            "coverage_impact_metric": "reported as clean PASS/UNKNOWN and usable coverage",
        },
        "records": records,
        "adversarial_records": old["records"] + focused["records"],
    }


def main() -> int:
    result = run()
    experiments = ROOT / "experiments"
    (experiments / "small_support_benchmark.json").write_text(
        json.dumps(
            {key: value for key, value in result.items() if key != "adversarial_records"},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    records = result["records"]
    with (experiments / "small_support_benchmark.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    adversarial = {
        "evidence_type": result["evidence_type"],
        "selected_certificate": result["selected_certificate"],
        "original_400_replay": result["original_400_replay"],
        "focused_adversarial": result["focused_adversarial"],
    }
    (experiments / "spatial_adversarial_results.json").write_text(
        json.dumps(adversarial, indent=2) + "\n", encoding="utf-8"
    )
    adversarial_records = result["adversarial_records"]
    with (experiments / "spatial_adversarial_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(adversarial_records[0]))
        writer.writeheader()
        writer.writerows(adversarial_records)
    print(json.dumps(result["heldout_comparison"], indent=2))
    print(json.dumps(result["original_400_replay"], indent=2))
    print(json.dumps(result["focused_adversarial"], indent=2))
    print(f"selected={result['selected_certificate']} conclusion={result['conclusion']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
