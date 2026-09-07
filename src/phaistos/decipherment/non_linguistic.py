"""Evaluation engines for non-linguistic hypotheses (calendars, game boards, tallies)."""

import math
from typing import Dict, List
from phaistos.core.models import DiscCorpus


def evaluate_lunisolar_calendar_hypothesis(corpus: DiscCorpus) -> Dict[str, float]:
    """
    Test astronomical calendar hypothesis:
    Compares 242 signs and 61 groups to key astronomical periods:
    - Synodic lunar month: 29.5306 days
    - Sidereal lunar month: 27.3216 days
    - Solar year: 365.2422 days
    - Metonic cycle: 19 solar years ≈ 235 synodic months
    - Saros / Nodal cycle: ~18.6 years (compared to 18 incised oblique strokes)
    """
    total_signs = float(corpus.total_signs)
    total_groups = float(corpus.total_groups)
    oblique_strokes = float(corpus.total_oblique_strokes)

    # 1. Lunar month fit
    synodic_8_months = 8.0 * 29.5306  # 236.24 days
    lunar_residual_days = abs(total_signs - synodic_8_months)

    # 2. Side division: Side A (123 signs) vs Side B (119 signs)
    side_a_ratio = 123.0 / total_signs
    side_b_ratio = 119.0 / total_signs

    # 3. Metonic / Saros nodal correspondence
    saros_residual = abs(oblique_strokes - 18.6)

    # 4. Fit penalty: penalizes ad-hoc day adjustments
    fit_score = 100.0 - (lunar_residual_days * 5.0) - (saros_residual * 10.0)

    return {
        "total_signs": total_signs,
        "total_groups": total_groups,
        "total_oblique_strokes": oblique_strokes,
        "synodic_8_months_days": synodic_8_months,
        "lunar_residual_days": lunar_residual_days,
        "saros_residual_years": saros_residual,
        "astronomical_fit_score": max(0.0, fit_score),
    }


def evaluate_game_board_hypothesis(corpus: DiscCorpus) -> Dict[str, float]:
    """
    Test spiral race/track game board hypothesis (e.g. Egyptian Mehen or Proto-Goose game):
    - 61 spiral compartments (cells)
    - Sign distribution acting as special cells (safe spaces, hazards, restarts)
    - Evaluates cell step distance between recurring marker signs (Sign 02 Plumed Head)
    """
    groups = corpus.all_groups()
    total_cells = len(groups)

    # Positions of groups initiated by Sign 02 (Plumed Head)
    head_cells = [i for i, g in enumerate(groups) if g.signs and g.signs[0] == "02"]
    intervals = [head_cells[i + 1] - head_cells[i] for i in range(len(head_cells) - 1)]

    mean_interval = float(sum(intervals) / len(intervals)) if intervals else 0.0
    interval_variance = float(sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)) if intervals else 0.0

    return {
        "total_cells": float(total_cells),
        "hazard_marker_cells_count": float(len(head_cells)),
        "mean_hazard_interval": mean_interval,
        "hazard_interval_variance": interval_variance,
        "board_regularity_score": max(0.0, 100.0 - interval_variance),
    }
