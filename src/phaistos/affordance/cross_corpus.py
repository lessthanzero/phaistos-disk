"""Cretan Bronze Age epigraphic cross-corpus material affordance comparison."""

from typing import Any, Dict, List
from pydantic import BaseModel


class CorpusMediaAffordance(BaseModel):
    media_name: str
    physical_support: str
    fabrication_method: str
    layout_topology: str
    portability: str
    typical_findspot: str
    primary_institutional_function: str
    shared_signs_with_disc: List[str]
    affordance_contrast_with_disc: str


def evaluate_cross_corpus_affordances() -> List[CorpusMediaAffordance]:
    """
    Compare the physical affordances of the Phaistos Disc against all major
    contemporary Bronze Age Cretan inscribed artifact classes.
    """
    corpus_items = [
        CorpusMediaAffordance(
            media_name="Phaistos Disc (HM 1358)",
            physical_support="Fired alluvial calcareous marl (16 cm diameter, 18 mm thickness, 507 g)",
            fabrication_method="Movable negative relief punches impressed into leather-hard clay, incised dividing lines",
            layout_topology="Archimedean unspooling spiral (2 faces, 4.2 & 4.1 turns, inside-facing orientation)",
            portability="Handheld (optimal in two-handed grip; rotatable like a steering wheel)",
            typical_findspot="Palatial bench sanctuary cist (Room 8 of Building 101, Phaistos)",
            primary_institutional_function="Sacred choral hymnal libretto / performance score & consecrated votive monument",
            shared_signs_with_disc=["All 45 canonical signs"],
            affordance_contrast_with_disc="Baseline reference: only known stamped, two-sided spiral inscription.",
        ),
        CorpusMediaAffordance(
            media_name="Arkalochori Double Axes (Gold & Bronze)",
            physical_support="Cast and hammered bronze and gold sheet votive miniature labryes",
            fabrication_method="Freehand engraving/incision with a sharp metal chisel or burin",
            layout_topology="Vertical linear columns (3 vertical lines on central blade)",
            portability="Votive miniature (easily held in palm; dedicated in sacred fissure)",
            typical_findspot="Sacred votive cave deposits (Arkalochori sacred cave hoard)",
            primary_institutional_function="Votive dedication to divine storm/sanctuary power",
            shared_signs_with_disc=["Crested head (02 parallel)", "Pillar/Shrine (24 parallel)", "Bucranium (28 parallel)"],
            affordance_contrast_with_disc=(
                "Non-spiral, single-sided, non-stamped. Shares sacred iconography but lacks "
                "the mechanical continuous-conveyor reading affordance of the Disc."
            ),
        ),
        CorpusMediaAffordance(
            media_name="Linear A Administrative Tablets (e.g. HT, PH, ZA)",
            physical_support="Unbaked sun-dried clay tablets (rectangular or page-shaped, 6-12 cm height)",
            fabrication_method="Freehand cursive stylus incision into soft moist clay, horizontal guidelines",
            layout_topology="Horizontal ruled lines read left-to-right, top-to-bottom",
            portability="Handheld archival documents (held in one hand while incising with the other)",
            typical_findspot="Palatial magazine archives, scribal bureaus, and elite villas (Ayia Triada, Zakros)",
            primary_institutional_function="Economic inventory, ration allocations, tributary ledgers (e.g. Tablet PH 1)",
            shared_signs_with_disc=["AB04 (olive/35)", "AB08 (axe/15)", "AB28 (shield/12)", "AB80 (cat/29)"],
            affordance_contrast_with_disc=(
                "Rectangular format optimized for tabular economic tallies with numerals. "
                "Not designed for oral recitation or rotation; discarded or recycled annually."
            ),
        ),
        CorpusMediaAffordance(
            media_name="Linear A Stone Libation Tables & Ladles (e.g. IO Za 2, PS Za 2)",
            physical_support="Carved steatite, chlorite, or limestone offering vessels with sunken central bowl",
            fabrication_method="Deep lapidary incision / chiseling into polished stone surface",
            layout_topology="Perimeter circumferential inscription running around top flat rim",
            portability="Heavy stationary ritual vessel (placed permanently on peak sanctuary terrace or altar)",
            typical_findspot="Peak sanctuaries (Mount Juktas) and sacred caves (Psychro)",
            primary_institutional_function="Pouring liquid libations (wine, honey, oil) to the mountain divinity",
            shared_signs_with_disc=["Libation Formula dedication JA-SA-SA-RA-ME (B13 geminate skeleton)"],
            affordance_contrast_with_disc=(
                "Circumferential inscription encircles an actual liquid basin. Read by walking around "
                "or rotating the vessel, but serves primarily as a permanent dedicating inscription."
            ),
        ),
        CorpusMediaAffordance(
            media_name="Minoan Roundels & Noduli",
            physical_support="Small clay discs and cones (2-4 cm diameter)",
            fabrication_method="Relief seal stones impressed along edges; occasional single incised Linear A sign in center",
            layout_topology="Edge perimeter stamping",
            portability="Pocket-sized administrative receipt token",
            typical_findspot="Palatial administrative offices and entry gateways",
            primary_institutional_function="Authentication of transactions, authorized quotas, and lock security",
            shared_signs_with_disc=["Sphragistic seal impression technique"],
            affordance_contrast_with_disc=(
                "Uses seal impressions for administrative verification, but lacks textual syntax, "
                "metrics, or continuous spiral narrative."
            ),
        ),
    ]

    return corpus_items
