import numpy as np

from rapid_proof_clean.domain_shift import (
    apply_diversity_response,
    apply_structured_response,
    morphology_mask,
)


def test_midband_response_leaves_endpoints_unchanged() -> None:
    frames = np.full((2, 6, 4, 4, 4), 0.6)
    profile = np.array([0.0, 0.0, 0.4, 0.4, 0.0, 0.0])
    shifted = apply_structured_response(frames, np.ones((4, 4), dtype=bool), profile)
    np.testing.assert_array_equal(shifted[:, [0, 5]], frames[:, [0, 5]])
    assert np.all(shifted[:, 2:4] < frames[:, 2:4])


def test_diversity_response_is_local_to_mask() -> None:
    cube = np.full((3, 2, 2, 4, 4), 0.3)
    mask = morphology_mask(4, "subpixel_proxy", 0.0, 1)
    shifted = apply_diversity_response(cube, mask, np.linspace(0.0, 0.3, 12))
    assert np.sum(np.any(shifted != cube, axis=(0, 1, 2))) == 1
