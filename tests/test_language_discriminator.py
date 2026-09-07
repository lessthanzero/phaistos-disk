"""Unit tests for Bayesian Cross-Linguistic Phonotactic Family Discriminator."""

import pytest
from phaistos.linguistics.language_discriminator import run_language_family_discrimination


def test_language_family_discrimination():
    """Verify that the Disc ranks Minoan highest and disfavors Greek/Egyptian."""
    report = run_language_family_discrimination(n_null_surrogates=200, seed=42)

    assert report.total_disc_groups == 61
    assert report.total_disc_tokens in {241, 242}
    assert report.best_fit_family.startswith("Minoan")

    # Minoan should have the highest fit and positive LLR
    minoan_rank = next(r for r in report.rankings if "Minoan" in r.family_name)
    assert minoan_rank.syllable_structure_fit_pct > 90.0
    assert minoan_rank.log_likelihood_ratio_vs_null > 0

    # Ancient Egyptian should have negative LLR vs null due to triconsonantal mismatch
    egyptian_rank = next(r for r in report.rankings if "Ancient Egyptian" in r.family_name)
    assert egyptian_rank.log_likelihood_ratio_vs_null < 0
    assert "FALSIFIED" in egyptian_rank.epistemic_status
