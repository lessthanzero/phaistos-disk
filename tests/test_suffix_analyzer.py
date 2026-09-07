"""Unit tests for Frontier B: Linear A suffix correspondence analyzer."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.comparative.suffix_analyzer import analyze_suffix_correspondence
from phaistos.comparative.suffix_models import SuffixAnalysisResult


def test_suffix_correspondence_analysis():
    corpus = load_transcription("godart_1995")
    result = analyze_suffix_correspondence(corpus)

    assert isinstance(result, SuffixAnalysisResult)
    assert result.total_groups == 61
    assert len(result.top_terminal_signs) >= 5

    # Check top terminal sign is 07 or 35 or 01
    top_ids = [s.sign_id for s in result.top_terminal_signs[:3]]
    assert "07" in top_ids
    assert "35" in top_ids

    # Check Sign 35 as ME vs TE
    me_test = result.sign_35_me_test
    te_test = result.sign_35_te_test

    assert me_test.tested_value == "ME"
    assert me_test.binomial_p_value < 1.0e-8
    assert "FALSIFIED" in me_test.verdict

    assert te_test.tested_value == "TE"
    assert te_test.likelihood > 0.05
    assert "STRONGLY SUPPORTED" in te_test.verdict

    assert result.likelihood_ratio_te_vs_me > 1.0e6

    # Aegean correspondences
    corr_signs = {c.sign_id: c for c in result.aegean_correspondences}
    assert "35" in corr_signs
    assert "07" in corr_signs
    assert "12" in corr_signs
    assert "18" in corr_signs

    # Skeptic verification
    assert "LINEAR A SUFFIX CORRESPONDENCE" in result.skeptic_verdict
    assert "Skeptic Rule Reminder" in result.skeptic_verdict
