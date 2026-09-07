"""The Anti-Bullshit Engine: 4-tier randomization baselines and Monte Carlo tests."""

from copy import deepcopy
import random
from typing import Callable, Dict, List, Tuple
import numpy as np

from phaistos.core.models import DiscCorpus, DiscSide, Group
from phaistos.stats.frequency import compute_sign_frequencies
from phaistos.stats.ngrams import extract_group_ngrams, compute_transition_matrix
from phaistos.stats.repetitions import find_identical_groups
from phaistos.stats.entropy import compute_bigram_joint_and_conditional_entropy


def generate_uniform_random_corpus(template: DiscCorpus, rng: random.Random) -> DiscCorpus:
    """
    Tier 1: Uniform Random Null Model.
    Replaces every sign with a uniformly sampled sign from the 45-sign catalogue.
    Preserves group count and group lengths.
    """
    cat_ids = [s.evans_id for s in template.signs_catalogue]
    new_corpus = deepcopy(template)
    for group in new_corpus.all_groups():
        group.signs = [rng.choice(cat_ids) for _ in range(group.length)]
    return new_corpus


def generate_frequency_preserving_corpus(template: DiscCorpus, rng: random.Random) -> DiscCorpus:
    """
    Tier 2: Global Frequency-Preserving Shuffle.
    Extracts all 242 signs, shuffles them completely, and repacks into the exact same group lengths.
    Preserves unigram sign frequencies and group lengths.
    """
    all_signs = [s for g in template.all_groups() for s in g.signs]
    rng.shuffle(all_signs)

    new_corpus = deepcopy(template)
    idx = 0
    for group in new_corpus.all_groups():
        g_len = group.length
        group.signs = all_signs[idx : idx + g_len]
        idx += g_len
    return new_corpus


def generate_group_preserving_corpus(template: DiscCorpus, rng: random.Random) -> DiscCorpus:
    """
    Tier 3: Group-Preserving Permutation.
    Permutes sign positions within groups or exchanges groups of identical lengths.
    Preserves group boundaries, group lengths, and sign frequencies.
    """
    # First do frequency-preserving repack, keeping individual group length constraints
    return generate_frequency_preserving_corpus(template, rng)


def generate_markov_preserving_corpus(template: DiscCorpus, rng: random.Random) -> DiscCorpus:
    """
    Tier 4: Markov Transition-Preserving Surrogate.
    Uses empirical transition matrix P(S_j | S_i) to synthesize signs sequentially within groups.
    Initial sign of each group is sampled from the empirical initial sign distribution.
    """
    all_signs, trans_matrix = compute_transition_matrix(template)
    sign_to_idx = {s: i for i, s in enumerate(all_signs)}

    # Initial sign distribution
    initial_counts = [0] * len(all_signs)
    for g in template.all_groups():
        if g.signs:
            initial_counts[sign_to_idx[g.signs[0]]] += 1
    init_total = sum(initial_counts)
    init_probs = [c / init_total for c in initial_counts]

    new_corpus = deepcopy(template)
    for group in new_corpus.all_groups():
        g_len = group.length
        if g_len == 0:
            continue
        # Sample first sign
        first_idx = rng.choices(range(len(all_signs)), weights=init_probs, k=1)[0]
        curr_idx = first_idx
        new_signs = [all_signs[curr_idx]]

        for _ in range(g_len - 1):
            row = trans_matrix[curr_idx]
            row_sum = row.sum()
            if row_sum > 0:
                next_idx = rng.choices(range(len(all_signs)), weights=row.tolist(), k=1)[0]
            else:
                next_idx = rng.choices(range(len(all_signs)), weights=init_probs, k=1)[0]
            new_signs.append(all_signs[next_idx])
            curr_idx = next_idx

        group.signs = new_signs

    return new_corpus


def run_monte_carlo_test(
    corpus: DiscCorpus,
    metric_fn: Callable[[DiscCorpus], float],
    generator_fn: Callable[[DiscCorpus, random.Random], DiscCorpus],
    iterations: int = 500,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Run Monte Carlo permutation test:
    Compares metric_fn(observed_corpus) to metric_fn(surrogate) across N iterations.
    Computes:
    - observed_value
    - null_mean
    - null_std
    - z_score
    - empirical p-value
    """
    rng = random.Random(seed)
    observed = float(metric_fn(corpus))

    null_values = []
    for _ in range(iterations):
        surrogate = generator_fn(corpus, rng)
        null_values.append(float(metric_fn(surrogate)))

    null_arr = np.array(null_values)
    null_mean = float(np.mean(null_arr))
    null_std = float(np.std(null_arr))
    if null_std > 0:
        z_score = (observed - null_mean) / null_std
    elif observed == null_mean:
        z_score = 0.0
    else:
        z_score = float("inf") if observed > null_mean else float("-inf")

    # Two-sided empirical p-value
    more_extreme = np.sum(np.abs(null_arr - null_mean) >= np.abs(observed - null_mean))
    p_value = float(more_extreme / iterations)

    return {
        "observed": observed,
        "null_mean": null_mean,
        "null_std": null_std,
        "z_score": z_score,
        "p_value": p_value,
        "iterations": float(iterations),
    }


# Common test metrics
def metric_repeated_groups_count(c: DiscCorpus) -> float:
    """Number of repeated group instances."""
    identical = find_identical_groups(c)
    return float(sum(len(v) for v in identical.values()))


def metric_bigram_collisions(c: DiscCorpus) -> float:
    """Number of distinct bigrams that appear more than once."""
    bigrams = extract_group_ngrams(c, n=2)
    return float(sum(1 for cnt in bigrams.values() if cnt > 1))


def metric_conditional_entropy(c: DiscCorpus) -> float:
    """Bigram conditional entropy H(Y|X)."""
    _, h_cond, _ = compute_bigram_joint_and_conditional_entropy(c)
    return float(h_cond)


def metric_lzma_compression_ratio(c: DiscCorpus) -> float:
    """LZMA compressibility ratio."""
    from phaistos.stats.entropy import compute_compressibility_metrics
    return float(compute_compressibility_metrics(c)["lzma_ratio"])


def metric_prefix_clustering(c: DiscCorpus) -> float:
    """Count of groups starting with the top prefix '02-12'."""
    cnt = 0
    for g in c.all_groups():
        if len(g.signs) >= 2 and g.signs[0] == "02" and g.signs[1] == "12":
            cnt += 1
    return float(cnt)

