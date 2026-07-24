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

AUTHOR_FILE = TRANSFORMED_DATA_DIR / "authors.csv"


# ==========================================================
# Load Authors
# ==========================================================

def load_authors():
    """
    Load authors.csv into PostgreSQL.

    Columns
    -------
    author_id
    author_name
    """

    authors = pd.read_csv(AUTHOR_FILE)

    authors = authors[
        [
            "author_id",
            "author_name"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO authors
    (
        author_id,
        author_name
    )
    VALUES
    (
        %s,
        %s
    );
    """

    data = []

    for row in authors.itertuples(index=False):

        data.append(

            (

                row.author_id,

                row.author_name

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
    print("LOAD AUTHORS".center(70))
    print("=" * 70)

    print(f"Inserted Authors : {len(data)}")

    print()
    print("authors table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_authors()