"""Unit tests for Side B strophic responsion analysis."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.prosody.strophic_b import evaluate_side_b_strophes, SideBStrophicResult


def test_side_b_strophes():
    corpus = load_transcription("godart_1995")
    res = evaluate_side_b_strophes(corpus, num_surrogates=500, seed=42)

    assert isinstance(res, SideBStrophicResult)
    assert res.total_groups == 30
    assert res.num_strophes == 5
    assert len(res.stanzas) == 5
    for s in res.stanzas:
        assert 20 <= s.total_morae <= 30
    assert res.stanza_mora_std < 2.0  # Very tight variance
    assert 0.90 <= res.cross_face_mora_ratio <= 1.05
    assert "SIDE B STROPHIC" in res.skeptic_verdict
