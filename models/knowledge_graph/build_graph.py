import sys
from pathlib import Path

import networkx as nx

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.knowledge_graph.load_data import load_data


# ==========================================================
# Build Knowledge Graph
# ==========================================================

def build_graph():
    """
    Build Knowledge Graph.

    Nodes
    -----
    Author
    Paper
    Institution
    Topic

    Relationships
    -------------
    Author -------- WRITES --------> Paper
    Author --- AFFILIATED_WITH ----> Institution
    Paper ----- BELONGS_TO --------> Topic
    """

    (
        papers,
        authors,
        institutions,
        paper_author,
        author_institution,
        paper_topic,
        topics
    ) = load_data()

    G = nx.MultiDiGraph()

    # ======================================================
    # Author Nodes
    # ======================================================

    for _, row in authors.iterrows():

        G.add_node(
            row.author_id,
            node_type="Author",
            name=row.author_name
        )

    # ======================================================
    # Paper Nodes
    # ======================================================

    for _, row in papers.iterrows():

        G.add_node(
            row.paper_id,
            node_type="Paper",
            name=row.title
        )

    # ======================================================
    # Institution Nodes
    # ======================================================

    for _, row in institutions.iterrows():

        G.add_node(
            row.institution_id,
            node_type="Institution",
            name=row.institution_name
        )

    # ======================================================
    # Topic Nodes
    # ======================================================

    for _, row in topics.iterrows():

        G.add_node(
            row.topic_id,
            node_type="Topic",
            name=row.topic_name
        )

    # ======================================================
    # Author -> Paper
    # ======================================================

    for _, row in paper_author.iterrows():

        G.add_edge(
            row.author_id,
            row.paper_id,
            relationship="WRITES"
        )

    # ======================================================
    # Author -> Institution
    # ======================================================

    for _, row in author_institution.iterrows():

        G.add_edge(
            row.author_id,
            row.institution_id,
            relationship="AFFILIATED_WITH"
        )

    # ======================================================
    # Paper -> Topic
    # ======================================================

    for _, row in paper_topic.iterrows():

        G.add_edge(
            row.paper_id,
            row.topic_id,
            relationship="BELONGS_TO"
        )

    # ======================================================
    # Summary
    # ======================================================

    print("=" * 70)
    print("KNOWLEDGE GRAPH".center(70))
    print("=" * 70)

    print(f"Nodes : {G.number_of_nodes()}")
    print(f"Edges : {G.number_of_edges()}")

    print()

    return G


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    G = build_graph()

    print("First 10 Nodes")
    print("-" * 40)

    for node, data in list(G.nodes(data=True))[:10]:

        print(node, data)

    print()

    print("First 10 Relationships")
    print("-" * 40)

    for u, v, data in list(G.edges(data=True))[:10]:

        print(u, "->", v, data)

    print()
    print("First 10 BELONGS_TO Relationships")
    print("-" * 40)

    count = 0

    for u, v, data in G.edges(data=True):

        if data["relationship"] == "BELONGS_TO":

            print(u, "->", v, data)

            count += 1

            if count == 10:
                break