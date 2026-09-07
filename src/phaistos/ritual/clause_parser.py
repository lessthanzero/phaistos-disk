"""Minoan Formulaic Clause Parser for the Phaistos Disc.

Parses the 61 individual inscription groups into 14 multi-group liturgical clauses
grounded in comparative Minoan ritual syntax (Linear A Libation Formula, Hurrian Hymn H6,
and Luwian cultic incantations), bridging the gap between isolated words and coherent ritual clauses.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from phaistos.corpus.loader import load_transcription
from phaistos.core.models import DiscCorpus, Group
from phaistos.visualizer.glyphs import get_sign_glyph_data


@dataclass
class LiturgicalClause:
    """A multi-group ritual clause bounded by syntax headers and stroke cadences."""
    clause_id: str
    side: str
    clause_number: int
    act_id: str
    act_title: str
    group_ids: List[str]
    syntactic_template: str  # e.g., [VOCATIVE_HEADER] + [DIVINE_EPITHET] + [OFFERING] + [CADENCE]
    reconstructed_action: str
    has_terminal_stroke: bool
    total_signs: int
    total_morae: int
    has_cartouche_header: bool


CANONICAL_CLAUSES_SIDE_A = [
    {
        "clause_id": "CLAUSE_A1",
        "act_id": "ACT_I",
        "act_title": "Act I: Invocation & Martial Heralds",
        "group_ids": ["A01"],
        "template": "[VOCATIVE_CARTUCHE] + [SACRED_OFFERING] + [VIRGULA_REST]",
        "action": "Opening martial proclamation invoking the plumed herald and sacred shield; sealed with cadential rest.",
    },
    {
        "clause_id": "CLAUSE_A2",
        "act_id": "ACT_I",
        "act_title": "Act I: Invocation & Martial Heralds",
        "group_ids": ["A02", "A03"],
        "template": "[ASTRAL_ROSETTE] + [CHTHONIC_INVOCATION] + [VIRGULA_REST]",
        "action": "Veneration of the celestial rosette and chthonic sanctuary guardian.",
    },
    {
        "clause_id": "CLAUSE_A3",
        "act_id": "ACT_I",
        "act_title": "Act I: Invocation & Martial Heralds",
        "group_ids": ["A04", "A05", "A06", "A07"],
        "template": "[HONEY_OFFERING] + [PELAGIC_FISH] + [CONSECRATED_HORNS] + [DOUBLE_AXE]",
        "action": "Preliminary sanctification: dedication of honey (Sign 34) and sea-offerings at the horned labrys pillar.",
    },
    {
        "clause_id": "CLAUSE_A4",
        "act_id": "ACT_II",
        "act_title": "Act II: The Great Procession of Votive Offerings",
        "group_ids": ["A08", "A09", "A10", "A11"],
        "template": "[GODDESS_CARTUCHE] + [GALLEY_BIRD] + [LIBATION_HYDRIA] + [SACRED_BRANCH]",
        "action": "The Great Goddess descent: youths lead procession with high-prow maritime galley and fluted hydria.",
    },
    {
        "clause_id": "CLAUSE_A5",
        "act_id": "ACT_II",
        "act_title": "Act II: The Great Procession of Votive Offerings",
        "group_ids": ["A12", "A13", "A14", "A15"],
        "template": "[PURIFICATION_WATER] + [SACRED_RECEPTACLE] + [HERALD_STROPHE]",
        "action": "Anointing the threshold and preparing the altar for the lyric triad paean.",
    },
    {
        "clause_id": "CLAUSE_A6",
        "act_id": "ACT_II",
        "act_title": "Act II: The Great Procession of Votive Offerings",
        "group_ids": ["A16", "A17", "A18", "A19", "A20", "A21", "A22"],
        "template": "[TRIAD_REFRAIN_1] + [CATALECTIC_STROKE] + [TRIAD_REFRAIN_2] + [STROPHE_CLOSE]",
        "action": "The Lyric Triad responsion paean (14 morae balanced across A16-A19-A22 with A18 catalectic compensation).",
    },
    {
        "clause_id": "CLAUSE_A7",
        "act_id": "ACT_III",
        "act_title": "Act III: Libation at the Double Axe Pillars",
        "group_ids": ["A23", "A24", "A25", "A26", "A27", "A28", "A29", "A30", "A31"],
        "template": "[KRATER_POURING] + [DOUBLE_AXES] + [SACRED_TREE] + [TURNOVER_CADENCE]",
        "action": "Grand libation poured between twin labrys pillars; closing Side A with solemn turnover gong.",
    },
]

CANONICAL_CLAUSES_SIDE_B = [
    {
        "clause_id": "CLAUSE_B1",
        "act_id": "ACT_IV",
        "act_title": "Act IV: The Chthonic Bull Sacrifice & Aulos Cadence",
        "group_ids": ["B01", "B02", "B03", "B04", "B05", "B06", "B07"],
        "template": "[STANZA_1_CHORUS] + [HERALDIC_SHIELD] + [CADENTIAL_VIRGULA]",
        "action": "Choral strophe 1: entering the sacrificial court with ancestral shields; sealed by stroke rest at B07.",
    },
    {
        "clause_id": "CLAUSE_B2",
        "act_id": "ACT_IV",
        "act_title": "Act IV: The Chthonic Bull Sacrifice & Aulos Cadence",
        "group_ids": ["B08", "B09", "B10", "B11", "B12"],
        "template": "[AULOS_MUSIC] + [BULL_SLAUGHTER] + [BLOOD_ASPERSION] + [CADENCE]",
        "action": "Stanza 2: Twin reed pipes (aulos, Sign 21) sound as the trussed sacrificial bull (Sign 27/28) is dedicated.",
    },
    {
        "clause_id": "CLAUSE_B3",
        "act_id": "ACT_IV",
        "act_title": "Act IV: The Chthonic Bull Sacrifice & Aulos Cadence",
        "group_ids": ["B13", "B14", "B15", "B16", "B17"],
        "template": "[MEAT_DEDICATION] + [HERALD_CARTUCHE] + [CADENTIAL_VIRGULA]",
        "action": "Stanza 3: Presentation of choice sacrificial meat portions (geras); closed by stroke rest at B17.",
    },
    {
        "clause_id": "CLAUSE_B4",
        "act_id": "ACT_IV",
        "act_title": "Act IV: The Chthonic Bull Sacrifice & Aulos Cadence",
        "group_ids": ["B18", "B19", "B20"],
        "template": "[ALTAR_VESSEL] + [INCENSE_OFFERING] + [INTER-STROPHE_PAUSE]",
        "action": "Stanza 4: Incense burning and cleansing of the sacrificial table before divine epiphany.",
    },
    {
        "clause_id": "CLAUSE_B5",
        "act_id": "ACT_V",
        "act_title": "Act V: Divine Epiphany & Closing Cadence",
        "group_ids": ["B21", "B22", "B23"],
        "template": "[GRIFFIN_HERALD] + [EPIPHANY_DESCENT] + [CADENTIAL_VIRGULA]",
        "action": "Stanza 5: Epiphany of the Great Goddess in her griffin-drawn chariot; stroke rest at B23.",
    },
    {
        "clause_id": "CLAUSE_B6",
        "act_id": "ACT_V",
        "act_title": "Act V: Divine Epiphany & Closing Cadence",
        "group_ids": ["B24", "B25", "B26", "B27"],
        "template": "[PEAK_SANCTUARY] + [CONSECRATED_HORNS] + [SACRED_TREE]",
        "action": "Consecration of the tripartite shrine facade and sacred tree in the presence of the descending deity.",
    },
    {
        "clause_id": "CLAUSE_B7",
        "act_id": "ACT_V",
        "act_title": "Act V: Divine Epiphany & Closing Cadence",
        "group_ids": ["B28", "B29", "B30"],
        "template": "[PALACE_ROSETTES] + [COSMIC_CYCLE] + [FINAL_LITURGICAL_CADENCE]",
        "action": "Final liturgical benediction framed by running palace rosettes; final rest closing the complete hymn.",
    },
]


def parse_liturgical_clauses(corpus: Optional[DiscCorpus] = None) -> List[LiturgicalClause]:
    """Parse the Disc groups into the 14 structured liturgical clauses."""
    if corpus is None:
        corpus = load_transcription()

    group_map: Dict[str, Group] = {g.id: g for g in list(corpus.side_a.groups) + list(corpus.side_b.groups)}
    results: List[LiturgicalClause] = []

    for c_idx, raw in enumerate(CANONICAL_CLAUSES_SIDE_A):
        c_groups = [group_map[gid] for gid in raw["group_ids"] if gid in group_map]
        total_signs = sum(len(g.signs) for g in c_groups)
        has_stroke = any(g.oblique_stroke for g in c_groups)
        total_morae = total_signs + (1 if has_stroke else 0)
        has_cartouche = any(len(g.signs) >= 2 and g.signs[0] == "02" and g.signs[1] == "12" for g in c_groups)

        results.append(LiturgicalClause(
            clause_id=raw["clause_id"],
            side="A",
            clause_number=c_idx + 1,
            act_id=raw["act_id"],
            act_title=raw["act_title"],
            group_ids=raw["group_ids"],
            syntactic_template=raw["template"],
            reconstructed_action=raw["action"],
            has_terminal_stroke=has_stroke,
            total_signs=total_signs,
            total_morae=total_morae,
            has_cartouche_header=has_cartouche,
        ))

    for c_idx, raw in enumerate(CANONICAL_CLAUSES_SIDE_B):
        c_groups = [group_map[gid] for gid in raw["group_ids"] if gid in group_map]
        total_signs = sum(len(g.signs) for g in c_groups)
        has_stroke = any(g.oblique_stroke for g in c_groups)
        total_morae = total_signs + (1 if has_stroke else 0)
        has_cartouche = any(len(g.signs) >= 2 and g.signs[0] == "02" and g.signs[1] == "12" for g in c_groups)

        results.append(LiturgicalClause(
            clause_id=raw["clause_id"],
            side="B",
            clause_number=c_idx + 1,
            act_id=raw["act_id"],
            act_title=raw["act_title"],
            group_ids=raw["group_ids"],
            syntactic_template=raw["template"],
            reconstructed_action=raw["action"],
            has_terminal_stroke=has_stroke,
            total_signs=total_signs,
            total_morae=total_morae,
            has_cartouche_header=has_cartouche,
        ))

    return results


def get_clauses_manifest(corpus: Optional[DiscCorpus] = None) -> Dict[str, Any]:
    """Serialize the parsed clauses for UI and CLI consumption."""
    clauses = parse_liturgical_clauses(corpus)
    return {
        "total_clauses": len(clauses),
        "side_a_clauses": [c.__dict__ for c in clauses if c.side == "A"],
        "side_b_clauses": [c.__dict__ for c in clauses if c.side == "B"],
        "clauses_by_id": {c.clause_id: c.__dict__ for c in clauses},
        "group_to_clause": {gid: c.clause_id for c in clauses for gid in c.group_ids},
    }
