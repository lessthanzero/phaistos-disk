"""Pydantic data models for the Bronze Age Cretan theological context layer.

Encodes:
1. Sacred semantic fields (Potnia, Epiphany, Peak Sanctuaries, Bull Complex, Chthonic Serpents).
2. Four-tier epistemic confidence hierarchy (Archaeological cult -> Linear B -> Classical -> Narrative).
3. Liturgical syntax engine (INVOCATION -> DIVINE_TITLE -> PLACE_DOMAIN -> PETITION_ACTION -> RITUAL_RESPONSE).
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TheologicalSemanticField(str, Enum):
    """Bronze Age Cretan sacred and cultic semantic fields."""
    DIVINE_INVOCATION = "DIVINE_INVOCATION"             # Invocational formulas (02-12- prefix, 02 Plumed Head)
    DIVINE_TITLE_POTNIA = "DIVINE_TITLE_POTNIA"         # Mistress / Potnia / Sovereign female authority (06, 03, 05)
    DIVINE_EPIPHANY_SKY = "DIVINE_EPIPHANY_SKY"         # Avian messengers, celestial radiant epiphany (31, 38)
    SACRED_TOPOGRAPHY = "SACRED_TOPOGRAPHY"             # Peak sanctuaries, sacred heights, shrine facades (07, 10, 24)
    BULL_COMPLEX_SACRIFICE = "BULL_COMPLEX_SACRIFICE"   # Horns of consecration, sacrificial oxen, vital potency (26, 27, 28)
    CHTHONIC_EARTH_RENEWAL = "CHTHONIC_EARTH_RENEWAL"   # Earth powers, subterranean regeneration, serpents (40, 29, 30)
    SACRED_VEGETATION = "SACRED_VEGETATION"             # Holy trees, olive, vine, aromatic sedge first-fruits (35, 36, 37, 39)
    CULT_EQUIPMENT_VESSEL = "CULT_EQUIPMENT_VESSEL"     # Libation jugs, double axes, sacred implements (13, 14, 17, 20, 21, 41)
    MARITIME_SANCTUARY = "MARITIME_SANCTUARY"           # Pelagic gifts, sacred voyages, marine life (25, 33, 45)
    RITUAL_PRACTITIONER = "RITUAL_PRACTITIONER"         # Processional priests, votaries, initiates (01, 04, 08, 09, 22)


class ConfidenceHierarchyLevel(str, Enum):
    """Strict epistemic confidence hierarchy for Aegean religious reconstructions."""
    HIGH_ARCHAEOLOGICAL_CULT = "HIGH_ARCHAEOLOGICAL_CULT"             # Direct archaeological cult objects & findspots
    MODERATE_LINEAR_B_CONTINUITY = "MODERATE_LINEAR_B_CONTINUITY"     # Bronze Age Linear B deity titles & epigraphy
    LOW_SPECULATIVE_CLASSICAL = "LOW_SPECULATIVE_CLASSICAL"           # Retrojected Classical Greek Olympian mythology
    VERY_LOW_MYTHOLOGICAL_NARRATIVE = "VERY_LOW_MYTHOLOGICAL_NARRATIVE" # Unproven narrative pantheons or mythic decodings


class LiturgicalSyntaxRole(str, Enum):
    """Functional roles within the Bronze Age Aegean liturgical hymn syntax."""
    INVOCATION = "INVOCATION"           # Sacred call to deity / incipit (e.g. 02-12- 'O Paean!')
    DIVINE_TITLE = "DIVINE_TITLE"       # Divine name, cult epithet, Potnia designation (e.g. JA-SA-SA-RA-ME)
    PLACE_DOMAIN = "PLACE_DOMAIN"       # Sacred peak, cave, sanctuary, elemental domain (mountain, sea, shrine)
    PETITION_ACTION = "PETITION_ACTION" # Sacred rite, offering presentation, libation, sacrificial action
    RITUAL_RESPONSE = "RITUAL_RESPONSE" # Liturgical choral cadence, strophic closure, affirmative response


# Backward-compatible alias
LiturgicalRole = LiturgicalSyntaxRole


class SignTheologicalProfile(BaseModel):
    """Theological and cultic semantic profile for a single sign."""
    sign_id: str
    name: str
    semantic_field: TheologicalSemanticField
    cultic_context: str
    linear_parallels: List[str] = Field(default_factory=list)
    aegean_material_parallels: List[str] = Field(default_factory=list)
    confidence_grade: ConfidenceHierarchyLevel
    falsified_classical_retrofit: str
    notes: str = ""


class ParsedLiturgicalGroup(BaseModel):
    """A sign group classified by its grammatical and liturgical role in the hymn."""
    group_id: str
    side: str
    signs: List[str]
    assigned_role: LiturgicalSyntaxRole
    has_invocational_prefix: bool
    has_terminal_stroke: bool
    is_refrain: bool
    confidence: ConfidenceHierarchyLevel
    rationale: str


class LiturgicalSyntaxAudit(BaseModel):
    """Statistical and grammatical audit of the liturgical syntax hypothesis."""
    total_groups: int
    total_stanzas: int
    valid_transitions: int
    total_transitions: int
    transition_adherence_pct: float
    monte_carlo_p_value: float
    is_statistically_significant: bool
    strophic_summary: str


class TheologicalAuditResult(BaseModel):
    """Complete output of the Bronze Age Cretan theological context evaluation."""
    total_signs_analyzed: int
    field_token_counts: Dict[str, int]
    field_token_percentages: Dict[str, float]
    confidence_counts: Dict[str, int]
    liturgical_syntax: LiturgicalSyntaxAudit
    epistemic_guardrails_passed: bool
    skeptic_verdict: str
