"""Tests ensuring epistemic category separation and statistical baselines."""

import pytest
from phaistos.core.provenance import ProvenanceCategory, ProvenanceRecord
from phaistos.corpus.loader import load_transcription
from phaistos.stats.frequency import (
    compute_sign_frequencies,
    compute_shannon_entropy,
    compute_positional_statistics,
)


def test_provenance_categories():
    """Verify strict separation between observation, transcription, and hypothesis."""
    obs = ProvenanceRecord(
        data={"overlap": "A01 punch 12 over punch 13"},
        category=ProvenanceCategory.OBSERVATION,
        source_ref="duhoux_1977",
    )
    assert obs.category == ProvenanceCategory.OBSERVATION

    hyp = ProvenanceRecord(
        data={"language": "Luwian", "sign_02": "/ti/"},
        category=ProvenanceCategory.HYPOTHESIS,
        source_ref="best_2004",
        confidence=0.1,
    )
    assert hyp.category == ProvenanceCategory.HYPOTHESIS
    assert hyp.category != obs.category


def test_statistical_baselines():
    """Verify entropy and positional statistics calculations."""
    corpus = load_transcription("godart_1995")
    counts = compute_sign_frequencies(corpus)

    entropy = compute_shannon_entropy(counts)
    # Natural language/syllabic entropy for 45 signs is typically between 4.0 and 5.2 bits
    assert 4.0 < entropy < 5.4

    pos_stats = compute_positional_statistics(corpus)
    # Sign 02 (Plumed Head) is strongly initial
    assert "02" in pos_stats
    assert pos_stats["02"]["p_initial"] > 0.5
