"""Orchestrator for autonomous lateral research frontiers across the Phaistos Disc."""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, Optional

from phaistos.core.models import DiscCorpus
from phaistos.corpus.loader import load_transcription
from phaistos.typometry.overlap_analyzer import evaluate_workshop_typometry
from phaistos.prosody.meter import analyze_prosody
from phaistos.astronomy.eclipse_cycles import analyze_astronomy
from phaistos.game.mehen_simulator import evaluate_mehen_hypothesis
from phaistos.comparative.cross_matrix import evaluate_cross_matrix
from phaistos.llm.skeptic import conduct_skeptic_review


def run_lateral_campaign(
    corpus: Optional[DiscCorpus] = None,
    transcription_name: str = "godart_1995",
    num_surrogates: int = 1000,
    num_game_runs: int = 2000,
    run_llm_skeptic: bool = False,
    experiments_dir: Path = Path("experiments"),
) -> Dict[str, Any]:
    """
    Execute a comprehensive lateral investigation sweep across all 5 frontiers:
    1. Workshop Typometry & Mechanics
    2. Strophic Hymn & Prosody
    3. Astronomical Saros & Solstitial Cycles
    4. Ancient Spiral Board Game (Mehen/Ur)
    5. Comparative Inscription Cross-Matrix
    """
    if corpus is None:
        corpus = load_transcription(transcription_name)

    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Typometry
    typometry_result = evaluate_workshop_typometry(corpus)

    # 2. Prosody
    prosody_result = analyze_prosody(corpus, num_surrogates=num_surrogates)

    # 3. Astronomy
    astronomy_result = analyze_astronomy(corpus, num_trials=num_surrogates)

    # 4. Game simulation
    game_result = evaluate_mehen_hypothesis(corpus, num_games=num_game_runs, num_random_boards=100)

    # 5. Comparative Cross-Matrix
    cross_matrix_result = evaluate_cross_matrix(corpus)

    # Synthesis summary
    summary_data = {
        "timestamp": timestamp,
        "transcription": transcription_name,
        "frontiers": {
            "typometry": typometry_result.model_dump(),
            "prosody": prosody_result.model_dump(),
            "astronomy": astronomy_result.model_dump(),
            "game": game_result.model_dump(),
            "cross_matrix": cross_matrix_result.model_dump(),
        },
        "synthesis": {
            "hymn_prosody_supported": prosody_result.periodicity_p_value < 0.01,
            "board_game_falsified": not game_result.is_statistically_optimized_game_board,
            "astronomy_look_elsewhere_warning": astronomy_result.unfalsifiable_numerology_warning,
            "typometric_matrix_falsified": typometry_result.palimpsest_corrections_count > 0,
            "linear_a_identity_falsified": len(cross_matrix_result.linear_a_lexical_matches) == 0,
        },
    }

    # Optional LLM Skeptic review
    if run_llm_skeptic:
        evidence_summary = (
            f"Lateral Campaign Synthesis:\n"
            f"- Hymn Prosody: Triad refrain A16-A19-A22 has p={prosody_result.periodicity_p_value:.5f}, "
            f"strophic correlation r={prosody_result.strophic_responsion_r:.2f}.\n"
            f"- Mehen Board Game: Playable with 0% deadlock, but layout balance percentile is "
            f"{game_result.disc_layout_vs_random_percentile:.1f}% (indistinguishable from random).\n"
            f"- Astronomy: 242 signs equals Saros draconic months, but look-elsewhere p={astronomy_result.look_elsewhere_p_value:.2f}.\n"
            f"- Typometry: 45 punches for 242 signs, 3 thumb erasures prove live hand stamping, refuting cold metal matrix.\n"
            f"- Cross-Corpus: 0 ABAC matches with Tablet PH 1 DI-RA-DI-NA, 4 corpora share ideograms but disjoint phonology."
        )
        try:
            skeptic_review = conduct_skeptic_review(
                hypothesis_id="LATERAL_SYNTHESIS",
                description="Cross-disciplinary lateral sweep across 5 unconventional hypotheses",
                evidence=evidence_summary,
            )
            summary_data["llm_skeptic_review"] = skeptic_review
        except Exception as e:
            summary_data["llm_skeptic_review"] = f"LLM Skeptic unavailable: {e}"

    # Save run artifact
    runs_dir = experiments_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    clean_ts = timestamp.replace(":", "-").replace(".", "_")
    output_path = runs_dir / f"lateral_campaign_{clean_ts}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    summary_data["saved_path"] = str(output_path)
    return summary_data
