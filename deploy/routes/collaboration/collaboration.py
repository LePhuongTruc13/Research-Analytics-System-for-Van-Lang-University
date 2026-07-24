import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================
# IMPORT DATA LOADERS
# ============================================================
from deploy.load_data.load_papers import load_papers
from deploy.load_data.load_topics import load_topics
from deploy.load_data.load_network import load_network
from deploy.load_data.load_authors import load_authors
from deploy.load_data.load_paper_topic import load_paper_topic
from deploy.load_data.load_paper_author import load_paper_author

from deploy.routes.collaboration.collaboration_filter_year import (
    filter_papers_by_year
)

from deploy.routes.collaboration.collaboration_filter_topic import (
    filter_papers_by_topic
)

from deploy.routes.collaboration.collaboration_graph import (
    build_collaboration_graph
)

# ============================================================
# LOAD ALL DATA
# ============================================================
# ============================================================
# LOAD ALL DATA (cache — chỉ load 1 lần)
# ============================================================
_cached_data = None

def load_collaboration_data():
    global _cached_data

    if _cached_data is not None:
        return _cached_data

    _cached_data = {

        "papers": load_papers(),

        "topics": load_topics(),

        "network": load_network(),

        "authors": load_authors(),

        "paper_topic": load_paper_topic(),

        "paper_author": load_paper_author()

    }

    return _cached_data

# ============================================================
# GET COLLABORATION GRAPH
# ============================================================

def get_collaboration_graph(
    year: int = None,
    topic_id: int = None
):
    
    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------
    data = load_collaboration_data()

    papers_df = data["papers"]

    # --------------------------------------------------------
    # FILTER BY YEAR
    # --------------------------------------------------------
    if year is not None:

        papers_df = filter_papers_by_year(

            papers_df,

            year

        )

    # --------------------------------------------------------
    # FILTER BY TOPIC
    # --------------------------------------------------------
    if topic_id is not None:

        papers_df = filter_papers_by_topic(

            papers_df,

            data["paper_topic"],

            topic_id

        )

    # --------------------------------------------------------
    # BUILD GRAPH
    # --------------------------------------------------------
    graph = build_collaboration_graph(

        papers_df,

        data["authors"],

        data["paper_author"]

    )

    return graph