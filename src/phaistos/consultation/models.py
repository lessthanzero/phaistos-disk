"""Data models for multi-model symbol consultations (Codex GPT-6 Astra, local models)."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SignIconographyConsultation(BaseModel):
    """Iconographic and material realia analysis for a Phaistos symbol."""
    sign_id: str
    canonical_name: str
    realia_identification: str
    material_category: str  # flora, fauna, warrior/dress, maritime, tool, sacred/symbol
    archaeological_parallels: List[str] = Field(default_factory=list)
    cretan_hieroglyphic_parallel: Optional[str] = None
    identification_confidence: str = "medium"  # high, medium, contested, speculative
    iconographic_notes: str = ""


class SignPhoneticConsultation(BaseModel):
    """Phonetic and cross-script acrophonic analysis for a Phaistos symbol."""
    sign_id: str
    proposed_linear_a_counterpart: Optional[str] = None
    proposed_linear_b_counterpart: Optional[str] = None
    proposed_phonetic_values: List[str] = Field(default_factory=list)
    candidate_acrophonic_roots: List[str] = Field(default_factory=list)
    primary_proponents: List[str] = Field(default_factory=list)
    inference_level: str = "L1"  # L0, L1, L2, L3
    phonetic_confidence: str = "speculative"  # plausible_parallel, speculative, unattested
    epistemic_warning: str = ""


class SignConsultationDossier(BaseModel):
    """Synthesized multi-model consultation dossier for a single sign."""
    sign_id: str
    model_used: str
    cached: bool = False
    consultation_timestamp: str = ""
    iconography: SignIconographyConsultation
    phonetics: SignPhoneticConsultation
    expert_synthesis: str = ""
    skeptic_ruling: str = ""
