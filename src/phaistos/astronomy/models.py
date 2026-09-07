"""Data models for astronomical and calendar cycle evaluations."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AstronomicalMatch(BaseModel):
    constant_name: str
    target_value: float
    observed_disc_feature: str
    observed_value: int
    relative_error_pct: float
    epistemic_plausibility: str


class AstronomicalAnalysisResult(BaseModel):
    matches: List[AstronomicalMatch]
    stroke_distribution: dict
    look_elsewhere_trials: int
    look_elsewhere_p_value: float
    unfalsifiable_numerology_warning: bool
    skeptic_verdict: str
