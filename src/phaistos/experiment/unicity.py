"""Shannon unicity distance calculations and theoretical overfit bounds."""

import math
from typing import Dict


def calculate_unicity_distance(
    alphabet_size: int = 45,
    target_alphabet_size: int = 45,
    is_syllabic: bool = True,
    language_redundancy_bits: float = 2.5,
) -> Dict[str, float]:
    """
    Calculate Claude Shannon's unicity distance:
    U ≈ H(K) / D
    where H(K) is the entropy of the key space,
    and D is the redundancy of the language (bits per symbol).
    """
    # 1. Key space entropy H(K)
    if is_syllabic:
        # Syllabic substitution: 45 signs mapped into target syllabary (e.g. 60-80 CV syllables)
        # H(K) = log2(target_size^45) = 45 * log2(target_size)
        target_syllables = max(target_alphabet_size, 60)
        h_k = 45 * math.log2(target_syllables)
    else:
        # Simple monoalphabetic substitution: 45 signs into 26 letters (or 45! permutations)
        # H(K) = log2(45!) ≈ 186.4 bits
        h_k = math.lgamma(alphabet_size + 1) / math.log(2)

    # 2. Redundancy D = R_0 - R
    # R_0 = log2(alphabet_size)
    r_0 = math.log2(alphabet_size)
    d = max(0.1, min(language_redundancy_bits, r_0 - 0.5))

    # 3. Shannon Unicity Distance
    u = h_k / d

    corpus_length = 242
    is_underdetermined = corpus_length < u

    return {
        "key_entropy_bits": float(h_k),
        "symbol_max_entropy_bits": float(r_0),
        "redundancy_bits": float(d),
        "unicity_distance_chars": float(u),
        "corpus_length_chars": float(corpus_length),
        "is_underdetermined": float(1.0 if is_underdetermined else 0.0),
        "required_ratio": float(u / corpus_length),
    }


def format_unicity_warning(calc: Dict[str, float]) -> str:
    """Format an epigraphic warning on mathematical unicity distance bounds."""
    u_len = calc["unicity_distance_chars"]
    ratio = calc["required_ratio"]
    return (
        f"Shannon Unicity Bound: U ≈ {u_len:.0f} characters needed to distinguish true decipherment from noise.\n"
        f"Corpus size is only 242 signs (model requires {ratio:.1f}x more text).\n"
        f"Any unconstrained phonetic mapping WILL overfit and produce spurious solutions."
    )
