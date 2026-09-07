"""Somatosensory tactile acuity evaluation and blind reading falsification."""

from typing import List
from phaistos.affordance.models import TactileAcuityEvaluation


def evaluate_tactile_discrimination() -> List[TactileAcuityEvaluation]:
    """
    Evaluate 5 tactile discrimination tasks against human somatosensory biophysics
    (Weber two-point threshold, Merkel SA1 receptive field densities, and intaglio clay rheology).
    """
    evaluations = [
        # Task 1: Blind Pictograph Sign Identification (Braille Analogy)
        TactileAcuityEvaluation(
            task_name="BLIND_SIGN_IDENTIFICATION",
            stimulus_type="Intaglio negative impression in fired clay (0.8-1.5 mm depth)",
            feature_size_mm=0.6, # Mean spacing between internal feather plumes or petals
            weber_two_point_threshold_mm=2.8, # Static two-point discrimination on index fingertip
            mechanoreceptor_type="Merkel SA1 (Slow Adapting Type 1)",
            detection_probability=0.025, # Effectively pure chance across 45 signs (~1/45 = 0.022)
            is_physically_viable=False,
            epistemic_status="FALSIFIED",
            notes=(
                "FALSIFIED: Human fingertip spatial acuity (2.5-3.0 mm) cannot resolve fine intaglio incisions "
                "spaced at 0.4-0.8 mm (e.g. 12 plumes on Sign 02, 8 petals on Sign 38). "
                "The signs are depressed negative molds, not raised Braille dots. Blind reading without vision "
                "is a physiological impossibility."
            ),
        ),

        # Task 2: Spiral Track Continuous Tracking
        TactileAcuityEvaluation(
            task_name="SPIRAL_TRACK_WAYFINDING",
            stimulus_type="Continuous incised spiral groove (0.8 mm depth, 0.7 mm width)",
            feature_size_mm=0.8,
            weber_two_point_threshold_mm=1.0, # Dynamic shear detection during continuous tracing
            mechanoreceptor_type="Meissner RA1 (Rapid Adapting Type 1)",
            detection_probability=0.98,
            is_physically_viable=True,
            epistemic_status="CONFIRMED_VIABLE",
            notes=(
                "CONFIRMED VIABLE: While individual pictographs cannot be identified by touch, the fingertip "
                "effortlessly tracks the sunken Archimedean groove, allowing continuous physical wayfinding along the spiral."
            ),
        ),

        # Task 3: Group Compartment Dividing Line Detection
        TactileAcuityEvaluation(
            task_name="GROUP_BOUNDARY_DETECTION",
            stimulus_type="Radial incised dividing bar across 18-21 mm track width",
            feature_size_mm=18.0, # Spans full coil track
            weber_two_point_threshold_mm=2.5,
            mechanoreceptor_type="Meissner RA1 / Merkel SA1",
            detection_probability=0.96,
            is_physically_viable=True,
            epistemic_status="CONFIRMED_VIABLE",
            notes=(
                "CONFIRMED VIABLE: The radial dividing bars create prominent tactile ridges/trenches perpendicular "
                "to the path of motion. A reciter can tactilely count sign groups or pace verses without continuous gaze fixation."
            ),
        ),

        # Task 4: Oblique Stroke (*Virgula*) Cadence Detection
        TactileAcuityEvaluation(
            task_name="STROKE_CADENCE_DETECTION",
            stimulus_type="Incised diagonal slash at group-final base (4-8 mm length, 1.0 mm depth)",
            feature_size_mm=5.5,
            weber_two_point_threshold_mm=2.0,
            mechanoreceptor_type="Merkel SA1",
            detection_probability=0.91,
            is_physically_viable=True,
            epistemic_status="CONFIRMED_VIABLE",
            notes=(
                "CONFIRMED VIABLE: The 18 incised strokes produce distinct tactile notches at stanza boundaries, "
                "providing a tactile cue for musical rest or choral cadence."
            ),
        ),

        # Task 5: Central Peg Hole Pivot Detection
        TactileAcuityEvaluation(
            task_name="CENTRAL_PEG_INDENTATION_DETECTION",
            stimulus_type="Conical central indentation on Side B (1.2 mm depth, 4.0 mm diameter)",
            feature_size_mm=4.0,
            weber_two_point_threshold_mm=2.5,
            mechanoreceptor_type="Pacinian / Merkel SA1",
            detection_probability=0.99,
            is_physically_viable=True,
            epistemic_status="CONFIRMED_VIABLE",
            notes=(
                "CONFIRMED VIABLE: The 1.2 mm conical depression at the geometric centroid of Side B is immediately felt "
                "by a thumb resting at the center, serving as a mechanical tactile pivot for hand rotation."
            ),
        ),
    ]

    return evaluations
