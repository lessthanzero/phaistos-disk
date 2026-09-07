"""Unit tests for Shannon unicity distance and mathematical overfit bounds."""

import pytest
from phaistos.experiment.unicity import calculate_unicity_distance, format_unicity_warning


def test_unicity_distance_calculation():
    # Test syllabic model calculation
    calc_s = calculate_unicity_distance(alphabet_size=45, is_syllabic=True)
    assert "unicity_distance_chars" in calc_s
    assert "key_entropy_bits" in calc_s
    assert calc_s["key_entropy_bits"] > 200.0
    assert calc_s["unicity_distance_chars"] > 50.0

    # Test monoalphabetic substitution
    calc_a = calculate_unicity_distance(alphabet_size=45, is_syllabic=False)
    assert calc_a["key_entropy_bits"] > 150.0

    # Warning formatting
    warn = format_unicity_warning(calc_s)
    assert "Shannon Unicity Bound" in warn
    assert "overfit" in warn
