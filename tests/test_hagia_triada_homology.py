"""Tests for Hagia Triada Sarcophagus Homology Engine."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.ritual.hagia_triada_homology import evaluate_hagia_triada_homology


def test_hagia_triada_homology_evaluation():
    """Verify correspondence between Phaistos Disc signs and the Hagia Triada scenes."""
    corpus = load_transcription("godart_1995")
    res = evaluate_hagia_triada_homology(corpus)

    assert res.total_scenes == 4
    assert res.shared_ritual_repertoire_count >= 20
    assert res.disc_scene_correspondence_rate > 0.80  # Over 80% of groups contain sarcophagus realia
    assert res.strophic_narrative_alignment_score > 80.0
