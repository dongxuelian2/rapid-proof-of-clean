import numpy as np
from proof_clean_local_plan.src.core import FLAG, PASS

from rapid_proof_clean.advanced import DiversityConfig, infer_diversity


def clean_cube(size: int = 4) -> np.ndarray:
    base = np.linspace(0.1, 0.4, 12).reshape(3, 2, 2, 1, 1)
    return np.broadcast_to(base, (3, 2, 2, size, size)).copy()


def test_diversity_ignores_uniform_exposure_change() -> None:
    sample = clean_cube() * 1.20
    references = np.stack([clean_cube(), clean_cube(), clean_cube()])
    result = infer_diversity(references, sample, "combined", DiversityConfig())
    assert np.all(result["status"] == PASS)


def test_diversity_flags_signature_shape_change() -> None:
    sample = clean_cube()
    sample[0] *= 0.65
    references = np.stack([clean_cube(), clean_cube(), clean_cube()])
    result = infer_diversity(references, sample, "combined", DiversityConfig())
    assert np.all(result["status"] == FLAG)
