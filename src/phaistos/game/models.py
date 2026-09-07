"""Data models for ancient spiral board game simulation (Mehen / Astragaloi)."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class GameSimulationResult(BaseModel):
    num_simulated_games: int
    num_players: int
    player_win_rates: Dict[str, float]
    mean_turns_to_win: float
    min_turns: int
    max_turns: int
    deadlock_rate_pct: float
    fairness_deviation_from_50pct: float
    disc_layout_vs_random_percentile: float
    is_statistically_optimized_game_board: bool
    skeptic_verdict: str
