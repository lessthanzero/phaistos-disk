"""Data models for agglutinative morphosyntax and prefix analysis."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ParsedGroup(BaseModel):
    group_id: str
    side: str
    raw_signs: List[str]
    prefix: Optional[str] = None
    stem: List[str]
    suffix: Optional[str] = None
    has_stroke: bool


class MorphologicalAnalysisResult(BaseModel):
    total_groups: int
    unique_raw_groups: int
    unique_stems_after_stripping: int
    vocabulary_compression_pct: float
    prefix_frequencies: Dict[str, int]
    suffix_frequencies: Dict[str, int]
    raw_zipf_r2: float
    stripped_zipf_r2: float
    zipf_improvement_delta: float
    monte_carlo_compression_p_value: float
    is_statistically_agglutinative: bool
    skeptic_verdict: str
