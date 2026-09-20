"""Deterministic synthetic nuisance-envelope helpers for the retained v1."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Nuisance:
    name: str
    exposure_scale: float = 1.0
    registration_shift_px: int = 0
    additive_noise: float = 0.0
    reference_aging: float = 0.0
    roughness_mismatch: float = 0.0
    illumination_gradient: float = 0.0
    missing_frequency: bool = False


def _requantize(frames: np.ndarray, levels: int) -> np.ndarray:
    return np.round(np.clip(frames, 0, 1) * (levels - 1)) / (levels - 1)


def perturb_frames(
    references: np.ndarray,
    sample: np.ndarray,
    cfg: dict,
    nuisance: Nuisance,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply declared measurement nuisances without changing ground truth.

    Reference aging and roughness mismatch are abstract frequency-dependent
    modulation losses. They are stress parameters, not calibrated physics.
    """

    refs = references.copy()
    sam = sample.copy()
    levels = int(cfg["quantization_levels"])

    # Scale modulation around the modeled DC level.
    sam = 0.5 + nuisance.exposure_scale * (sam - 0.5)

    if nuisance.registration_shift_px:
        sam = np.roll(
            sam,
            shift=(nuisance.registration_shift_px, nuisance.registration_shift_px),
            axis=(-2, -1),
        )

    frequencies = np.asarray(cfg["frequencies_cycles_per_screen"], dtype=float)
    frequencies /= float(cfg["screen_coordinate_width"])
    x = 2 * np.pi**2 * frequencies**2
    if nuisance.reference_aging:
        scale = np.exp(-x * nuisance.reference_aging)[None, None, :, None, None, None]
        refs = 0.5 + scale * (refs - 0.5)
    if nuisance.roughness_mismatch:
        scale = np.exp(-x * nuisance.roughness_mismatch)[None, :, None, None, None]
        sam = 0.5 + scale * (sam - 0.5)

    if nuisance.illumination_gradient:
        width = sam.shape[-1]
        gradient = np.linspace(
            1 - nuisance.illumination_gradient,
            1 + nuisance.illumination_gradient,
            width,
        )[None, None, None, None, :]
        sam = 0.5 + gradient * (sam - 0.5)

    if nuisance.additive_noise:
        sam += rng.uniform(-nuisance.additive_noise, nuisance.additive_noise, size=sam.shape)

    return _requantize(refs, levels), _requantize(sam, levels)
