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


class ReconstructedPunch(BaseModel):
    sign_id: str
    name: str
    fired_width_mm: float
    fired_height_mm: float
    fired_area_mm2: float
    reconstructed_punch_width_mm: float
    reconstructed_punch_height_mm: float
    reconstructed_punch_area_mm2: float
    estimated_stamping_force_newtons: float


class ClayShrinkageProfile(BaseModel):
    clay_type: str
    drying_shrinkage_pct: float
    firing_shrinkage_pct: float
    total_linear_shrinkage_pct: float
    disc_fired_diameter_mm: float
    disc_wet_diameter_mm: float
    center_thickness_mm: float
    edge_thickness_mm: float
    thickness_gradient_ratio: float


class ShrinkageReconstructionResult(BaseModel):
    shrinkage_profile: ClayShrinkageProfile
    punches: List[ReconstructedPunch]
    mean_expansion_factor: float
    mean_stamping_force_newtons: float
    punch_material_verdict: str
    skeptic_verdict: str

