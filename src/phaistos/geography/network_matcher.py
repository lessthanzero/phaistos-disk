"""Graph-theoretic matcher comparing Phaistos Disc transitions to the Messara regional network."""

import math
import random
from typing import Dict, List, Tuple
import networkx as nx
import numpy as np

from phaistos.core.models import DiscCorpus
from phaistos.geography.models import MessaraNetwork


def build_messara_network_graph(network: MessaraNetwork) -> nx.Graph:
    """Construct an undirected weighted NetworkX graph of the Minoan Messara regional network."""
    g = nx.Graph()
    for site in network.sites:
        g.add_node(
            site.id,
            name=site.name,
            type=site.type,
            elevation=site.elevation_m,
            distance_km=site.distance_km,
            azimuth_deg=site.azimuth_deg,
            prominence=site.prominence_rank,
        )

    for route in network.routes:
        g.add_edge(
            route.from_site,
            route.to_site,
            id=route.id,
            name=route.name,
            weight=route.distance_km,
            type=route.type,
        )

    return g


def build_disc_group_transition_graph(corpus: DiscCorpus) -> nx.DiGraph:
    """Construct directed graph of group-to-group sequential transitions on the Disc."""
    g = nx.DiGraph()
    groups = corpus.all_groups()
    for i in range(len(groups) - 1):
        g1, g2 = groups[i], groups[i + 1]
        # Skip across sides transition if distinct
        if g1.side == g2.side:
            g.add_edge(g1.id, g2.id)
    return g


def build_disc_sign_cooccurrence_graph(corpus: DiscCorpus) -> nx.Graph:
    """Construct undirected graph where signs are nodes and edges represent co-occurrence in the same group."""
    g = nx.Graph()
    for group in corpus.all_groups():
        unique_signs = list(set(group.signs))
        for i in range(len(unique_signs)):
            for j in range(i + 1, len(unique_signs)):
                s1, s2 = unique_signs[i], unique_signs[j]
                if g.has_edge(s1, s2):
                    g[s1][s2]["weight"] += 1
                else:
                    g.add_edge(s1, s2, weight=1)
    return g


def compare_network_topologies(
    corpus: DiscCorpus,
    network: MessaraNetwork,
) -> Dict[str, float]:
    """
    Compare topological graph invariants between the Phaistos regional network
    and the Phaistos Disc sign co-occurrence network.
    """
    g_geo = build_messara_network_graph(network)
    g_disc = build_disc_sign_cooccurrence_graph(corpus)

    # Topological metrics
    geo_nodes = float(g_geo.number_of_nodes())
    geo_edges = float(g_geo.number_of_edges())
    geo_density = float(nx.density(g_geo))

    disc_nodes = float(g_disc.number_of_nodes())
    disc_edges = float(g_disc.number_of_edges())
    disc_density = float(nx.density(g_disc))

    # Clustering coefficients
    geo_clustering = float(nx.average_clustering(g_geo))
    disc_clustering = float(nx.average_clustering(g_disc))

    # Hub prominence: Max degree / mean degree
    geo_degrees = [d for _, d in g_geo.degree()]
    disc_degrees = [d for _, d in g_disc.degree()]

    geo_hub_ratio = float(max(geo_degrees) / np.mean(geo_degrees)) if geo_degrees else 1.0
    disc_hub_ratio = float(max(disc_degrees) / np.mean(disc_degrees)) if disc_degrees else 1.0

    return {
        "geo_sites_count": geo_nodes,
        "geo_routes_count": geo_edges,
        "geo_network_density": geo_density,
        "geo_average_clustering": geo_clustering,
        "geo_hub_prominence_ratio": geo_hub_ratio,
        "disc_sign_nodes_count": disc_nodes,
        "disc_cooccurrence_edges": disc_edges,
        "disc_network_density": disc_density,
        "disc_average_clustering": disc_clustering,
        "disc_hub_prominence_ratio": disc_hub_ratio,
    }
