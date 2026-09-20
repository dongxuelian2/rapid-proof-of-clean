import numpy as np

from rapid_proof_clean.realistic import (
    MATERIALS,
    RESIDUES,
    clean_signature,
    interface_reflectance,
    make_latents,
    residue_signature,
    simulate_diversity_observation,
    thin_film_reflectance,
)


def test_zero_thickness_matches_bare_interface() -> None:
    substrate = MATERIALS["glass"].refractive_index
    for polarization in ("s", "p"):
        expected = interface_reflectance(substrate, 15.0, polarization)
        actual = thin_film_reflectance(1.40 + 0j, substrate, 0.0, 550.0, 15.0, polarization)
        np.testing.assert_allclose(actual, expected, rtol=1e-12)


def test_matched_invisible_is_exactly_clean_in_all_retained_states() -> None:
    for material in MATERIALS.values():
        np.testing.assert_array_equal(
            residue_signature(material, RESIDUES["matched_invisible"]),
            clean_signature(material),
        )


def test_primary_degenerate_film_has_diversity_contrast() -> None:
    material = MATERIALS["glass"]
    clean = clean_signature(material)
    film = residue_signature(material, RESIDUES["primary_degenerate_film"])
    primary_relative_error = abs(film[1, 0].mean() - clean[1, 0].mean()) / clean[1, 0].mean()
    assert primary_relative_error < 0.02
    assert np.max(np.abs(np.log(film / clean))) > 0.09


def test_diversity_simulator_shapes() -> None:
    residue = RESIDUES["oil_film"]
    latents = make_latents(8, residue, 7)
    references, sample = simulate_diversity_observation(
        MATERIALS["stainless_steel"],
        residue,
        latents,
        7,
        reference_noise_log=0.0,
        sample_noise_log=0.0,
    )
    assert references.shape == (3, 3, 2, 2, 8, 8)
    assert sample.shape == (3, 2, 2, 8, 8)
