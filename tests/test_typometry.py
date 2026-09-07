"""Unit tests for typometry and workshop overlap analysis."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.typometry.overlap_analyzer import evaluate_workshop_typometry
from phaistos.typometry.models import WorkshopMatrixResult


def test_typometry_evaluation():
    corpus = load_transcription("godart_1995")
    result = evaluate_workshop_typometry(corpus)

    assert isinstance(result, WorkshopMatrixResult)
    assert result.total_punches_used == 45
    assert result.total_impressions == 242
    assert result.mean_punch_reuse > 5.0
    assert result.max_punch_reuse == 20  # Sign 02 (20x in Godart 1995)
    assert result.palimpsest_corrections_count == 3
    assert result.tool_switching_overhead_score > 90.0
    assert "WORKSHOP PROOF-OF-CONCEPT" in result.skeptic_verdict
