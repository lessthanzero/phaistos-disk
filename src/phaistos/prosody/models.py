"""Data models for metrical and strophic prosody analysis."""

from typing import List, Optional, Tuple
from pydantic import BaseModel, Field


class MoraGroup(BaseModel):
    group_id: str
    side: str
    signs: List[str]
    sign_count: int
    has_stroke: bool
    estimated_morae: int  # 1 mora per CV sign, +1 if oblique stroke (virama/lengthening)


class TriadRefrain(BaseModel):
    refrain_sign_ids: List[str]
    occurrences: List[str]
    interval_steps: List[int]
    is_strictly_periodic: bool


class StrophicAnalysisResult(BaseModel):
    total_groups: int
    side_a_groups: int
    side_b_groups: int
    mean_morae_per_group: float
    triad_refrain: Optional[TriadRefrain] = None
    periodicity_p_value: float
    strophic_responsion_r: float
    dactylic_fit_score: float
    anapestic_fit_score: float
    paeonic_fit_score: float
    skeptic_verdict: str
