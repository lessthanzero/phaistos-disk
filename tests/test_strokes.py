"""Unit tests for Frontier A: Epigraphic and metric analysis of the 18 oblique strokes."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.epigraphy.models import StrokeAnalysisResult
from phaistos.epigraphy.strokes import evaluate_oblique_strokes


def test_evaluate_oblique_strokes():
    corpus = load_transcription("godart_1995")
    result = evaluate_oblique_strokes(corpus)

    assert isinstance(result, StrokeAnalysisResult)
    assert result.total_strokes == 18
    assert result.side_a_strokes == 10
    assert result.side_b_strokes == 8

    # Positional check: 100% attached to terminal sign of group
    for occ in result.occurrences:
        assert occ.is_terminal is True

    # Check terminal sign distribution: 07 is most frequent (4x)
    assert result.sign_distribution["07"] == 4
    assert result.sign_distribution["08"] == 3
    assert result.sign_distribution["26"] == 3
    assert result.sign_distribution["01"] == 2

    # Virama evaluation
    v_eval = result.virama_eval
    assert v_eval.terminal_position_rate == 1.0
    assert v_eval.textual_coverage_pct < 35.0
    assert len(v_eval.lexical_inconsistency_instances) > 0
    assert "FALSIFIED" in v_eval.falsification_verdict

    # Musical ictus evaluation
    i_eval = result.ictus_eval
    assert i_eval.side_a_triad_responsion_match is True
    assert i_eval.side_b_stanza_cadence_count == 4
    assert i_eval.side_b_stanza_cadence_p_value < 0.05
    assert "STRONGLY SUPPORTED" in i_eval.support_verdict

    # Skeptic verdict
    assert "SKEPTICAL RESOLUTION" in result.skeptic_verdict
