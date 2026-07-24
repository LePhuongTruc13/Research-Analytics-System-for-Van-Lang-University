import sys
from pathlib import Path
from itertools import combinations

import networkx as nx

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.networkx.load_data import load_data


# ==========================================================
# Build Author Collaboration Graph
# ==========================================================

def build_graph():
    """
    Build an author collaboration graph.

    Node
    ----
    author_id

    Edge
    ----
    Two authors have co-authored at least one paper.

    Edge Weight
    -----------
    Number of co-authored papers.
    """

    _, paper_author = load_data()

    G = nx.Graph()

    # ======================================================
    # Group authors by paper
    # ======================================================

    grouped = (
        paper_author
        .groupby("paper_id")["author_id"]
        .apply(list)
    )

    # ======================================================
    # Build graph
    # ======================================================

    for authors in grouped:

        # Remove duplicate author ids
        authors = list(set(authors))

        # Single-author paper
        if len(authors) == 1:

            G.add_node(authors[0])

            continue

        # Multi-author paper
        for author1, author2 in combinations(authors, 2):

            if G.has_edge(author1, author2):

                G[author1][author2]["weight"] += 1

            else:

                G.add_edge(
                    author1,
                    author2,
                    weight=1
                )

    print("=" * 70)
    print("AUTHOR COLLABORATION GRAPH".center(70))
    print("=" * 70)

    print(f"Nodes : {G.number_of_nodes()}")
    print(f"Edges : {G.number_of_edges()}")

    return G


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    graph = build_graph()

    print()

    print("First 10 Edges")

    for edge in list(graph.edges(data=True))[:10]:

        print(edge)