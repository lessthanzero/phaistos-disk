"""Data models for attested Aegean theonyms and structural sieve matching."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AegeanTheonym(BaseModel):
    id: str
    name: str
    script: str
    attested_forms: List[str]
    syllable_count: int
    skeleton: str
    has_geminate: bool
    case: str
    interpretation: str
    epigraphic_findspots: List[str]


class SkeletonMatch(BaseModel):
    theonym_id: str
    theonym_name: str
    group_id: str
    side: str
    group_signs: List[str]
    is_geminate_match: bool
    is_exact_length_match: bool
    notes: str = ""


class PhonotacticTrial(BaseModel):
    theonym_name: str
    target_group_id: str
    bound_signs: Dict[str, str]
    total_signs_bound: int
    corpus_coverage_pct: float
    illegal_hiatus_count: int
    illegal_cluster_count: int
    phonotactic_satisfaction_score: float
    notes: str = ""


class TheonymSieveResult(BaseModel):
    total_theonyms_evaluated: int
    candidate_skeleton_matches_count: int
    skeleton_matches: List[SkeletonMatch]
    phonotactic_trials: List[PhonotacticTrial]
    monte_carlo_skeleton_p_value: float
    monte_carlo_phonotactic_p_value: float
    skeptic_verdict: str
