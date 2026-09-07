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


class StrokeOccurrence(BaseModel):
    group_id: str
    side: str
    sign_evans_id: str
    sign_name: str
    position_in_group: int
    group_length: int
    is_terminal: bool
    is_initial: bool
    is_stanza_final: bool = False
    is_lyric_triad_cadence: bool = False


class ViramaEvaluation(BaseModel):
    terminal_position_rate: float
    coda_consonant_inventory_size: int
    lexical_inconsistency_instances: List[Dict]
    textual_coverage_pct: float
    phonotactic_coda_clusters: List[Dict]
    falsification_verdict: str


class MusicalIctusEvaluation(BaseModel):
    side_a_triad_responsion_match: bool
    side_b_stanza_cadence_count: int
    side_b_stanza_cadence_p_value: float
    triad_responsion_p_value: float
    mora_prolongation_ratio: float
    support_verdict: str


class StrokeAnalysisResult(BaseModel):
    total_strokes: int
    side_a_strokes: int
    side_b_strokes: int
    occurrences: List[StrokeOccurrence]
    sign_distribution: Dict[str, int]
    category_distribution: Dict[str, int]
    category_p_value: float
    virama_eval: ViramaEvaluation
    ictus_eval: MusicalIctusEvaluation
    skeptic_verdict: str

