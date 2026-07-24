import sys
from pathlib import Path

import networkx as nx
import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.networkx.build_graph import build_graph


# ==========================================================
# Compute Centrality Metrics
# ==========================================================

def compute_centrality():
    """
    Compute centrality metrics for the author collaboration graph.

    Returns
    -------
    pandas.DataFrame

        Columns
        -------
        author_id
        degree
        betweenness
        closeness
        pagerank
    """

    G = build_graph()

    print()
    print("=" * 70)
    print("CENTRALITY ANALYSIS".center(70))
    print("=" * 70)

    # ======================================================
    # Degree Centrality
    # ======================================================

    print("Computing Degree Centrality...")

    degree = nx.degree_centrality(G)

    # ======================================================
    # Betweenness Centrality
    # ======================================================

    print("Computing Betweenness Centrality...")

    betweenness = nx.betweenness_centrality(
        G,
        weight="weight"
    )

    # ======================================================
    # Closeness Centrality
    # ======================================================

    print("Computing Closeness Centrality...")

    closeness = nx.closeness_centrality(G)

    # ======================================================
    # PageRank
    # ======================================================

    print("Computing PageRank...")

    pagerank = nx.pagerank(
        G,
        weight="weight"
    )

    # ======================================================
    # Build DataFrame
    # ======================================================

    metrics = pd.DataFrame({

        "author_id": list(G.nodes()),

        "degree": [
            degree[node]
            for node in G.nodes()
        ],

        "betweenness": [
            betweenness[node]
            for node in G.nodes()
        ],

        "closeness": [
            closeness[node]
            for node in G.nodes()
        ],

        "pagerank": [
            pagerank[node]
            for node in G.nodes()
        ]

    })

    print()

    print(f"Computed metrics for {len(metrics)} authors.")

    return metrics


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    metrics = compute_centrality()

    print()

    print(metrics.head())