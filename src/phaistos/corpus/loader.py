"""Corpus loader for canonical Phaistos Disc datasets."""

from pathlib import Path
from typing import Dict, List, Optional
import yaml

from phaistos.core.models import DiscCorpus, DiscSide, Group, Sign


def get_default_corpus_dir() -> Path:
    """Find the canonical corpus directory relative to the repository root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        candidate = current / "corpus"
        if candidate.is_dir() and (candidate / "signs.yaml").is_file():
            return candidate
        current = current.parent
    raise FileNotFoundError("Could not locate corpus directory in parent hierarchy")


def load_signs(corpus_dir: Optional[Path] = None) -> List[Sign]:
    """Load the canonical 45 signs catalogue from signs.yaml."""
    base_dir = corpus_dir or get_default_corpus_dir()
    signs_file = base_dir / "signs.yaml"
    with open(signs_file, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [Sign(**s) for s in raw["signs"]]


def load_transcription(source_name: str = "godart_1995", corpus_dir: Optional[Path] = None) -> DiscCorpus:
    """Load canonical transcription and hydrate DiscCorpus."""
    base_dir = corpus_dir or get_default_corpus_dir()
    trans_file = base_dir / "transcriptions" / f"{source_name}.yaml"
    if not trans_file.is_file():
        raise FileNotFoundError(f"Transcription file not found: {trans_file}")

    signs = load_signs(base_dir)

    with open(trans_file, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    meta = raw["transcription"]

    side_a_groups = [
        Group(
            id=g["id"],
            side="A",
            turn=g.get("turn", 1),
            signs=g["signs"],
            oblique_stroke=g.get("oblique_stroke", False),
            erasure=g.get("erasure", False),
            uncertain=g.get("uncertain", False),
            notes=g.get("notes"),
        )
        for g in raw["side_a"]["groups"]
    ]

    side_b_groups = [
        Group(
            id=g["id"],
            side="B",
            turn=g.get("turn", 1),
            signs=g["signs"],
            oblique_stroke=g.get("oblique_stroke", False),
            erasure=g.get("erasure", False),
            uncertain=g.get("uncertain", False),
            notes=g.get("notes"),
        )
        for g in raw["side_b"]["groups"]
    ]

    return DiscCorpus(
        source_id=meta["source_id"],
        reading_direction=meta["reading_direction"],
        signs_catalogue=signs,
        side_a=DiscSide(side="A", groups=side_a_groups),
        side_b=DiscSide(side="B", groups=side_b_groups),
    )
