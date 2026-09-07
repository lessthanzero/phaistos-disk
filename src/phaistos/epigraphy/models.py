"""Data models for microscopic epigraphy, stamp overlaps, and palimpsests."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class StampOverlap(BaseModel):
    group_id: str
    side: str
    punch_first: str
    punch_second: str
    overlap_type: str  # flange_clip, edge_suppression, partial_overstrike
    direction: str     # outside_over_inner, inner_over_outside, indeterminate
    confidence: str    # high, medium, low
    notes: str = ""


class PalimpsestDetail(BaseModel):
    group_id: str
    side: str
    initial_underlying_traces: str
    final_stamped_signs: List[str]
    erasure_technique: str
    epigrapher_consensus: str
    notes: str = ""


class RadialCompressionSector(BaseModel):
    coil_number: int  # 1 = outer rim, 4 = inner core
    side: str
    mean_track_height_mm: float
    mean_sign_spacing_mm: float
    crowding_factor: float


class EpigraphicMicroAnalysisResult(BaseModel):
    total_overlaps_cataloged: int
    outside_in_consistency_pct: float
    palimpsests_cataloged: List[PalimpsestDetail]
    radial_compression_gradient: List[RadialCompressionSector]
    stroke_incision_sequence: str
    forgery_falsification_score: float
    skeptic_verdict: str
