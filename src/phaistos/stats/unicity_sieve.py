"""Information-Theoretic Model Parsimony & Degrees-of-Freedom Sieve.

Evaluates whether any hypothesized phonetic and lexical decipherment model has fewer
degrees of freedom (parameter bits) than the empirical information capacity of the
242-token Phaistos Disc corpus (930.3 bits).

Grounds the Skeptic Rule (AGENTS.md) in information-theoretic bounds: any model introducing
more parameter bits than the text possesses is mathematically underdetermined and overfit.
"""

from dataclasses import dataclass
import math
from typing import Any, Dict, List, Optional
import numpy as np

from phaistos.core.models import DiscCorpus
from phaistos.corpus.loader import load_transcription
from phaistos.stats.frequency import compute_sign_frequencies


@dataclass
class UnicityEvaluationResult:
    """Rigorous evaluation of a decipherment model against information-theoretic parsimony bounds."""
    model_name: str
    mapped_signs_count: int
    total_disc_signs: int
    candidate_syllables_per_sign: int
    corpus_total_tokens: int
    corpus_entropy_bits_per_symbol: float
    corpus_total_information_capacity_bits: float
    model_degrees_of_freedom_bits: float
    unicity_distance_required_signs: float
    unicity_ratio: float  # DoF / Capacity (< 1.0 is constrained; > 1.0 is overfit)
    is_mathematically_constrained: bool
    verdict: str


def evaluate_model_unicity(
    model_name: str = "custom_phonetic_model",
    mapped_signs_count: int = 45,
    candidate_syllables_per_sign: int = 60,
    target_lexicon_size: int = 1,
    translated_words_count: int = 0,
    corpus: Optional[DiscCorpus] = None,
) -> UnicityEvaluationResult:
    """
    Evaluate whether a phonetic/lexical decipherment model is mathematically constrained.

    Parameters
    ----------
    model_name: Name of the proposed reconstruction (e.g. '7_cross_script_anchors', 'full_45_pie_reading')
    mapped_signs_count: Number of signs assigned explicit phonetic values
    candidate_syllables_per_sign: Number of potential syllable choices tested (e.g. 60 open CV syllables)
    target_lexicon_size: Number of vocabulary roots in candidate language dictionary (e.g. 3,000 PIE roots)
    translated_words_count: Number of Disc words assigned a translated lexical meaning
    corpus: Canonical Disc corpus
    """
    if corpus is None:
        corpus = load_transcription()

    freqs = compute_sign_frequencies(corpus)
    total_tokens = sum(freqs.values())  # 242
    num_unique_signs = len(freqs)  # 45

    # 1. Compute empirical Shannon entropy of the sign distribution
    p_dist = np.array([count / total_tokens for count in freqs.values()], dtype=np.float64)
    h_symbol = -float(np.sum(p_dist * np.log2(np.clip(p_dist, 1e-12, 1.0))))  # ~5.09 bits/symbol

    # Theoretical maximum entropy log2(|A|) = log2(45) ~ 5.49 bits
    max_h = math.log2(num_unique_signs)
    redundancy_rate = 1.0 - (h_symbol / max_h)  # ~0.073 unigram redundancy

    # For natural language written in a syllabary, language redundancy R_L is typically ~0.70
    # The effective information distance D_L = R_L * log2(|A|) ~ 0.70 * 5.49 ~ 3.844 bits/symbol
    d_l = 0.70 * max_h
    total_capacity = total_tokens * d_l  # 242 * 3.844 ~ 930.3 bits

    # 2. Model Degrees of Freedom (Parameter Key Space Entropy H(K))
    # Phonetic mapping DoF: choosing 1 syllable out of N choices for each mapped sign
    bits_per_phonetic_choice = math.log2(candidate_syllables_per_sign) if candidate_syllables_per_sign > 1 else 1.0
    phonetic_dof = mapped_signs_count * bits_per_phonetic_choice

    # Lexical translation DoF: choosing 1 root meaning out of L candidate words in vocabulary
    lexical_bits_per_word = math.log2(target_lexicon_size) if target_lexicon_size > 1 else 0.0
    lexical_dof = translated_words_count * lexical_bits_per_word

    total_dof = phonetic_dof + lexical_dof

    # 3. Parsimony / Unicity Bound U = DoF / D_L
    unicity_distance = total_dof / d_l if d_l > 0 else float("inf")
    ratio = total_dof / total_capacity if total_capacity > 0 else float("inf")

    is_constrained = ratio < 1.0

    if ratio <= 0.20:
        verdict = (
            f"STRICTLY CONSTRAINED (Ratio={ratio:.2f}, Required={unicity_distance:.0f} signs < {total_tokens}). "
            f"The model degrees of freedom ({total_dof:.1f} bits) are far below the corpus information "
            f"capacity ({total_capacity:.1f} bits). The parameter space is mathematically verifiable."
        )
    elif ratio < 1.0:
        verdict = (
            f"BORDERLINE CONSTRAINED (Ratio={ratio:.2f}, Required={unicity_distance:.0f} signs). "
            f"The hypothesis does not exceed total information content, but leaves narrow statistical margin."
        )
    else:
        verdict = (
            f"UNCONSTRAINED OVERFIT / PSEUDO-DECIPHERMENT (Ratio={ratio:.2f} > 1.0, Required={unicity_distance:.0f} signs > {total_tokens}). "
            f"The model introduces {total_dof:.1f} parameter bits, exceeding the corpus capacity ({total_capacity:.1f} bits). "
            f"Under information-theoretic parsimony bounds, any apparent reading is an underdetermined mathematical artifact."
        )

    return UnicityEvaluationResult(
        model_name=model_name,
        mapped_signs_count=mapped_signs_count,
        total_disc_signs=num_unique_signs,
        candidate_syllables_per_sign=candidate_syllables_per_sign,
        corpus_total_tokens=total_tokens,
        corpus_entropy_bits_per_symbol=round(h_symbol, 3),
        corpus_total_information_capacity_bits=round(total_capacity, 1),
        model_degrees_of_freedom_bits=round(total_dof, 1),
        unicity_distance_required_signs=round(unicity_distance, 1),
        unicity_ratio=round(ratio, 3),
        is_mathematically_constrained=is_constrained,
        verdict=verdict,
    )
