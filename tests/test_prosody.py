"""Unit tests for prosodic and strophic meter analysis."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.prosody.meter import (
    analyze_prosody,
    compute_mora_groups,
    detect_triad_refrain,
    calculate_triad_p_value,
)
from phaistos.prosody.models import StrophicAnalysisResult


def test_mora_groups():
    corpus = load_transcription("godart_1995")
    mora_groups = compute_mora_groups(corpus)
    assert len(mora_groups) == 61
    for mg in mora_groups:
        assert mg.estimated_morae >= mg.sign_count
        if mg.has_stroke:
            assert mg.estimated_morae == mg.sign_count + 1


def test_triad_refrain_detection():
    corpus = load_transcription("godart_1995")
    triad = detect_triad_refrain(corpus)
    assert triad is not None
    assert triad.refrain_sign_ids == ["02", "12", "31", "26"]
    assert triad.occurrences == ["A16", "A19", "A22"]
    assert triad.interval_steps == [3, 3]
    assert triad.is_strictly_periodic is True


def test_triad_p_value():
    corpus = load_transcription("godart_1995")
    # Quick surrogate test for test speed
    p_val = calculate_triad_p_value(corpus, num_surrogates=500, seed=42)
    assert p_val < 0.05  # Highly significant refrain periodicity


def test_full_prosody_analysis():
    corpus = load_transcription("godart_1995")
    result = analyze_prosody(corpus, num_surrogates=200)
    assert isinstance(result, StrophicAnalysisResult)
    assert result.total_groups == 61
    assert result.triad_refrain is not None
    assert result.periodicity_p_value < 0.05
    assert result.hymn_reconstruction is not None
    assert result.hymn_reconstruction.strophic_mora_equality is True
    assert len(result.hymn_reconstruction.triad_strophes) == 3
    for strophe in result.hymn_reconstruction.triad_strophes:
        assert strophe.total_morae == 14
    assert "PROSODIC HYMN ANALYSIS" in result.skeptic_verdict

