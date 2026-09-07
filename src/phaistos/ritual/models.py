"""Data models for Stratified Multi-Plane Ritual Decipherment and Hagia Triada Homology."""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class RitualSignPlane(str, Enum):
    """The functional semiotic plane of a sign in Minoan liturgical performance."""
    THEONYMIC_INVOCATION = "Plane_I_Theonymic"         # Divine names, titles, epiphany calls, sacred emblems
    MATERIA_SACRA_OFFERING = "Plane_II_Offering"       # Sacrificial animals, botanical votives, libation vessels, dedications
    SONIC_PERFORMANCE_CONTROL = "Plane_III_Sonic"      # Musical instruments, resonant sound-makers, breath pauses (virgulae)
    STRUCTURAL_CONNECTIVE = "Plane_IV_Structural"      # Grammatical stems, pronominal affixes, motion verbs


class PlaneSignDefinition(BaseModel):
    """Epigraphic and archaeological definition of a sign within the ritual plane hierarchy."""
    sign_id: str
    canonical_name: str
    unicode_glyph: str
    assigned_plane: RitualSignPlane
    primary_ritual_function: str
    archaeological_parallel: str
    hagia_triada_scene_parallel: Optional[str] = None
    syntactic_slot_tendency: str  # head, core, coda


class ParsedLiturgicalUnit(BaseModel):
    """A sign group parsed through the Tripartite Liturgical Grammar."""
    group_id: str
    side: str
    turn: int
    raw_signs: List[str]
    plane_sequence: List[RitualSignPlane]
    has_virgula: bool
    structural_role: str  # INVOCATIONAL_HEAD, SACRIFICIAL_CORE, VOTIVE_CODA, PERFORMANCE_REST
    invocational_head_present: bool
    offering_present: bool
    sonic_marker_present: bool
    liturgical_paraphrase: str


class RitualPlanesResult(BaseModel):
    """Global corpus breakdown across the semiotic ritual planes."""
    total_signs: int = 242
    total_groups: int = 61
    plane_sign_counts: Dict[str, int]
    plane_token_frequencies: Dict[str, int]
    plane_token_percentages: Dict[str, float]
    plane_transition_matrix: Dict[str, Dict[str, float]]
    parsed_units: List[ParsedLiturgicalUnit]
    theonymic_head_rate: float
    offering_presence_rate: float
    shannon_plane_entropy_bits: float
    skeptic_verdict: str


class HagiaTriadaScene(BaseModel):
    """A distinct liturgical scene from the Hagia Triada Sarcophagus (c. 1400-1350 BC)."""
    scene_id: str
    title: str
    description: str
    liturgical_action: str
    diagnostic_objects: List[str]
    parallel_phaistos_signs: List[str]
    match_confidence: str  # high, medium


class HagiaTriadaHomologyResult(BaseModel):
    """Homology evaluation between the Phaistos Disc text and the Hagia Triada Sarcophagus."""
    total_scenes: int = 4
    scenes: List[HagiaTriadaScene]
    disc_scene_correspondence_rate: float
    strophic_narrative_alignment_score: float
    shared_ritual_repertoire_count: int
    skeptic_verdict: str


class PlaneSegregationResult(BaseModel):
    """Monte Carlo statistical test of positional plane segregation against randomized controls."""
    observed_segregation_score: float
    null_surrogate_mean: float
    null_surrogate_std: float
    z_score: float
    empirical_p_value: float
    iterations_run: int
    is_statistically_significant: bool
    model_degrees_of_freedom: int
    unicity_limit_symbols: float = 106.0
    shannon_unicity_satisfied: bool
    skeptic_verdict: str
