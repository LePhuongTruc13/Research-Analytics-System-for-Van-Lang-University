import pandas as pd


# ==========================================================
# GET KNOWLEDGE GRAPH
# ==========================================================
def get_knowledge_graph(
    knowledge_graph: dict,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extract all nodes and edges.

    Parameters
    ----------
    knowledge_graph : dict

    Returns
    -------
    nodes_df
    edges_df
    """

    nodes_df = pd.DataFrame(

        knowledge_graph.get(
            "nodes",
            []
        )

    )

    edges_df = pd.DataFrame(

        knowledge_graph.get(
            "edges",
            []
        )

    )

    return (
        nodes_df,
        edges_df,
    )


# ==========================================================
# BUILD AUTHOR GRAPH
# ==========================================================
def build_author_graph(
    knowledge_graph: dict,
    author_id: str,
    max_papers: int = 5,
) -> dict:
    """
    Build graph for one author.

    Graph Structure

    Author
        │
        ├── Institution
        ├── Paper
        └── Topic

    Parameters
    ----------
    knowledge_graph : dict

    author_id : str

    max_papers : int

    Returns
    -------
    dict
    """

    nodes_df, edges_df = get_knowledge_graph(
        knowledge_graph
    )

    # ======================================================
    # RESULT
    # ======================================================

    result_nodes = []

    result_edges = []

    node_ids = set()

    # ======================================================
    # AUTHOR NODE
    # ======================================================

    author_node = nodes_df[
        nodes_df["id"] == author_id
    ]

    if author_node.empty:

        return {
            "nodes": [],
            "edges": []
        }

    result_nodes.extend(

        author_node.to_dict(
            "records"
        )

    )

    node_ids.add(author_id)

    # ======================================================
    # PAPERS
    # ======================================================

    paper_edges = edges_df[

        (edges_df["source"] == author_id)

        &

        (
            edges_df["relationship"]
            == "WRITES"
        )

    ].head(max_papers)

    result_edges.extend(

        paper_edges.to_dict(
            "records"
        )

    )

    paper_ids = list(

        paper_edges["target"]

    )

    if len(paper_ids):

        paper_nodes = nodes_df[

            nodes_df["id"].isin(
                paper_ids
            )

        ]

        result_nodes.extend(

            paper_nodes.to_dict(
                "records"
            )

        )

        node_ids.update(

            paper_ids

        )

    # ======================================================
    # INSTITUTION
    # ======================================================

    institution_edges = edges_df[

        (edges_df["source"] == author_id)

        &

        (
            edges_df["relationship"]
            ==
            "AFFILIATED_WITH"
        )

    ]

    result_edges.extend(

        institution_edges.to_dict(
            "records"
        )

    )

    institution_ids = list(

        institution_edges["target"]

    )

    if len(institution_ids):

        institution_nodes = nodes_df[

            nodes_df["id"].isin(
                institution_ids
            )

        ]

        result_nodes.extend(

            institution_nodes.to_dict(
                "records"
            )

        )

        node_ids.update(

            institution_ids

        )

    # ======================================================
    # TOPICS
    # ======================================================

    if len(paper_ids):

        topic_edges = edges_df[

            edges_df["source"].isin(
                paper_ids
            )

            &

            (
                edges_df["relationship"]
                ==
                "BELONGS_TO"
            )

        ]

        result_edges.extend(

            topic_edges.to_dict(
                "records"
            )

        )

        topic_ids = list(

            topic_edges["target"]

        )

        if len(topic_ids):

            topic_nodes = nodes_df[

                nodes_df["id"].isin(
                    topic_ids
                )

            ]

            result_nodes.extend(

                topic_nodes.to_dict(
                    "records"
                )

            )

            node_ids.update(

                topic_ids

            )

    # ======================================================
    # REMOVE DUPLICATES
    # ======================================================

    result_nodes = (

        pd.DataFrame(
            result_nodes
        )

        .drop_duplicates(
            subset="id"
        )

        .to_dict(
            "records"
        )

    )

    result_edges = (

        pd.DataFrame(
            result_edges
        )

        .drop_duplicates()

        .to_dict(
            "records"
        )

    )

    return {

        "nodes": result_nodes,

        "edges": result_edges,

    }
