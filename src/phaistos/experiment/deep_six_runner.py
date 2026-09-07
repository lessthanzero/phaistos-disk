"""Orchestrator for the 6 Advanced Research Frontiers across the Phaistos Disc."""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, Optional

from phaistos.core.models import DiscCorpus
from phaistos.corpus.loader import load_transcription
from phaistos.linguistics.morphology import evaluate_morphosyntax
from phaistos.prosody.strophic_b import evaluate_side_b_strophes
from phaistos.geometry.spiral_kinematics import evaluate_spiral_kinematics
from phaistos.prosody.acoustic import render_central_triad_audio
from phaistos.linguistics.automata import evaluate_chomsky_complexity
from phaistos.epigraphy.petrography import evaluate_clay_provenance


def run_deep_six_campaign(
    corpus: Optional[DiscCorpus] = None,
    transcription_name: str = "godart_1995",
    num_surrogates: int = 1000,
    audio_output_dir: Path = Path("experiments/audio"),
    experiments_dir: Path = Path("experiments"),
) -> Dict[str, Any]:
    """
    Execute all 6 advanced research frontiers:
    1. Morphosyntax & Prefix Stripping
    2. Side B Strophic Structure
    3. Kinematic Spiral Modeling
    4. Acoustic Lyre Resynthesis
    5. Chomsky Automata & Formal Complexity
    6. Petrographic Clay Provenance
    """
    if corpus is None:
        corpus = load_transcription(transcription_name)

    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Morphosyntax
    morph_res = evaluate_morphosyntax(corpus, num_surrogates=num_surrogates)

    # 2. Side B Strophes
    strophic_b_res = evaluate_side_b_strophes(corpus, num_surrogates=num_surrogates)

    # 3. Spiral Kinematics (Side A and Side B)
    spiral_a = evaluate_spiral_kinematics("A")
    spiral_b = evaluate_spiral_kinematics("B")

    # 4. Acoustic Lyre Resynthesis
    audio_res = render_central_triad_audio(output_dir=audio_output_dir)

    # 5. Chomsky Automata Complexity
    automata_res = evaluate_chomsky_complexity(corpus, num_surrogates=num_surrogates)

    # 6. Petrography & Clay Provenance
    petrography_res = evaluate_clay_provenance()

    # Consolidated data
    summary = {
        "timestamp": timestamp,
        "transcription": transcription_name,
        "frontiers": {
            "morphosyntax": morph_res.model_dump(),
            "strophic_b": strophic_b_res.model_dump(),
            "spiral_kinematics": {
                "side_a": spiral_a.model_dump(),
                "side_b": spiral_b.model_dump(),
            },
            "acoustic": audio_res.model_dump(),
            "automata": automata_res.model_dump(),
            "petrography": petrography_res.model_dump(),
        },
        "epistemic_conclusions": {
            "agglutinative_prefixes_confirmed": morph_res.is_statistically_agglutinative,
            "side_b_antistrophe_confirmed": strophic_b_res.stanza_mora_std < 2.0,
            "mechanical_pin_and_cord_confirmed": spiral_b.is_mechanically_guided,
            "chomsky_regular_grammar": "Type 3" in automata_res.chomsky_hierarchy_level,
            "local_mesara_clay_confirmed": petrography_res.exotic_origin_falsified,
        },
    }

    # Save artifact
    runs_dir = experiments_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    clean_ts = timestamp.replace(":", "-").replace(".", "_")
    out_path = runs_dir / f"deep_six_campaign_{clean_ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    summary["saved_path"] = str(out_path)
    return summary
