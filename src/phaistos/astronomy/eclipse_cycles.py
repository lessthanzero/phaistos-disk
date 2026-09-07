"""Evaluation of Saros eclipse cycle, lunar nodal precession, and calendar hypotheses."""

from typing import List, Tuple
import numpy as np

from phaistos.core.models import DiscCorpus
from phaistos.astronomy.models import AstronomicalAnalysisResult, AstronomicalMatch


# Canonical astronomical constants known in ancient naked-eye astronomy
ASTRONOMICAL_TARGETS = [
    ("Saros Draconic Months", 242.0, "Total Signs (242)"),
    ("Saros Synodic Months", 223.0, "Total Signs (242)"),
    ("Metonic Synodic Months", 235.0, "Total Signs (242)"),
    ("Lunar Nodal Cycle (Years)", 18.618, "Incised Oblique Strokes (18)"),
    ("Tropical Solar Year (Days / 10)", 36.52, "Side A Groups (31)"),
    ("Lunar Year (Months x 5)", 60.0, "Total Groups (61)"),
    ("Venus Synodic Cycle / 10", 58.4, "Total Groups (61)"),
]


def evaluate_astronomical_matches(corpus: DiscCorpus) -> List[AstronomicalMatch]:
    """Compare observed physical features of the Disc against astronomical constants."""
    total_signs = corpus.total_signs
    total_groups = len(corpus.all_groups())
    strokes_a = sum(1 for g in corpus.side_a.groups if g.oblique_stroke)
    strokes_b = sum(1 for g in corpus.side_b.groups if g.oblique_stroke)
    total_strokes = strokes_a + strokes_b

    matches = []

    # 1. 242 Signs vs 242 Draconic Months in 1 Saros Cycle (223 synodic months = 242 draconic months)
    err_saros = abs(float(total_signs) - 242.0) / 242.0 * 100.0
    matches.append(
        AstronomicalMatch(
            constant_name="Saros Draconic Months (242 nodical months = 18.03 yrs)",
            target_value=242.0,
            observed_disc_feature="Total sign impressions across Side A + Side B",
            observed_value=total_signs,
            relative_error_pct=round(err_saros, 3),
            epistemic_plausibility="Exact numerical match (0.00% error), but susceptible to look-elsewhere selection bias.",
        )
    )

    # 2. 18 Incised Strokes vs 18.618-Year Lunar Nodal Precession Cycle
    err_nodal = abs(float(total_strokes) - 18.618) / 18.618 * 100.0
    matches.append(
        AstronomicalMatch(
            constant_name="Lunar Nodal Precession (18.618 tropical years)",
            target_value=18.618,
            observed_disc_feature="Incised oblique strokes under initial signs (10 on Side A, 8 on Side B)",
            observed_value=total_strokes,
            relative_error_pct=round(err_nodal, 2),
            epistemic_plausibility="Close numerical match (3.32% error); Side A (10) + Side B (8) fits seasonal balance.",
        )
    )

    # 3. 61 Groups vs 2 Lunar Years / Seasonal Solstices (60 pentads / 2 lunar years ~ 60 fortnights)
    err_groups = abs(float(total_groups) - 60.0) / 60.0 * 100.0
    matches.append(
        AstronomicalMatch(
            constant_name="Bi-annual Lunar Fortnights (60 fortnights = 30 lunar months)",
            target_value=60.0,
            observed_disc_feature="Total bounded compartments / sign groups (Side A: 31, Side B: 30)",
            observed_value=total_groups,
            relative_error_pct=round(err_groups, 2),
            epistemic_plausibility="Plausible calendar division (1.67% error), but group division varies in sign density (2 to 7 signs).",
        )
    )

    return matches


def compute_look_elsewhere_effect(num_trials: int = 10000, tolerance_pct: float = 2.0, seed: int = 42) -> float:
    """
    Monte Carlo evaluation of the Look-Elsewhere Effect:
    Given the dozens of astronomical constants in naked-eye astronomy,
    what is the probability that an arbitrary set of 3 random integers
    (drawn uniformly from plausible archaeological artifact count ranges)
    will match AT LEAST ONE target constant within tolerance_pct?
    """
    rng = np.random.default_rng(seed)
    target_values = [t[1] for t in ASTRONOMICAL_TARGETS]

    false_positive_matches = 0
    for _ in range(num_trials):
        # Draw 3 random counts: strokes (5-30), groups (30-100), signs (150-350)
        c_strokes = rng.integers(5, 31)
        c_groups = rng.integers(30, 101)
        c_signs = rng.integers(150, 351)

        matched = False
        for val in [c_strokes, c_groups, c_signs]:
            for target in target_values:
                rel_err = abs(float(val) - target) / target * 100.0
                if rel_err <= tolerance_pct:
                    matched = True
                    break
            if matched:
                break

        if matched:
            false_positive_matches += 1

    return float(false_positive_matches) / float(num_trials)


def analyze_astronomy(corpus: DiscCorpus, num_trials: int = 10000) -> AstronomicalAnalysisResult:
    """Run full astronomical and calendar hypothesis testing with Skeptic controls."""
    matches = evaluate_astronomical_matches(corpus)
    strokes_a = sum(1 for g in corpus.side_a.groups if g.oblique_stroke)
    strokes_b = sum(1 for g in corpus.side_b.groups if g.oblique_stroke)

    p_look_elsewhere = compute_look_elsewhere_effect(num_trials=num_trials, tolerance_pct=2.0)

    verdict = (
        f"ASTRONOMICAL SAROS & CALENDAR EVALUATION: Total sign count (242) is an EXACT mathematical match "
        f"to the 242 draconic months constituting 1 Saros eclipse cycle (6585.35 days ~ 18.03 years), and "
        f"the 18 incised oblique strokes correspond closely to the 18.618-year lunar nodal cycle (3.3% error). "
        f"HOWEVER, Skeptic Look-Elsewhere Monte Carlo testing indicates that when searching across canonical "
        f"ancient naked-eye astronomical periods, arbitrary artifact counts have a {p_look_elsewhere * 100.0:.1f}% "
        f"probability of hitting at least one astronomical constant within 2%. "
        f"Furthermore, physical palimpsests (A05, A08, B01) altered sign counts during manufacture, "
        f"strongly refuting the claim that the Disc was manufactured as a precision astronomical computation tool."
    )

    return AstronomicalAnalysisResult(
        matches=matches,
        stroke_distribution={"Side_A": strokes_a, "Side_B": strokes_b, "Total": strokes_a + strokes_b},
        look_elsewhere_trials=num_trials,
        look_elsewhere_p_value=p_look_elsewhere,
        unfalsifiable_numerology_warning=p_look_elsewhere > 0.05,
        skeptic_verdict=verdict,
    )
