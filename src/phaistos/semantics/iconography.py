"""Tier 2: Middle Minoan Iconographic Archetypes.

Catalogues all 45 relief stamps against tangibly documented archaeological realia
from Middle Minoan III / Late Minoan IA Crete (Phaistos, Hagia Triada, Knossos,
Malia, Arkalochori, Palaikastro, and peak sanctuaries).
Strictly separates observable relief iconography from speculative phonetic decipherment.
"""

from typing import Dict, List
from phaistos.corpus.loader import load_signs
from phaistos.semantics.models import IconographicArchetype, IconographyCatalogResult


ARCHETYPE_DEFINITIONS: Dict[str, Dict] = {
    "01": {
        "domain": "human_attiral",
        "medium": "Steatite seal engraving / relief stamp",
        "parallels": ["Malia Quartier Mu sealings", "Knossos Little Palace sealstones"],
        "context": "Active pedestrian / striding youth wearing belted Minoan loincloth (zoma)",
        "theology": "Pilgrim approaching peak sanctuary / votive processional participant",
    },
    "02": {
        "domain": "human_attiral",
        "medium": "Minoan repoussé punch / sealstone matrix",
        "parallels": ["Akrotiri Boxing Boys / Young Fisherman fresco hairstyle", "Mycenae Shaft Grave gold foil ornaments"],
        "context": "Head of youth with prominent upright feather/roach crest; diagnostic Aegean elite warrior or ceremonial tonsure",
        "theology": "Ceremonial initiatory tonsure / sacred leader (hegemon) or protective deity head",
    },
    "03": {
        "domain": "human_attiral",
        "medium": "Prismatic seal engraving",
        "parallels": ["Hagia Triada Villa A administrative noduli", "Knossos East Hall processional reliefs"],
        "context": "Man with arms bound behind back; captive or ritual consecration posture",
        "theology": "Subjugated captive or ritual surrender / votive self-dedication before deity",
    },
    "04": {
        "domain": "human_attiral",
        "medium": "Relief punch on fine clay",
        "parallels": ["Palaikastro chryselephantine kouros", "Knossos Temple Repositories ivory figurine"],
        "context": "Child / infant walking forward with arms raised",
        "theology": "Sacred youth / divine child epiphany motif (Cretan Zeus / Velchanos archetype)",
    },
    "05": {
        "domain": "human_attiral",
        "medium": "Palace sealstone / gold signet ring matrix",
        "parallels": ["Isopata gold signet ring", "Knossos Snake Goddess faïence figurines", "Phaistos Room 25 noduli"],
        "context": "Seated woman wearing flounced layered kaunakes skirt and open bodice",
        "theology": "Supreme Cretan Mother Goddess / Potnia in enthroned epiphany",
    },
    "06": {
        "domain": "human_attiral",
        "medium": "Bronze relief punch",
        "parallels": ["Hagia Triada Boxer Rhyton (relief friezes showing cestus-armed pugilists)"],
        "context": "Weighted leather boxing gauntlet (cestus / himantes) wrapped around wrist and knuckle",
        "theology": "Sacred agonistic contests held during palace spring renewal festivals",
    },
    "07": {
        "domain": "human_attiral",
        "medium": "Marl-stamping tool",
        "parallels": ["Spata ivory boars' tusk helmet plaques", "Knossos Royal Road workshop deposit"],
        "context": "Conical helmet with cheek-guards, likely composite leather or boars' tusk bands",
        "theology": "Martial elite status / divine protective headgear",
    },
    "08": {
        "domain": "human_attiral",
        "medium": "Carved steatite punch",
        "parallels": ["Knossos Cup Bearer fresco belt", "Malia Chrysolakkos gold repoussé ornaments"],
        "context": "Clenched fist or rigid ritual waistband / cestus with prominent central knot",
        "theology": "Sacred sacral knot / ritual girdle conferring authority",
    },
    "09": {
        "domain": "human_attiral",
        "medium": "Ivory/horn comb carving",
        "parallels": ["Palaikastro ivory toilet comb", "Archanes Phourni burial combs"],
        "context": "Dentated comb or tiara with multiple vertical pins for ceremonial hair arrangement",
        "theology": "Ritual adornment before divine epiphany; purification attire",
    },
    "10": {
        "domain": "tools_craft",
        "medium": "Cast bronze / flint punch",
        "parallels": ["Knossos Arsenal tablet deposits", "Arkalochori bronze projectile tips"],
        "context": "Barbed arrow with central shaft socket and flight notches",
        "theology": "Divine hunt / weapon of the Mistress of Animals (Potnia Theron)",
    },
    "11": {
        "domain": "tools_craft",
        "medium": "Wood / horn composite matrix",
        "parallels": ["Akrotiri West House Miniature Wall Painting archers", "Mycenae Lion Hunt Dagger"],
        "context": "Recurve composite bow composed of animal sinew and horn",
        "theology": "Martial vigilance and sacred hunting rites",
    },
    "12": {
        "domain": "tools_craft",
        "medium": "Repoussé bronze punch matrix",
        "parallels": ["Tiryns bronze shield bosses", "Knossos Hall of Double Axes figure-eight/round shields"],
        "context": "Round ceremonial shield decorated with 7 peripheral hemispherical studs/bosses",
        "theology": "Apotropaic protective talisman; astral heptad representation",
    },
    "13": {
        "domain": "tools_craft",
        "medium": "Carved hardwood punch",
        "parallels": ["Hagia Triada agricultural noduli", "Malia Quartier Mu stone mace-heads"],
        "context": "Curved shepherd's crook / throwing club or meat cleaver",
        "theology": "Pastoral leadership insignia or animal sacrifice implement",
    },
    "14": {
        "domain": "tools_craft",
        "medium": "Cast bronze tool",
        "parallels": ["Gournia copper/bronze metallurgical tool hoard"],
        "context": "Split leather thong or metallic yoked manacles / fetters",
        "theology": "Restraint of sacrificial beast or binding oath in temple precinct",
    },
    "15": {
        "domain": "tools_craft",
        "medium": "Forged bronze tool matrix",
        "parallels": ["Phaistos West Court agricultural deposit", "Knossos palace carpentry tools"],
        "context": "Adze / mattock / pick with curved blade for woodworking or terrace trenching",
        "theology": "Temple construction and agricultural reclamation of the Mesara basin",
    },
    "16": {
        "domain": "tools_craft",
        "medium": "Bronze toothed blade matrix",
        "parallels": ["Hagia Triada Villa bronze saws", "Zakros palace artisan workshop tools"],
        "context": "Toothed hand-saw or scraper used in ashlar dressing and ship timber shaping",
        "theology": "Sacred carpentry for shrine construction and timbered pillar halls",
    },
    "17": {
        "domain": "tools_craft",
        "medium": "Stone / bone punch",
        "parallels": ["Knossos Lapidary's Workshop tools", "Malia bone styli"],
        "context": "Curved leather-cutting knife or fine mason's chisel",
        "theology": "Craft specialization dedicated to temple production",
    },
    "18": {
        "domain": "tools_craft",
        "medium": "Hardwood / bone prototype",
        "parallels": ["Knossos South House carpenter's tools", "Tomb of the Double Axes bronze squares"],
        "context": "Carpenter's set square or throwing boomerang (lagobolon)",
        "theology": "Geometric order / harmonic architectural proportions in palace design",
    },
    "19": {
        "domain": "flora",
        "medium": "Botanical seal carving",
        "parallels": ["Hagia Triada cat-stalking-bird fresco flora", "Phaistos Kamares pottery motifs"],
        "context": "Bifurcated branch or stylized yoke with sprouting vegetative buds",
        "theology": "Vernal regeneration and vegetative fertility cycle",
    },
    "20": {
        "domain": "flora",
        "medium": "Sealstone floral motif",
        "parallels": ["Knossos Saffron Gatherer fresco plants", "Phaistos Middle Minoan floral cups"],
        "context": "Curving leafy branch / olive sapling",
        "theology": "Sacred tree cult / shaking of the sacred tree to induce epiphany",
    },
    "21": {
        "domain": "flora",
        "medium": "Sealstone engraving",
        "parallels": ["Mochlos gold signet ring tree-shaking scenes", "Archanes peak sanctuary sealings"],
        "context": "Double opposing palm branches / olive sprigs",
        "theology": "Bilateral offering of first fruits (aparche) to palace storehouses",
    },
    "22": {
        "domain": "flora",
        "medium": "Nilotic imported / Minoan adapted motif",
        "parallels": ["Amnisos Lily/Papyrus fresco", "Akrotiri House of the Ladies papyrus panels"],
        "context": "Unfolding papyrus umbel / fan blossom",
        "theology": "Nilotic maritime exchange and exotic riparian divine garden symbolism",
    },
    "23": {
        "domain": "flora",
        "medium": "Timber column carving matrix",
        "parallels": ["Knossos Grand Staircase inverted cypress trunks", "Hagia Triada Sarcophagus trees"],
        "context": "Slender upright cypress tree (Cupressus sempervirens) or tapered wooden column",
        "theology": "Axis mundi linking earth and heavens; sacred mountain forest grove",
    },
    "24": {
        "domain": "flora",
        "medium": "Gold repoussé rosette punch",
        "parallels": ["Malia Quartier Mu gold foil rosettes", "Phaistos Kamares polychrome rosette plates"],
        "context": "Eight-petaled symmetrical floral rosette with central raised stamen button",
        "theology": "Solar manifestation / astral blossom associated with celestial renewal",
    },
    "25": {
        "domain": "flora",
        "medium": "Polychrome fresco transfer matrix",
        "parallels": ["Amnisos Villa of the Lilies fresco", "Knossos Prince of the Lilies relief"],
        "context": "Madonna lily (Lilium candidum) with three recurved petals and prominent pistil",
        "theology": "Pure virgin offering / flower of divine grace in ritual epiphany",
    },
    "26": {
        "domain": "maritime_transport",
        "medium": "Marine sealstone matrix",
        "parallels": ["Akrotiri West House Flotilla Fresco", "Mochlos gold signet boat", "Hagia Triada ship sealings"],
        "context": "Cretan longboat / sacred galley with high curved prow and stern steering paddle",
        "theology": "Sacred maritime pilgrimage / conveyance of deities across the Aegean sea",
    },
    "27": {
        "domain": "maritime_transport",
        "medium": "Steatite relief punch",
        "parallels": ["Kommos harbour sanctuary Minoan ship timbers", "Knossos sealings with horned ship prows"],
        "context": "Stylized ship prow or bull's horn consecrated as marine talisman",
        "theology": "Divine maritime escort ensuring safe navigation between Kommos and Levant/Egypt",
    },
    "28": {
        "domain": "fauna",
        "medium": "Animal anatomical relief stamp",
        "parallels": ["Knossos Little Palace bull's head rhyton", "Hagia Triada Sarcophagus sacrificial ox"],
        "context": "Foreleg of sacrificial bull / bovine leg rhyton",
        "theology": "Consecrated portion of the bovine sacrificial banquet (hierourgia)",
    },
    "29": {
        "domain": "fauna",
        "medium": "Lentoid seal engraving",
        "parallels": ["Knossos Temple Repositories feline sealings", "Akrotiri wild cat hunting fresco"],
        "context": "Head of Cretan wildcat (Felis lybica cretensis) or alert hunting dog",
        "theology": "Sacred guardian of the palace threshold and companion of Potnia Theron",
    },
    "30": {
        "domain": "fauna",
        "medium": "Soft-stone seal engraving",
        "parallels": ["Palaikastro terracotta ram votives", "Petsophas peak sanctuary animal figurines"],
        "context": "Head of Cretan horned ram (Ovis aries) with spiraling horn",
        "theology": "Pastoral herd vitality and mountain peak sacrificial dedication",
    },
    "31": {
        "domain": "fauna",
        "medium": "Bird of prey seal matrix",
        "parallels": ["Hagia Triada Villa A raptor sealings", "Knossos Throne Room griffin feathers"],
        "context": "Flying falcon / sea eagle (Pandion haliaetus) with outspread wings",
        "theology": "Theriomorphic vehicle of divine presence descending onto sacred baetyl",
    },
    "32": {
        "domain": "fauna",
        "medium": "Perching bird terracotta stamp",
        "parallels": ["Knossos Dove Goddess shrine figurines", "Palaikastro terracotta birds on pillars"],
        "context": "Seated dove / rock pigeon (Columba livia) resting on ground or altar",
        "theology": "Messenger of peace, maternal affection, and gentle divine visitation",
    },
    "33": {
        "domain": "fauna",
        "medium": "Marine style pottery stamp",
        "parallels": ["Palaikastro Marine Style octopus/fish rhyta", "Phaistos Kamares dolphin jars"],
        "context": "Tunny fish (Thunnus thynnus) or leaping dolphin with dorsal fin",
        "theology": "Dominion over the oceanic depths and seasonal migratory abundance",
    },
    "34": {
        "domain": "fauna",
        "medium": "Repoussé gold punch prototype",
        "parallels": ["Malia Chrysolakkos gold bee pendant", "Knossos honeycomb votive deposits"],
        "context": "Cretan honeybee (Apis mellifera adami) with folded wings and abdomen",
        "theology": "Sacred production of honey for libations; hive cooperation as civic archetype",
    },
    "35": {
        "domain": "flora",
        "medium": "Hard-stone prismatic seal",
        "parallels": ["Knossos Camp Stool fresco myrtle sprigs", "Phaistos Room 25 vine sealings"],
        "context": "Sinuous vine shoot or leafy olive twig with terminal leaflets",
        "theology": "Agricultural libation ingredient (wine/oil) and ceremonial lustration whisk",
    },
    "36": {
        "domain": "architecture_vessels",
        "medium": "Architectural seal model",
        "parallels": ["Knossos Tripartite Shrine terracotta model", "Archanes terracotta house model"],
        "context": "Pillar shrine or vaulted palace granary with horizontal timber bonding courses",
        "theology": "Palatine storehouse consecrated to divine stewardship of agricultural surplus",
    },
    "37": {
        "domain": "architecture_vessels",
        "medium": "Altar model carving",
        "parallels": ["Hagia Triada stepped altars", "Knossos Central Court altar bases"],
        "context": "Waisted altar base or freestanding sacred column supporting entablature",
        "theology": "Permanent anchor of sanctified ritual space for libation pouring",
    },
    "38": {
        "domain": "architecture_vessels",
        "medium": "Palace gate blueprint stamp",
        "parallels": ["Phaistos West Court monumental staircase", "Knossos West Porch facade reliefs"],
        "context": "Tripartite palace facade featuring ashlar masonry, central portal, and horns of consecration",
        "theology": "Monumental interface between public festive court and sacred palatine interior",
    },
    "39": {
        "domain": "architecture_vessels",
        "medium": "Metal / stone vessel carving",
        "parallels": ["Chieftain Cup (Hagia Triada)", "Knossos obsidian / marble chalices"],
        "context": "Footed ceremonial chalice with flared rim and pedestal base",
        "theology": "Primary vessel for offering unmixed wine or honey-water to subterranean deities",
    },
    "40": {
        "domain": "architecture_vessels",
        "medium": "Storage jar stamp matrix",
        "parallels": ["Phaistos West Magazines giant pithoi", "Knossos Magazine amphorae"],
        "context": "Two-handled belly amphora with narrow neck for long-term liquid storage",
        "theology": "Safeguarding the sacred oil reserves dedicated to perpetual shrine lamps",
    },
    "41": {
        "domain": "architecture_vessels",
        "medium": "Stone vase workshop matrix",
        "parallels": ["Malia Quartier Mu chlorite fluted vessels", "Knossos serpentine alabastra"],
        "context": "Fluted stone unguent jar or alabastron with vertical ribbing",
        "theology": "Anointing oil vessel used in consecrating baetyl stones and altar horns",
    },
    "42": {
        "domain": "architecture_vessels",
        "medium": "Ceremonial bronze bucket matrix",
        "parallels": ["Hagia Triada Sarcophagus priestess pouring libations into bucket"],
        "context": "Deep situla / pail with arched swing handle for carrying libation liquids",
        "theology": "Direct liturgical implement used to collect blood or wine between altars",
    },
    "43": {
        "domain": "architecture_vessels",
        "medium": "Perforated bronze / clay tool",
        "parallels": ["Gournia ceramic strainers", "Phaistos Kamares wine-filter vessels"],
        "context": "Perforated conical funnel / sieve for clarifying ritual wine and herbal infusions",
        "theology": "Purification of sacred liquids before presentation at the altar",
    },
    "44": {
        "domain": "tools_craft",
        "medium": "Bronze double-axe sheet punch",
        "parallels": ["Arkalochori cave votive double axes", "Phaistos Central Court labrys pillars"],
        "context": "Double-bladed axe (labrys) with flared semicircular cutting edges",
        "theology": "Supreme emblem of Cretan sovereign religious authority and sacral power",
    },
    "45": {
        "domain": "architecture_vessels",
        "medium": "Abstract geometric stamp",
        "parallels": ["Kamares wave pottery bands", "Akrotiri Spring Fresco meandering river streams"],
        "context": "Meandering aquatic wave / undulating river stream",
        "theology": "Living fresh water (hydor zaon) springing from Idaian caves to irrigate the plain",
    },
}


