"""Unit tests for Statistical Null Surrogate Homology Verification."""

import pytest
from phaistos.stats.homology_surrogate import evaluate_homology_significance


def test_evaluate_homology_significance():
    """Verify Monte Carlo null testing falsifies random iconographic drift."""
    res = evaluate_homology_significance(n_iterations=2000, seed=42)

    assert res.observed_realia_count == 19
    assert res.total_disc_signs == 45
    assert res.z_score > 5.0
    assert res.p_value < 0.001
    assert "REJECT NULL HYPOTHESIS" in res.skeptic_verdict
