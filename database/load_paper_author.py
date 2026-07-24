import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.database import get_connection
from utils.path import TRANSFORMED_DATA_DIR


# ==========================================================
# Config
# ==========================================================

PAPER_AUTHOR_FILE = TRANSFORMED_DATA_DIR / "paper_author.csv"


# ==========================================================
# Load Paper Author
# ==========================================================

def load_paper_author():
    """
    Load paper_author.csv into PostgreSQL.

    Columns
    -------
    paper_id
    author_id
    """

    paper_author = pd.read_csv(PAPER_AUTHOR_FILE)

    paper_author = paper_author[
        [
            "paper_id",
            "author_id"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO paper_author
    (
        paper_id,
        author_id
    )
    VALUES
    (
        %s,
        %s
    );
    """

    data = []

    for row in paper_author.itertuples(index=False):

        data.append(

            (

                row.paper_id,

                row.author_id

            )

        )

    cursor.executemany(
        sql,
        data
    )

    conn.commit()

    cursor.close()
    conn.close()

    print("=" * 70)
    print("LOAD PAPER_AUTHOR".center(70))
    print("=" * 70)

    print(f"Inserted Paper-Author : {len(data)}")

    print()
    print("paper_author table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_paper_author()