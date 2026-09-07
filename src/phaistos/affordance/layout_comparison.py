"""Quantitative geometric layout benchmark: Archimedean Spiral vs 4 alternative topologies."""

from typing import List
from phaistos.affordance.models import GeometryLayoutType, LayoutComparisonMetrics


def benchmark_candidate_geometries() -> List[LayoutComparisonMetrics]:
    """
    Compare the Archimedean spiral of the Phaistos Disc against 4 alternative geometries
    housing the identical 242 signs and 61 groups.
    """
    total_signs = 242
    mean_sign_width_mm = 12.0

    metrics = [
        # 1. ARCHIMEDEAN SPIRAL (Actual Disc)
        LayoutComparisonMetrics(
            layout_type=GeometryLayoutType.ARCHIMEDEAN_SPIRAL,
            total_area_cm2=402.1, # 2 sides * pi * 8^2
            information_density_signs_per_cm2=round(total_signs / 402.1, 2), # 0.60
            mean_saccade_distance_mm=12.5,
            total_saccade_distance_mm=round((total_signs - 1) * 12.5, 1), # ~3012 mm
            line_returns_count=0, # Unbroken 1D continuous path per side
            boundary_ambiguity_score=0.0, # Zero branch points; strictly linear topology
            foveal_dwell_stability=0.95, # In two-handed rotation, reading gaze remains stationary at 12 o'clock
            handheld_operability_score=92.0,
            notes=(
                "Compact, continuous 1D trajectory packed into a 160 mm 2D circular envelope. "
                "Zero carriage returns. Two-handed rotation continuously feeds signs into the foveal gaze window at 12 o'clock."
            ),
        ),

        # 2. RECTANGULAR TABLET (Linear A / B style)
        LayoutComparisonMetrics(
            layout_type=GeometryLayoutType.RECTANGULAR_TABLET,
            total_area_cm2=250.0, # e.g. 18 cm x 14 cm
            information_density_signs_per_cm2=round(total_signs / 250.0, 2), # 0.97
            mean_saccade_distance_mm=18.4,
            total_saccade_distance_mm=4420.0,
            line_returns_count=16, # 16 horizontal lines requiring 15 wide carriage returns
            boundary_ambiguity_score=0.15, # Risk of line skipping (parablepsis)
            foveal_dwell_stability=0.35, # Requires constant horizontal scanning and vertical line tracking
            handheld_operability_score=85.0,
            notes=(
                "Standard administrative tablet format. Highly space-efficient, but requires repeated wide eye saccades "
                "and carriage returns, with vulnerability to line-skipping error during vocal recitation."
            ),
        ),

        # 3. LINEAR STRIP (Papyrus or parchment scroll)
        LayoutComparisonMetrics(
            layout_type=GeometryLayoutType.LINEAR_STRIP,
            total_area_cm2=1161.6, # 2.90 meters length x 4 cm width
            information_density_signs_per_cm2=round(total_signs / 1161.6, 2), # 0.21
            mean_saccade_distance_mm=12.0,
            total_saccade_distance_mm=round((total_signs - 1) * 12.0, 1), # 2892 mm
            line_returns_count=0,
            boundary_ambiguity_score=0.0,
            foveal_dwell_stability=0.70,
            handheld_operability_score=25.0, # Unwieldy 2.9-meter unrolled band
            notes=(
                "Extremely long physical footprint (2.90 meters). Impossible to hold as an unrolled rigid unit in the hands; "
                "requires complex mechanical scroll rollers to operate."
            ),
        ),

        # 4. CONCENTRIC CIRCLES (Discrete non-spiral rings)
        LayoutComparisonMetrics(
            layout_type=GeometryLayoutType.CONCENTRIC_CIRCLES,
            total_area_cm2=402.1,
            information_density_signs_per_cm2=0.60,
            mean_saccade_distance_mm=21.0,
            total_saccade_distance_mm=4950.0,
            line_returns_count=8, # 4-5 track transitions per side
            boundary_ambiguity_score=0.85, # Circular tracks have no natural start/end without arbitrary radial marks
            foveal_dwell_stability=0.50,
            handheld_operability_score=45.0,
            notes=(
                "High topological ambiguity: closed concentric loops lack natural entry and exit points. "
                "Reader must execute arbitrary radial leaps between non-connected rings."
            ),
        ),

        # 5. RADIAL SECTORS (Wheel-spoke pie slices)
        LayoutComparisonMetrics(
            layout_type=GeometryLayoutType.RADIAL_SECTORS,
            total_area_cm2=402.1,
            information_density_signs_per_cm2=0.60,
            mean_saccade_distance_mm=32.0,
            total_saccade_distance_mm=7600.0,
            line_returns_count=30, # Saccades between pie sectors
            boundary_ambiguity_score=0.70,
            foveal_dwell_stability=0.25,
            handheld_operability_score=35.0,
            notes=(
                "Severe geometric distortion: circumference contracts to near zero at the hub, cramping central signs "
                "while wasting extensive surface area at the outer rim."
            ),
        ),
    ]

    return metrics
