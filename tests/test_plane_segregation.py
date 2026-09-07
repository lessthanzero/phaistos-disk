"""Tests for Monte Carlo Plane Segregation Engine."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.ritual.plane_segregation import evaluate_plane_segregation


def test_plane_segregation_monte_carlo():
    """Verify positional plane segregation is statistically non-random vs null surrogates."""
    corpus = load_transcription("godart_1995")
    res = evaluate_plane_segregation(corpus, n_iterations=100, seed=42)

    assert res.iterations_run == 100
    assert res.observed_segregation_score > 0.70
    assert res.observed_segregation_score > res.null_surrogate_mean
    assert res.z_score >= 3.0  # Significant at > 3 sigma
    assert res.empirical_p_value < 0.01
    assert res.is_statistically_significant is True
    assert res.shannon_unicity_satisfied is True
