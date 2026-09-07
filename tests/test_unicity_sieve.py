"""Unit tests for Shannon Unicity Sieve & Degrees-of-Freedom Gatekeeper."""

import pytest
from phaistos.stats.unicity_sieve import evaluate_model_unicity


def test_anchor_subset_is_constrained():
    """Verify that a 7-anchor subset passes the unicity distance test."""
    res = evaluate_model_unicity(
        model_name="7_Anchors",
        mapped_signs_count=7,
        candidate_syllables_per_sign=3,
        target_lexicon_size=1,
        translated_words_count=0,
    )

    assert res.is_mathematically_constrained is True
    assert res.unicity_ratio < 0.20
    assert res.unicity_distance_required_signs < res.corpus_total_tokens
    assert "STRICTLY CONSTRAINED" in res.verdict


def test_full_translation_overfits():
    """Verify that claiming to translate 61 words into PIE or Egyptian overfits."""
    res = evaluate_model_unicity(
        model_name="Full_PIE_Translation",
        mapped_signs_count=45,
        candidate_syllables_per_sign=60,
        target_lexicon_size=3000,
        translated_words_count=61,
    )

    assert res.is_mathematically_constrained is False
    assert res.unicity_ratio > 1.0
    assert res.unicity_distance_required_signs > res.corpus_total_tokens
    assert "UNCONSTRAINED OVERFIT" in res.verdict
