"""Permutation testing for cross-script correspondence hypotheses."""

import random
from typing import Dict, List
import numpy as np

from phaistos.core.models import DiscCorpus
from phaistos.comparative.models import ProposedCorrespondence, LinearASign
from phaistos.comparative.matcher import evaluate_frequency_rank_correlation


def run_correspondence_permutation_test(
    corpus: DiscCorpus,
    correspondences: List[ProposedCorrespondence],
    linear_a_signs: List[LinearASign],
    iterations: int = 500,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Test whether the observed rank correlation between Phaistos and Linear A signs
    is significantly higher than a random assignment of Linear A signs.
    """
    rng = random.Random(seed)
    obs_res = evaluate_frequency_rank_correlation(corpus, correspondences, linear_a_signs)
    obs_rho = obs_res["spearman_rho"]

    # Extract eligible Linear A signs
    available_la_signs = [c.linear_a_sign for c in correspondences if c.linear_a_sign is not None]

    null_rhos = []
    for _ in range(iterations):
        shuffled_la = list(available_la_signs)
        rng.shuffle(shuffled_la)

        # Build surrogate correspondences with shuffled Linear A signs
        surr_corrs = []
        s_idx = 0
        for c in correspondences:
            if c.linear_a_sign is not None:
                new_c = c.model_copy(update={"linear_a_sign": shuffled_la[s_idx]})
                surr_corrs.append(new_c)
                s_idx += 1
            else:
                surr_corrs.append(c)

        surr_res = evaluate_frequency_rank_correlation(corpus, surr_corrs, linear_a_signs)
        null_rhos.append(surr_res["spearman_rho"])

    null_arr = np.array(null_rhos)
    null_mean = float(np.mean(null_arr))
    null_std = float(np.std(null_arr))
    z_score = (obs_rho - null_mean) / null_std if null_std > 0 else 0.0

    # Probability of observing higher correlation by chance
    p_val = float(np.sum(null_arr >= obs_rho) / iterations)

    return {
        "observed_rho": obs_rho,
        "null_mean_rho": null_mean,
        "null_std_rho": null_std,
        "z_score": z_score,
        "p_value": p_val,
        "iterations": float(iterations),
    }
