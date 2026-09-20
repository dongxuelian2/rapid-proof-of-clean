from __future__ import annotations

import numpy as np

from rapid_proof_clean.robustness import Nuisance, perturb_frames


def test_identity_nuisance_preserves_frames() -> None:
    refs = np.full((3, 2, 2, 4, 3, 3), 0.6)
    sample = np.full((2, 2, 4, 3, 3), 0.4)
    cfg = {
        "quantization_levels": 256,
        "frequencies_cycles_per_screen": [2, 4],
        "screen_coordinate_width": 256,
    }
    got_refs, got_sample = perturb_frames(
        refs, sample, cfg, Nuisance("nominal"), np.random.default_rng(1)
    )
    assert np.allclose(got_refs, refs, atol=1 / 255)
    assert np.allclose(got_sample, sample, atol=1 / 255)


def test_registration_shift_is_spatial_only() -> None:
    refs = np.zeros((3, 2, 1, 4, 3, 3))
    sample = np.arange(72, dtype=float).reshape(2, 1, 4, 3, 3) / 100
    cfg = {
        "quantization_levels": 10_001,
        "frequencies_cycles_per_screen": [2],
        "screen_coordinate_width": 256,
    }
    _, shifted = perturb_frames(
        refs, sample, cfg, Nuisance("shift", registration_shift_px=1), np.random.default_rng(1)
    )
    assert np.allclose(shifted, np.roll(sample, shift=(1, 1), axis=(-2, -1)), atol=1 / 10_000)
