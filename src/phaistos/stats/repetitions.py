"""Repetition, refrain, and affix analysis."""

from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple
from phaistos.core.models import DiscCorpus, Group


def find_identical_groups(corpus: DiscCorpus) -> Dict[str, List[str]]:
    """
    Find groups that share the exact same sequence of signs.
    Returns mapping from sign sequence (e.g. '10-03-38') to list of group IDs (e.g. ['A28', 'A31']).
    """
    seq_to_groups = defaultdict(list)
    for g in corpus.all_groups():
        key = "-".join(g.signs)
        seq_to_groups[key].append(g.id)

    # Filter to only repeated sequences
    return {k: v for k, v in seq_to_groups.items() if len(v) > 1}


def find_common_affixes(corpus: DiscCorpus, min_len: int = 2) -> Dict[str, Counter]:
    """
    Compute distribution of prefixes and suffixes of length >= min_len across groups.
    """
    prefixes = Counter()
    suffixes = Counter()

    for g in corpus.all_groups():
        if len(g.signs) >= min_len:
            prefix = "-".join(g.signs[:min_len])
            suffix = "-".join(g.signs[-min_len:])
            prefixes[prefix] += 1
            suffixes[suffix] += 1

    return {"prefixes": prefixes, "suffixes": suffixes}


def find_near_identical_groups(corpus: DiscCorpus, max_distance: int = 1) -> List[Tuple[str, str, int]]:
    """
    Find pairs of groups with Levenshtein edit distance <= max_distance (excluding exact matches).
    """
    groups = corpus.all_groups()
    near_matches = []

    def edit_distance(s1: List[str], s2: List[str]) -> int:
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[m][n]

    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            g1, g2 = groups[i], groups[j]
            dist = edit_distance(g1.signs, g2.signs)
            if 0 < dist <= max_distance:
                near_matches.append((g1.id, g2.id, dist))

    return near_matches


def analyze_oblique_stroke_associations(corpus: DiscCorpus) -> Counter:
    """
    Analyze which signs bear the incised oblique stroke beneath them.
    """
    sign_counts = Counter()
    for g in corpus.all_groups():
        if g.oblique_stroke and len(g.signs) > 0:
            final_sign = g.signs[-1]
            sign_counts[final_sign] += 1
    return sign_counts
