"""Tests for Arkalochori Axe inscription and cross-script generalization."""

from phaistos.corpus.loader import load_transcription
from phaistos.comparative.loader import (
    load_arkalochori_inscription,
    load_proposed_correspondences,
)
from phaistos.comparative.generalization import evaluate_arkalochori_generalization


def test_arkalochori_corpus_loading():
    axe = load_arkalochori_inscription()
    assert axe.artifact == "Arkalochori Votive Double Axe"
    assert len(axe.signs) == 15
    # Column counts
    col1 = [s for s in axe.signs if s.column == 1]
    col2 = [s for s in axe.signs if s.column == 2]
    col3 = [s for s in axe.signs if s.column == 3]
    assert len(col1) == 5
    assert len(col2) == 5
    assert len(col3) == 5


def test_arkalochori_sign_parallels():
    axe = load_arkalochori_inscription()
    # Sign 02 (Plumed Head) should be present multiple times
    head_signs = [s for s in axe.signs if s.proposed_phaistos_parallel == "02"]
    assert len(head_signs) == 4
    # Double axe signs (21)
    axe_signs = [s for s in axe.signs if s.proposed_phaistos_parallel == "21"]
    assert len(axe_signs) == 4


def test_arkalochori_generalization_eval():
    corpus = load_transcription("godart_1995")
    axe = load_arkalochori_inscription()
    corrs = load_proposed_correspondences()
    res = evaluate_arkalochori_generalization(corpus, axe, corrs, n_surrogates=200, seed=42)

    assert res.total_signs == 15
    assert res.matched_phaistos_signs_count == 15
    assert res.coverage_percentage == 100.0
    # The concentration on 02, 21, 35 should produce high Z-score
    assert res.structural_formula_z_score > 3.0
    assert "EXTREME CONCENTRATION" in res.skeptic_verdict
