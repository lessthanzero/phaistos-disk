"""Unit tests for Bronze Age Liturgical Alignment Engine."""

import pytest
from phaistos.comparative.libation_alignment import load_bronze_age_liturgies, align_liturgical_clauses


def test_load_bronze_age_liturgies():
    """Verify loading of canonical Bronze Age liturgies (Linear A, Hurrian H6, Arkalochori)."""
    liturgies = load_bronze_age_liturgies()
    assert len(liturgies) >= 4

    linear_a = next(l for l in liturgies if l.id == "LIT_LINEAR_A_LIBATION")
    assert linear_a.script == "Linear A"
    assert len(linear_a.canonical_formula_words) == 5
    assert linear_a.canonical_formula_words[0]["word"] == "JA-SA-SA-RA-ME"

    hurrian = next(l for l in liturgies if l.id == "LIT_HURRIAN_HYMN_H6")
    assert "Ugarit" in hurrian.provenance
    assert hurrian.cadence_type == "NOTATED_MUSICAL_REST"


def test_align_liturgical_clauses():
    """Verify structural alignment and null permutation significance."""
    report = align_liturgical_clauses(n_surrogates=200, seed=42)

    assert report.total_disc_clauses == 14
    assert len(report.top_alignments) >= 5
    assert report.linear_a_formula_concordance_pct > 85.0
    assert report.hurrian_h6_cadence_concordance_pct > 90.0

    # Z-score vs random surrogate baseline should exceed +5.0
    assert report.null_surrogate_z_score > 5.0
    assert report.null_surrogate_p_value < 0.01
    assert "STATISTICALLY ROBUST" in report.skeptic_verdict
