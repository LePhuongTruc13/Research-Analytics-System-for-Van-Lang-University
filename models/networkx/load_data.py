import pandas as pd
import sys
from pathlib import Path

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import TRANSFORMED_DATA_DIR


# ==========================================================
# Config
# ==========================================================

AUTHOR_FILE = TRANSFORMED_DATA_DIR / "authors.csv"
PAPER_AUTHOR_FILE = TRANSFORMED_DATA_DIR / "paper_author.csv"


# ==========================================================
# Load Data
# ==========================================================

def load_data():
    """
    Load data for Author Collaboration Network.

    Returns
    -------
    authors : pandas.DataFrame
        Columns:
            - author_id
            - author_name

    paper_author : pandas.DataFrame
        Columns:
            - paper_id
            - author_id
    """

    authors = pd.read_csv(AUTHOR_FILE)

    authors = authors[
        [
            "author_id",
            "author_name"
        ]
    ]

    paper_author = pd.read_csv(PAPER_AUTHOR_FILE)

    paper_author = paper_author[
        [
            "paper_id",
            "author_id"
        ]
    ]

    print(f"Loaded {len(authors)} authors.")
    print(f"Loaded {len(paper_author)} paper-author relationships.")

    return authors, paper_author


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    authors, paper_author = load_data()

    print()

    print("Authors")
    print(authors.head())

    print()

    print("Paper-Author")
    print(paper_author.head())