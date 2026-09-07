"""Combinatorial syllabic admissibility solver with Shannon unicity bounds."""

import math
import random
import re
from typing import Dict, List, Set, Tuple
import numpy as np
from pydantic import BaseModel, Field

from phaistos.core.models import DiscCorpus
from phaistos.stats.frequency import compute_sign_frequencies
from phaistos.decipherment.scorer import score_aegean_phonotactics
from phaistos.experiment.unicity import calculate_unicity_distance
from phaistos.stats.permutations import generate_frequency_preserving_corpus


class LanguageTemplate(BaseModel):
    name: str
    vowels: Set[str] = Field(default_factory=lambda: {"a", "e", "i", "o", "u"})
    valid_codas: Set[str] = Field(default_factory=lambda: {"s", "n", "r", ""})
    banned_clusters: List[str] = Field(default_factory=lambda: ["ccc", "ptk", "bdd"])
    characteristic_affixes: List[str] = Field(default_factory=list)


LANGUAGE_TEMPLATES: Dict[str, LanguageTemplate] = {
    "mycenaean_greek": LanguageTemplate(
        name="mycenaean_greek",
        vowels={"a", "e", "i", "o", "u"},
        valid_codas={"s", "n", "r", ""},
        banned_clusters=["ccc", "qq", "ww", "jj"],
        characteristic_affixes=["qe", "jo", "si", "te", "de", "pi"],
    ),
    "syllabic_luwian": LanguageTemplate(
        name="syllabic_luwian",
        vowels={"a", "i", "u"},
        valid_codas={"s", "n", "r", "l", ""},
        banned_clusters=["ccc", "oo", "ee"],
        characteristic_affixes=["ti", "za", "wa", "ha", "sa"],
    ),
    "minoan_linear_a": LanguageTemplate(
        name="minoan_linear_a",
        vowels={"a", "e", "i", "u"},
        valid_codas={""},  # strictly open CV syllables
        banned_clusters=["cc", "coda"],
        characteristic_affixes=["ja", "sa", "ra", "me", "te", "da"],
    ),
    "northwest_semitic": LanguageTemplate(
        name="northwest_semitic",
        vowels={"a", "i", "u"},
        valid_codas={"b", "d", "g", "k", "t", "m", "n", "r", "l", "s", "z", ""},
        banned_clusters=["cccc"],
        characteristic_affixes=["ba", "la", "ma", "na", "ja"],
    ),
}


class SyllabicSolverResult(BaseModel):
    target_language: str
    tested_groups_count: int
    observed_admissibility_rate: float
    null_mean_admissibility_rate: float
    null_std_admissibility_rate: float
    z_score: float
    p_value: float
    unicity_distance_chars: float
    unicity_ratio: float
    is_falsified: bool
    skeptic_verdict: str
    phonotactic_sample: Dict[str, str] = Field(default_factory=dict)


def evaluate_syllabic_admissibility(
    corpus: DiscCorpus,
    target_language: str = "minoan_linear_a",
    n_surrogates: int = 200,
    seed: int = 42,
) -> SyllabicSolverResult:
    """
    Test whether the Disc's sequence structure adheres to candidate Bronze Age
    phonotactics significantly better than frequency-preserving random noise.
    
    Enforces Shannon unicity bound: any solution with degrees of freedom exceeding
    the 242-character limit is flagged as underdetermined.
    """
    rng = random.Random(seed)
    tmpl = LANGUAGE_TEMPLATES.get(target_language, LANGUAGE_TEMPLATES["minoan_linear_a"])

    # Build a frequency-aligned phonetic hypothesis:
    # High frequency signs map to high frequency syllables
    counts = compute_sign_frequencies(corpus)
    sorted_signs = [s for s, _ in counts.most_common()]
    
    # Syllabary pool
    syllables = []
    consonants = ["p", "t", "k", "m", "n", "s", "r", "w", "j", "d"]
    for c in consonants:
        for v in sorted(list(tmpl.vowels)):
            syllables.append(f"{c}{v}")
    # Add pure vowels
    syllables.extend(sorted(list(tmpl.vowels)))

    # Deterministic mapping based on frequency rank
    mapping = {}
    for idx, s in enumerate(sorted_signs):
        mapping[s] = syllables[idx % len(syllables)]

    def compute_admissibility(c: DiscCorpus) -> Tuple[float, Dict[str, str]]:
        valid_count = 0
        samples = {}
        for g in c.all_groups():
            w = "".join(mapping.get(s, "") for s in g.signs)
            score = score_aegean_phonotactics(w)
            # A group is phonotactically admissible if score >= 0 (no illegal clusters or bad codas)
            is_valid = score >= 0.0
            if is_valid:
                valid_count += 1
            if len(samples) < 5:
                samples[g.id] = f"{w} (score={score:+.1f})"
        rate = (valid_count / float(c.total_groups)) * 100.0 if c.total_groups > 0 else 0.0
        return rate, samples

    obs_rate, obs_samples = compute_admissibility(corpus)

    null_rates = []
    for _ in range(n_surrogates):
        surrogate = generate_frequency_preserving_corpus(corpus, rng)
        rate, _ = compute_admissibility(surrogate)
        null_rates.append(rate)

    null_arr = np.array(null_rates)
    null_mean = float(np.mean(null_arr))
    null_std = float(np.std(null_arr)) if float(np.std(null_arr)) > 0 else 1e-6
    z_score = (obs_rate - null_mean) / null_std
    p_value = float(np.mean(null_arr >= obs_rate))

    unicity = calculate_unicity_distance(
        alphabet_size=len(corpus.signs_catalogue),
        is_syllabic=True,
    )

    is_falsified = z_score <= 1.96 or p_value > 0.05
    if is_falsified:
        verdict = (
            f"FALSIFIED: {tmpl.name.replace('_', ' ').title()} phonotactic admissibility rate ({obs_rate:.1f}%) "
            f"is indistinguishable from random frequency-preserving noise (Null: {null_mean:.1f}% ± {null_std:.1f}%, "
            f"Z = {z_score:+.2f}, p = {p_value:.4f}). Any apparent grammatical regularities are chance artifacts."
        )
    else:
        verdict = (
            f"ADMISSIBLE BUT UNDERDETERMINED: Phonotactic legality ({obs_rate:.1f}%, Z = {z_score:+.2f}) "
            f"exceeds random controls, but the Shannon unicity bound requires {unicity['required_ratio']:.1f}x "
            f"more text ({unicity['unicity_distance_chars']:.0f} chars) to confirm a unique solution."
        )

    return SyllabicSolverResult(
        target_language=tmpl.name,
        tested_groups_count=corpus.total_groups,
        observed_admissibility_rate=obs_rate,
        null_mean_admissibility_rate=null_mean,
        null_std_admissibility_rate=null_std,
        z_score=z_score,
        p_value=p_value,
        unicity_distance_chars=unicity["unicity_distance_chars"],
        unicity_ratio=unicity["required_ratio"],
        is_falsified=is_falsified,
        skeptic_verdict=verdict,
        phonotactic_sample=obs_samples,
    )
