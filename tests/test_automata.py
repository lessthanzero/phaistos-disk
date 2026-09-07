"""Unit tests for Chomsky grammar complexity and automata."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.linguistics.automata import (
    build_transition_graph,
    compute_topological_entropy,
    evaluate_chomsky_complexity,
    AutomataComplexityResult,
)


def test_build_transition_graph():
    corpus = load_transcription("godart_1995")
    g = build_transition_graph(corpus)
    assert g.number_of_nodes() == 45
    assert g.number_of_edges() > 50


def test_automata_complexity_evaluation():
    corpus = load_transcription("godart_1995")
    res = evaluate_chomsky_complexity(corpus, num_surrogates=100, seed=42)

    assert isinstance(res, AutomataComplexityResult)
    assert res.num_nodes == 45
    assert res.topological_entropy_bits > 0.0
    assert "Type 3" in res.chomsky_hierarchy_level
    assert "CHOMSKY GRAMMAR" in res.skeptic_verdict
