"""Unit tests for Hagia Triada realia crop gallery and teleprompter synchronization."""

from pathlib import Path
import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.ritual.hagia_gallery import (
    REALIA_CROP_DEFINITIONS,
    get_hagia_gallery_manifest,
    get_realia_for_group,
)
from phaistos.visualizer.workbench import generate_workbench_html


def test_realia_crop_definitions_integrity():
    """Verify that all 10 diagnostic realia crops have valid coordinates and metadata."""
    assert len(REALIA_CROP_DEFINITIONS) == 10

    for defn in REALIA_CROP_DEFINITIONS:
        assert "id" in defn
        assert "title" in defn
        assert "scene_id" in defn
        assert "ritual_plane" in defn
        assert defn["ritual_plane"] in {"OFFERING", "MUSIC / CONTROL", "INVOCATION / DEITY"}
        assert len(defn["primary_signs"]) >= 1
        assert len(defn["all_signs"]) >= len(defn["primary_signs"])

        l, t, r, b = defn["crop_box"]
        assert 0.0 <= l < r <= 1.0, f"Invalid horizontal box bounds for {defn['id']}: {l}, {r}"
        assert 0.0 <= t < b <= 1.0, f"Invalid vertical box bounds for {defn['id']}: {t}, {b}"


def test_gallery_manifest_generation():
    """Verify gallery manifest structure and sign-to-realia lookups."""
    manifest = get_hagia_gallery_manifest(pages_safe=True)

    assert manifest["total_crops"] == 10
    assert len(manifest["crops"]) == 10
    assert "c. 1400–1350 BC" in manifest["date_provenance"]
    assert "Heraklion" in manifest["museum"]

    s2c = manifest["sign_to_crops"]
    assert "21" in s2c  # Aulos Flute
    assert "crop_aulos_player" in s2c["21"]

    assert "26" in s2c  # Galley Boat
    assert "crop_boat_model" in s2c["26"]

    assert "28" in s2c  # Bull Haunch
    assert "crop_trussed_bull" in s2c["28"] or "crop_calf_offering" in s2c["28"]

    assert "41" in s2c  # Libation Hydria
    assert "crop_libation_hydria" in s2c["41"]


def test_get_realia_for_group():
    """Verify group-level heuristic scoring and realia matching."""
    manifest = get_hagia_gallery_manifest(pages_safe=True)

    # Aulos flute group B08 (21-27)
    match_b08 = get_realia_for_group(["21", "27"], manifest=manifest)
    assert match_b08 is not None
    assert match_b08["id"] in {"crop_aulos_player", "crop_trussed_bull"}

    # Boat & bird group A16 (26-31)
    match_a16 = get_realia_for_group(["26", "31"], manifest=manifest)
    assert match_a16 is not None
    assert match_a16["id"] in {"crop_boat_model", "crop_labrys_double_axe"}

    # Libation group (41-39)
    match_lib = get_realia_for_group(["41", "39"], manifest=manifest)
    assert match_lib is not None
    assert match_lib["id"] == "crop_libation_hydria"

    # Bogus signs
    match_none = get_realia_for_group(["99", "88"], manifest=manifest)
    assert match_none is None


def test_workbench_hagia_triada_integration(tmp_path: Path):
    """Verify that generated workbench HTML embeds Hagia Triada sync data and controls."""
    corpus = load_transcription("godart_1995")
    out_file = tmp_path / "workbench.html"
    html = generate_workbench_html(corpus, output_path=out_file, pages_safe=True)

    assert "hagia_gallery" in html
    assert "initHagiaGallery" in html
    assert "selectHagiaRealia" in html
    assert "updateHagiaSync" in html
    assert "highlightMatchingSignsOnDisc" in html
    assert "hagiaThumbStrip" in html
    assert "Hagia Triada Realia Homology" in html
    assert "crop_boat_model" in html
    assert "crop_aulos_player" in html
