"""Statistical analysis engine for sign frequencies, positions, and entropy."""

from collections import Counter
import math
from typing import Dict, List, Tuple
from phaistos.core.models import DiscCorpus


def compute_sign_frequencies(corpus: DiscCorpus) -> Counter:
    """Compute raw frequency of each sign across the entire disc."""
    counts = Counter()
    for group in corpus.all_groups():
        counts.update(group.signs)
    return counts


def compute_group_length_distribution(corpus: DiscCorpus) -> Counter:
    """Compute distribution of word/group lengths."""
    return Counter(group.length for group in corpus.all_groups())


def compute_positional_statistics(corpus: DiscCorpus) -> Dict[str, Dict[str, float]]:
    """
    Compute initial, medial, and final positional probabilities for each sign:
    P(initial), P(medial), P(final).
    """
    initial_counts = Counter()
    medial_counts = Counter()
    final_counts = Counter()
    total_counts = Counter()

    for group in corpus.all_groups():
        g_len = len(group.signs)
        for idx, sign in enumerate(group.signs):
            total_counts[sign] += 1
            if idx == 0:
                initial_counts[sign] += 1
            elif idx == g_len - 1:
                final_counts[sign] += 1
            else:
                medial_counts[sign] += 1

    stats = {}
    for sign in sorted(total_counts.keys()):
        tot = total_counts[sign]
        stats[sign] = {
            "total": tot,
            "p_initial": initial_counts[sign] / tot,
            "p_medial": medial_counts[sign] / tot,
            "p_final": final_counts[sign] / tot,
        }
    return stats


def compute_shannon_entropy(counts: Counter) -> float:
    """Compute Shannon entropy in bits for a given discrete frequency distribution."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy
