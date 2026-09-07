"""Tests for SVG coordinate generation and file output."""

from pathlib import Path
from phaistos.corpus.loader import load_transcription
from phaistos.geometry.svg import export_disc_svgs, render_side_svg


def test_svg_rendering(tmp_path: Path):
    corpus = load_transcription("godart_1995")
    path_a, path_b = export_disc_svgs(corpus, tmp_path)

    assert path_a.is_file()
    assert path_b.is_file()

    content_a = path_a.read_text(encoding="utf-8")
    assert "<svg" in content_a
    assert "A01" in content_a
    assert "A31" in content_a
    assert "PHAISTOS DISC — SIDE A" in content_a

    content_b = path_b.read_text(encoding="utf-8")
    assert "<svg" in content_b
    assert "B01" in content_b
    assert "B30" in content_b
    assert "PHAISTOS DISC — SIDE B" in content_b
