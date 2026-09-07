"""Data models for comparative scripts and cross-script correspondences."""

from enum import Enum
from typing import List, Optional
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
