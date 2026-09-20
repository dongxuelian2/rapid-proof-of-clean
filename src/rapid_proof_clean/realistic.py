"""Physically motivated, assumption-driven optical scene simulator.

This module is deliberately not labelled as a validated digital twin.  It
combines Fresnel thin-film optics with an empirical structured-light blur
proxy, finite residue support, mixed specular/diffuse return, illumination
nonuniformity, exposure drift, quantization, sensor noise, and registration
error.  Its purpose is adversarial architecture comparison, not a real-world
limit-of-detection claim.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

WAVELENGTHS_NM = np.array([470.0, 550.0, 850.0])
ANGLES_DEG = np.array([15.0, 55.0])
POLARIZATIONS = ("s", "p")


@dataclass(frozen=True)
class Material:
    """Coarse optical constants used only in the assumption-driven model."""

    name: str
    refractive_index: complex
    base_modulation: float
    reference_blur_pixel2: float
    diffuse_fraction: float


@dataclass(frozen=True)
class Residue:
    """Synthetic residue family and its assumed optical effects."""

    name: str
    refractive_index: complex
    thickness_nm: float
    coverage: float
    blur_pixel2: float
    diffuse_fraction: float
    spectral_attenuation: tuple[float, float, float]
    matched_to_clean: bool = False
    primary_degenerate: bool = False


@dataclass(frozen=True)
class SceneLatents:
    """Nuisances shared across v1 and diversity-channel comparisons."""

    residue_mask: np.ndarray
    exposure_scale: float
    illumination_gradient: float
    registration_shift: tuple[int, int]
    roughness_delta_pixel2: float
    film_thickness_scale: float


MATERIALS = {
    "glass": Material("glass", 1.52 + 0.0j, 0.31, 0.55, 0.04),
    "stainless_steel": Material("stainless_steel", 2.5 + 3.3j, 0.28, 0.80, 0.12),
    "hdpe": Material("hdpe", 1.50 + 0.0j, 0.22, 1.05, 0.28),
    "glazed_ceramic": Material("glazed_ceramic", 1.60 + 0.0j, 0.25, 0.90, 0.20),
}

RESIDUES = {
    "clean": Residue("clean", 1.0 + 0.0j, 0.0, 0.0, 0.0, 0.0, (1.0, 1.0, 1.0)),
    "water_film": Residue(
        "water_film", 1.333 + 0.0j, 900.0, 0.65, 0.03, 0.01, (0.998, 0.998, 0.992)
    ),
    "oil_film": Residue(
        "oil_film", 1.47 + 0.0j, 1250.0, 0.65, 0.05, 0.01, (0.995, 0.997, 0.990)
    ),
    "protein_smear": Residue(
        "protein_smear", 1.43 + 0.015j, 4000.0, 0.55, 0.45, 0.18, (0.78, 0.88, 0.96)
    ),
    "detergent_crystals": Residue(
        "detergent_crystals", 1.49 + 0.0j, 9000.0, 0.35, 1.05, 0.34, (0.89, 0.92, 0.95)
    ),
    "particles": Residue(
        "particles", 1.55 + 0.002j, 15000.0, 0.30, 1.25, 0.42, (0.82, 0.86, 0.90)
    ),
    "primary_degenerate_film": Residue(
        "primary_degenerate_film",
        1.40 + 0.0j,
        0.0,
        0.65,
        0.0,
        0.0,
        (1.0, 1.0, 1.0),
        primary_degenerate=True,
    ),
    "matched_invisible": Residue(
        "matched_invisible",
        1.0 + 0.0j,
        0.0,
        0.65,
        0.0,
        0.0,
        (1.0, 1.0, 1.0),
        matched_to_clean=True,
    ),
}


def _cosine_in_medium(n_from: complex, n_to: complex, theta_from: float) -> complex:
    sine = n_from * np.sin(theta_from) / n_to
    return np.sqrt(1.0 - sine * sine + 0j)


def _fresnel_amplitude(
    n_left: complex,
    n_right: complex,
    cos_left: complex,
    cos_right: complex,
    polarization: str,
) -> complex:
    if polarization == "s":
        return (n_left * cos_left - n_right * cos_right) / (
            n_left * cos_left + n_right * cos_right
        )
    if polarization == "p":
        return (n_right * cos_left - n_left * cos_right) / (
            n_right * cos_left + n_left * cos_right
        )
    raise ValueError(f"unsupported polarization: {polarization}")


def interface_reflectance(
    substrate_index: complex, angle_deg: float, polarization: str
) -> float:
    """Air/substrate Fresnel intensity reflectance."""

    theta = np.deg2rad(angle_deg)
    cos_air = complex(np.cos(theta))
    cos_substrate = _cosine_in_medium(1.0 + 0j, substrate_index, theta)
    amplitude = _fresnel_amplitude(
        1.0 + 0j, substrate_index, cos_air, cos_substrate, polarization
    )
    return float(np.abs(amplitude) ** 2)


def thin_film_reflectance(
    film_index: complex,
    substrate_index: complex,
    thickness_nm: float,
    wavelength_nm: float,
    angle_deg: float,
    polarization: str,
) -> float:
    """Single coherent film on a semi-infinite substrate."""

    theta = np.deg2rad(angle_deg)
    cos_air = complex(np.cos(theta))
    cos_film = _cosine_in_medium(1.0 + 0j, film_index, theta)
    sine_film = np.sin(theta) / film_index
    sine_substrate = film_index * sine_film / substrate_index
    cos_substrate = np.sqrt(1.0 - sine_substrate * sine_substrate + 0j)
    r01 = _fresnel_amplitude(1.0 + 0j, film_index, cos_air, cos_film, polarization)
    r12 = _fresnel_amplitude(
        film_index, substrate_index, cos_film, cos_substrate, polarization
    )
    phase = 2.0 * np.pi * film_index * thickness_nm * cos_film / wavelength_nm
    round_trip = np.exp(2j * phase)
    amplitude = (r01 + r12 * round_trip) / (1.0 + r01 * r12 * round_trip)
    return float(np.abs(amplitude) ** 2)


def clean_signature(material: Material) -> np.ndarray:
    """Return shape ``(wavelength, angle, polarization)``."""

    signature = np.empty((len(WAVELENGTHS_NM), len(ANGLES_DEG), len(POLARIZATIONS)))
    for wi, _ in enumerate(WAVELENGTHS_NM):
        for ai, angle in enumerate(ANGLES_DEG):
            for pi, polarization in enumerate(POLARIZATIONS):
                specular = interface_reflectance(material.refractive_index, angle, polarization)
                signature[wi, ai, pi] = (1 - material.diffuse_fraction) * specular + (
                    material.diffuse_fraction * 0.04
                )
    return signature


def _degenerate_thickness(material: Material, residue: Residue) -> float:
    """Find a film nearly matched at the v1 state but distinct elsewhere."""

    clean = clean_signature(material)
    target = float(clean[1, 0].mean())
    best_score = np.inf
    best_thickness = 1000.0
    for thickness in np.linspace(80.0, 4000.0, 981):
        candidate = residue_signature(material, residue, thickness_nm=thickness, search=False)
        primary_error = abs(float(candidate[1, 0].mean()) - target) / max(target, 1e-5)
        diversity = float(np.max(np.abs(np.log((candidate + 1e-5) / (clean + 1e-5)))))
        score = primary_error - 0.025 * min(diversity, 2.0)
        if primary_error <= 0.012 and score < best_score:
            best_score = score
            best_thickness = float(thickness)
    return best_thickness


def residue_signature(
    material: Material,
    residue: Residue,
    *,
    thickness_nm: float | None = None,
    search: bool = True,
) -> np.ndarray:
    """Model a local residue-covered signature before spatial mixing."""

    clean = clean_signature(material)
    if residue.name == "clean" or residue.matched_to_clean:
        return clean.copy()
    thickness = residue.thickness_nm if thickness_nm is None else thickness_nm
    if residue.primary_degenerate and thickness_nm is None and search:
        thickness = _degenerate_thickness(material, residue)
    signature = np.empty_like(clean)
    for wi, wavelength in enumerate(WAVELENGTHS_NM):
        attenuation = residue.spectral_attenuation[wi]
        for ai, angle in enumerate(ANGLES_DEG):
            for pi, polarization in enumerate(POLARIZATIONS):
                coherent = thin_film_reflectance(
                    residue.refractive_index,
                    material.refractive_index,
                    thickness,
                    angle_deg=angle,
                    wavelength_nm=wavelength,
                    polarization=polarization,
                )
                signature[wi, ai, pi] = attenuation * (
                    (1 - residue.diffuse_fraction) * coherent
                    + residue.diffuse_fraction * 0.12
                )
    return np.maximum(signature, 1e-6)


def make_latents(image_size: int, residue: Residue, seed: int) -> SceneLatents:
    """Create a reproducible, finite-support stain and shared nuisance state."""

    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[:image_size, :image_size]
    if residue.name == "clean":
        mask = np.zeros((image_size, image_size), dtype=bool)
    else:
        radius_x = image_size * np.sqrt(max(residue.coverage, 0.02)) * rng.uniform(0.46, 0.62)
        radius_y = image_size * np.sqrt(max(residue.coverage, 0.02)) * rng.uniform(0.46, 0.62)
        center_x = image_size * rng.uniform(0.42, 0.58)
        center_y = image_size * rng.uniform(0.42, 0.58)
        field = ((xx - center_x) / radius_x) ** 2 + ((yy - center_y) / radius_y) ** 2
        waviness = 0.10 * np.sin(xx * 0.7 + rng.uniform(-np.pi, np.pi))
        mask = field + waviness <= 1.0
    return SceneLatents(
        residue_mask=mask,
        exposure_scale=float(np.exp(rng.normal(0.0, 0.035))),
        illumination_gradient=float(rng.uniform(-0.08, 0.08)),
        registration_shift=(int(rng.integers(-1, 2)), int(rng.integers(-1, 2))),
        roughness_delta_pixel2=float(rng.normal(0.0, 0.035)),
        film_thickness_scale=float(np.exp(rng.normal(0.0, 0.04))),
    )


def _roll_frames(frames: np.ndarray, shift: tuple[int, int]) -> np.ndarray:
    return np.roll(frames, shift=shift, axis=(-2, -1))


def simulate_structured_scene(
    cfg: dict,
    material: Material,
    residue: Residue,
    latents: SceneLatents,
    seed: int,
    *,
    controlled: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return three references, sample, visible mask, and contamination mask."""

    rng = np.random.default_rng(seed + (100_000 if controlled else 0))
    size = cfg["image_size"]
    frequencies = np.asarray(cfg["frequencies_cycles_per_screen"], dtype=float)
    frequencies /= cfg["screen_coordinate_width"]
    coordinate = np.linspace(0, cfg["screen_coordinate_width"], size, endpoint=False)
    xx, yy = np.meshgrid(coordinate, coordinate)
    spatial_x = np.linspace(-1.0, 1.0, size)[None, :]
    illumination = 1.0 + latents.illumination_gradient * spatial_x
    film = residue_signature(
        material,
        residue,
        thickness_nm=(
            _degenerate_thickness(material, residue) * latents.film_thickness_scale
            if residue.primary_degenerate
            else residue.thickness_nm * latents.film_thickness_scale
        ),
    )
    clean = clean_signature(material)
    primary_ratio = float(film[1, 0].mean() / max(clean[1, 0].mean(), 1e-6))
    if residue.matched_to_clean:
        primary_ratio = 1.0

    def render(is_sample: bool) -> np.ndarray:
        frames = np.empty((2, len(frequencies), 4, size, size))
        base_gain = float(rng.uniform(0.96, 1.04))
        if is_sample:
            base_gain *= latents.exposure_scale
        phase0 = rng.uniform(-np.pi, np.pi, size=(size, size))
        if controlled:
            b = 0.0
        elif is_sample:
            b = latents.roughness_delta_pixel2
        else:
            b = float(rng.normal(0.0, 0.02))
        noise_bound = float(cfg["additive_noise_bound"])
        levels = int(cfg["quantization_levels"])
        for orientation, axis in enumerate((xx, yy)):
            for fi, frequency in enumerate(frequencies):
                coefficient = 2 * np.pi**2 * frequency**2
                local_blur = material.reference_blur_pixel2 + b
                local_gain = np.ones((size, size))
                if is_sample:
                    local_blur = local_blur + residue.blur_pixel2 * latents.residue_mask
                    local_gain = np.where(latents.residue_mask, primary_ratio, 1.0)
                modulation = (
                    material.base_modulation
                    * base_gain
                    * illumination
                    * local_gain
                    * np.exp(-coefficient * local_blur)
                )
                for phase_index in range(4):
                    phase = 2 * np.pi * frequency * axis + phase0 + phase_index * np.pi / 2
                    image = 0.5 + modulation * np.cos(phase)
                    image += rng.uniform(-noise_bound, noise_bound, size=(size, size))
                    frames[orientation, fi, phase_index] = np.round(
                        np.clip(image, 0, 1) * (levels - 1)
                    ) / (levels - 1)
        if is_sample and latents.registration_shift != (0, 0):
            frames = _roll_frames(frames, latents.registration_shift)
        return frames

    references = np.stack([render(False) for _ in range(3)])
    sample = render(True)
    visible = np.ones((size, size), dtype=bool)
    return references, sample, visible, latents.residue_mask


