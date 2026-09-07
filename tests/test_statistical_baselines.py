"""Unit tests for statistical baseline calculations: ngrams, repetitions, entropy."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.stats.ngrams import (
    extract_group_ngrams,
    extract_global_ngrams,
    compute_transition_matrix,
    build_transition_graph,
)
from phaistos.stats.repetitions import (
    find_identical_groups,
    find_common_affixes,
    find_near_identical_groups,
    analyze_oblique_stroke_associations,
)
from phaistos.stats.entropy import (
    compute_unigram_entropy,
    compute_bigram_joint_and_conditional_entropy,
    compute_compressibility_metrics,
)


def test_ngrams_extraction():
    corpus = load_transcription("godart_1995")
    bigrams = extract_group_ngrams(corpus, n=2)
    trigrams = extract_group_ngrams(corpus, n=3)

    assert len(bigrams) > 0
    assert len(trigrams) > 0
    # Top bigram should be ('02', '12')
    assert bigrams[("02", "12")] == 13

    # Transition matrix dimensions
    all_signs, trans_mat = compute_transition_matrix(corpus)
    assert len(all_signs) == 45
    assert trans_mat.shape == (45, 45)

    # Transition graph
    G = build_transition_graph(corpus, min_weight=1)
    assert G.number_of_nodes() == 45
    assert G.has_edge("02", "12")


def test_repetitions_and_affixes():
    corpus = load_transcription("godart_1995")
    identical = find_identical_groups(corpus)

    # The 7 known repeated groups must be detected
    assert "02-12-31-26" in identical
    assert len(identical["02-12-31-26"]) == 3
    assert "10-03-38" in identical
    assert len(identical["10-03-38"]) == 2
    assert "29-45-07" in identical
    assert len(identical["29-45-07"]) == 2

    # Affixes
    affixes = find_common_affixes(corpus, min_len=2)
    assert affixes["prefixes"]["02-12"] == 13

    # Near matches
    near = find_near_identical_groups(corpus, max_distance=1)
    assert len(near) > 0

    # Oblique strokes
    oblique = analyze_oblique_stroke_associations(corpus)
    assert sum(oblique.values()) == 18


def test_entropy_and_compressibility():
    corpus = load_transcription("godart_1995")
    h_uni = compute_unigram_entropy(corpus)
    h_joint, h_cond, mi = compute_bigram_joint_and_conditional_entropy(corpus)

    assert 4.5 < h_uni < 5.2
    assert 1.0 < h_cond < 3.0
    assert mi > 0.0

    comp = compute_compressibility_metrics(corpus)
    assert comp["zlib_ratio"] < 0.6
    assert comp["lzma_ratio"] < 0.7
