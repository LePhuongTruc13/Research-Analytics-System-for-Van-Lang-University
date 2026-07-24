import sys
from pathlib import Path

import networkx as nx

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.networkx.build_graph import build_graph


# ==========================================================
# Evaluate Graph
# ==========================================================

def evaluate_graph():
    """
    Evaluate the author collaboration network.
    """

    G = build_graph()

    print("=" * 70)
    print("NETWORK ANALYSIS EVALUATION".center(70))
    print("=" * 70)

    # ------------------------------------------------------
    # Basic Statistics
    # ------------------------------------------------------

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    density = nx.density(G)

    avg_degree = (
        sum(dict(G.degree()).values())
        / num_nodes
    )

    avg_clustering = nx.average_clustering(
        G,
        weight="weight"
    )

    # ------------------------------------------------------
    # Connected Components
    # ------------------------------------------------------

    connected_components = list(
        nx.connected_components(G)
    )

    num_components = len(connected_components)

    largest_component = max(
        connected_components,
        key=len
    )

    largest_size = len(largest_component)

    # ------------------------------------------------------
    # Largest Connected Subgraph
    # ------------------------------------------------------

    largest_graph = G.subgraph(
        largest_component
    ).copy()

    if nx.is_connected(largest_graph):

        diameter = nx.diameter(largest_graph)

        avg_shortest_path = nx.average_shortest_path_length(
            largest_graph
        )

    else:

        diameter = "N/A"
        avg_shortest_path = "N/A"

    # ------------------------------------------------------
    # Print Results
    # ------------------------------------------------------

    print(f"Number of Nodes                 : {num_nodes}")
    print(f"Number of Edges                 : {num_edges}")
    print(f"Density                         : {density:.6f}")
    print(f"Connected Components            : {num_components}")
    print(f"Largest Component               : {largest_size}")
    print(f"Average Degree                  : {avg_degree:.2f}")
    print(f"Average Clustering Coefficient  : {avg_clustering:.4f}")
    print(f"Diameter (Largest Component)    : {diameter}")

    if isinstance(avg_shortest_path, float):
        print(f"Average Shortest Path Length    : {avg_shortest_path:.4f}")
    else:
        print(f"Average Shortest Path Length    : {avg_shortest_path}")

    print()
    print("Network evaluation completed.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    evaluate_graph()