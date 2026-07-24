import pandas as pd
import sys
from pathlib import Path

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import TRANSFORMED_DATA_DIR
from utils.path import BERTOPIC_RESULT_DIR


# ==========================================================
# Config
# ==========================================================

PAPER_FILE = TRANSFORMED_DATA_DIR / "papers.csv"
AUTHOR_FILE = TRANSFORMED_DATA_DIR / "authors.csv"
INSTITUTION_FILE = TRANSFORMED_DATA_DIR / "institutions.csv"

PAPER_AUTHOR_FILE = TRANSFORMED_DATA_DIR / "paper_author.csv"
AUTHOR_INSTITUTION_FILE = TRANSFORMED_DATA_DIR / "author_institution.csv"

PAPER_TOPIC_FILE = BERTOPIC_RESULT_DIR / "paper_topic.csv"
TOPIC_FILE = BERTOPIC_RESULT_DIR / "topics_update.csv"


# ==========================================================
# Load Data
# ==========================================================

def load_data():
    """
    Load datasets for Knowledge Graph.

    Returns
    -------
    tuple
        (
            papers,
            authors,
            institutions,
            paper_author,
            author_institution,
            paper_topic,
            topics
        )
    """

    papers = pd.read_csv(PAPER_FILE)[
        [
            "paper_id",
            "title"
        ]
    ]

    authors = pd.read_csv(AUTHOR_FILE)[
        [
            "author_id",
            "author_name"
        ]
    ]

    institutions = pd.read_csv(INSTITUTION_FILE)[
        [
            "institution_id",
            "institution_name"
        ]
    ]

    paper_author = pd.read_csv(PAPER_AUTHOR_FILE)[
        [
            "paper_id",
            "author_id"
        ]
    ]

    author_institution = pd.read_csv(AUTHOR_INSTITUTION_FILE)[
        [
            "author_id",
            "institution_id"
        ]
    ]

    paper_topic = pd.read_csv(PAPER_TOPIC_FILE)[
        [
            "paper_id",
            "topic_id"
        ]
    ]

    topics = pd.read_csv(TOPIC_FILE)[
        [
            "topic_id",
            "topic_name"
        ]
    ]

    print("=" * 70)
    print("KNOWLEDGE GRAPH DATA".center(70))
    print("=" * 70)

    print(f"Papers               : {len(papers)}")
    print(f"Authors              : {len(authors)}")
    print(f"Institutions         : {len(institutions)}")
    print(f"Paper-Author         : {len(paper_author)}")
    print(f"Author-Institution   : {len(author_institution)}")
    print(f"Paper-Topic          : {len(paper_topic)}")
    print(f"Topics               : {len(topics)}")

    print()

    return (
        papers,
        authors,
        institutions,
        paper_author,
        author_institution,
        paper_topic,
        topics
    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    (
        papers,
        authors,
        institutions,
        paper_author,
        author_institution,
        paper_topic,
        topics
    ) = load_data()

    print(papers.head())