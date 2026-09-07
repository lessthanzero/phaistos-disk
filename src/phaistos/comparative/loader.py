"""Loaders for comparative script inventories and correspondences."""

from pathlib import Path
from typing import Dict, List, Optional
import yaml

from phaistos.comparative.models import (
    LinearASign,
    LinearBSign,
    ProposedCorrespondence,
)
from phaistos.corpus.loader import get_default_corpus_dir


def load_linear_a_signs(corpus_dir: Optional[Path] = None) -> List[LinearASign]:
    base_dir = corpus_dir or get_default_corpus_dir()
    file_path = base_dir / "comparative" / "linear_a_signs.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [LinearASign(**s) for s in raw["signs"]]


def load_linear_b_signs(corpus_dir: Optional[Path] = None) -> List[LinearBSign]:
    base_dir = corpus_dir or get_default_corpus_dir()
    file_path = base_dir / "comparative" / "linear_b_signs.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [LinearBSign(**s) for s in raw["signs"]]


def load_proposed_correspondences(corpus_dir: Optional[Path] = None) -> List[ProposedCorrespondence]:
    base_dir = corpus_dir or get_default_corpus_dir()
    file_path = base_dir / "comparative" / "correspondences.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return [ProposedCorrespondence(**c) for c in raw["correspondences"]]
