"""Tests for Autonomous Skeptic Adversary Engine."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.skeptic.adversary import run_adversarial_falsification


def test_adversarial_falsification_phonetic_claim():
    """Verify that phonetic decipherment claims are rejected under Shannon unicity limits."""
    corpus = load_transcription("godart_1995")
    dossier = run_adversarial_falsification(
        claim="The disc translates to archaic Greek lyric poetry dedicated to Apollo and the goddess Dictynna",
        corpus=corpus,
        n_null_iterations=50,
        use_local_model=False,
        seed=42,
    )

    assert dossier.claim_type == "phonetic_translation"
    assert dossier.unicity_verdict == "UNCONSTRAINED_OVERFIT"
    assert dossier.statistical_verdict == "FALSIFIED"
    assert dossier.estimated_model_degrees_of_freedom > 929
    assert len(dossier.archaeological_contradictions) >= 3
    assert "Unicity Distance Violation" in dossier.archaeological_contradictions[0]
    assert "FALSIFIED" in dossier.final_verdict


def test_adversarial_falsification_calendar_claim():
    """Verify evaluation of astronomical calendar claims."""
    corpus = load_transcription("godart_1995")
    dossier = run_adversarial_falsification(
        claim="The spiral text encodes a 365-day solar calendar and planetary eclipse cycles",
        corpus=corpus,
        n_null_iterations=50,
        use_local_model=False,
        seed=42,
    )

    assert dossier.claim_type == "astronomical_calendar"
    assert len(dossier.archaeological_contradictions) >= 2
    assert "Duhoux Epigraphic Rule Applied" in dossier.local_model_critique


def test_adversarial_falsification_structural_hypothesis():
    """Verify structural invocation hypothesis testing."""
    corpus = load_transcription("godart_1995")
    dossier = run_adversarial_falsification(
        claim="The repeated prefix 02-12 functions as a recurrent structural invocation refrain",
        corpus=corpus,
        n_null_iterations=100,
        use_local_model=False,
        seed=42,
    )

    assert dossier.claim_type == "structural_hypothesis"
    assert dossier.unicity_verdict == "MATHEMATICALLY_CONSTRAINED"
    assert dossier.z_score > 3.0
    assert dossier.statistical_verdict == "SURVIVES_NULL_GAUNTLET"
