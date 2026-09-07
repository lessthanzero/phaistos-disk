"""Unit tests for comparative script loader, matcher, and permutation tests."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.comparative.loader import (
    load_linear_a_signs,
    load_linear_b_signs,
    load_proposed_correspondences,
)
from phaistos.comparative.matcher import evaluate_frequency_rank_correlation
from phaistos.comparative.permutations import run_correspondence_permutation_test


def test_comparative_loaders():
    la_signs = load_linear_a_signs()
    lb_signs = load_linear_b_signs()
    corrs = load_proposed_correspondences()

    assert len(la_signs) > 10
    assert len(lb_signs) > 10
    assert len(corrs) >= 8

    # Verify Chain of Inference tags exist
    for c in corrs:
        assert c.inference_level.value in ["L0", "L1", "L2", "L3"]
        assert c.visual_similarity.value in ["high", "medium", "low"]


def test_frequency_rank_correlation():
    corpus = load_transcription("godart_1995")
    corrs = load_proposed_correspondences()
    la_signs = load_linear_a_signs()

    res = evaluate_frequency_rank_correlation(corpus, corrs, la_signs)
    assert "spearman_rho" in res
    assert "p_value" in res
    assert res["sample_size"] >= 5


def test_comparative_permutation_test():
    corpus = load_transcription("godart_1995")
    corrs = load_proposed_correspondences()
    la_signs = load_linear_a_signs()

    perm_res = run_correspondence_permutation_test(
        corpus, corrs, la_signs, iterations=100, seed=42
    )
    assert "observed_rho" in perm_res
    assert "null_mean_rho" in perm_res
    assert "p_value" in perm_res
    assert 0.0 <= perm_res["p_value"] <= 1.0


def test_tablet_ph1_loader():
    from phaistos.comparative.loader import load_tablet_ph1

    data = load_tablet_ph1()
    assert data["metadata"]["museum_id"] == "Heraklion Museum HM 1359"
    assert "face_a" in data["transcription"]
    assert "DI-RA-DI-NA" in data["transcription"]["face_a"]["line_1"]["raw"]
    assert data["analysis"]["genre"] == "administrative_commodity_ledger"

