"""Tests for Sign Dossier Engine across physical, distributional, and comparative axes."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.semantics.sign_dossier import build_sign_dossier, build_all_sign_dossiers


def test_build_sign_dossier_02():
    """Verify sign monograph for Sign 02 (Plumed Head)."""
    corpus = load_transcription("godart_1995")
    dossier = build_sign_dossier("02", corpus=corpus)

    assert dossier.sign_id == "02"
    assert dossier.distribution.total_occurrences == 20
    assert dossier.distribution.initial_count >= 13
    assert dossier.distribution.functional_class == "invocational_clitic"
    assert dossier.physical.estimated_area_mm2 > 100.0
    assert "02-12" in dossier.distribution.top_collocations


def test_build_sign_dossier_44():
    """Verify sign monograph for Sign 44 (Small Axe)."""
    corpus = load_transcription("godart_1995")
    dossier = build_sign_dossier("44", corpus=corpus)

    assert dossier.sign_id == "44"
    assert dossier.distribution.total_occurrences == 1
    assert dossier.distribution.functional_class == "hapax_isolated"
    assert dossier.comparative.linear_a_counterpart == "AB08"
    assert "/a/" in dossier.comparative.proposed_phonetic_values
    assert "Tier A" in dossier.comparative.confidence_tier


def test_build_all_sign_dossiers():
    """Verify full 45-sign library generation."""
    corpus = load_transcription("godart_1995")
    all_dossiers = build_all_sign_dossiers(corpus=corpus)

    assert len(all_dossiers) == 45
    assert all_dossiers["12"].canonical_name == "SHIELD"
    assert all_dossiers["24"].canonical_name == "BEEHIVE"
