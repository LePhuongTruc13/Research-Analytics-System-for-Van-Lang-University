import sys
import json
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.knowledge_graph.build_graph import build_graph
from utils.path import KNOWLEDGE_GRAPH_RESULT_DIR


# ==========================================================
# Config
# ==========================================================

NODE_OUTPUT = KNOWLEDGE_GRAPH_RESULT_DIR / "kg_nodes.csv"
EDGE_OUTPUT = KNOWLEDGE_GRAPH_RESULT_DIR / "kg_edges.csv"

JSON_OUTPUT = KNOWLEDGE_GRAPH_RESULT_DIR / "knowledge_graph.json"


# ==========================================================
# Export Knowledge Graph
# ==========================================================

def export_graph():
    """
    Export Knowledge Graph.

    Input
    -----
    build_graph()

    Output
    ------
    kg_nodes.csv
        - node_id
        - node_type
        - node_name

    kg_edges.csv
        - source
        - target
        - relationship

    knowledge_graph.json
        - nodes
        - edges
    """

    G = build_graph()

    # ======================================================
    # Export Nodes
    # ======================================================

    nodes = []

    for node_id, data in G.nodes(data=True):

        nodes.append({

            "node_id": node_id,

            "node_type": data.get("node_type"),

            "node_name": data.get("name")

        })

    nodes_df = pd.DataFrame(nodes)

    nodes_df.to_csv(
        NODE_OUTPUT,
        index=False
    )

    # ======================================================
    # Export Edges
    # ======================================================

    edges = []

    for source, target, data in G.edges(data=True):

        edges.append({

            "source": source,

            "target": target,

            "relationship": data.get("relationship")

        })

    edges_df = pd.DataFrame(edges)

    edges_df.to_csv(
        EDGE_OUTPUT,
        index=False
    )

    # ======================================================
    # Export JSON
    # ======================================================

    json_data = {

        "nodes": [

            {

                "id": row["node_id"],

                "type": row["node_type"],

                "label": row["node_name"]

            }

            for _, row in nodes_df.iterrows()

        ],

        "edges": [

            {

                "source": row["source"],

                "target": row["target"],

                "relationship": row["relationship"]

            }

            for _, row in edges_df.iterrows()

        ]

    }

    with open(
        JSON_OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            json_data,
            f,
            ensure_ascii=False,
            indent=4
        )

    # ======================================================
    # Summary
    # ======================================================

    print("=" * 70)
    print("KNOWLEDGE GRAPH EXPORT".center(70))
    print("=" * 70)

    print(f"Nodes Exported : {len(nodes_df)}")
    print(f"Edges Exported : {len(edges_df)}")

    print()

    print("Saved Files")
    print(f"✔ {NODE_OUTPUT}")
    print(f"✔ {EDGE_OUTPUT}")
    print(f"✔ {JSON_OUTPUT}")

    return nodes_df, edges_df


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    export_graph()