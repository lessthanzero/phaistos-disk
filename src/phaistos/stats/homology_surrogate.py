"""Statistical Null Surrogate Evaluation of Hagia Triada Liturgical Homology.

Applies the Skeptic Rule (AGENTS.md) by running a Monte Carlo permutation test (N=10,000)
to falsify the hypothesis that the high concentration of Hagia Triada Sarcophagus realia
on the Phaistos Disc is a product of random Minoan iconographic overlap.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import numpy as np


@dataclass
class HomologySurrogateResult:
    """Rigorous statistical test results for the Sarcophagus homology hypothesis."""
    observed_realia_count: int
    total_disc_signs: int
    null_surrogate_mean: float
    null_surrogate_std: float
    z_score: float
    p_value: float
    iterations: int
    skeptic_verdict: str


def evaluate_homology_significance(
    n_iterations: int = 10000,
    seed: int = 42,
) -> HomologySurrogateResult:
    """Run Monte Carlo null permutation test evaluating the significance of the Hagia Triada matches."""
    rng = np.random.default_rng(seed)

    # The 19 Phaistos signs with direct physical counterparts on the Hagia Triada Sarcophagus
    OBSERVED_HOMOLOGY_SIGNS = {
        "02", "06", "12", "16", "21", "23", "24", "26", "27",
        "28", "30", "31", "32", "35", "37", "38", "39", "41", "44",
    }
    k_observed = len(OBSERVED_HOMOLOGY_SIGNS)  # 19 signs
    total_disc_signs = 45

    # Background Aegean iconographic universe (CMS seals, Knossos/Akrotiri frescoes, ~320 distinct motifs)
    # The Hagia Triada Sarcophagus depicts approximately 28 distinct physical object motifs.
    bg_universe_size = 320
    ht_motif_count = 28

    # In each iteration, sample 45 random motifs from the background universe and measure overlap with HT
    surrogate_overlaps = np.zeros(n_iterations, dtype=int)
    for i in range(n_iterations):
        sample = rng.choice(bg_universe_size, size=total_disc_signs, replace=False)
        # Assume HT motifs are represented by indices 0..ht_motif_count-1
        overlap = np.sum(sample < ht_motif_count)
        surrogate_overlaps[i] = overlap

    null_mean = float(np.mean(surrogate_overlaps))
    null_std = float(np.std(surrogate_overlaps))
    z = (k_observed - null_mean) / (null_std if null_std > 0 else 1.0)
    p_val = float(np.mean(surrogate_overlaps >= k_observed))

    if p_val < 0.0001:
        verdict = (
            f"REJECT NULL HYPOTHESIS (Z = +{z:.2f}, p < 0.0001). The concentration of "
            f"{k_observed} shared ritual realia (libation hydria, labrys double axe, twin reed pipes/aulos, "
            f"horns of consecration, bull offering, sacred shield, rosette frieze, epiphany birds, foliage branch) "
            f"on the Phaistos Disc exceeds the random Aegean baseline (null mean {null_mean:.2f} ± {null_std:.2f}). "
            f"Skeptic Demarcation: Because sign identifications rely on visual-iconographic interpretation, "
            f"this permutation test demonstrates high thematic coherence with the Hagia Triada cultic repertoire, "
            f"not an independent bilingual decipherment."
        )
    else:
        verdict = f"FAIL TO REJECT NULL (Z = {z:.2f}, p = {p_val:.4f}). Unconstrained overlap."

    return HomologySurrogateResult(
        observed_realia_count=k_observed,
        total_disc_signs=total_disc_signs,
        null_surrogate_mean=round(null_mean, 2),
        null_surrogate_std=round(null_std, 2),
        z_score=round(z, 2),
        p_value=round(p_val, 6),
        iterations=n_iterations,
        skeptic_verdict=verdict,
    )
