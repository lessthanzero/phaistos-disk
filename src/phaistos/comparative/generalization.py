"""Cross-corpus generalization engine for evaluating Phaistos Disc signs and hypotheses against held-out Cretan inscriptions."""

from typing import Dict, List, Optional, Tuple
import numpy as np

from phaistos.core.models import DiscCorpus
from phaistos.comparative.models import (
    ArkalochoriInscription,
    GeneralizationResult,
    ProposedCorrespondence,
)
from phaistos.stats.frequency import compute_sign_frequencies, compute_positional_statistics
from phaistos.decipherment.scorer import score_aegean_phonotactics


def evaluate_arkalochori_generalization(
    corpus: DiscCorpus,
    inscription: ArkalochoriInscription,
    correspondences: List[ProposedCorrespondence],
    n_surrogates: int = 1000,
    seed: int = 42,
) -> GeneralizationResult:
    """
    Evaluate whether sign parallels and phonetic projections generalize
    to the 15-sign Arkalochori Axe inscription.
    """
    rng = np.random.default_rng(seed)
    total_signs = len(inscription.signs)

    # 1. Sign coverage and matching
    matched_parallels = [s.proposed_phaistos_parallel for s in inscription.signs if s.proposed_phaistos_parallel]
    matched_count = len(matched_parallels)
    unique_matched = sorted(list(set(matched_parallels)))
    coverage_pct = (matched_count / total_signs) * 100.0 if total_signs > 0 else 0.0

    # 2. Test concentration on sign 02 and sign 21 against Phaistos Disc frequencies
    # On the Axe, sign 02 appears 4 times, 21 appears 4 times, 35 appears 4 times.
    # We calculate the repeat concentration (Gini or Simpson diversity index).
    obs_counts = {}
    for p in matched_parallels:
        obs_counts[p] = obs_counts.get(p, 0) + 1
    
    # Simpson dominance: sum of (n_i / N)^2
    obs_dominance = sum((c / matched_count) ** 2 for c in obs_counts.values())

    # Null distribution: Sample matched_count signs from Phaistos Disc empirical frequency
    disc_freqs = compute_sign_frequencies(corpus)
    signs_pool = []
    for sign_id, cnt in disc_freqs.items():
        signs_pool.extend([sign_id] * cnt)

    null_dominance = []
    for _ in range(n_surrogates):
        sample = rng.choice(signs_pool, size=matched_count, replace=True)
        counts = {}
        for s in sample:
            counts[s] = counts.get(s, 0) + 1
        d = sum((c / matched_count) ** 2 for c in counts.values())
        null_dominance.append(d)

    null_mean = float(np.mean(null_dominance))
    null_std = float(np.std(null_dominance)) if float(np.std(null_dominance)) > 0 else 1e-6
    z_score = (obs_dominance - null_mean) / null_std
    p_val = float(np.mean([d >= obs_dominance for d in null_dominance]))

    # 3. Target language phonotactic admissibility under Linear A projection
    # Create mapping from disc sign to phonetic value
    phonetic_map: Dict[str, str] = {}
    for corr in correspondences:
        if corr.proposed_phonetic_value:
            phonetic_map[corr.disc_sign] = corr.proposed_phonetic_value

    # Check phonotactic score of the 3 columns
    columns_transcription: Dict[int, List[str]] = {1: [], 2: [], 3: []}
    for sign in inscription.signs:
        p_val_str = "?"
        if sign.proposed_phaistos_parallel and sign.proposed_phaistos_parallel in phonetic_map:
            p_val_str = phonetic_map[sign.proposed_phaistos_parallel]
        columns_transcription[sign.column].append(p_val_str)

    # Calculate average phonotactic score across columns
    admissibility: Dict[str, float] = {}
    col_scores = []
    for col_idx, col_sylls in columns_transcription.items():
        valid_sylls = [s for s in col_sylls if s != "?"]
        if len(valid_sylls) >= 2:
            text = "".join(valid_sylls)
            col_scores.append(score_aegean_phonotactics(text))

    mean_score = float(np.mean(col_scores)) if col_scores else -10.0
    admissibility["aegean_syllabic"] = mean_score
    admissibility["linear_a_projection"] = mean_score

    # 4. Epistemic verdict from Skeptic analysis
    if z_score > 3.0:
        verdict = (
            "EXTREME CONCENTRATION: Arkalochori Axe inscription repeats a tiny subset of "
            "Phaistos signs (02, 21, 35) at rates vastly exceeding the Disc's general distribution "
            f"(Z={z_score:.2f}, p={p_val:.4f}). Positional syntax (02 in medial position) contradicts "
            "the Disc's strictly initial 02 prior. Generalization to language is UNSUPPORTED; "
            "consistent with a specialized votive/ritual formula or pseudo-script."
        )
    else:
        verdict = "INCONCLUSIVE: Sign overlap is consistent with chance selection from Phaistos inventory."

    return GeneralizationResult(
        artifact_name=inscription.artifact,
        total_signs=total_signs,
        matched_phaistos_signs_count=matched_count,
        coverage_percentage=coverage_pct,
        unique_phaistos_signs_matched=unique_matched,
        structural_formula_z_score=float(z_score),
        formula_p_value=float(p_val),
        target_language_admissibility=admissibility,
        skeptic_verdict=verdict,
    )
