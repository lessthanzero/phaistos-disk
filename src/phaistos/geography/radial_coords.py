"""Radial spatial coordinate extractor and circular statistics engine for the Phaistos Disc."""

import math
import random
from typing import Dict, List, Optional, Tuple
import numpy as np

from phaistos.core.models import DiscCorpus, DiscSide
from phaistos.geography.models import RadialClusteringResult, RadialSignCoordinate


def compute_radial_sign_coordinates(side: DiscSide) -> List[RadialSignCoordinate]:
    """
    Compute continuous polar coordinates (r, theta) for every sign occurrence
    based on the physical Archimedean spiral outside-inward sequence.
    """
    coords = []
    total_signs = side.sign_count
    max_turns = 4.2
    max_theta = max_turns * 2.0 * math.pi

    sign_index = 0
    for group in side.groups:
        for sign_id in group.signs:
            frac = sign_index / float(total_signs) if total_signs > 0 else 0.0
            theta = frac * max_theta
            r_norm = 1.0 - frac  # 1.0 = outermost perimeter, 0.0 = spiral centre

            # Convert theta to compass bearing: 0 deg = North (top), 90 deg = East, etc.
            # In our SVG spiral: top-right start, angle = theta - pi/2
            bearing = (math.degrees(theta) % 360.0)

            coords.append(
                RadialSignCoordinate(
                    sign_id=sign_id,
                    group_id=group.id,
                    side=side.side,
                    radius_normalized=float(r_norm),
                    theta_rad=float(theta % (2.0 * math.pi)),
                    compass_bearing_deg=float(bearing),
                )
            )
            sign_index += 1

    return coords


def evaluate_angular_ray_clustering(
    side: DiscSide,
    target_sign_id: Optional[str] = "02",
    iterations: int = 1000,
    seed: int = 42,
) -> RadialClusteringResult:
    """
    Test whether sign occurrences (e.g. Sign 02 Plumed Head) cluster along
    specific angular rays / cardinal directions on the disc using Rayleigh's circular test.
    Compares observed mean resultant length R to randomized coordinate shuffles.
    """
    rng = random.Random(seed)
    coords = compute_radial_sign_coordinates(side)

    # Filter by target sign, or test all signs if target_sign_id is None
    if target_sign_id:
        target_coords = [c for c in coords if c.sign_id == target_sign_id]
    else:
        target_coords = coords

    n = len(target_coords)
    if n < 3:
        return RadialClusteringResult(
            side=side.side,
            total_signs_analyzed=n,
            observed_rayleigh_statistic=0.0,
            null_mean_rayleigh=0.0,
            null_std_rayleigh=1.0,
            z_score=0.0,
            p_value=1.0,
            is_clustered=False,
            cardinal_peak_azimuth=None,
            skeptic_verdict="INSUFFICIENT DATA: Fewer than 3 occurrences to evaluate circular clustering.",
        )

    # Compute observed Rayleigh resultant vector length
    angles = [c.theta_rad for c in target_coords]
    c_bar = sum(math.cos(a) for a in angles) / float(n)
    s_bar = sum(math.sin(a) for a in angles) / float(n)
    r_bar = math.sqrt(c_bar ** 2 + s_bar ** 2)
    obs_rayleigh = 2.0 * n * (r_bar ** 2)
    mean_angle = (math.degrees(math.atan2(s_bar, c_bar)) + 360.0) % 360.0

    # Null distribution: shuffle signs across the spiral positions
    all_angles = [c.theta_rad for c in coords]
    null_stats = []
    for _ in range(iterations):
        sampled_angles = rng.sample(all_angles, k=n)
        cb = sum(math.cos(a) for a in sampled_angles) / float(n)
        sb = sum(math.sin(a) for a in sampled_angles) / float(n)
        rb = math.sqrt(cb ** 2 + sb ** 2)
        null_stats.append(2.0 * n * (rb ** 2))

    null_arr = np.array(null_stats)
    null_mean = float(np.mean(null_arr))
    null_std = float(np.std(null_arr)) if float(np.std(null_arr)) > 0 else 1e-6
    z_score = (obs_rayleigh - null_mean) / null_std
    p_value = float(np.mean(null_arr >= obs_rayleigh))

    is_clustered = z_score > 2.0 and p_value < 0.05
    sign_label = f"Sign {target_sign_id}" if target_sign_id else "All Signs"

    if is_clustered:
        verdict = (
            f"CLUSTERED (NON-RANDOM RADIAL ALIGNMENT): {sign_label} exhibits statistically significant "
            f"directional ray alignment (Rayleigh R={r_bar:.3f}, Z={z_score:+.2f}, p={p_value:.4f}) "
            f"concentrating near azimuth {mean_angle:.1f}°."
        )
    else:
        verdict = (
            f"UNIFORM / NO RADIAL ALIGNMENT: {sign_label} angular positions on Side {side.side} "
            f"are consistent with a uniform circular distribution (Rayleigh Z={z_score:+.2f}, p={p_value:.4f}). "
            f"No evidence that the spiral was organized along cardinal rays or radial map bearings."
        )

    return RadialClusteringResult(
        side=side.side,
        total_signs_analyzed=n,
        observed_rayleigh_statistic=float(obs_rayleigh),
        null_mean_rayleigh=null_mean,
        null_std_rayleigh=null_std,
        z_score=float(z_score),
        p_value=float(p_value),
        is_clustered=is_clustered,
        cardinal_peak_azimuth=float(mean_angle) if is_clustered else None,
        skeptic_verdict=verdict,
    )
