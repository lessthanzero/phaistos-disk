"""Unit tests for Frontier C: Kober-Ventris Grid Factorization."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.linguistics.grid_factorization import (
    build_transition_matrix,
    compute_ppmi_matrix,
    factorize_kober_grid,
)
from phaistos.linguistics.models import KoberGridResult


def test_transition_matrix_construction():
    corpus = load_transcription("godart_1995")
    counts, all_signs, sign_to_idx = build_transition_matrix(corpus)

    assert counts.shape == (45, 45)
    assert len(all_signs) == 45
    assert counts.sum() > 150  # Total bigrams within groups


def test_ppmi_computation():
    corpus = load_transcription("godart_1995")
    counts, _, _ = build_transition_matrix(corpus)
    ppmi = compute_ppmi_matrix(counts)

    assert ppmi.shape == (45, 45)
    assert (ppmi >= 0.0).all()


def test_kober_grid_factorization():
    corpus = load_transcription("godart_1995")
    result = factorize_kober_grid(corpus, n_consonants=5, n_vowels=4, n_null_iterations=20)

    assert isinstance(result, KoberGridResult)
    assert result.n_signs == 45
    assert result.n_consonant_classes == 5
    assert result.n_vowel_classes == 4

    # All 45 signs must be mapped
    assert len(result.sign_consonant_map) == 45
    assert len(result.sign_vowel_map) == 45

    # Check metrics
    m = result.metrics
    assert len(m.explained_variance_ratio_svd) == 5
    assert m.explained_variance_ratio_svd[0] > 0.05
    assert m.frobenius_reconstruction_error > 0.0


    # Skeptic verification
    assert "KOBER-VENTRIS OBJECTIVE GRID" in result.skeptic_verdict
    assert "Shannon Unicity Guard" in result.skeptic_verdict
