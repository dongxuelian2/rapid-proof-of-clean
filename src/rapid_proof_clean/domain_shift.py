"""Materially different evaluation perturbations for optical evidence.

These utilities operate on generated frames rather than sharing the retained
simulator's residue forward model.  They support non-parametric state response,
alternative morphology, common-mode reference corruption and non-uniform noise.
They remain synthetic and do not define real prevalence distributions.
"""

from __future__ import annotations

import numpy as np


def morphology_mask(
    size: int,
    kind: str,
    support_fraction: float,
    seed: int,
) -> np.ndarray:
    """Return a deterministic morphology with normalized pixel support."""

    if not 0 <= support_fraction <= 1:
        raise ValueError("support_fraction must be in [0, 1]")
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[:size, :size]
    target = max(1, int(round(size * size * support_fraction)))
    if kind == "uniform":
        return np.ones((size, size), dtype=bool)
    if kind == "droplet":
        radius = np.sqrt(target / np.pi)
        cx = rng.uniform(0.3, 0.7) * (size - 1)
        cy = rng.uniform(0.3, 0.7) * (size - 1)
        return (xx - cx) ** 2 + (yy - cy) ** 2 <= radius**2
    if kind == "streak":
        width = max(1, int(round(target / size)))
        start = int(rng.integers(0, max(1, size - width + 1)))
        mask = np.zeros((size, size), dtype=bool)
        mask[:, start : start + width] = True
        return mask
    if kind == "edge":
        width = max(1, int(round(target / size)))
        mask = np.zeros((size, size), dtype=bool)
        mask[:, :width] = True
        return mask
    if kind == "particles":
        mask = np.zeros((size, size), dtype=bool)
        indices = rng.choice(size * size, size=min(target, size * size), replace=False)
        mask.flat[indices] = True
        return mask
    if kind == "subpixel_proxy":
        mask = np.zeros((size, size), dtype=bool)
        mask[int(rng.integers(size)), int(rng.integers(size))] = True
        return mask
    if kind == "patchy":
        field = rng.normal(size=(size, size))
        for _ in range(3):
            field = (
                field
                + np.roll(field, 1, 0)
                + np.roll(field, -1, 0)
                + np.roll(field, 1, 1)
                + np.roll(field, -1, 1)
            ) / 5
        threshold = np.partition(field.ravel(), -target)[-target]
        return field >= threshold
    raise ValueError(f"unsupported morphology: {kind}")


def apply_structured_response(
    frames: np.ndarray,
    mask: np.ndarray,
    frequency_log_attenuation: np.ndarray,
    *,
    gain: float = 1.0,
) -> np.ndarray:
    """Apply an arbitrary frequency response to reference or sample frames."""

    if frames.shape[-5] != 2 or frames.shape[-3] != 4:
        raise ValueError("frames must end in (2,F,4,H,W)")
    frequency_log_attenuation = np.asarray(frequency_log_attenuation, dtype=float)
    if frames.shape[-4] != len(frequency_log_attenuation):
        raise ValueError("frequency response length mismatch")
    output = frames.copy()
    scale = np.exp(-frequency_log_attenuation)
    for fi, factor in enumerate(scale):
        view = output[..., :, fi, :, :, :]
        changed = 0.5 + gain * factor * (view - 0.5)
        view[..., mask] = changed[..., mask]
    return np.clip(output, 0.0, 1.0)


def apply_diversity_response(
    cube: np.ndarray,
    mask: np.ndarray,
    feature_log_attenuation: np.ndarray,
    *,
    gain: float = 1.0,
) -> np.ndarray:
    """Apply arbitrary 12-state log attenuation to a diversity cube."""

    if cube.shape[-5:-2] != (3, 2, 2):
        raise ValueError("cube must end in (3,2,2,H,W)")
    attenuation = np.asarray(feature_log_attenuation, dtype=float)
    if attenuation.shape != (12,):
        raise ValueError("feature response must contain 12 values")
    output = cube.copy()
    leading = output.shape[:-5]
    flat = output.reshape(*leading, 12, *output.shape[-2:])
    changed = flat * (gain * np.exp(-attenuation))[..., None, None]
    flat[..., mask] = changed[..., mask]
    return np.maximum(output, 1e-9)


def add_evaluation_noise(
    values: np.ndarray,
    seed: int,
    *,
    gaussian_sigma: float,
    outlier_probability: float = 0.0,
    outlier_scale: float = 0.0,
) -> np.ndarray:
    """Gaussian plus sparse impulsive noise, unlike the design generators."""

    rng = np.random.default_rng(seed)
    output = values + rng.normal(0.0, gaussian_sigma, size=values.shape)
    if outlier_probability > 0:
        outliers = rng.random(values.shape) < outlier_probability
        output += outliers * rng.normal(0.0, outlier_scale, size=values.shape)
    return np.clip(output, 1e-9, 1.0)
