"""N-gram analysis, transition matrices, and graph structure."""

from collections import Counter
from typing import Dict, List, Tuple
import numpy as np
import networkx as nx

from phaistos.core.models import DiscCorpus


def extract_group_ngrams(corpus: DiscCorpus, n: int = 2) -> Counter:
    """
    Extract n-grams strictly within individual groups (no spanning across group dividers).
    """
    ngrams = Counter()
    for group in corpus.all_groups():
        signs = group.signs
        if len(signs) >= n:
            for i in range(len(signs) - n + 1):
                gram = tuple(signs[i : i + n])
                ngrams[gram] += 1
    return ngrams


def extract_global_ngrams(corpus: DiscCorpus, n: int = 2) -> Counter:
    """
    Extract n-grams along the continuous reading trajectory of each side.
    """
    ngrams = Counter()
    for side in (corpus.side_a, corpus.side_b):
        all_signs = [s for g in side.groups for s in g.signs]
        if len(all_signs) >= n:
            for i in range(len(all_signs) - n + 1):
                gram = tuple(all_signs[i : i + n])
                ngrams[gram] += 1
    return ngrams


def compute_transition_matrix(corpus: DiscCorpus) -> Tuple[List[str], np.ndarray]:
    """
    Compute empirical Markov transition matrix T where T[i, j] = P(sign_j | sign_i)
    within group boundaries.
    """
    # Sorted list of unique sign IDs (1-45)
    all_signs = sorted(list({s.evans_id for s in corpus.signs_catalogue}))
    sign_to_idx = {s: i for i, s in enumerate(all_signs)}
    dim = len(all_signs)

    counts = np.zeros((dim, dim), dtype=np.float64)
    bigrams = extract_group_ngrams(corpus, n=2)

    for (s1, s2), freq in bigrams.items():
        if s1 in sign_to_idx and s2 in sign_to_idx:
            i, j = sign_to_idx[s1], sign_to_idx[s2]
            counts[i, j] += freq

    # Row-normalize to get transition probabilities
    row_sums = counts.sum(axis=1, keepdims=True)
    probs = np.divide(counts, row_sums, out=np.zeros_like(counts), where=row_sums != 0)

    return all_signs, probs


def build_transition_graph(corpus: DiscCorpus, min_weight: int = 1) -> nx.DiGraph:
    """
    Build directed graph of sign transitions.
    Nodes: sign IDs
    Edges: directed transitions with 'weight' = frequency.
    """
    G = nx.DiGraph()
    for sign in corpus.signs_catalogue:
        G.add_node(
            sign.evans_id,
            name=sign.name,
            glyph=sign.unicode_char,
            category=sign.category,
        )

    bigrams = extract_group_ngrams(corpus, n=2)
    for (u, v), count in bigrams.items():
        if count >= min_weight:
            G.add_edge(u, v, weight=count)

    return G
