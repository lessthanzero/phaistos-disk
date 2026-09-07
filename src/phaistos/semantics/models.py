"""Data models for Phaistos Disc Semantics: Iconography, Distributional Semantics, and Libation Sieve."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class IconographicArchetype(BaseModel):
    """Middle Minoan archaeological archetype for a single relief stamp."""
    evans_id: str
    canonical_name: str
    unicode_char: str
    domain: str  # flora, fauna, tools_craft, maritime_transport, architecture_vessels, human_attiral
    physical_medium: str
    archaeological_parallels: List[str]
    material_context: str
    theological_association: Optional[str] = None
    epistemic_warning: str = "Observable relief morphology only; phonetic sound value unproven"


class IconographyCatalogResult(BaseModel):
    """Comprehensive catalog of all 45 Middle Minoan relief stamp archetypes."""
    total_stamps: int = 45
    archetypes: Dict[str, IconographicArchetype]
    domain_counts: Dict[str, int]
    dominant_material_culture: str
    skeptic_summary: str


class DistributionalVector(BaseModel):
    """Positional distribution and grammatical topology of a single sign."""
    sign_id: str
    total_occurrences: int
    initial_count: int
    medial_count: int
    final_count: int
    stroke_count: int
    initial_rate: float
    medial_rate: float
    final_rate: float
    stroke_rate: float
    functional_class: str  # invocational_clitic, core_stem, suffixal_postposition, hapax_isolated
    latent_coordinates: List[float] = Field(default_factory=list)


class DistributionalSemanticsResult(BaseModel):
    """Unsupervised distributional semantics and functional clustering across all 61 groups."""
    total_signs_analyzed: int
    sign_vectors: Dict[str, DistributionalVector]
    functional_classes: Dict[str, List[str]]
    explained_variance_ratio_svd: List[float]
    clustering_silhouette_score: float
    null_surrogate_mean_silhouette: float
    null_surrogate_std_silhouette: float
    clustering_z_score: float
    clustering_p_value: float
    skeptic_verdict: str


class LibationSieveAlignment(BaseModel):
    """Structural alignment between a GORILA Linear A libation vessel and Phaistos Disc patterns."""
    inscription_id: str
    findspot: str
    sanctuary_type: str
    material_object: str
    linear_a_text: str
    formulaic_head: str
    theonym_present: bool
    structural_matches: List[str]


class LibationSieveResult(BaseModel):
    """Comparative structural sieve comparing the Phaistos Disc against the 14 GORILA Linear A libation vessels."""
    total_linear_a_inscriptions: int = 14
    alignments: List[LibationSieveAlignment]
    disc_formulaic_prefix: str = "02-12 (Plumed Head + Shield)"
    disc_prefix_recurrence_rate: float
    linear_a_head_recurrence_rate: float
    herfindahl_index_disc_heads: float
    herfindahl_index_linear_a_heads: float
    liturgical_affinity_z_score: float
    administrative_divergence_p_value: float
    skeptic_verdict: str
