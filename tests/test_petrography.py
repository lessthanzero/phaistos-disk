"""Unit tests for clay petrography and provenance analysis."""

import pytest
from phaistos.epigraphy.petrography import evaluate_clay_provenance, PetrographicAuditResult


def test_clay_provenance():
    res = evaluate_clay_provenance()
    assert isinstance(res, PetrographicAuditResult)
    assert res.candidate_regions_evaluated >= 4
    assert "Mesara" in res.top_match_region
    assert res.elemental_affinity_pct > 80.0
    assert res.exotic_origin_falsified is True
    assert "PETROGRAPHIC CLAY PROVENANCE" in res.skeptic_verdict

    # Check that Anatolia and Thera have low compatibility
    thera = next(m for m in res.matches if "cycladic" in m.region_id)
    assert thera.petrographic_compatibility_score < 30.0

    anatolia = next(m for m in res.matches if "anatolian" in m.region_id)
    assert anatolia.petrographic_compatibility_score < 30.0
