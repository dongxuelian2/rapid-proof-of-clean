import numpy as np

from rapid_proof_clean.reference_integrity import qualify_reference_features


def signature(scale: float = 1.0) -> np.ndarray:
    values = np.linspace(0.1, 0.4, 12).reshape(12, 1, 1) * scale
    return np.broadcast_to(values, (12, 4, 4)).copy()


def test_anchor_detects_consistent_common_mode_shape_drift() -> None:
    anchor = signature()
    shifted = signature()
    shifted[:4] *= 0.75
    references = np.stack([shifted, shifted, shifted])
    result = qualify_reference_features(references, anchor=anchor)
    assert result["pairwise_confidence"] == 1.0
    assert not result["valid"]
    assert result["reason"] == "common_mode_anchor_drift"


def test_independent_outlier_is_trimmed_with_anchor() -> None:
    anchor = signature()
    outlier = signature()
    outlier[:4] *= 0.70
    references = np.stack([outlier, signature(), signature()])
    result = qualify_reference_features(references, anchor=anchor)
    assert result["valid"]
    assert set(result["selected"]) == {1, 2}


def test_no_anchor_does_not_pretend_common_mode_is_known() -> None:
    references = np.stack([signature(), signature(), signature()])
    result = qualify_reference_features(references, anchor=None)
    assert not result["valid"]
    assert result["reason"] == "common_mode_unidentified_no_anchor"
