"""Pydantic data models for Object Function and Material Affordance analysis."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GeometryLayoutType(str, Enum):
    """Candidate geometric layouts for housing the 242-sign corpus."""
    ARCHIMEDEAN_SPIRAL = "ARCHIMEDEAN_SPIRAL"       # Actual Phaistos Disc geometry
    RECTANGULAR_TABLET = "RECTANGULAR_TABLET"       # Standard Linear A / B tablet format
    LINEAR_STRIP = "LINEAR_STRIP"                   # Papyrus / parchment continuous band
    CONCENTRIC_CIRCLES = "CONCENTRIC_CIRCLES"       # Discrete non-spiral concentric rings
    RADIAL_SECTORS = "RADIAL_SECTORS"               # Wheel-spoke circular sectors


class LayoutComparisonMetrics(BaseModel):
    """Quantitative affordance metrics for comparing geometric layouts."""
    layout_type: GeometryLayoutType
    total_area_cm2: float
    information_density_signs_per_cm2: float
    mean_saccade_distance_mm: float
    total_saccade_distance_mm: float
    line_returns_count: int
    boundary_ambiguity_score: float         # 0.0 (unambiguous continuous path) to 1.0 (highly ambiguous jumps)
    foveal_dwell_stability: float           # 0.0 (erratic saccades) to 1.0 (fixed focal window with rotation)
    handheld_operability_score: float       # 0.0 (unusable in hand) to 100.0 (ergonomically optimal)
    notes: str = ""


class GripPosture(str, Enum):
    """Biomechanical handling postures for a 16 cm, 500 g terracotta disc."""
    ONE_HANDED_EDGE = "ONE_HANDED_EDGE"                     # Held with single hand pinched at rim
    TWO_HANDED_PERIMETER = "TWO_HANDED_PERIMETER"           # Held with both hands on opposing rims ("steering wheel")
    PALMAR_REST_ONE_HAND = "PALMAR_REST_ONE_HAND"           # Resting flat on left palm, right hand gestures/traces
    TABLE_STAND_DISPLAY = "TABLE_STAND_DISPLAY"             # Placed upright or flat on sanctuary altar/stand


class ErgonomicGripEvaluation(BaseModel):
    """Biomechanical ergonomic evaluation of a grip posture."""
    posture: GripPosture
    wrist_cantilever_torque_nm: float
    sustainable_hold_seconds: float
    rotational_dexterity_score: float       # 0 to 100
    muscle_fatigue_index: float             # 0 (no fatigue) to 100 (acute strain)
    feasibility_rating: str                 # "POOR", "MODERATE", "OPTIMAL"
    notes: str = ""


class RotationKinematicMetrics(BaseModel):
    """Kinematic metrics synchronizing Archimedean spiral rotation with oral recitation."""
    side: str
    total_turns: float
    total_angular_span_deg: float
    total_morae: int
    estimated_duration_sec: float
    angular_velocity_deg_per_sec: float
    rpm: float
    optical_conveyor_stability_score: float
    notes: str = ""


class TactileAcuityEvaluation(BaseModel):
    """Somatosensory evaluation of tactile discrimination on clay intaglio features."""
    task_name: str
    stimulus_type: str
    feature_size_mm: float
    weber_two_point_threshold_mm: float
    mechanoreceptor_type: str
    detection_probability: float
    is_physically_viable: bool
    epistemic_status: str                   # "FALSIFIED", "CONFIRMED_VIABLE", "EQUIVOCAL"
    notes: str = ""


class StampingEconomicProfile(BaseModel):
    """Production economics and breakeven modeling for movable relief punches."""
    num_unique_punches: int
    punch_fabrication_hours: float
    single_disc_stamping_hours: float
    single_disc_incision_hours: float
    breakeven_copy_count: int
    sphragistic_authority_index: float      # 0 to 100
    economic_verdict: str
    notes: str = ""


class ObjectFunctionHypothesis(str, Enum):
    """The 9 candidate cultural/object functions for the Phaistos Disc."""
    OF_01 = "OF_01_ORDINARY_DOCUMENT"               # Archival administrative record
    OF_02 = "OF_02_ROTATIONAL_DOCUMENT"             # Visual document explicitly designed to be rotated
    OF_03 = "OF_03_TACTILE_MNEMONIC_AID"            # Blind/tactile finger-traceable recitation tool
    OF_04 = "OF_04_PERFORMANCE_CUE_SHEET"           # Choral libretto / performance cue sheet
    OF_05 = "OF_05_RITUAL_VOTIVE_MONUMENT"          # Consecrated sanctuary votive deposit
    OF_06 = "OF_06_ASTRONOMICAL_CALENDAR"           # Cyclical astronomical / eclipse calculator
    OF_07 = "OF_07_GAME_BOARD_PATH"                 # Mehen / race game board
    OF_08 = "OF_08_SPATIAL_GEOGRAPHIC_MAP"          # Topographical / route itinerary map
    OF_09 = "OF_09_TYPOMETRIC_MASTERPIECE"          # Seal-cutter's workshop demonstration piece


class RankedFunctionEvaluation(BaseModel):
    """A ranked hypothesis evaluation with evidence, controls, confidence, and objections."""
    hypothesis_id: str
    title: str
    supporting_evidence: List[str]
    falsifying_controls: List[str]
    confidence_grade: str                           # "HIGH", "MODERATE", "LOW", "FALSIFIED"
    strongest_objection: str
    next_test: str
    rank: int


class ExperimentAffordanceResult(BaseModel):
    """Output container for an individual OFX experiment run."""
    experiment_id: str
    title: str
    metrics: Dict[str, Any]
    skeptic_verdict: str
