"""Unit tests for microscopic epigraphy and palimpsest analysis."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.epigraphy.overlap_micro import evaluate_epigraphic_microscopy
from phaistos.epigraphy.models import EpigraphicMicroAnalysisResult


def test_epigraphic_microscopy():
    corpus = load_transcription("godart_1995")
    result = evaluate_epigraphic_microscopy(corpus)

    assert isinstance(result, EpigraphicMicroAnalysisResult)
    assert result.total_overlaps_cataloged > 25
    assert result.outside_in_consistency_pct > 80.0
    assert len(result.palimpsests_cataloged) == 3
    assert len(result.radial_compression_gradient) == 8
    assert result.forgery_falsification_score > 99.0
    assert "MICROSCOPIC EPIGRAPHY" in result.skeptic_verdict

    # Check palimpsests
    palimpsest_ids = [p.group_id for p in result.palimpsests_cataloged]
    assert "A05" in palimpsest_ids
    assert "A08" in palimpsest_ids
    assert "B01" in palimpsest_ids
