"""Unit tests for cross-script phylogenetic network and typological distance."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.comparative.script_network import compute_script_phylogenetic_network
from phaistos.comparative.models import ScriptNetworkResult


def test_script_phylogenetic_network():
    corpus = load_transcription("godart_1995")
    result = compute_script_phylogenetic_network(corpus)

    assert isinstance(result, ScriptNetworkResult)
    assert len(result.scripts_analyzed) == 4
    assert "Phaistos_Disc" in result.scripts_analyzed
    assert "Cretan_Hieroglyphic" in result.scripts_analyzed
    assert "Linear_A" in result.scripts_analyzed
    assert "Arkalochori_Axe" in result.scripts_analyzed

    # Check pairwise distances exist
    assert "Phaistos_Disc__Cretan_Hieroglyphic" in result.pairwise_distances
    assert "Phaistos_Disc__Linear_A" in result.pairwise_distances
    assert "Phaistos_Disc__Arkalochori_Axe" in result.pairwise_distances

    # Distance to Cretan Hieroglyphic is significantly closer than to Linear A
    d_ch = result.pairwise_distances["Phaistos_Disc__Cretan_Hieroglyphic"].composite_phylogenetic_distance
    d_la = result.pairwise_distances["Phaistos_Disc__Linear_A"].composite_phylogenetic_distance
    assert d_ch < d_la

    # Nearest neighbor
    assert result.nearest_neighbor_to_phaistos == "Cretan_Hieroglyphic"
    assert result.hieroglyphic_affinity_z > 3.0
    assert "SCRIPT PHYLOGENY SYNTHESIS" in result.skeptic_verdict
