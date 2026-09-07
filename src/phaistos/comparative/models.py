"""Data models for comparative scripts and cross-script correspondences."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class InferenceLevel(str, Enum):
    """The Chain of Inference depth for cross-script mappings."""
    L0_OBSERVATION = "L0"           # Direct physical observation on the disc
    L1_FORMAL_RESEMBLANCE = "L1"    # Visual / palaeographic resemblance to Linear A/CH
    L2_PHONETIC_PROJECTION = "L2"   # Phonetic syllabary projection (via Linear B)
    L3_TRANSLATION_HYPOTHESIS = "L3"# Semantic reading in a target language


class VisualSimilarity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LinearASign(BaseModel):
    id: str
    name: str
    category: str
    description: str
    relative_frequency_rank: int


class LinearBSign(BaseModel):
    id: str
    phonetic_value: str
    consonant: Optional[str] = None
    vowel: str
    description: str


class ProposedCorrespondence(BaseModel):
    disc_sign: str = Field(..., description="Evans sign ID (e.g. '38')")
    disc_name: str
    linear_a_sign: Optional[str] = None
    linear_b_sign: Optional[str] = None
    proposed_phonetic_value: Optional[str] = None
    proponents: List[str]
    inference_level: InferenceLevel
    visual_similarity: VisualSimilarity
    evidence_notes: str


class ArkalochoriSign(BaseModel):
    id: str
    column: int
    position: int
    description: str
    diacritical_mark: Optional[str] = None
    proposed_phaistos_parallel: Optional[str] = None
    proposed_linear_a_parallel: Optional[str] = None
    visual_similarity: str = "medium"
    notes: str = ""


class ArkalochoriInscription(BaseModel):
    artifact: str
    discovery_year: int
    provenance: str
    date_period: str
    signs: List[ArkalochoriSign]


class GeneralizationResult(BaseModel):
    artifact_name: str
    total_signs: int
    matched_phaistos_signs_count: int
    coverage_percentage: float
    unique_phaistos_signs_matched: List[str]
    structural_formula_z_score: float
    formula_p_value: float
    target_language_admissibility: Dict[str, float]
    skeptic_verdict: str


class CrossMatrixResult(BaseModel):
    corpora_analyzed: List[str]
    total_signs_in_network: int
    shared_glyph_parallels: Dict[str, List[str]]
    linear_a_lexical_matches: List[str]
    combinatorial_satisfaction_pct: float
    phonotactic_conflict_count: int
    skeptic_verdict: str


class ScriptPhylogeneticDistance(BaseModel):
    script_a: str
    script_b: str
    morphological_jaccard_distance: float
    positional_jsd: float
    collocation_overlap_score: float
    composite_phylogenetic_distance: float


class ScriptNetworkResult(BaseModel):
    scripts_analyzed: List[str]
    total_taxa_signs: Dict[str, int]
    pairwise_distances: Dict[str, ScriptPhylogeneticDistance]
    nearest_neighbor_to_phaistos: str
    transition_hypothesis_verdict: str
    hieroglyphic_affinity_z: float
    linear_a_affinity_z: float
    skeptic_verdict: str



