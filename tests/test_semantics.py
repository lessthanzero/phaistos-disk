"""Unit tests for Tiers 2-4: Iconography, Distributional Semantics, and Libation Sieve."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.semantics.iconography import get_iconographic_catalog
from phaistos.semantics.distributional import analyze_distributional_semantics, compute_distributional_vectors
from phaistos.semantics.libation_sieve import evaluate_libation_sieve


def test_iconographic_catalog():
    """Verify all 45 stamps have archaeological archetypes and valid domains."""
    cat = get_iconographic_catalog()
    assert cat.total_stamps == 45
    assert len(cat.archetypes) == 45

    expected_domains = {
        "human_attiral",
        "tools_craft",
        "flora",
        "maritime_transport",
        "fauna",
        "architecture_vessels",
    }
    assert set(cat.domain_counts.keys()) == expected_domains

    # Check specific diagnostic signs
    sign_02 = cat.archetypes["02"]
    assert "feather" in sign_02.material_context.lower() or "crest" in sign_02.material_context.lower()
    assert sign_02.domain == "human_attiral"

    sign_12 = cat.archetypes["12"]
    assert "shield" in sign_12.canonical_name.lower() or "shield" in sign_12.material_context.lower()
    assert sign_12.domain == "tools_craft"

    sign_26 = cat.archetypes["26"]
    assert sign_26.domain == "maritime_transport"

    sign_44 = cat.archetypes["44"]
    assert "axe" in sign_44.canonical_name.lower() or "labrys" in sign_44.material_context.lower()

    for s_id, arch in cat.archetypes.items():
        assert len(arch.archaeological_parallels) > 0
        assert len(arch.material_context) > 10
        assert arch.epistemic_warning.startswith("Sign")


def test_distributional_vectors():
    """Verify positional vector extraction across 61 groups."""
    corpus = load_transcription("godart_1995")
    vectors, matrix, sign_order = compute_distributional_vectors(corpus)

    assert len(vectors) == 45
    assert len(sign_order) == 45
    assert matrix.shape == (45, 4)

    # Sign 02 (Plumed Head) is strongly initial
    vec_02 = vectors["02"]
    assert vec_02.initial_count >= 13
    assert vec_02.initial_rate > 0.50
    assert vec_02.functional_class == "invocational_clitic"

    # Sign 35 (Branch) is strongly final and associated with strokes
    vec_35 = vectors["35"]
    assert vec_35.final_rate > 0.40 or vec_35.stroke_rate > 0.20
    assert vec_35.functional_class == "suffixal_postposition"


def test_distributional_clustering_null_hypothesis():
    """Verify that positional clustering significantly beats randomized Monte Carlo baselines."""
    corpus = load_transcription("godart_1995")
    result = analyze_distributional_semantics(corpus, n_null_iterations=50, seed=42)

    assert result.total_signs_analyzed == 45
    assert result.clustering_silhouette_score > 0.30
    assert result.clustering_z_score > 2.0
    assert result.clustering_p_value < 0.05
    assert len(result.functional_classes["invocational_clitic"]) > 0
    assert len(result.functional_classes["core_stem"]) > 0
    assert len(result.functional_classes["suffixal_postposition"]) > 0
    assert "STATISTICAL GRAMMAR VALIDATED" in result.skeptic_verdict


def test_libation_sieve():
    """Verify structural alignment against the 14 GORILA Linear A libation vessels."""
    corpus = load_transcription("godart_1995")
    sieve = evaluate_libation_sieve(corpus)

    assert sieve.total_linear_a_inscriptions == 14
    assert len(sieve.alignments) == 14
    assert sieve.disc_prefix_recurrence_rate > 0.15  # 13 / 61 = 21.3%
    assert sieve.linear_a_head_recurrence_rate > 0.60  # 10 / 14 = 71.4%
    assert sieve.herfindahl_index_disc_heads > 0.05
    assert sieve.liturgical_affinity_z_score > 2.5
    assert sieve.administrative_divergence_p_value < 1e-4

    # Check Mount Kophinas alignment (Asterousia hinterland)
    ko_za_1 = next(a for a in sieve.alignments if a.inscription_id == "KO Za 1")
    assert ko_za_1.findspot == "Mount Kophinas"
    assert ko_za_1.theonym_present is True
    assert "JA-SA-SA-RA-ME" in ko_za_1.linear_a_text
