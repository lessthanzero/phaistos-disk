"""Data models for the Autonomous Skeptic Adversary & Falsification Engine."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class FalsificationDossier(BaseModel):
    """Rigorous epistemic falsification dossier evaluating a proposed hypothesis."""
    claim: str
    claim_type: str  # phonetic_translation, astronomical_calendar, architectural_blueprint, mathematical_game
    unicity_distance_symbols: float = 106.0
    corpus_length_symbols: int = 242
    estimated_model_degrees_of_freedom: int
    unicity_verdict: str  # UNCONSTRAINED_OVERFIT, MATHEMATICALLY_VALID
    null_surrogates_evaluated: int
    observed_signal_metric: float
    null_surrogate_mean: float
    null_surrogate_std: float
    empirical_p_value: float
    z_score: float
    statistical_verdict: str  # FALSIFIED, STATISTICALLY_EQUIVOCAL, SURVIVES_NULL_GAUNTLET
    archaeological_contradictions: List[str]
    local_model_critique: str
    final_verdict: str
