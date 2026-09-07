"""Unit tests verifying corpus epigraphic invariants and Unicode integrity."""

import pytest
from phaistos.corpus.loader import load_signs, load_transcription
from phaistos.corpus.validator import validate_corpus, ValidationError


def test_signs_catalogue_completeness():
    """Verify exactly 45 unique Evans signs with correct Unicode mappings."""
    signs = load_signs()
    assert len(signs) == 45
    evans_ids = {s.evans_id for s in signs}
    assert len(evans_ids) == 45

    for s in signs:
        code_point = int(s.unicode_hex, 16)
        assert code_point in range(0x101D0, 0x101FD)
        assert s.unicode_char == chr(code_point)


def test_godart_1995_invariants():
    """Verify Godart 1995 transcription satisfies all epigraphic invariants."""
    corpus = load_transcription("godart_1995")
    validation_results = validate_corpus(corpus)

    assert validation_results["signs_catalogue_45_unique"] is True
    assert validation_results["unicode_code_points_match"] is True
    assert validation_results["group_count_61"] is True
    assert validation_results["total_signs_242"] is True
    assert validation_results["oblique_strokes_18"] is True
    assert validation_results["all_referenced_signs_valid"] is True

    # Check side counts
    assert corpus.side_a.group_count == 31
    assert corpus.side_b.group_count == 30
    assert corpus.side_a.oblique_stroke_count == 10
    assert corpus.side_b.oblique_stroke_count == 8


def test_sign_occurrences_generator():
    """Verify global indexing and positional boundary flags."""
    corpus = load_transcription("godart_1995")
    occurrences = corpus.all_occurrences()

    assert len(occurrences) == 242
    assert occurrences[0].group_id == "A01"
    assert occurrences[0].is_initial is True
    assert occurrences[0].is_final is False
    assert occurrences[0].global_index == 0

    # Last sign of A01 is final and has oblique stroke
    a01_final = occurrences[4]
    assert a01_final.group_id == "A01"
    assert a01_final.is_final is True
    assert a01_final.has_oblique_stroke is True
