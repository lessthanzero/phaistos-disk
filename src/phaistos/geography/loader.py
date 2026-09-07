"""Loader for Minoan archaeological geography datasets."""

from pathlib import Path
from typing import Optional
import yaml

from phaistos.geography.models import MessaraNetwork, MinoanRoute, MinoanSite
from phaistos.corpus.loader import get_default_corpus_dir


def load_messara_network(corpus_dir: Optional[Path] = None) -> MessaraNetwork:
    """Load the archaeological regional network of South-Central Crete centered on Phaistos."""
    base_dir = corpus_dir or get_default_corpus_dir()
    file_path = base_dir / "geography" / "messara_network.yaml"
    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    meta = raw["metadata"]
    sites = [MinoanSite(**s) for s in raw["sites"]]
    routes = [MinoanRoute(**r) for r in raw["routes"]]

    return MessaraNetwork(
        region=meta["region"],
        hub_site=meta["hub_site"],
        period=meta["period"],
        description=meta["description"],
        sites=sites,
        routes=routes,
    )
