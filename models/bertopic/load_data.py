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

INPUT_FILE = TRANSFORMED_DATA_DIR / "papers.csv"


# ==========================================================
# Load Data
# ==========================================================

def load_papers():
    """
    Load papers for BERTopic.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing:
        - paper_id
        - abstract
    """

    df = pd.read_csv(INPUT_FILE)

    # Keep only required columns
    df = df[
        [
            "paper_id",
            "abstract"
        ]
    ]

    # Remove missing abstracts
    df = df.dropna(subset=["abstract"])

    # Remove empty abstracts
    df = df[df["abstract"].str.strip() != ""]

    # Reset index
    df = df.reset_index(drop=True)

    print(f"Loaded {len(df)} papers for BERTopic.")

    return df


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    papers = load_papers()

    print()
    print(papers.head())

    print()
    print(papers.info())