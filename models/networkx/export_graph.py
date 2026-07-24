import sys
import json
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import NETWORKX_RESULT_DIR
from models.networkx.load_data import load_data
from models.networkx.build_graph import build_graph
from models.networkx.centrality import compute_centrality


# ==========================================================
# Config
# ==========================================================

AUTHOR_NODE_FILE = NETWORKX_RESULT_DIR / "author_nodes.csv"
AUTHOR_EDGE_FILE = NETWORKX_RESULT_DIR / "author_edges.csv"
AUTHOR_METRIC_FILE = NETWORKX_RESULT_DIR / "author_metrics.csv"

NETWORK_JSON_FILE = NETWORKX_RESULT_DIR / "network.json"


# ==========================================================
# Export Graph
# ==========================================================

def export_graph():
    """
    Export network analysis results.

    Output
    ------
    author_nodes.csv
        author_id
        author_name

    author_edges.csv
        source
        target
        weight

    author_metrics.csv
        author_id
        degree
        betweenness
        closeness
        pagerank

    network.json
        nodes
        edges
    """

    print("=" * 70)
    print("EXPORT GRAPH".center(70))
    print("=" * 70)

    # ------------------------------------------------------
    # Load data
    # ------------------------------------------------------

    authors, _ = load_data()

    # ------------------------------------------------------
    # Build graph
    # ------------------------------------------------------

    G = build_graph()

    # ------------------------------------------------------
    # Centrality metrics
    # ------------------------------------------------------

    metrics = compute_centrality()

    # ------------------------------------------------------
    # Author Nodes
    # ------------------------------------------------------

    author_nodes = authors.copy()

    author_nodes = author_nodes[
        [
            "author_id",
            "author_name"
        ]
    ]

    author_nodes.to_csv(
        AUTHOR_NODE_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ------------------------------------------------------
    # Author Edges
    # ------------------------------------------------------

    edges = []

    for source, target, data in G.edges(data=True):

        edges.append({

            "source": source,
            "target": target,
            "weight": data["weight"]

        })

    author_edges = pd.DataFrame(edges)

    author_edges.to_csv(
        AUTHOR_EDGE_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ------------------------------------------------------
    # Author Metrics
    # ------------------------------------------------------

    metrics = metrics.sort_values(
        by="pagerank",
        ascending=False
    )

    metrics.to_csv(
        AUTHOR_METRIC_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    # ------------------------------------------------------
    # network.json
    # ------------------------------------------------------

    metric_map = metrics.set_index("author_id").to_dict("index")

    nodes = []

    for _, row in author_nodes.iterrows():

        author_id = row["author_id"]

        node = {

            "id": author_id,
            "label": row["author_name"],
            "degree": metric_map.get(author_id, {}).get("degree", 0),
            "betweenness": metric_map.get(author_id, {}).get("betweenness", 0),
            "closeness": metric_map.get(author_id, {}).get("closeness", 0),
            "pagerank": metric_map.get(author_id, {}).get("pagerank", 0)

        }

        nodes.append(node)

    json_data = {

        "nodes": nodes,

        "edges": edges

    }

    with open(
        NETWORK_JSON_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            json_data,
            f,
            ensure_ascii=False,
            indent=4
        )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print(f"Author Nodes   : {len(author_nodes)}")
    print(f"Author Edges   : {len(author_edges)}")
    print(f"Author Metrics : {len(metrics)}")

    print()
    print("Export completed.")

    print("Saved:")

    print(f"  - {AUTHOR_NODE_FILE}")
    print(f"  - {AUTHOR_EDGE_FILE}")
    print(f"  - {AUTHOR_METRIC_FILE}")
    print(f"  - {NETWORK_JSON_FILE}")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    export_graph()