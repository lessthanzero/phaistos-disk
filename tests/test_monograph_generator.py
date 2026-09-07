"""Unit tests for Comprehensive Epigraphic Monograph Generator."""

from pathlib import Path
import pytest
from phaistos.report.monograph_generator import generate_comprehensive_monograph


def test_monograph_generation(tmp_path: Path):
    """Verify end-to-end monograph compilation across all 6 chapters."""
    test_out = tmp_path / "test_monograph.md"
    generated_path = generate_comprehensive_monograph(output_path=test_out)

    assert generated_path.exists()
    content = generated_path.read_text(encoding="utf-8")

    # Verify all 6 chapters and executive abstract are present
    assert "## Executive Abstract" in content
    assert "## Chapter 1: The Material Machine" in content
    assert "## Chapter 2: The Strophic Score" in content
    assert "## Chapter 3: The Rosetta Split" in content
    assert "## Chapter 4: Epistemic Phonology" in content
    assert "## Chapter 5: The Liturgical Libretto" in content
    assert "## Chapter 6: The Skeptic Gauntlet" in content

    # Verify key scientific findings are embedded
    assert "Single-Die Matrix Invariants" in content
    assert "Lyric Triad" in content
    assert "Hagia Triada Sarcophagus" in content
    assert "London Medical Papyrus" in content
    assert "Shannon Unicity" in content
    assert len(content) > 5000  # Detailed treatise
