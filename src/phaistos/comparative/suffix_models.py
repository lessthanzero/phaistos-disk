"""Data models for Linear A suffix correspondence and morphological comparison."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SuffixFrequency(BaseModel):
    sign_id: str
    linear_a_sign: Optional[str] = None
    phonetic_value: Optional[str] = None
    count: int
    total_occurrences: int
    terminal_rate: float
    corpus_share_pct: float


class HypothesisComparison(BaseModel):
    sign_id: str
    tested_value: str
    linear_a_counterpart: str
    expected_rate: float
    observed_rate: float
    binomial_p_value: float
    likelihood: float
    verdict: str


class SuffixAnalysisResult(BaseModel):
    total_groups: int
    top_terminal_signs: List[SuffixFrequency]
    sign_35_me_test: HypothesisComparison
    sign_35_te_test: HypothesisComparison
    likelihood_ratio_te_vs_me: float
    aegean_correspondences: List[HypothesisComparison]
    skeptic_verdict: str
