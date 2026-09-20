import json
from pathlib import Path

import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS, UNKNOWN, infer
from proof_clean_local_plan.src.simulation import make_scene

from rapid_proof_clean.phase1 import (
    V1Config,
    combine_measurement_states,
    infer_reference_ensemble,
    reference_consensus,
)

ROOT = Path(__file__).resolve().parents[1]


def config() -> dict:
    cfg = json.loads((ROOT / "proof_clean_local_plan" / "config.json").read_text())
    cfg["image_size"] = 8
    return cfg


def clean_reference(cfg: dict, rng: np.random.Generator) -> np.ndarray:
    return make_scene(cfg, rng, "clean")[0]


def controlled_config(cfg: dict) -> dict:
    result = dict(cfg)
    result["clean_variation_bound_pixel2"] = 0.01
    result["additive_noise_bound"] = 0.0002
    result["quantization_levels"] = 4096
    return result


def ensemble_for_scene(scene: tuple, cfg: dict, rng: np.random.Generator) -> np.ndarray:
    references = np.stack([scene[0], clean_reference(cfg, rng), clean_reference(cfg, rng)])
    return infer_reference_ensemble(
        references, scene[1], cfg, scene[3], V1Config(), use_gain_guard=True
    )["status"]


def test_primary_generator_remains_deterministic() -> None:
    cfg = config()
    implicit = make_scene(cfg, np.random.default_rng(91), "negative_blur_cancellation")
    explicit = make_scene(
        cfg, np.random.default_rng(91), "negative_blur_cancellation", measurement_state="primary"
    )
    for left, right in zip(implicit[:4], explicit[:4], strict=True):
        np.testing.assert_array_equal(left, right)


def test_reference_consensus_rejects_one_dirty_reference() -> None:
    cfg = config()
    rng = np.random.default_rng(92)
    dirty, sample, _, visible, _ = make_scene(cfg, rng, "dirty_reference")
    references = np.stack([dirty, clean_reference(cfg, rng), clean_reference(cfg, rng)])
    selected, confidence, distances = reference_consensus(references, cfg, V1Config())
    assert set(selected) == {1, 2}
    assert confidence == 2 / 3
    assert distances[0, 1] > V1Config().reference_consistency_bound_pixel2
    result = infer_reference_ensemble(
        references, sample, cfg, visible, V1Config(), use_gain_guard=True
    )
    assert np.all(result["status"] == FLAG)


def test_controlled_geometry_breaks_negative_cancellation() -> None:
    cfg = config()
    primary = make_scene(
        cfg, np.random.default_rng(93), "negative_blur_cancellation", measurement_state="primary"
    )
    controlled_cfg = controlled_config(cfg)
    secondary = make_scene(
        controlled_cfg,
        np.random.default_rng(94),
        "negative_blur_cancellation",
        measurement_state="controlled_geometry",
    )
    primary_status = infer(primary[0], primary[1], cfg, primary[3])["status"]
    secondary_status = infer(secondary[0], secondary[1], controlled_cfg, secondary[3])["status"]
    combined = combine_measurement_states(primary_status, secondary_status)
    assert np.all(primary_status == PASS)
    assert np.all(combined == FLAG)


def test_combiner_does_not_turn_unknown_into_pass() -> None:
    primary = np.array([[PASS, PASS, UNKNOWN, FLAG]], dtype=np.uint8)
    secondary = np.array([[PASS, UNKNOWN, PASS, UNKNOWN]], dtype=np.uint8)
    np.testing.assert_array_equal(
        combine_measurement_states(primary, secondary),
        np.array([[PASS, UNKNOWN, UNKNOWN, FLAG]], dtype=np.uint8),
    )


def test_retained_v1_preserves_clean_pass() -> None:
    cfg = config()
    primary_rng = np.random.default_rng(95)
    primary = make_scene(cfg, primary_rng, "clean")
    first = ensemble_for_scene(primary, cfg, primary_rng)
    controlled_cfg = controlled_config(cfg)
    controlled_rng = np.random.default_rng(96)
    secondary = make_scene(
        controlled_cfg,
        controlled_rng,
        "clean",
        measurement_state="controlled_geometry",
    )
    second = ensemble_for_scene(secondary, controlled_cfg, controlled_rng)
    assert np.all(combine_measurement_states(first, second) == PASS)


def test_invisible_residue_remains_a_retained_v1_false_clean() -> None:
    cfg = config()
    primary_rng = np.random.default_rng(97)
    primary = make_scene(cfg, primary_rng, "optically_invisible_residue")
    first = ensemble_for_scene(primary, cfg, primary_rng)
    controlled_cfg = controlled_config(cfg)
    controlled_rng = np.random.default_rng(98)
    secondary = make_scene(
        controlled_cfg,
        controlled_rng,
        "optically_invisible_residue",
        measurement_state="controlled_geometry",
    )
    second = ensemble_for_scene(secondary, controlled_cfg, controlled_rng)
    assert np.all(combine_measurement_states(first, second) == PASS)
