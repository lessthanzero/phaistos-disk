"""Unit tests for ancient board game (Mehen) simulation."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.game.mehen_simulator import (
    build_disc_board,
    evaluate_mehen_hypothesis,
    roll_casting_sticks,
    simulate_single_game,
)
from phaistos.game.models import GameSimulationResult
import numpy as np


def test_roll_casting_sticks():
    rng = np.random.default_rng(42)
    rolls = [roll_casting_sticks(rng) for _ in range(100)]
    assert all(1 <= r <= 5 for r in rolls)
    assert set(rolls) == {1, 2, 3, 4, 5}


def test_build_disc_board():
    corpus = load_transcription("godart_1995")
    board = build_disc_board(corpus)
    assert len(board) == 61
    assert board[0]["id"] == "A01"
    assert board[60]["id"] == "B30"
    # Check hazard presence (A01 contains '02')
    assert board[0]["is_hazard"] is True


def test_single_game_simulation():
    corpus = load_transcription("godart_1995")
    board = build_disc_board(corpus)
    rng = np.random.default_rng(42)
    winner, turns = simulate_single_game(board, num_players=2, rng=rng)
    assert winner in (0, 1)
    assert 5 <= turns <= 100


def test_full_game_evaluation():
    corpus = load_transcription("godart_1995")
    # Quick simulation for test speed
    result = evaluate_mehen_hypothesis(corpus, num_games=200, num_random_boards=10, seed=42)
    assert isinstance(result, GameSimulationResult)
    assert result.deadlock_rate_pct == 0.0
    assert result.mean_turns_to_win > 0.0
    assert "ANCIENT SPIRAL GAME BOARD" in result.skeptic_verdict
