"""Unit tests for Frontier E: Interactive Audio-Epigraphic Visualizer."""

from pathlib import Path
import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.visualizer.workbench import generate_workbench_html


def test_generate_workbench_html(tmp_path: Path):
    corpus = load_transcription("godart_1995")
    out_file = tmp_path / "workbench.html"
    html = generate_workbench_html(corpus, output_path=out_file)

    assert len(html) > 5000
    assert out_file.is_file()
    assert "Phaistos Disc Analytical Workbench" in html
    assert "discSvg" in html
    assert "Frontier A: The 18 Oblique Strokes" in html
    assert "Frontier B: Linear A Suffix Correspondence" in html
    assert "Frontier C: Kober-Ventris Grid Factorization" in html
    assert "Frontier D: 3D Clay Shrinkage & Punches" in html
    assert "playPluckedString" in html
