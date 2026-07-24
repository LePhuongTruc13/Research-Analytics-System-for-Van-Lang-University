import itertools

import networkx as nx
import pandas as pd

# ============================================================
# FUNCTION: BUILD COLLABORATION GRAPH
# ============================================================
def build_collaboration_graph(
    papers_df: pd.DataFrame,
    authors_df: pd.DataFrame,
    paper_author_df: pd.DataFrame
) -> dict:
   
    # ========================================================
    # CHECK REQUIRED COLUMNS
    # ========================================================
    if "paper_id" not in papers_df.columns:
        raise ValueError(
            "Không tìm thấy column 'paper_id' trong papers dataframe."
        )

    required_author_columns = {
        "author_id",
        "author_name"
    }

    missing_author_columns = (
        required_author_columns
        - set(authors_df.columns)
    )

    if missing_author_columns:
        raise ValueError(
            f"Thiếu column trong authors dataframe: "
            f"{missing_author_columns}"
        )

    required_paper_author_columns = {
        "paper_id",
        "author_id"
    }

    missing_columns = (
        required_paper_author_columns
        - set(paper_author_df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Thiếu column trong paper_author dataframe: "
            f"{missing_columns}"
        )

    # ========================================================
    # CREATE GRAPH
    # ========================================================
    graph = nx.Graph()

    # ========================================================
    # GET FILTERED PAPER IDS
    # ========================================================
    filtered_paper_ids = set(
        papers_df["paper_id"]
    )

    # ========================================================
    # FILTER PAPER_AUTHOR
    # ========================================================
    filtered_paper_author = paper_author_df[
        paper_author_df["paper_id"].isin(
            filtered_paper_ids
        )
    ].copy()

    filtered_paper_author.reset_index(
        drop=True,
        inplace=True
    )

    # ========================================================
    # GROUP AUTHORS BY PAPER
    # ========================================================
    grouped_authors = (
        filtered_paper_author
        .groupby("paper_id")["author_id"]
        .apply(list)
    )

    # ========================================================
    # ADD AUTHORS TO GRAPH
    # ========================================================
    # Lấy toàn bộ author xuất hiện sau khi filter
    filtered_author_ids = set(
        filtered_paper_author["author_id"]
    )

    # Lấy thông tin author
    filtered_authors = authors_df[
        authors_df["author_id"].isin(
            filtered_author_ids
        )
    ].copy()

    # ========================================================
    # ADD NODES
    # ========================================================
    for _, author in filtered_authors.iterrows():

        graph.add_node(

            author["author_id"],

            label=author["author_name"]

        )

    # ========================================================
    # BUILD EDGES
    # ========================================================
    for author_list in grouped_authors:

        # ----------------------------------------------------
        # Loại bỏ author bị trùng (nếu có)
        # ----------------------------------------------------

        author_list = list(
            dict.fromkeys(author_list)
        )

        # ----------------------------------------------------
        # Paper chỉ có 1 author
        # ----------------------------------------------------

        if len(author_list) == 1:

            graph.add_node(
                author_list[0]
            )

            continue

        # ----------------------------------------------------
        # Sinh toàn bộ cặp author
        # ----------------------------------------------------
        for source, target in itertools.combinations(
            author_list,
            2
        ):

            # Nếu edge đã tồn tại
            if graph.has_edge(
                source,
                target
            ):

                graph[source][target]["weight"] += 1

            # Edge mới
            else:

                graph.add_edge(

                    source,

                    target,

                    weight=1

                )

    # ========================================================
    # CALCULATE CENTRALITY
    # ========================================================
    raw_degree = dict(graph.degree())

    degree_centrality = nx.degree_centrality(
        graph
    )

    betweenness = nx.betweenness_centrality(

        graph,

        weight="weight"

    )

    closeness = nx.closeness_centrality(
        graph,
        distance="weight"
    )   

    pagerank = nx.pagerank(

        graph,

        weight="weight"

    )

    # ========================================================
    # LIMIT TOP-N NODES (tránh graph quá nặng)
    # ========================================================

    MAX_NODES = 20

    if graph.number_of_nodes() > MAX_NODES:
        top_degree_ids = sorted(
            degree_centrality,
            key=degree_centrality.get,
            reverse=True
        )[:MAX_NODES]

        top_betweenness_ids = sorted(
            betweenness,
            key=betweenness.get,
            reverse=True
        )[:3]

        top_node_ids = list(
            dict.fromkeys(top_degree_ids + top_betweenness_ids)
        )

        graph = graph.subgraph(
            top_node_ids
        ).copy()

    # ========================================================
    # BUILD NODE LIST
    # ========================================================
    nodes = []

    for node_id in graph.nodes():

        # ---------------------------------------------
        # Lấy tên tác giả
        # ---------------------------------------------

        author = filtered_authors[
            filtered_authors["author_id"] == node_id
        ]

        if author.empty:
            author_name = None
        else:
            author_name = author.iloc[0]["author_name"]

        nodes.append(

            {

                "id": node_id,

                "label": author_name,

                "collab_count": raw_degree.get(
                    node_id,
                    0
                ),

                "degree": degree_centrality.get(
                    node_id,
                    0
                ),

                "betweenness": betweenness.get(
                    node_id,
                    0
                ),

                "closeness": closeness.get(
                    node_id,
                    0
                ),

                "pagerank": pagerank.get(
                    node_id,
                    0
                )

            }

        )

    # ========================================================
    # BUILD EDGE LIST
    # ========================================================

    edges = []

    for source, target, data in graph.edges(data=True):

        edges.append(

            {

                "source": source,

                "target": target,

                "weight": data.get(
                    "weight",
                    1
                )

            }

        )

    # ========================================================
    # ADD RANKING (top cầu nối, top ảnh hưởng...)
    # ========================================================

    def add_rank(nodes_list, key, rank_key):
        sorted_nodes = sorted(
            nodes_list,
            key=lambda n: n[key],
            reverse=True
        )
        for idx, n in enumerate(sorted_nodes):
            n[rank_key] = idx + 1

    add_rank(nodes, "betweenness", "betweenness_rank")
    add_rank(nodes, "pagerank", "pagerank_rank")
    add_rank(nodes, "closeness", "closeness_rank")
    add_rank(nodes, "collab_count", "degree_rank")

    # ========================================================
    # CONVERT NaN -> None
    # ========================================================

    nodes = (
        pd.DataFrame(nodes)
        .astype(object)
        .where(
            pd.notnull(pd.DataFrame(nodes)),
            None
        )
        .to_dict("records")
    )

    edges = (
        pd.DataFrame(edges)
        .astype(object)
        .where(
            pd.notnull(pd.DataFrame(edges)),
            None
        )
        .to_dict("records")
    )

    # ========================================================
    # RETURN GRAPH
    # ========================================================

    return {

        "nodes": nodes,

        "edges": edges

    }

