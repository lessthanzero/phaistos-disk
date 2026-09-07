"""Sign-by-Sign Liturgical Homology Breakdown Engine.

Connects every sign punch on the Phaistos Disc directly to physical Minoan realia
depicted on the contemporary Hagia Triada Sarcophagus (c. 1400–1350 BC, Heraklion Museum Λ396),
resolving the visual association gap with explicit scholarly grounding.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from phaistos.corpus.loader import load_transcription
from phaistos.core.models import DiscCorpus, Group
from phaistos.visualizer.glyphs import get_sign_glyph_data


@dataclass
class SignRealiaMatch:
    """Explicit homology match between a Phaistos punch and Hagia Triada fresco realia."""
    sign_id: str
    sign_name: str
    sign_emoji: str
    crop_id: str
    crop_title: str
    scene_id: str
    scene_title: str
    ritual_plane: str
    fresco_element: str
    scholarly_rationale: str
    confidence_tier: str  # PRIMARY_ARCHETYPE, SECONDARY_PARALLEL, STRUCTURAL_CLASSIFIER


@dataclass
class GroupHomologyBreakdown:
    """Detailed liturgical and iconographic dissection of a single Phaistos Disc group."""
    group_id: str
    side: str
    turn: int
    signs: List[str]
    is_determinative_header: bool  # True if starts with 02-12 (Plumed Head + Shield)
    act_id: str
    act_title: str
    primary_scene_id: str
    primary_scene_title: str
    liturgical_role: str
    action_narrative: str
    sign_matches: List[Dict[str, Any]]
    has_stroke: bool


# Canonical Sign Homology Registry grounded in Evans (1909), Long (1974), and Marinatos (1993)
SIGN_HOMOLOGY_REGISTRY: Dict[str, Dict[str, Any]] = {
    "02": {
        "crop_id": "crop_griffin_chariot",
        "crop_title": "Winged Griffin Chariot Epiphany",
        "scene_id": "HT_SCENE_4",
        "scene_title": "Scene 4: Divine Epiphany & Peak Shrine",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Plumed crest of divine attendants / warrior herald preceding deity chariot",
        "scholarly_rationale": "Evans (1909) and Long (1974) identify the crested head as a sacred herald or military leader dedicated to the Mother Goddess.",
        "confidence_tier": "STRUCTURAL_CLASSIFIER",
    },
    "06": {
        "crop_id": "crop_griffin_chariot",
        "crop_title": "Winged Griffin Chariot Epiphany",
        "scene_id": "HT_SCENE_4",
        "scene_title": "Scene 4: Divine Epiphany & Peak Shrine",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Goddess in flounced ritual skirt enthroned in chariot",
        "scholarly_rationale": "Marinatos (1993): The flounced-skirt female figure represents the Minoan Great Goddess receiving the dead hero's offerings.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "12": {
        "crop_id": "crop_lyre_player",
        "crop_title": "7-String Phorminx Musician",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation & Labrys Sanctuary",
        "ritual_plane": "MUSIC / CONTROL",
        "fresco_element": "Figure-eight sacred shield worn as talisman; paired with phorminx player",
        "scholarly_rationale": "Nilsson (1950): The figure-eight shield is an apotropaic aniconic manifestation of the war/chthonic goddess guarding the ceremony.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "21": {
        "crop_id": "crop_aulos_player",
        "crop_title": "Twin Reed Pipes (Aulos) Musician",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "MUSIC / CONTROL",
        "fresco_element": "Youth playing the twin reed pipes (diaulos) directly beside the sacrificial altar",
        "scholarly_rationale": "Long (1974): Continuous double-reed music was required during Minoan animal sacrifice to mask dying groans and induce ritual ecstasy.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "23": {
        "crop_id": "crop_peak_shrine_tree",
        "crop_title": "Sacred Tree & Peak Shrine Altar",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Sacred olive/cypress tree growing within the sanctuary precinct behind the altar",
        "scholarly_rationale": "Marinatos (1993): Dendrolatry (tree worship) was central to Minoan peak sanctuaries, symbolizing seasonal rebirth.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "24": {
        "crop_id": "crop_palace_rosette",
        "crop_title": "Palatial Rosette Frize",
        "scene_id": "HT_SCENE_4",
        "scene_title": "Scene 4: Divine Epiphany & Peak Shrine",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Running 8-petaled rosette frieze bordering the sacred perimeter of the sarcophagus",
        "scholarly_rationale": "Evans (1909): The rosette signifies the astral solar aspect of the Minoan goddess and marks palatial ritual boundaries.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "26": {
        "crop_id": "crop_boat_model",
        "crop_title": "Processional High-Prow Boat Model",
        "scene_id": "HT_SCENE_3",
        "scene_title": "Scene 3: Procession of Votive Offerings",
        "ritual_plane": "OFFERING",
        "fresco_element": "Youth holding a high-prow bronze/terracotta galley model offered to the hero's tomb",
        "scholarly_rationale": "Long (1974) & Marinatos (1993): The boat offering represents the voyage across the Western Sea to the Isles of the Blessed.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "27": {
        "crop_id": "crop_trussed_bull",
        "crop_title": "Trussed Sacrificial Bull",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "OFFERING",
        "fresco_element": "Consecrated bovine horns and blood collection bucket beneath sacrificial table",
        "scholarly_rationale": "Long (1974): Horns of consecration establish the holy boundary where the bull's life-force is returned to the deity.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "28": {
        "crop_id": "crop_trussed_bull",
        "crop_title": "Trussed Sacrificial Bull",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "OFFERING",
        "fresco_element": "Trussed bull's hind leg and sacrificial meat haunch dedicated on the altar",
        "scholarly_rationale": "Nilsson (1950): The bull leg represents the choicest priestly meat portion (geras) reserved for the divinity.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "30": {
        "crop_id": "crop_calf_offering",
        "crop_title": "Bovine Votive Figurines",
        "scene_id": "HT_SCENE_3",
        "scene_title": "Scene 3: Procession of Votive Offerings",
        "ritual_plane": "OFFERING",
        "fresco_element": "Sculptural animal figurines (calves/rams) carried horizontally in youths' arms",
        "scholarly_rationale": "Long (1974): Votive substitutes presented to the chthonic recipient in lieu of living sacrificial beasts.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "31": {
        "crop_id": "crop_labrys_double_axe",
        "crop_title": "Stepped Double Axe & Epiphany Bird",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation & Labrys Sanctuary",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Sacred black bird perched atop the gilded double axe on stepped vegetation base",
        "scholarly_rationale": "Nilsson (1950): The bird represents the physical epiphany of the deity descending onto the sacrificial pillar.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "32": {
        "crop_id": "crop_labrys_double_axe",
        "crop_title": "Stepped Double Axe & Epiphany Bird",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation & Labrys Sanctuary",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Second bird perched on right-hand labrys pillar overlooking the libation krater",
        "scholarly_rationale": "Marinatos (1993): Paired birds denote the dual presence of the celestial and underworld aspects of the divinity.",
        "confidence_tier": "SECONDARY_PARALLEL",
    },
    "35": {
        "crop_id": "crop_peak_shrine_tree",
        "crop_title": "Sacred Tree & Peak Shrine Altar",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "OFFERING",
        "fresco_element": "Freshly cut branches and foliage decorating the sacrificial altar table",
        "scholarly_rationale": "Long (1974): Foliage placed under the sacrificial victim to catch dripping blood and adorn the shrine.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "37": {
        "crop_id": "crop_peak_shrine_tree",
        "crop_title": "Sacred Tree & Peak Shrine Altar",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Stepped podium architecture elevating the altar and sacred tree above ground level",
        "scholarly_rationale": "Evans (1909): The stepped structure represents Minoan tripartite stepped altars found in Phaistos central court.",
        "confidence_tier": "SECONDARY_PARALLEL",
    },
    "38": {
        "crop_id": "crop_peak_shrine_tree",
        "crop_title": "Sacred Tree & Peak Shrine Altar",
        "scene_id": "HT_SCENE_2",
        "scene_title": "Scene 2: Blood Sacrifice of Trussed Bull",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Tripartite shrine building crowned by horns of consecration and sacred tree",
        "scholarly_rationale": "Marinatos (1993): Tripartite sanctuary facade housing the inner sanctum of the peak goddess.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "39": {
        "crop_id": "crop_libation_hydria",
        "crop_title": "Libation Pitcher & Krater",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation & Labrys Sanctuary",
        "ritual_plane": "OFFERING",
        "fresco_element": "Large bronze/ceramic krater sitting between the two labrys pillars catching the liquid",
        "scholarly_rationale": "Long (1974): Krater used for mixing wine, honey, and blood during the funerary libation rite.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "41": {
        "crop_id": "crop_libation_hydria",
        "crop_title": "Libation Pitcher & Krater",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation & Labrys Sanctuary",
        "ritual_plane": "OFFERING",
        "fresco_element": "High-necked fluted libation hydria held by the priestess pouring liquid offering",
        "scholarly_rationale": "Nilsson (1950): The hydria is the canonical vessel of liquid libation in Middle and Late Minoan ritual.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
    "44": {
        "crop_id": "crop_labrys_double_axe",
        "crop_title": "Stepped Double Axe & Epiphany Bird",
        "scene_id": "HT_SCENE_1",
        "scene_title": "Scene 1: Libation & Labrys Sanctuary",
        "ritual_plane": "INVOCATION / DEITY",
        "fresco_element": "Gilded ceremonial double axe mounted on a tall stepped base covered in greenery",
        "scholarly_rationale": "Marinatos (1993): The labrys is the paramount cult emblem of Minoan religion, channeling divine presence.",
        "confidence_tier": "PRIMARY_ARCHETYPE",
    },
}

# The 5 Sacred Liturgical Acts defining the overarching ceremonial storyboard
LITURGICAL_ACTS = [
    {
        "id": "ACT_I",
        "title": "Act I: Invocation & Martial Heralds",
        "group_range": "A01–A08",
        "groups": ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08"],
        "scene_id": "HT_SCENE_4",
        "scene_name": "Divine Epiphany & Heralds",
        "theme": "Opening invocation of divine and ancestral guardians; heralds display the sacred figure-eight shield and plumed crest.",
    },
    {
        "id": "ACT_II",
        "title": "Act II: The Great Procession of Votive Offerings",
        "group_range": "A09–A22",
        "groups": ["A09", "A10", "A11", "A12", "A13", "A14", "A15", "A16", "A17", "A18", "A19", "A20", "A21", "A22"],
        "scene_id": "HT_SCENE_3",
        "scene_name": "Procession of Votives",
        "theme": "Procession of youths bearing models of high-prow maritime galleys (Sign 26) and bovine figurines (Sign 30), punctuated by the lyric triad refrain (A16-A19-A22).",
    },
    {
        "id": "ACT_III",
        "title": "Act III: Libation at the Double Axe Pillars",
        "group_range": "A23–A31",
        "groups": ["A23", "A24", "A25", "A26", "A27", "A28", "A29", "A30", "A31"],
        "scene_id": "HT_SCENE_1",
        "scene_name": "Libation at Double Axes",
        "theme": "Priestess pours libation from the high-necked hydria (Sign 41) into the sacred krater between stepped double axes crowned with birds of epiphany.",
    },
    {
        "id": "ACT_IV",
        "title": "Act IV: The Chthonic Bull Sacrifice & Aulos Cadence",
        "group_range": "B01–B20",
        "groups": [
            "B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10",
            "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20"
        ],
        "scene_id": "HT_SCENE_2",
        "scene_name": "Blood Sacrifice of the Trussed Bull",
        "theme": "Slaughter of the trussed bull on the wooden table; dedication of sacrificial haunches (Sign 28) and horns (Sign 27) accompanied by twin reed pipes / aulos music (Sign 21).",
    },
    {
        "id": "ACT_V",
        "title": "Act V: Divine Epiphany & Closing Cadence",
        "group_range": "B21–B30",
        "groups": ["B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29", "B30"],
        "scene_id": "HT_SCENE_4",
        "scene_name": "Divine Epiphany & Peak Shrine",
        "theme": "The descent of the Great Goddess in her griffin-drawn chariot, circumscribed by palace rosettes (Sign 24), closing with the final ritual virgula stroke rest.",
    },
]


def get_act_for_group(group_id: str) -> Dict[str, Any]:
    """Return the Liturgical Act metadata corresponding to a group ID."""
    for act in LITURGICAL_ACTS:
        if group_id in act["groups"]:
            return act
    return LITURGICAL_ACTS[0]


def build_group_breakdown(group: Group, corpus: DiscCorpus) -> GroupHomologyBreakdown:
    """Build a complete, transparent archaeological breakdown for a single group."""
    is_header = len(group.signs) >= 2 and group.signs[0] == "02" and group.signs[1] == "12"
    act = get_act_for_group(group.id)

    sign_matches: List[Dict[str, Any]] = []
    primary_scene_id = act["scene_id"]
    primary_scene_title = act["scene_name"]

    for idx, s in enumerate(group.signs):
        pad_s = f"{int(s):02d}" if s.isdigit() else s
        glyph_data = get_sign_glyph_data(pad_s)
        match_info = SIGN_HOMOLOGY_REGISTRY.get(pad_s)

        if match_info:
            sign_matches.append({
                "sign_id": pad_s,
                "name": glyph_data.get("name", f"Sign {pad_s}"),
                "emoji": glyph_data.get("emoji", "𐇐"),
                "short_name": glyph_data.get("short_name", f"Sign {pad_s}"),
                "has_realia_match": True,
                "crop_id": match_info["crop_id"],
                "crop_title": match_info["crop_title"],
                "scene_id": match_info["scene_id"],
                "scene_title": match_info["scene_title"],
                "ritual_plane": match_info["ritual_plane"],
                "fresco_element": match_info["fresco_element"],
                "rationale": match_info["scholarly_rationale"],
                "confidence_tier": match_info["confidence_tier"],
            })
            # Refine primary scene to the most diagnostic specific realia match if present
            if match_info["confidence_tier"] == "PRIMARY_ARCHETYPE":
                primary_scene_id = match_info["scene_id"]
                primary_scene_title = match_info["scene_title"]
        else:
            sign_matches.append({
                "sign_id": pad_s,
                "name": glyph_data.get("name", f"Sign {pad_s}"),
                "emoji": glyph_data.get("emoji", "𐇐"),
                "short_name": glyph_data.get("short_name", f"Sign {pad_s}"),
                "has_realia_match": False,
                "crop_id": None,
                "crop_title": "Secondary / Subordinate Phonetic Token",
                "scene_id": act["scene_id"],
                "scene_title": act["scene_name"],
                "ritual_plane": "PHONETIC MORA",
                "fresco_element": "Phonetic connective or inflectional element without isolated fresco depiction",
                "rationale": "Functions as a syllabic phonogram connecting primary iconographic archetypes.",
                "confidence_tier": "PHONETIC_CONNECTIVE",
            })

    # Synthesize group-level action narrative
    matched_names = [m["short_name"] for m in sign_matches if m["has_realia_match"]]
    matched_elements = [m["fresco_element"] for m in sign_matches if m["has_realia_match"]]

    if is_header:
        header_text = "Formulaic Plumed Herald + Shield Header (Honorific Cartouche). "
    else:
        header_text = ""

    if matched_elements:
        narrative = f"{header_text}Liturgical presentation invoking {', '.join(matched_names)}. Archaeological parallel: {'; '.join(matched_elements[:2])}."
    else:
        narrative = f"{header_text}Intoned phonetic chant strophe in {act['title']}."

    return GroupHomologyBreakdown(
        group_id=group.id,
        side=group.side,
        turn=group.turn,
        signs=group.signs,
        is_determinative_header=is_header,
        act_id=act["id"],
        act_title=act["title"],
        primary_scene_id=primary_scene_id,
        primary_scene_title=primary_scene_title,
        liturgical_role="CARTUCHE_HEADER" if is_header else "SACRED_RECITATION",
        action_narrative=narrative,
        sign_matches=sign_matches,
        has_stroke=group.oblique_stroke,
    )


def get_all_groups_homology_manifest(corpus: Optional[DiscCorpus] = None) -> Dict[str, Any]:
    """Compute and serialize the complete 61-group homology manifest for frontend consumption."""
    if corpus is None:
        corpus = load_transcription()

    groups_manifest: Dict[str, Any] = {}

    all_groups = list(corpus.side_a.groups) + list(corpus.side_b.groups)
    for g in all_groups:
        bd = build_group_breakdown(g, corpus)
        groups_manifest[g.id] = {
            "group_id": bd.group_id,
            "side": bd.side,
            "turn": bd.turn,
            "signs": bd.signs,
            "is_determinative_header": bd.is_determinative_header,
            "act_id": bd.act_id,
            "act_title": bd.act_title,
            "primary_scene_id": bd.primary_scene_id,
            "primary_scene_title": bd.primary_scene_title,
            "liturgical_role": bd.liturgical_role,
            "action_narrative": bd.action_narrative,
            "has_stroke": bd.has_stroke,
            "sign_matches": bd.sign_matches,
        }

    return {
        "acts": LITURGICAL_ACTS,
        "sign_registry": SIGN_HOMOLOGY_REGISTRY,
        "groups": groups_manifest,
    }
