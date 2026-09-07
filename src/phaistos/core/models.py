"""Data models for Phaistos Disc corpus and epigraphic entities."""

from typing import List, Optional
from pydantic import BaseModel, Field


class Sign(BaseModel):
    """Canonical catalogue entry for a stamped punch sign."""
    id: int = Field(..., ge=1, le=45, description="Sign index 1-45")
    evans_id: str = Field(..., description="Evans catalogue ID (e.g. '01', '02')")
    name: str = Field(..., description="Descriptive archaeological name")
    unicode_hex: str = Field(..., description="Unicode code point in hex (e.g. '0x101D0')")
    unicode_char: str = Field(..., description="Rendered Unicode character")
    category: str = Field(..., description="Iconographic class (human, animal, plant, etc.)")
    description: str = Field(..., description="Visual description of the punch impression")


class SignOccurrence(BaseModel):
    """An individual stamped impression at a specific position on the disc."""
    side: str = Field(..., pattern="^[AB]$")
    group_id: str = Field(..., description="E.g. 'A01', 'B12'")
    position_in_group: int = Field(..., ge=0, description="0-indexed position within group")
    global_index: int = Field(..., ge=0, description="Sequential index along reading trajectory")
    evans_id: str
    is_initial: bool = False
    is_final: bool = False
    has_oblique_stroke: bool = False
    uncertain: bool = False
    erasure: bool = False


class Group(BaseModel):
    """A radial segment / word boundary on the disc."""
    id: str = Field(..., description="Group ID, e.g. 'A01', 'B30'")
    side: str = Field(..., pattern="^[AB]$")
    turn: int = Field(..., ge=1, le=5, description="Spiral turn (1 = outermost rim)")
    signs: List[str] = Field(..., description="List of Evans sign IDs in outside-in order")
    oblique_stroke: bool = Field(default=False, description="Incised stroke beneath final sign")
    erasure: bool = Field(default=False, description="Documented palimpsest / scribal erasure")
    uncertain: bool = Field(default=False, description="Damaged or ambiguous reading")
    notes: Optional[str] = None

    @property
    def length(self) -> int:
        return len(self.signs)


class DiscSide(BaseModel):
    """One face of the Phaistos Disc."""
    side: str = Field(..., pattern="^[AB]$")
    groups: List[Group]

    @property
    def group_count(self) -> int:
        return len(self.groups)

    @property
    def sign_count(self) -> int:
        return sum(g.length for g in self.groups)

    @property
    def oblique_stroke_count(self) -> int:
        return sum(1 for g in self.groups if g.oblique_stroke)


class DiscCorpus(BaseModel):
    """Full canonical dataset of the Phaistos Disc."""
    source_id: str
    reading_direction: str
    signs_catalogue: List[Sign]
    side_a: DiscSide
    side_b: DiscSide

    @property
    def total_groups(self) -> int:
        return self.side_a.group_count + self.side_b.group_count

    @property
    def total_signs(self) -> int:
        return self.side_a.sign_count + self.side_b.sign_count

    @property
    def total_oblique_strokes(self) -> int:
        return self.side_a.oblique_stroke_count + self.side_b.oblique_stroke_count

    def all_groups(self) -> List[Group]:
        return self.side_a.groups + self.side_b.groups

    def all_occurrences(self) -> List[SignOccurrence]:
        occurrences = []
        global_idx = 0
        for group in self.all_groups():
            grp_len = len(group.signs)
            for pos, sign_id in enumerate(group.signs):
                is_final = (pos == grp_len - 1)
                occurrences.append(
                    SignOccurrence(
                        side=group.side,
                        group_id=group.id,
                        position_in_group=pos,
                        global_index=global_idx,
                        evans_id=sign_id,
                        is_initial=(pos == 0),
                        is_final=is_final,
                        has_oblique_stroke=(is_final and group.oblique_stroke),
                        uncertain=group.uncertain,
                        erasure=group.erasure,
                    )
                )
                global_idx += 1
        return occurrences
