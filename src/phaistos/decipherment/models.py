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
    target_language: str = "structural_or_non_linguistic"
    observed_score: float = 0.0
    null_mean_score: float = 0.0
    null_std_score: float = 0.0
    z_score: float = 0.0
    p_value: float = 1.0
    is_falsified: bool = False
    skeptic_verdict: str = ""
    unicity_ratio: float = 1.0
    sample_transliteration: Dict[str, str] = Field(default_factory=dict, description="Group ID to transliteration string")
    contradictions: List[str] = Field(default_factory=list)
