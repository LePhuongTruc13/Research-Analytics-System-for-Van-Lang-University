import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# IMPORT DATA LOADERS
# ==========================================================
from deploy.load_data.load_papers import load_papers
from deploy.load_data.load_topics import load_topics
from deploy.load_data.load_authors import load_authors
from deploy.load_data.load_institution import load_institutions
from deploy.load_data.load_paper_topic import load_paper_topic
from deploy.load_data.load_paper_author import load_paper_author
from deploy.load_data.load_author_institution import load_author_institution
from deploy.load_data.load_knowledge_graph import load_knowledge_graph

# ==========================================================
# IMPORT KNOWLEDGE GRAPH MODULES
# ==========================================================
from deploy.routes.knowledge_graph.filter_author import filter_authors
from deploy.routes.knowledge_graph.graph import get_knowledge_graph
from deploy.routes.knowledge_graph.node_detail import (
    node_author,
    node_paper,
    node_topic,
    node_institution,
)

# ==========================================================
# LOAD ALL DATA
# ==========================================================
_cached_data = None


def load_knowledge_graph_data():

    global _cached_data

    if _cached_data is not None:
        return _cached_data

    # ------------------------------------------------------
    # Raw Data
    # ------------------------------------------------------

    papers = load_papers()

    topics = load_topics()

    authors = load_authors()

    institutions = load_institutions()

    paper_topic = load_paper_topic()

    paper_author = load_paper_author()

    author_institution = load_author_institution()

    knowledge_graph = load_knowledge_graph()

    # ------------------------------------------------------
    # Graph Data
    # ------------------------------------------------------

    nodes_df, edges_df = get_knowledge_graph(
        knowledge_graph
    )

    author_filter_df = filter_authors(
        authors
    )

    # ------------------------------------------------------
    # Cache
    # ------------------------------------------------------

    _cached_data = {

        # Raw Data
        "papers": papers,
        "topics": topics,
        "authors": authors,
        "institution": institutions,
        "paper_topic": paper_topic,
        "paper_author": paper_author,
        "author_institution": author_institution,
        "knowledge_graph": knowledge_graph,

        # Processed Data
        "nodes": nodes_df,
        "edges": edges_df,
        "author_filter": author_filter_df,

        # Node Detail Functions
        "node_author": node_author,
        "node_paper": node_paper,
        "node_topic": node_topic,
        "node_institution": node_institution,
    }

    return _cached_data