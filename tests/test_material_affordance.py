"""Unit tests for Object Function and Material Affordance evaluations."""

from pathlib import Path
import pytest

from phaistos.affordance.ergonomics import evaluate_grip_postures
from phaistos.affordance.layout_comparison import benchmark_candidate_geometries
from phaistos.affordance.rotation_kinematics import evaluate_rotation_kinematics
from phaistos.affordance.tactile_physics import evaluate_tactile_discrimination
from phaistos.affordance.stamping_economics import evaluate_stamping_economics
from phaistos.affordance.cross_corpus import evaluate_cross_corpus_affordances
from phaistos.affordance.models import GeometryLayoutType, GripPosture
from phaistos.experiment.affordance_runner import (
    generate_ranked_function_matrix,
    run_all_affordance_experiments,
)


def test_grip_postures():
    grips = evaluate_grip_postures()
    assert len(grips) == 4
    postures = {g.posture: g for g in grips}

    # Two-handed perimeter should be optimal with 0 cantilever torque
    assert postures[GripPosture.TWO_HANDED_PERIMETER].wrist_cantilever_torque_nm == 0.0
    assert postures[GripPosture.TWO_HANDED_PERIMETER].feasibility_rating == "OPTIMAL"

    # One-handed edge grip should have high cantilever torque and poor rating
    assert postures[GripPosture.ONE_HANDED_EDGE].wrist_cantilever_torque_nm > 0.35
    assert postures[GripPosture.ONE_HANDED_EDGE].feasibility_rating == "POOR"


def test_layout_benchmark():
    geos = benchmark_candidate_geometries()
    assert len(geos) == 5
    by_type = {g.layout_type: g for g in geos}

    spiral = by_type[GeometryLayoutType.ARCHIMEDEAN_SPIRAL]
    tablet = by_type[GeometryLayoutType.RECTANGULAR_TABLET]

    # Spiral has 0 line returns and high foveal dwell stability
    assert spiral.line_returns_count == 0
    assert spiral.boundary_ambiguity_score == 0.0
    assert spiral.foveal_dwell_stability > tablet.foveal_dwell_stability
    assert tablet.line_returns_count >= 15


def test_rotation_kinematics():
    kin = evaluate_rotation_kinematics(morae_per_second=3.0)
    assert len(kin) == 2
    side_a = kin[0]
    side_b = kin[1]

    assert side_a.side == "A"
    assert side_b.side == "B"
    assert 40.0 <= side_a.estimated_duration_sec <= 50.0
    assert 30.0 <= side_a.angular_velocity_deg_per_sec <= 40.0
    assert side_a.rpm > 4.0


def test_tactile_acuity():
    evals = evaluate_tactile_discrimination()
    assert len(evals) == 5
    by_name = {e.task_name: e for e in evals}

    # Blind sign identification must be falsified
    blind_sign = by_name["BLIND_SIGN_IDENTIFICATION"]
    assert blind_sign.epistemic_status == "FALSIFIED"
    assert blind_sign.is_physically_viable is False
    assert blind_sign.detection_probability < 0.10

    # Boundary tracking must be confirmed viable
    groove = by_name["SPIRAL_TRACK_WAYFINDING"]
    assert groove.epistemic_status == "CONFIRMED_VIABLE"
    assert groove.detection_probability > 0.90


def test_stamping_economics():
    econ = evaluate_stamping_economics()
    assert econ.num_unique_punches == 45
    assert econ.punch_fabrication_hours > 100.0
    assert econ.breakeven_copy_count > 250
    assert "SPHRAGISTIC AUTHORITY" in econ.economic_verdict


def test_cross_corpus():
    corpus = evaluate_cross_corpus_affordances()
    assert len(corpus) >= 5
    disc = next(c for c in corpus if "Phaistos Disc" in c.media_name)
    assert "Archimedean" in disc.layout_topology
    assert "bench sanctuary" in disc.typical_findspot


def test_run_all_affordance_experiments(tmp_path: Path):
    results = run_all_affordance_experiments(tmp_path)
    assert len(results) == 10
    exp_ids = [r.experiment_id for r in results]
    assert "OFX-01" in exp_ids
    assert "OFX-10" in exp_ids

    # Check persistence
    for exp_id in exp_ids:
        assert (tmp_path / exp_id / "result.json").exists()


def test_ranked_function_matrix():
    matrix = generate_ranked_function_matrix()
    assert len(matrix) >= 7
    top = matrix[0]
    assert top.rank == 1
    assert "Liturgical Score" in top.title
    assert top.confidence_grade == "HIGH CONFIDENCE"

    # Verify falsifications
    falsified_ids = [m.hypothesis_id for m in matrix if m.confidence_grade == "FALSIFIED"]
    assert "OF_01" in falsified_ids
    assert "OF_03" in falsified_ids
    assert "OF_06" in falsified_ids
    assert "OF_07" in falsified_ids
    assert "OF_08" in falsified_ids
