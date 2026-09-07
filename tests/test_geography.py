"""Unit tests for Minoan geography, radial topology, and structural genre classification."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.geography.loader import load_messara_network
from phaistos.geography.radial_coords import (
    compute_radial_sign_coordinates,
    evaluate_angular_ray_clustering,
)
from phaistos.geography.network_matcher import (
    build_messara_network_graph,
    compare_network_topologies,
)
from phaistos.geography.typology import (
    classify_disc_genre,
    extract_disc_genre_profile,
)
from phaistos.geography.skeptic_geo import conduct_geospatial_skeptic_audit


def test_messara_network_loading():
    network = load_messara_network()
    assert network.hub_site == "Phaistos Palace"
    assert len(network.sites) == 15
    assert len(network.routes) >= 6

    # Verify Phaistos is origin
    phaistos = next(s for s in network.sites if s.id == "PHA")
    assert phaistos.distance_km == 0.0
    assert phaistos.prominence_rank == 1

    # Verify Kommos port
    kommos = next(s for s in network.sites if s.id == "KOM")
    assert kommos.distance_km > 5.0
    assert kommos.cardinal_sector == "WSW"


def test_radial_coordinates_calculation():
    corpus = load_transcription("godart_1995")
    coords_a = compute_radial_sign_coordinates(corpus.side_a)
    assert len(coords_a) == 123
    # Radius normalized: outermost starts near 1.0, ends near 0.0
    assert coords_a[0].radius_normalized > 0.95
    assert coords_a[-1].radius_normalized < 0.05
    # Bearing in degrees within [0, 360)
    for c in coords_a:
        assert 0.0 <= c.compass_bearing_deg < 360.0


def test_rayleigh_circular_uniformity():
    corpus = load_transcription("godart_1995")
    # Test Sign 02
    res = evaluate_angular_ray_clustering(corpus.side_a, target_sign_id="02", iterations=100)
    assert res.total_signs_analyzed == 15
    # Should not show significant ray clustering (uniform null)
    assert res.p_value > 0.05
    assert res.is_clustered is False
    assert "UNIFORM" in res.skeptic_verdict


def test_network_topological_invariants():
    corpus = load_transcription("godart_1995")
    network = load_messara_network()
    topo = compare_network_topologies(corpus, network)

    assert topo["geo_sites_count"] == 15.0
    assert topo["disc_sign_nodes_count"] == 45.0
    # Phaistos regional network has high hub prominence (Phaistos is central star node)
    assert topo["geo_hub_prominence_ratio"] > 3.0


def test_genre_typology_ranking():
    corpus = load_transcription("godart_1995")
    profile = extract_disc_genre_profile(corpus)
    # 45 unique / 242 total = ~0.186
    assert 0.15 < profile.vocabulary_richness < 0.22
    assert profile.block_repetition_rate > 0.20

    res = classify_disc_genre(corpus)
    assert len(res.ranked_genres) == 12
    # Closest should be ritual_sequence
    assert res.closest_genre == "ritual_sequence"
    # Linear writing (prose) should rank very low (10 or 11 of 12)
    linear_rank = next(i for i, g in enumerate(res.ranked_genres) if g.genre_name == "linear_writing")
    assert linear_rank >= 8
    # Radial geography should rank among top 3
    geo_rank = next(i for i, g in enumerate(res.ranked_genres) if g.genre_name == "radial_geography")
    assert geo_rank < 4


def test_geospatial_skeptic_audit():
    audit = conduct_geospatial_skeptic_audit()
    assert audit.category.value == "MODEL_INFERENCE"
    assert "Degrees of Freedom" in audit.data
    assert "10^" in audit.data
