"""Experiment execution harness, surrogate scoring, and skeptic review."""

import json
from datetime import datetime, timezone
from pathlib import Path
import random
from typing import Dict, List
import numpy as np
import yaml

from phaistos.core.models import DiscCorpus
from phaistos.decipherment.models import DeciphermentHypothesis, DeciphermentResult
from phaistos.decipherment.scorer import evaluate_hypothesis_score, transliterate_group
from phaistos.experiment.unicity import calculate_unicity_distance
from phaistos.stats.permutations import generate_frequency_preserving_corpus


def run_decipherment_experiment(
    corpus: DiscCorpus,
    hypothesis: DeciphermentHypothesis,
    iterations: int = 200,
    seed: int = 42,
    experiments_dir: Path = Path("experiments"),
) -> DeciphermentResult:
    """
    Run full anti-bullshit evaluation of a decipherment hypothesis:
    1. Shannon unicity bounds check.
    2. Score observed disc.
    3. Score N frequency-preserving shuffled surrogate discs.
    4. Compute Z-score and Skeptic ruling.
    5. Save immutable run artifact.
    """
    rng = random.Random(seed)

    # 1. Unicity bounds
    unicity_res = calculate_unicity_distance(
        alphabet_size=len(corpus.signs_catalogue),
        is_syllabic=True,
    )
    unicity_ratio = unicity_res["required_ratio"]

    # 2. Observed score
    observed_score = evaluate_hypothesis_score(corpus, hypothesis)

    # 3. Null distribution over frequency-preserving surrogates
    null_scores = []
    for _ in range(iterations):
        surrogate = generate_frequency_preserving_corpus(corpus, rng)
        null_scores.append(evaluate_hypothesis_score(surrogate, hypothesis))

    null_arr = np.array(null_scores)
    null_mean = float(np.mean(null_arr))
    null_std = float(np.std(null_arr))
    z_score = (observed_score - null_mean) / null_std if null_std > 0 else 0.0

    # Probability that random noise produces a score >= observed
    p_value = float(np.sum(null_arr >= observed_score) / iterations)

    # 4. Skeptic Verdict
    is_falsified = False
    contradictions = []

    if z_score <= 1.96 or p_value > 0.05:
        is_falsified = True
        verdict = (
            f"FALSIFIED: The hypothesis performs no better than random frequency-preserving shuffles "
            f"(Z = {z_score:+.2f}, p = {p_value:.4f}). High scores are an artifact of random noise."
        )
        contradictions.append("Equally high phonotactic likelihood achieved on shuffled control texts.")
    elif unicity_ratio > 1.0:
        verdict = (
            f"UNDERDETERMINED: Statistically superior to noise (Z = {z_score:+.2f}), but the model requires "
            f"{unicity_ratio:.1f}x more text to reach Shannon unicity. Cannot distinguish true key from spurious overfit."
        )
        contradictions.append(f"Text length (242) is far below Shannon unicity distance ({unicity_res['unicity_distance_chars']:.0f}).")
    else:
        verdict = f"SUPPORTED: Significantly outperforms randomized controls (Z = {z_score:+.2f}, p = {p_value:.4f})."

    # Sample transliteration of first 5 groups on Side A
    sample_trans = {}
    for g in corpus.side_a.groups[:6]:
        sample_trans[g.id] = transliterate_group(g.signs, hypothesis.sign_mapping)

    result = DeciphermentResult(
        hypothesis_id=hypothesis.id,
        target_language=hypothesis.target_language,
        observed_score=observed_score,
        null_mean_score=null_mean,
        null_std_score=null_std,
        z_score=z_score,
        p_value=p_value,
        is_falsified=is_falsified,
        skeptic_verdict=verdict,
        unicity_ratio=unicity_ratio,
        sample_transliteration=sample_trans,
        contradictions=contradictions,
    )

    # 5. Save run artifact
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = experiments_dir / "runs" / f"{timestamp}_{hypothesis.id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    result_file = run_dir / "result.json"
    result_file.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    # Update registry
    registry_file = experiments_dir / "registry.yaml"
    if registry_file.is_file():
        with open(registry_file, "r", encoding="utf-8") as f:
            reg = yaml.safe_load(f) or {}
    else:
        reg = {}

    runs = reg.get("experiments", [])
    runs.append({
        "run_id": f"{timestamp}_{hypothesis.id}",
        "hypothesis_id": hypothesis.id,
        "target_language": hypothesis.target_language,
        "timestamp": timestamp,
        "z_score": z_score,
        "p_value": p_value,
        "is_falsified": is_falsified,
    })
    reg["experiments"] = runs

    with open(registry_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(reg, f)

    return result
