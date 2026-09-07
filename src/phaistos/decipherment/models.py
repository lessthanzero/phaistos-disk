"""Data models for decipherment hypotheses, phonotactics, and evaluation results."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class DeciphermentHypothesis(BaseModel):
    id: str
    title: str
    target_language: str
    assumptions: List[str]
    sign_mapping: Dict[str, str] = Field(..., description="Evans sign ID to target phoneme/syllable")
    complexity_penalty: float = Field(default=0.0, description="Penalty for ad-hoc exceptions or ungrounded signs")
    source_reference: str


class DeciphermentResult(BaseModel):
    hypothesis_id: str
    target_language: str
    observed_score: float
    null_mean_score: float
    null_std_score: float
    z_score: float
    p_value: float
    is_falsified: bool
    skeptic_verdict: str
    unicity_ratio: float
    sample_transliteration: Dict[str, str] = Field(..., description="Group ID to transliteration string")
    contradictions: List[str] = Field(default_factory=list)