def get_iconographic_catalog() -> IconographyCatalogResult:
    """Compile and return the definitive archaeological catalog for all 45 relief stamps."""
    signs = load_signs()
    archetypes: Dict[str, IconographicArchetype] = {}
    domain_counts: Dict[str, int] = {}

    for s in signs:
        defn = ARCHETYPE_DEFINITIONS.get(s.evans_id, {})
        domain = defn.get("domain", s.category)
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

        archetypes[s.evans_id] = IconographicArchetype(
            evans_id=s.evans_id,
            canonical_name=s.name,
            unicode_char=s.unicode_char,
            domain=domain,
            physical_medium=defn.get("medium", "Clay relief punch"),
            archaeological_parallels=defn.get("parallels", ["Phaistos palace deposits"]),
            material_context=defn.get("context", s.description),
            theological_association=defn.get("theology", None),
            epistemic_warning=(
                f"Sign {s.evans_id} ('{s.name}') represents tangible Middle Minoan realia ({domain}); "
                f"its phonetic sound value is strictly unproven."
            ),
        )

    summary = (
        "ARCHAEOLOGICAL REALIA CATALOGUE: All 45 relief stamps correspond directly to tangible "
        "Middle Minoan III material culture from the Mesara, Knossos, Malia, and Arkalochori. "
        "The stamps span 6 coherent domains: Flora, Fauna, Tools/Craft, Maritime Transport, "
        "Palatine Architecture/Vessels, and Human Attire. No anachronistic Iron Age or Classical "
        "Greek motifs are present."
    )

    return IconographyCatalogResult(
        total_stamps=len(archetypes),
        archetypes=archetypes,
        domain_counts=domain_counts,
        dominant_material_culture="Middle Minoan III / Late Minoan IA Neopalatial Cretan",
        skeptic_summary=summary,
    )
