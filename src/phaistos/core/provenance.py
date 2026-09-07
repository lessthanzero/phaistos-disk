"""Epistemic provenance system for evidence separation."""

from enum import Enum
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ProvenanceCategory(str, Enum):
    """The 5 strict epistemic categories of the laboratory."""
    OBSERVATION = "OBSERVATION"          # Physical material trace (e.g. stamp overlap, clay erasure)
    TRANSCRIPTION = "TRANSCRIPTION"      # Epigraphic reading of signs (e.g. Evans sign 02)
    SCHOLARLY_CLAIM = "SCHOLARLY_CLAIM"  # Attested proposal in published literature
    HYPOTHESIS = "HYPOTHESIS"            # Testable candidate model (e.g. syllabic Luwian)
    MODEL_INFERENCE = "MODEL_INFERENCE"  # Computational score or statistical likelihood


class ProvenanceRecord(BaseModel, Generic[T]):
    """Wraps any datum with strict provenance and epistemic classification."""
    data: T
    category: ProvenanceCategory
    source_ref: str = Field(..., description="Citation ID or method generator")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    notes: str | None = None
