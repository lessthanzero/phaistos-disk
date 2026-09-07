"""Unit tests for astronomical cycle and Saros hypothesis evaluation."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.astronomy.eclipse_cycles import (
    analyze_astronomy,
    compute_look_elsewhere_effect,
    evaluate_astronomical_matches,
)
from phaistos.astronomy.models import AstronomicalAnalysisResult


def test_astronomical_matches():
    corpus = load_transcription("godart_1995")
    matches = evaluate_astronomical_matches(corpus)
    assert len(matches) >= 3

    # Check Saros draconic match
    saros = next(m for m in matches if "Saros Draconic" in m.constant_name)
    assert saros.observed_value == 242
    assert saros.relative_error_pct == 0.0

    # Check Lunar nodal match
    nodal = next(m for m in matches if "Lunar Nodal" in m.constant_name)
    assert nodal.observed_value == 18
    assert nodal.relative_error_pct < 5.0


def test_look_elsewhere_effect():
    # Fast test for look-elsewhere probability
    p = compute_look_elsewhere_effect(num_trials=1000, tolerance_pct=2.0, seed=42)
    assert 0.0 < p < 1.0
    assert p > 0.10  # Demonstrates look-elsewhere vulnerability


def test_full_astronomy_analysis():
    corpus = load_transcription("godart_1995")
    result = analyze_astronomy(corpus, num_trials=500)
    assert isinstance(result, AstronomicalAnalysisResult)
    assert result.unfalsifiable_numerology_warning is True
    assert "ASTRONOMICAL SAROS" in result.skeptic_verdict
    assert result.stroke_distribution["Total"] == 18
