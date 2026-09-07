"""Phonotactic scoring engine for decipherment hypotheses."""

import math
import re
from typing import Dict, List, Tuple
from phaistos.core.models import DiscCorpus
from phaistos.decipherment.models import DeciphermentHypothesis


def transliterate_group(signs: List[str], mapping: Dict[str, str]) -> str:
    """Transliterate a group of Evans signs using a phonetic mapping."""
    return "".join(mapping.get(s, f"[{s}]") for s in signs)


def score_aegean_phonotactics(word: str) -> float:
    """
    Score phonotactic plausibility for Bronze Age Aegean syllabic language
    (predominantly open CV / V syllables, rare consonant clusters, final vowels or sonorants).
    Returns log-likelihood proxy score.
    """
    if not word or "[" in word:
        # Penalize unmapped signs
        return -5.0

    score = 0.0
    # Clean word of separators
    clean = re.sub(r"[^a-zA-Z]", "", word.lower())
    if not clean:
        return -5.0

    vowels = set("aeiou")
    consonants = set("bcdfghjklmnpqrstvwxyz")

    # Reward open syllable endings
    if clean[-1] in vowels:
        score += 2.0
    elif clean[-1] in {"s", "n", "r"}:
        score += 0.5
    else:
        # Obstruent word-final penalty
        score -= 2.0

    # Penalize consonant clusters > 2
    for i in range(len(clean) - 2):
        if clean[i] in consonants and clean[i + 1] in consonants and clean[i + 2] in consonants:
            score -= 3.0

    # Reward regular alternating CV structure
    cv_alternations = 0
    for i in range(len(clean) - 1):
        if (clean[i] in consonants and clean[i + 1] in vowels) or (clean[i] in vowels and clean[i + 1] in consonants):
            cv_alternations += 1
    score += cv_alternations * 0.5

    return score


def evaluate_hypothesis_score(corpus: DiscCorpus, hypothesis: DeciphermentHypothesis) -> float:
    """
    Evaluate composite score of a decipherment hypothesis across all groups.
    Sum of phonotactic log-likelihoods minus complexity penalty.
    """
    total_score = 0.0
    for group in corpus.all_groups():
        trans = transliterate_group(group.signs, hypothesis.sign_mapping)
        total_score += score_aegean_phonotactics(trans)

    # Subtract complexity penalty
    total_score -= hypothesis.complexity_penalty
    return float(total_score)
