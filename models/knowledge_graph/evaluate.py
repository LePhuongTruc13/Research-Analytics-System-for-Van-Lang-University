import sys
from pathlib import Path

import networkx as nx

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.knowledge_graph.build_graph import build_graph


# ==========================================================
# Evaluate Knowledge Graph
# ==========================================================

def evaluate_graph():
    """
    Evaluate Knowledge Graph.
    """

    G = build_graph()

    # ======================================================
    # Node Statistics
    # ======================================================

    node_types = nx.get_node_attributes(
        G,
        "node_type"
    )

    author_count = sum(

        t == "Author"

        for t in node_types.values()

    )

    paper_count = sum(

        t == "Paper"

        for t in node_types.values()

    )

    institution_count = sum(

        t == "Institution"

        for t in node_types.values()

    )

    topic_count = sum(

        t == "Topic"

        for t in node_types.values()

    )

    # ======================================================
    # Relationship Statistics
    # ======================================================

    writes = 0
    affiliated = 0
    belongs = 0

    for _, _, data in G.edges(data=True):

        relationship = data["relationship"]

        if relationship == "WRITES":
            writes += 1

        elif relationship == "AFFILIATED_WITH":
            affiliated += 1

        elif relationship == "BELONGS_TO":
            belongs += 1

    # ======================================================
    # Graph Statistics
    # ======================================================

    undirected = G.to_undirected()

    density = nx.density(
        undirected
    )

    average_degree = (

        sum(dict(undirected.degree()).values())

        / undirected.number_of_nodes()

    )

    connected_components = nx.number_connected_components(
        undirected
    )

    # ======================================================
    # Summary
    # ======================================================

    print("=" * 70)
    print("KNOWLEDGE GRAPH EVALUATION".center(70))
    print("=" * 70)

    print()
    print("Node Statistics")
    print("-" * 40)

    print(f"Authors          : {author_count}")
    print(f"Papers           : {paper_count}")
    print(f"Institutions     : {institution_count}")
    print(f"Topics           : {topic_count}")

    print()

    print("Relationship Statistics")
    print("-" * 40)

    print(f"WRITES           : {writes}")
    print(f"AFFILIATED_WITH  : {affiliated}")
    print(f"BELONGS_TO       : {belongs}")

    print()

    print("Graph Statistics")
    print("-" * 40)

    print(f"Nodes            : {G.number_of_nodes()}")
    print(f"Edges            : {G.number_of_edges()}")

    print(f"Average Degree   : {average_degree:.2f}")
    print(f"Density          : {density:.6f}")

    print(f"Components       : {connected_components}")

    print()
    print("Knowledge Graph evaluation completed.")

    return G


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    evaluate_graph()