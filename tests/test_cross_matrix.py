"""Unit tests for cross-corpus comparative matrix evaluation."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.comparative.cross_matrix import evaluate_cross_matrix
from phaistos.comparative.models import CrossMatrixResult


def test_cross_matrix_evaluation():
    corpus = load_transcription("godart_1995")
    result = evaluate_cross_matrix(corpus)

    assert isinstance(result, CrossMatrixResult)
    assert len(result.corpora_analyzed) == 4
    assert result.total_signs_in_network > 280
    assert "21" in result.shared_glyph_parallels  # Double axe
    assert "38" in result.shared_glyph_parallels  # Rosette
    assert len(result.linear_a_lexical_matches) == 0  # 0 ABAC matches
    assert "CROSS-CORPUS COMPARATIVE NETWORK" in result.skeptic_verdict
