"""Unit tests for the 4-tier randomization generators and Monte Carlo controls."""

import random
import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.stats.frequency import compute_sign_frequencies
from phaistos.stats.permutations import (
    generate_uniform_random_corpus,
    generate_frequency_preserving_corpus,
    generate_markov_preserving_corpus,
    run_monte_carlo_test,
    metric_repeated_groups_count,
    metric_bigram_collisions,
)


def test_uniform_random_generator():
    corpus = load_transcription("godart_1995")
    rng = random.Random(42)
    surrogate = generate_uniform_random_corpus(corpus, rng)

    assert surrogate.total_groups == corpus.total_groups
    assert surrogate.total_signs == corpus.total_signs
    for g_orig, g_surr in zip(corpus.all_groups(), surrogate.all_groups()):
        assert len(g_orig.signs) == len(g_surr.signs)


def test_frequency_preserving_generator():
    corpus = load_transcription("godart_1995")
    rng = random.Random(42)
    surrogate = generate_frequency_preserving_corpus(corpus, rng)

    assert surrogate.total_groups == corpus.total_groups
    assert surrogate.total_signs == corpus.total_signs

    # Sign frequencies must be identical
    orig_counts = compute_sign_frequencies(corpus)
    surr_counts = compute_sign_frequencies(surrogate)
    assert orig_counts == surr_counts


def test_markov_preserving_generator():
    corpus = load_transcription("godart_1995")
    rng = random.Random(42)
    surrogate = generate_markov_preserving_corpus(corpus, rng)

    assert surrogate.total_groups == corpus.total_groups
    assert surrogate.total_signs == corpus.total_signs


def test_monte_carlo_test_runner():
    corpus = load_transcription("godart_1995")
    res = run_monte_carlo_test(
        corpus,
        metric_fn=metric_repeated_groups_count,
        generator_fn=generate_frequency_preserving_corpus,
        iterations=50,
        seed=42,
    )
    assert "observed" in res
    assert "null_mean" in res
    assert "z_score" in res
    assert "p_value" in res
    # Observed repeated groups (15) must vastly exceed randomized null mean (~0.0)
    assert res["z_score"] > 5.0
    assert res["p_value"] < 0.05
