"""Unit tests for Virgula (Oblique Stroke) Phonology Evaluation."""

import pytest
from phaistos.linguistics.virgula_phonology import evaluate_virgula_phonology


def test_virgula_phonology_evaluation():
    """Verify that the oblique stroke distribution falsifies the coda hypothesis."""
    res = evaluate_virgula_phonology()

    assert res.total_strokes >= 15
    # Strokes appear on heterogeneous signs (> 6 distinct signs)
    assert res.distinct_signs_bearing_stroke > 6
    assert res.is_coda_restricted is False
    assert res.preferred_hypothesis == "CADENTIAL_REST_AND_METRIC_PAUSE"
    assert "FALSIFICATION OF HALANT/CODA HYPOTHESIS" in res.skeptic_verdict
