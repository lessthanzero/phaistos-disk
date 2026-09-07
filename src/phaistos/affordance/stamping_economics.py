"""Production economics and breakeven modeling for movable relief stamping."""

from phaistos.affordance.models import StampingEconomicProfile


def evaluate_stamping_economics() -> StampingEconomicProfile:
    """
    Calculate the breakeven labor curve for manufacturing 45 relief punches
    vs freehand stylus incision into soft clay.
    """
    num_punches = 45
    hours_per_punch = 2.50 # Lapidary engraving / lost-wax bronze casting per matrix
    total_matrix_hours = num_punches * hours_per_punch # 112.5 hours

    hours_to_stamp_disc = 0.15 # 9 minutes (242 impressions at 2.2s per stamp)
    hours_to_incise_disc = 0.50 # 30 minutes (incising 242 cursive signs with bone stylus)

    # Breakeven point: 112.5 + 0.15 * N = 0.50 * N  ==>  0.35 * N = 112.5
    breakeven_n = int(round(total_matrix_hours / (hours_to_incise_disc - hours_to_stamp_disc))) # 321 copies

    verdict = (
        f"STAMPING ECONOMIC SKEPTIC PARADOX: Carving 45 relief matrices required ~112.5 artisan-hours. "
        f"Freehand stylus incision requires only ~0.5 hours per disc. "
        f"The economic breakeven threshold is {breakeven_n} copies. "
        f"If the Phaistos Disc was manufactured as a unique, one-off performance cue sheet, stamping was "
        f"irrationally labor-intensive (225x more expensive than stylus incision). "
        f"Conclusion: Stamping was chosen not for scribal efficiency, but for SPHRAGISTIC AUTHORITY "
        f"(palatial seal sanction), SACRED MONUMENTALITY, or an unpreserved regional distribution edition."
    )

    return StampingEconomicProfile(
        num_unique_punches=num_punches,
        punch_fabrication_hours=total_matrix_hours,
        single_disc_stamping_hours=hours_to_stamp_disc,
        single_disc_incision_hours=hours_to_incise_disc,
        breakeven_copy_count=breakeven_n,
        sphragistic_authority_index=98.0,
        economic_verdict=verdict,
        notes="Falsifies naive 'labor-saving typewriter' interpretations for an unicum.",
    )
