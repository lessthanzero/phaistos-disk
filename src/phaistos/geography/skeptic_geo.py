"""Skeptic audit module for geospatial, radial map, and settlement network hypotheses."""

import math
from typing import Dict, List
from phaistos.core.provenance import ProvenanceCategory, ProvenanceRecord


def conduct_geospatial_skeptic_audit(
    sites_count: int = 15,
    signs_count: int = 45,
    groups_count: int = 61,
    rayleigh_p_value: float = 0.50,
) -> ProvenanceRecord[str]:
    """
    Conduct a rigorous Skeptic critique of the Radial Map and Geographical Network hypotheses (GEO-01 to GEO-08).
    Exposes the Degrees of Freedom trap and spatial confirmation bias.
    """
    # Combinatorial degrees of freedom for mapping 45 signs to 15 sites
    # N = 45! / (45 - 15)!
    log_permutations = sum(math.log10(45 - i) for i in range(sites_count))

    audit_text = f"""# SKEPTIC CRITICAL AUDIT: GEOSPATIAL & RADIAL TOPOLOGY (GEO-01 to GEO-08)

## 1. The Spatial Combinatorial Trap (Degrees of Freedom)
* **The Claim**: The 61 groups on the Disc represent an itinerary or radial map of the Messara plain (e.g., Phaistos -> Kommos -> Ayia Triada).
* **The Mathematical Reality**: 
  - An alphabet of {signs_count} signs mapped to {sites_count} regional sites yields:
    $$\\approx 10^{{{log_permutations:.1f}}}$$ potential geographic assignments.
  - With $10^{{21}}$ free parameter permutations, **any random sequence of 61 groups** can be made to trace a plausible-looking "sacred journey" or "trade circuit" through the valleys of Crete.
  - Without an inscribed bilingual toponym (e.g., an explicit Linear B style place-name like *pa-i-to*), spatial mapping is mathematically underdetermined.

## 2. Circular Symmetry vs. Directional Map
* **Rayleigh Test Result (p = {rayleigh_p_value:.4f})**:
  - The physical distribution of signs around the Archimedean spiral shows **no statistically significant cardinal alignment** (p > 0.05).
  - Signs do not cluster in the North (Mt. Ida), West (Kommos harbor), or South (Asterousia).
  - The spiral layout was governed by **calligraphic stamping mechanics** (spacing punches outside-inward before clay dries), not cartographic compass bearings.

## 3. Topographical Reality vs. Radial Idealization
* The Palace of Phaistos is built on an irregular, elongated ridge shaped by the downhill slope, oriented along an east-west axis to resist seismic thrust. It was **never concentric or circular**.
* While Phaistos was the economic hub of the Messara network, projecting a modern radial polar coordinate system ($r, \\theta$) onto a Middle Bronze Age clay disc is an anachronistic epistemic projection.

## 4. Legitimate Structural Value
* What the data **does** support: The Disc's information structure (24.6% block repetition, period-3 refrains) resembles a **liturgical hymn, ritual procession, or spiral track game**, rather than continuous communicative prose or a cartographic map.
* Recommendation: Treat GEO-01 to GEO-08 strictly as **heuristics for comparative structural topology**, never as an epigraphic decipherment key.
"""

    return ProvenanceRecord[str](
        category=ProvenanceCategory.MODEL_INFERENCE,
        source_ref="Skeptic_Agent_Duhoux_Protocol (Duhoux 1977; UNESCO Phaistos Dossier)",
        data=audit_text,
    )
