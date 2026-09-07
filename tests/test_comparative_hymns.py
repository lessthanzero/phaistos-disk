"""Unit tests for comparative Eastern Mediterranean rubrication and prosody."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.prosody.comparative_hymns import evaluate_comparative_prosody, ComparativeProsodyResult


def test_comparative_prosody():
    corpus = load_transcription("godart_1995")
    res = evaluate_comparative_prosody(corpus)

    assert isinstance(res, ComparativeProsodyResult)
    assert len(res.comparative_corpora) == 3
    assert 25.0 <= res.phaistos_mean_strophe_morae <= 28.0
    assert 28.0 <= res.phaistos_cadence_density_pct <= 31.0

    # KS tests: distributions should not be rejected as different (p > 0.05)
    assert res.ks_test_egyptian_p_value > 0.05
    assert res.ks_test_hurrian_p_value > 0.05

    # Verdicts
    assert "LITURGICAL RUBRICATION HOMOLOGY SUPPORTED" in res.rubrication_homology_verdict
    assert "EASTERN MEDITERRANEAN PROSODIC SYNTHESIS" in res.skeptic_verdict
