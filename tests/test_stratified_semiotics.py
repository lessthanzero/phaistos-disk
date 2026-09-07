"""Tests for Stratified Semiotics and Tripartite Liturgical Grammar."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.ritual.models import RitualSignPlane
from phaistos.ritual.stratified_semiotics import get_plane_definitions, parse_liturgical_grammar


def test_plane_definitions_coverage():
    """Verify all 45 signs are classified into the 4 ritual planes."""
    defs = get_plane_definitions()
    assert len(defs) == 45

    # Check diagnostic sign planes
    assert defs["02"].assigned_plane == RitualSignPlane.THEONYMIC_INVOCATION
    assert defs["06"].assigned_plane == RitualSignPlane.THEONYMIC_INVOCATION
    assert defs["28"].assigned_plane == RitualSignPlane.MATERIA_SACRA_OFFERING
    assert defs["41"].assigned_plane == RitualSignPlane.MATERIA_SACRA_OFFERING
    assert defs["21"].assigned_plane == RitualSignPlane.SONIC_PERFORMANCE_CONTROL
    assert defs["12"].assigned_plane == RitualSignPlane.SONIC_PERFORMANCE_CONTROL


def test_parse_liturgical_grammar():
    """Verify liturgical parsing of all 61 sign groups."""
    corpus = load_transcription("godart_1995")
    res = parse_liturgical_grammar(corpus)

    assert res.total_groups == 61
    assert res.total_signs == 242
    assert res.theonymic_head_rate > 0.30  # At least 30% of groups have divine heads
    assert res.offering_presence_rate > 0.70  # Over 70% of groups contain sacrificial/votive realia

    # Check transition matrix properties
    assert "Plane_I_Theonymic" in res.plane_transition_matrix
    trans_from_theo = res.plane_transition_matrix["Plane_I_Theonymic"]
    assert trans_from_theo.get("Plane_III_Sonic", 0.0) > 0.30  # High transition to sonic/gong
