"""Unit tests for the Ecological and Geographic Constraint Layer."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.geography.ecological_constraints import evaluate_ecological_constraints
from phaistos.geography.ecological_models import EcologicalConstraintResult


def test_ecological_constraints_evaluation():
    corpus = load_transcription("godart_1995")
    result = evaluate_ecological_constraints(corpus)

    assert isinstance(result, EcologicalConstraintResult)
    assert result.total_signs_analyzed == 45

    # Check domains
    domains = {d.domain: d for d in result.domain_distribution}
    assert len(domains) == 7
    assert "DIVINE_SKY" in domains
    assert "HUMAN_SOCIAL" in domains
    assert "AGRICULTURAL_LAND" in domains
    assert "FLORA" in domains
    assert "FAUNA" in domains
    assert "MARINE_WATER" in domains
    assert "CRAFT_TRADE" in domains

    # Counts
    assert result.flora_signs_count >= 4
    assert result.fauna_signs_count >= 7
    assert result.marine_signs_count >= 3


    # Anthropogenic landscape check
    assert 50.0 < result.anthropogenic_landscape_score < 80.0
    assert result.bayesian_mean_confidence > 0.85

    # Falsification audit
    falsified_texts = [f["falsified_claim"] for f in result.falsification_audit]
    assert any("papyrus" in f.lower() for f in falsified_texts)
    assert any("lion" in f.lower() for f in falsified_texts)

    # Skeptic verdict
    assert "ECOLOGICAL & GEOGRAPHIC CONSTRAINT AUDIT" in result.skeptic_verdict
