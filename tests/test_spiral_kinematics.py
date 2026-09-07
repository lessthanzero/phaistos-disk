"""Unit tests for kinematic spiral modeling."""

import pytest
from phaistos.geometry.spiral_kinematics import evaluate_spiral_kinematics, SpiralKinematicsResult


def test_spiral_kinematics_side_a():
    res = evaluate_spiral_kinematics("A")
    assert isinstance(res, SpiralKinematicsResult)
    assert res.num_measured_points == 31
    assert res.total_coils > 4.0
    assert 12.0 <= res.mean_coil_pitch_mm <= 16.0
    assert res.is_mechanically_guided is True
    assert any("Archimedean" in m.model_name for m in res.models)
    # Check goodness of fit
    best = next(m for m in res.models if m.model_name == res.best_fitting_model)
    assert best.r2_score > 0.99
    assert best.rmse_mm < 0.60


def test_spiral_kinematics_side_b():
    res = evaluate_spiral_kinematics("B")
    assert isinstance(res, SpiralKinematicsResult)
    assert res.num_measured_points == 30
    assert res.center_pin_indentation_documented is True
    assert res.is_mechanically_guided is True
    assert "SPIRAL KINEMATICS" in res.skeptic_verdict