def simulate_diversity_observation(
    material: Material,
    residue: Residue,
    latents: SceneLatents,
    seed: int,
    *,
    reference_noise_log: float,
    sample_noise_log: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return three reference and one sample spectro-goniometric cubes.

    Arrays have shape ``(R, W, A, P, H, W)`` and ``(W, A, P, H, W)``.
    Noise is multiplicative/log-normal, which keeps reflectance positive.
    """

    rng = np.random.default_rng(seed + 200_000)
    clean = clean_signature(material)
    thickness = (
        _degenerate_thickness(material, residue) * latents.film_thickness_scale
        if residue.primary_degenerate
        else residue.thickness_nm * latents.film_thickness_scale
    )
    covered = residue_signature(material, residue, thickness_nm=thickness)
    size = latents.residue_mask.shape[0]
    clean_cube = np.broadcast_to(clean[..., None, None], (*clean.shape, size, size)).copy()
    sample = clean_cube.copy()
    sample[..., latents.residue_mask] = covered[..., None]
    sample *= latents.exposure_scale
    reference_shape = (3, *sample.shape)
    references = np.broadcast_to(clean_cube, reference_shape).copy()
    references *= np.exp(rng.normal(0.0, reference_noise_log, size=reference_shape))
    sample *= np.exp(rng.normal(0.0, sample_noise_log, size=sample.shape))
    if latents.registration_shift != (0, 0):
        sample = _roll_frames(sample, latents.registration_shift)
    return references, sample
