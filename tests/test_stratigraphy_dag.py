"""Unit tests for micro-stratigraphic DAG, topological sort, and drying rheology."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.epigraphy.dag import build_stratigraphic_dag
from phaistos.epigraphy.models import StratigraphicDAGResult


def test_stratigraphic_dag_side_a():
    corpus = load_transcription("godart_1995")
    res = build_stratigraphic_dag(corpus, "A")

    assert isinstance(res, StratigraphicDAGResult)
    assert res.side == "A"
    assert res.total_nodes == 123
    assert res.total_edges > 100
    assert res.is_dag is True
    assert res.has_cycles is False
    assert len(res.topological_sequence) == 123

    # Strong negative correlation with radial distance (outside-in)
    assert res.outside_in_spearman_rho < -0.90
    assert res.outside_in_p_value < 1e-10
    assert res.radial_monotonicity_pct > 95.0

    # Palimpsests
    assert "A05" in res.palimpsest_insertion_ranks
    assert "A08" in res.palimpsest_insertion_ranks

    # Rheology
    assert res.drying_rheology.final_yield_stress_kpa > res.drying_rheology.initial_yield_stress_kpa
    assert res.drying_rheology.outer_burr_displacement_mm > res.drying_rheology.inner_burr_displacement_mm


def test_stratigraphic_dag_side_b():
    corpus = load_transcription("godart_1995")
    res = build_stratigraphic_dag(corpus, "B")

    assert res.side == "B"
    assert res.total_nodes == 119
    assert res.is_dag is True
    assert res.has_cycles is False
    assert len(res.topological_sequence) == 119
    assert res.outside_in_spearman_rho < -0.90
    assert res.radial_monotonicity_pct > 95.0
    assert "STRATIGRAPHIC DAG PROOF" in res.skeptic_verdict
