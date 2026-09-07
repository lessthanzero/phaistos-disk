"""Unit tests for decipherment hypotheses, phonotactic scoring, and non-linguistic models."""

from pathlib import Path
import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.decipherment.models import DeciphermentHypothesis
from phaistos.decipherment.scorer import score_aegean_phonotactics, evaluate_hypothesis_score
from phaistos.decipherment.non_linguistic import (
    evaluate_lunisolar_calendar_hypothesis,
    evaluate_game_board_hypothesis,
)
from phaistos.experiment.runner import run_decipherment_experiment


def test_phonotactic_scoring():
    # Regular CV syllables ending in vowels should score high
    score_good = score_aegean_phonotactics("teqesa")
    assert score_good > 0.0

    # Unmapped signs should be heavily penalized
    score_bad = score_aegean_phonotactics("te[02]qa")
    assert score_bad < 0.0

    # Large consonant clusters should be penalized
    score_cluster = score_aegean_phonotactics("strpka")
    assert score_cluster < score_good


def test_non_linguistic_models():
    corpus = load_transcription("godart_1995")
    cal = evaluate_lunisolar_calendar_hypothesis(corpus)
    game = evaluate_game_board_hypothesis(corpus)

    assert "astronomical_fit_score" in cal
    assert "lunar_residual_days" in cal
    assert cal["total_signs"] == 242

    assert "board_regularity_score" in game
    assert game["total_cells"] == 61
    assert game["hazard_marker_cells_count"] > 10


def test_experiment_runner(tmp_path: Path):
    corpus = load_transcription("godart_1995")
    hypo = DeciphermentHypothesis(
        id="H_TEST",
        title="Test Aegean Hypothesis",
        target_language="test",
        assumptions=["Test assumption"],
        sign_mapping={"02": "te", "12": "qe", "38": "a"},
        complexity_penalty=5.0,
        source_reference="test",
    )

    res = run_decipherment_experiment(corpus, hypo, iterations=20, seed=42, experiments_dir=tmp_path)
    assert res.hypothesis_id == "H_TEST"
    assert "z_score" in res.model_dump()
    assert len(res.skeptic_verdict) > 0
