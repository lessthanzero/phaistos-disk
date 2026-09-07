"""Unit tests for Minoan Formulaic Clause Parser."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.ritual.clause_parser import parse_liturgical_clauses, get_clauses_manifest


def test_clause_parser_structure():
    """Verify that Disc groups are partitioned into 14 clauses (7 Side A, 7 Side B)."""
    corpus = load_transcription()
    clauses = parse_liturgical_clauses(corpus)

    assert len(clauses) == 14

    side_a_clauses = [c for c in clauses if c.side == "A"]
    side_b_clauses = [c for c in clauses if c.side == "B"]

    assert len(side_a_clauses) == 7
    assert len(side_b_clauses) == 7

    # Verify all 61 groups are partitioned without omission or duplicate
    all_clause_groups = []
    for c in clauses:
        all_clause_groups.extend(c.group_ids)

    assert len(all_clause_groups) == 61
    assert len(set(all_clause_groups)) == 61

    # Check first and last groups
    assert clauses[0].group_ids[0] == "A01"
    assert clauses[-1].group_ids[-1] == "B30"


def test_clause_morae_and_strokes():
    """Verify stroke rests and cartouche header identification."""
    clauses = parse_liturgical_clauses()

    # Clause A1 (A01) has stroke rest and 02-12 cartouche header
    c_a1 = next(c for c in clauses if c.clause_id == "CLAUSE_A1")
    assert c_a1.has_terminal_stroke is True
    assert c_a1.has_cartouche_header is True
    assert c_a1.total_morae == c_a1.total_signs + 1

    # Clause A6 (A16-A22 Lyric Triad)
    c_a6 = next(c for c in clauses if c.clause_id == "CLAUSE_A6")
    assert c_a6.has_cartouche_header is True
    assert c_a6.has_terminal_stroke is True  # A18 has stroke

    # Clause B1 (B01-B07)
    c_b1 = next(c for c in clauses if c.clause_id == "CLAUSE_B1")
    assert c_b1.has_cartouche_header is True
    assert c_b1.has_terminal_stroke is True


def test_clauses_manifest_serialization():
    """Verify serialization dictionary structure for UI and CLI."""
    manifest = get_clauses_manifest()
    assert manifest["total_clauses"] == 14
    assert len(manifest["side_a_clauses"]) == 7
    assert len(manifest["side_b_clauses"]) == 7
    assert len(manifest["group_to_clause"]) == 61
    assert manifest["group_to_clause"]["A01"] == "CLAUSE_A1"
    assert manifest["group_to_clause"]["B30"] == "CLAUSE_B7"
