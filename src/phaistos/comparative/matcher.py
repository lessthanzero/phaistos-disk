"""Statistical correlation and scoring for candidate cross-script correspondences."""

from typing import Dict, List, Tuple
from scipy import stats
import numpy as np

from phaistos.core.models import DiscCorpus
from phaistos.comparative.models import ProposedCorrespondence, LinearASign
from phaistos.stats.frequency import compute_sign_frequencies, compute_positional_statistics


def evaluate_frequency_rank_correlation(
    corpus: DiscCorpus,
    correspondences: List[ProposedCorrespondence],
    linear_a_signs: List[LinearASign],
) -> Dict[str, float]:
    """
    Compute Spearman's rank correlation between Phaistos Disc frequency rank
    and corresponding Linear A frequency rank.
    """
    # 1. Rank Phaistos signs by frequency
    disc_counts = compute_sign_frequencies(corpus)
    # Sort descending: rank 1 = most frequent
    sorted_disc_signs = [s for s, _ in disc_counts.most_common()]
    disc_ranks = {s: r + 1 for r, s in enumerate(sorted_disc_signs)}

    # 2. Linear A rank lookup
    la_ranks = {la.id: la.relative_frequency_rank for la in linear_a_signs}

    paired_disc_ranks = []
    paired_la_ranks = []

    for corr in correspondences:
        if corr.linear_a_sign and corr.linear_a_sign in la_ranks:
            if corr.disc_sign in disc_ranks:
                paired_disc_ranks.append(disc_ranks[corr.disc_sign])
                paired_la_ranks.append(la_ranks[corr.linear_a_sign])

    if len(paired_disc_ranks) < 3:
        return {"spearman_rho": 0.0, "p_value": 1.0, "sample_size": float(len(paired_disc_ranks))}

    rho, p_val = stats.spearmanr(paired_disc_ranks, paired_la_ranks)
    return {
        "spearman_rho": float(rho) if not np.isnan(rho) else 0.0,
        "p_value": float(p_val) if not np.isnan(p_val) else 1.0,
        "sample_size": float(len(paired_disc_ranks)),
    }
