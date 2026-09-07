"""Unit tests for Frontier D: 3D clay shrinkage and punch reconstruction."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.typometry.models import ShrinkageReconstructionResult
from phaistos.typometry.shrinkage_model import reconstruct_punches_and_shrinkage


def test_clay_shrinkage_and_punch_reconstruction():
    corpus = load_transcription("godart_1995")
    result = reconstruct_punches_and_shrinkage(corpus)

    assert isinstance(result, ShrinkageReconstructionResult)
    assert len(result.punches) == 45

    profile = result.shrinkage_profile
    assert 7.0 < profile.total_linear_shrinkage_pct < 10.0
    assert profile.disc_wet_diameter_mm > profile.disc_fired_diameter_mm
    assert profile.disc_wet_diameter_mm > 170.0

    # Expansion factor should be ~1.085 - 1.095
    assert 1.07 < result.mean_expansion_factor < 1.12

    # Every reconstructed punch should be strictly larger than fired impression
    for p in result.punches:
        assert p.reconstructed_punch_width_mm > p.fired_width_mm
        assert p.reconstructed_punch_height_mm > p.fired_height_mm
        assert p.reconstructed_punch_area_mm2 > p.fired_area_mm2
        assert 10.0 < p.estimated_stamping_force_newtons < 100.0

    # Mean stamping force should match human thumb/palm ergonomics (20 - 60 N)
    assert 20.0 < result.mean_stamping_force_newtons < 60.0

    # Verdict checks
    assert "BRONZE" in result.punch_material_verdict
    assert "CERAMIC THERMAL SHRINKAGE" in result.skeptic_verdict
