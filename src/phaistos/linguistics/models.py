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


class GridClusteringMetrics(BaseModel):
    consonant_silhouette_score: float
    vowel_silhouette_score: float
    explained_variance_ratio_svd: List[float]
    frobenius_reconstruction_error: float
    null_control_reconstruction_error_mean: float
    null_control_reconstruction_error_std: float
    structure_z_score: float
    structure_p_value: float


class KoberGridResult(BaseModel):
    n_signs: int
    n_consonant_classes: int
    n_vowel_classes: int
    grid: Dict[str, Dict[str, List[str]]]
    sign_consonant_map: Dict[str, str]
    sign_vowel_map: Dict[str, str]
    metrics: GridClusteringMetrics
    skeptic_verdict: str

