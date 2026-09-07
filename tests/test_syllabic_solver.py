"""Tests for combinatorial syllabic admissibility solver and unicity guards."""

from phaistos.corpus.loader import load_transcription
from phaistos.decipherment.solver import (
    evaluate_syllabic_admissibility,
    LANGUAGE_TEMPLATES,
)


def test_language_templates():
    assert "mycenaean_greek" in LANGUAGE_TEMPLATES
    assert "minoan_linear_a" in LANGUAGE_TEMPLATES
    assert "syllabic_luwian" in LANGUAGE_TEMPLATES
    assert "northwest_semitic" in LANGUAGE_TEMPLATES


def test_syllabic_admissibility_falsification_vs_noise():
    corpus = load_transcription("godart_1995")
    res = evaluate_syllabic_admissibility(
        corpus=corpus,
        target_language="minoan_linear_a",
        n_surrogates=50,
        seed=42,
    )
    assert res.tested_groups_count == 61
    assert res.observed_admissibility_rate == 100.0
    # Crucial epistemic check: shuffled null also produces 100% CV legality!
    assert res.null_mean_admissibility_rate == 100.0
    assert res.is_falsified is True
    assert "FALSIFIED" in res.skeptic_verdict
