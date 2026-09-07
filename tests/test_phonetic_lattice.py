"""Tests for Probabilistic Cross-Script Phonetic Lattice & Bayesian Sieve."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.decipherment.phonetic_lattice import build_phonetic_lattice


def test_phonetic_lattice_anchor_nodes():
    """Verify high-confidence cross-script anchors in the phonetic lattice."""
    corpus = load_transcription("godart_1995")
    res = build_phonetic_lattice(corpus)

    assert res.total_signs == 45
    assert res.secure_anchors_count >= 5
    assert res.entropy_reduction_pct > 20.0  # Significant entropy reduction over uniform space
    assert res.unicity_status == "MATHEMATICALLY_CONSTRAINED_FOR_ANCHOR_SUBSET"

    # Specific anchor signs
    node_12 = res.nodes["12"]
    assert node_12.is_secure_anchor is True
    assert node_12.candidates[0].syllable == "/ka/"

    node_44 = res.nodes["44"]
    assert node_44.is_secure_anchor is True
    assert node_44.candidates[0].syllable == "/a/"

    node_29 = res.nodes["29"]
    assert node_29.is_secure_anchor is True
    assert node_29.candidates[0].syllable == "/za/"


def test_phonetic_lattice_transliteration_samples():
    """Verify sample transliteration generation."""
    corpus = load_transcription("godart_1995")
    res = build_phonetic_lattice(corpus)

    assert len(res.sample_strophic_transliteration) == 5
    assert "A01" in res.sample_strophic_transliteration
    assert "ka" in res.sample_strophic_transliteration["A01"]
