"""Unit tests for agglutinative morphology and prefix stripping."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.linguistics.morphology import evaluate_morphosyntax, parse_group
from phaistos.linguistics.models import MorphologicalAnalysisResult


def test_parse_group():
    corpus = load_transcription("godart_1995")
    g_a01 = corpus.side_a.groups[0]  # A01: 02-12-13-01-18
    parsed = parse_group(g_a01)
    assert parsed.prefix == "02-12"
    assert parsed.stem == ["13", "01"]
    assert parsed.suffix == "18"


def test_morphology_evaluation():
    corpus = load_transcription("godart_1995")
    res = evaluate_morphosyntax(corpus, num_surrogates=200, seed=42)

    assert isinstance(res, MorphologicalAnalysisResult)
    assert res.total_groups == 61
    assert res.unique_stems_after_stripping < res.unique_raw_groups
    assert res.vocabulary_compression_pct > 15.0
    assert "02-12" in res.prefix_frequencies
    assert res.monte_carlo_compression_p_value < 0.05
    assert "AGGLUTINATIVE MORPHOSYNTAX" in res.skeptic_verdict
