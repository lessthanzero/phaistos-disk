"""Data models for typometry, stamp punches, and workshop mechanics."""

from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class PunchProfile(BaseModel):
    sign_id: str
    name: str
    total_impressions: int
    side_a_impressions: int
    side_b_impressions: int
    estimated_width_mm: float
    estimated_height_mm: float
    category: str


class OverlapObservation(BaseModel):
    group_id: str
    side: str
    first_sign: str
    second_sign: str
    outer_overlaps_inner: bool
    epigrapher_source: str
    notes: str = ""


class WorkshopMatrixResult(BaseModel):
    total_punches_used: int
    total_impressions: int
    mean_punch_reuse: float
    max_punch_reuse: int
    most_used_punches: List[Tuple[str, int]] = Field(default_factory=list)
    palimpsest_corrections_count: int
    outside_in_overlap_consistency_pct: float
    tool_switching_overhead_score: float
    matrix_demonstration_likelihood_score: float
    skeptic_verdict: str
