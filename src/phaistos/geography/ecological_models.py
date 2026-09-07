"""Data models for Bronze Age Cretan ecological and geographical constraints."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SignEcologyProfile(BaseModel):
    sign_id: str
    evans_name: str
    category: str
    morphology: str
    candidate_objects: List[str]
    ecological_domain: str  # DIVINE_SKY, HUMAN_SOCIAL, AGRICULTURAL_LAND, FLORA, FAUNA, MARINE_WATER, CRAFT_TRADE
    cretan_ecological_plausibility: str  # Endemic, Cultivated, Domesticated, Exotic_Import, Mythological
    archaeological_attestation: str  # Archaeobotany (seeds, pollen) or Zooarchaeology (bones, shells)
    ritual_context: str  # Peak sanctuaries, sacred caves, libations, temple cists
    minoan_iconographic_attestation: str  # Kamares pottery, frescoes, sealstones
    near_east_parallels: str  # Egypt / Levant / Cycladic parallels
    spatial_sequential_behavior: str  # Distribution on disc (initial, medial, terminal, refrain)
    falsified_identifications: List[str]  # Candidates ruled out by ecological/material constraints
    bayesian_confidence_score: float  # 0.0 to 1.0
    epistemic_grade: str  # DIRECT, STRONG_INFERENCE, WEAK_INFERENCE, SPECULATION


class EcologicalDomainSummary(BaseModel):
    domain: str
    sign_count: int
    token_count: int
    share_of_corpus_pct: float
    key_signs: List[str]
    ecological_description: str


class EcologicalConstraintResult(BaseModel):
    total_signs_analyzed: int
    domain_distribution: List[EcologicalDomainSummary]
    flora_signs_count: int
    fauna_signs_count: int
    marine_signs_count: int
    anthropogenic_landscape_score: float
    bayesian_mean_confidence: float
    falsification_audit: List[Dict[str, str]]
    skeptic_verdict: str
