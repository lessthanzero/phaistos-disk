"""Unit tests for universal glyph repertoire and multi-mode rendering (Emoji, Vector SVG, Unicode)."""

from pathlib import Path
import pytest

from phaistos.corpus.loader import load_transcription
from phaistos.geometry.svg import render_side_svg, export_disc_svgs
from phaistos.visualizer.glyphs import (
    GLYPH_REGISTRY,
    get_sign_glyph_data,
    get_sign_display,
    get_all_glyphs_catalog,
)
from phaistos.visualizer.workbench import generate_workbench_html


def test_glyph_repertoire_completeness():
    """Verify all 45 canonical Evans signs have complete visual representations."""
    catalog = get_all_glyphs_catalog()
    assert len(catalog) == 45

    for i in range(1, 46):
        sid = f"{i:02d}"
        assert sid in catalog, f"Sign {sid} missing from GLYPH_REGISTRY"
        data = catalog[sid]

        # Verify mandatory visual fields
        for field in ["name", "emoji", "short_name", "label", "unicode_char", "unicode_hex", "vector_svg"]:
            assert field in data and data[field], f"Sign {sid} missing field '{field}'"

        # Verify emoji is non-empty and vector_svg contains valid SVG elements
        assert len(data["emoji"]) >= 1
        assert any(tag in data["vector_svg"] for tag in ["<path", "<circle", "<rect", "<line", "<ellipse"])


def test_get_sign_glyph_data():
    """Verify data lookup handles unpadded, padded, and invalid IDs."""
    # Padded string
    d02 = get_sign_glyph_data("02")
    assert d02["emoji"] == "🪶"
    assert "Plumed" in d02["label"]

    # Unpadded string
    d2 = get_sign_glyph_data("2")
    assert d2["emoji"] == d02["emoji"]

    # Unknown ID fallback
    d_unknown = get_sign_glyph_data("999")
    assert d_unknown["emoji"] == "𐇐"
    assert "SIGN 999" in d_unknown["name"]
    assert "<circle" in d_unknown["vector_svg"] or "<text" in d_unknown["vector_svg"]


def test_get_sign_display_modes():
    """Verify get_sign_display formats strings correctly across all display modes."""
    # Default: emoji_utf8
    disp_default = get_sign_display("12")
    assert "🛡️" in disp_default
    assert "12" in disp_default

    # emoji_only
    disp_emoji = get_sign_display("12", mode="emoji_only")
    assert disp_emoji == "🛡️"

    # label
    disp_label = get_sign_display("12", mode="label")
    assert "Shield" in disp_label

    # unicode
    disp_unicode = get_sign_display("12", mode="unicode")
    assert disp_unicode == "𐇛"


def test_svg_rendering_modes(tmp_path: Path):
    """Verify render_side_svg and export_disc_svgs work across all glyph modes."""
    corpus = load_transcription("godart_1995")

    # 1. Emoji mode (Default)
    svg_emoji = render_side_svg(corpus.side_a, corpus, glyph_mode="emoji_utf8")
    assert "Mode: Emoji + ID" in svg_emoji
    assert "🪶" in svg_emoji or "🛡️" in svg_emoji

    # 2. Vector SVG mode
    svg_vector = render_side_svg(corpus.side_a, corpus, glyph_mode="vector_svg")
    assert "Mode: Vector SVG" in svg_vector
    assert "<g transform=" in svg_vector
    assert "<circle" in svg_vector

    # 3. Unicode raw mode
    svg_unicode = render_side_svg(corpus.side_a, corpus, glyph_mode="unicode_raw")
    assert "Mode: Unicode SMP" in svg_unicode

    # 4. File export
    path_a, path_b = export_disc_svgs(corpus, tmp_path, glyph_mode="emoji_utf8")
    assert path_a.is_file() and path_b.is_file()
    assert "Mode: Emoji + ID" in path_a.read_text(encoding="utf-8")


def test_workbench_glyph_switcher(tmp_path: Path):
    """Verify workbench HTML embeds the switcher segmented buttons, catalog, and JS switcher function."""
    corpus = load_transcription("godart_1995")
    out_file = tmp_path / "workbench.html"
    html = generate_workbench_html(corpus, output_path=out_file)

    # Verify switcher buttons
    assert 'id="glyphModeGroup"' in html
    assert 'id="btnModeEmoji"' in html
    assert 'id="btnModeVector"' in html
    assert 'id="btnModeUnicode"' in html
    assert 'setGlyphMode' in html

    # Verify catalog is embedded in payload
    assert '"glyphs_catalog"' in html
    assert 'currentGlyphMode' in html
