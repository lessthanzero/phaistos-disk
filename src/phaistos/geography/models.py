"""Data models for Minoan geography, radial topology, and genre typology."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class MinoanSite(BaseModel):
    id: str
    name: str
    type: str
    elevation_m: int
    distance_km: float
    azimuth_deg: float
    cardinal_sector: str
    description: str
    prominence_rank: int


class MinoanRoute(BaseModel):
    id: str
    name: str
    from_site: str
    to_site: str
    distance_km: float
    type: str
    description: str


class MessaraNetwork(BaseModel):
    region: str
    hub_site: str
    period: str
    description: str
    sites: List[MinoanSite]
    routes: List[MinoanRoute]


class GenreProfile(BaseModel):
    name: str
    description: str
    vocabulary_richness: float      # Type-Token Ratio (V/N)
    positional_entropy: float       # Entropy of initial sign distribution
    block_repetition_rate: float    # Ratio of repeated groups to total groups
    periodic_autocorrelation: float # Spacing periodicity score
    conditional_entropy: float      # Bigram conditional entropy H(Y|X)
    branching_factor: float         # Mean outgoing transitions per symbol


class GenreDistance(BaseModel):
    genre_name: str
    distance: float
    similarity_percentage: float
    description: str


class GenreTypologyResult(BaseModel):
    disc_profile: GenreProfile
    ranked_genres: List[GenreDistance]
    closest_genre: str
    furthest_genre: str
    skeptic_verdict: str


class RadialSignCoordinate(BaseModel):
    sign_id: str
    group_id: str
    side: str
    radius_normalized: float        # 1.0 = outer edge, 0.0 = center
    theta_rad: float                # Polar angle in radians
    compass_bearing_deg: float      # Bearing in degrees (0° = North, 90° = East, etc.)


class RadialClusteringResult(BaseModel):
    side: str
    total_signs_analyzed: int
    observed_rayleigh_statistic: float
    null_mean_rayleigh: float
    null_std_rayleigh: float
    z_score: float
    p_value: float
    is_clustered: bool
    cardinal_peak_azimuth: Optional[float] = None
    skeptic_verdict: str
