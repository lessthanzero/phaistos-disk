"""Unit tests for Sign-by-Sign Liturgical Homology Breakdown Engine."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.ritual.homology_breakdown import (
    SIGN_HOMOLOGY_REGISTRY,
    LITURGICAL_ACTS,
    build_group_breakdown,
    get_all_groups_homology_manifest,
)


def test_sign_homology_registry_integrity():
    """Verify that all mapped signs have valid fields and confidence tiers."""
    assert len(SIGN_HOMOLOGY_REGISTRY) >= 15

    for sign_id, info in SIGN_HOMOLOGY_REGISTRY.items():
        assert "crop_id" in info
        assert "crop_title" in info
        assert "scene_id" in info
        assert "ritual_plane" in info
        assert "fresco_element" in info
        assert "scholarly_rationale" in info
        assert "confidence_tier" in info
        assert info["confidence_tier"] in {
            "PRIMARY_ARCHETYPE",
            "SECONDARY_PARALLEL",
            "STRUCTURAL_CLASSIFIER",
        }


def test_liturgical_acts_coverage():
    """Verify that the 5 Liturgical Acts span all 61 groups with zero overlap."""
    assert len(LITURGICAL_ACTS) == 5

    all_act_groups = []
    for act in LITURGICAL_ACTS:
        assert act["id"].startswith("ACT_")
        assert len(act["groups"]) > 0
        all_act_groups.extend(act["groups"])

    assert len(all_act_groups) == 61
    assert len(set(all_act_groups)) == 61  # No duplicate groups


def test_group_a16_breakdown():
    """Verify that group A16 displays the expected cartouche header and realia matches."""
    corpus = load_transcription()
    g_a16 = next(g for g in corpus.side_a.groups if g.id == "A16")
    bd = build_group_breakdown(g_a16, corpus)

    assert bd.group_id == "A16"
    assert bd.is_determinative_header is True
    assert bd.act_id == "ACT_II"
    assert len(bd.sign_matches) == 4

    # Sign 26 (Boat)
    boat_match = next(s for s in bd.sign_matches if s["sign_id"] == "26")
    assert boat_match["has_realia_match"] is True
    assert boat_match["crop_id"] == "crop_boat_model"
    assert boat_match["confidence_tier"] == "PRIMARY_ARCHETYPE"
    assert "galley model" in boat_match["fresco_element"].lower()

    # Sign 31 (Eagle)
    bird_match = next(s for s in bd.sign_matches if s["sign_id"] == "31")
    assert bird_match["has_realia_match"] is True
    assert bird_match["crop_id"] == "crop_labrys_double_axe"
    assert bird_match["confidence_tier"] == "PRIMARY_ARCHETYPE"


def test_all_groups_homology_manifest():
    """Verify complete serialization of the 61-group manifest."""
    manifest = get_all_groups_homology_manifest()
    assert len(manifest["acts"]) == 5
    assert len(manifest["groups"]) == 61
    assert "A01" in manifest["groups"]
    assert "B30" in manifest["groups"]
