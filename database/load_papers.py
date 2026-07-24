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

PAPER_FILE = TRANSFORMED_DATA_DIR / "papers.csv"


# ==========================================================
# Load Papers
# ==========================================================

def load_papers():
    """
    Load papers.csv into PostgreSQL.

    Columns
    -------
    paper_id
    doi
    title
    abstract
    publication_year
    cited_by_count
    is_open_access
    """

    papers = pd.read_csv(PAPER_FILE)

    papers = papers[
        [
            "paper_id",
            "doi",
            "title",
            "abstract",
            "publication_year",
            "cited_by_count",
            "is_open_access"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO papers
    (
        paper_id,
        doi,
        title,
        abstract,
        publication_year,
        cited_by_count,
        is_open_access
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    );
    """

    data = []

    for row in papers.itertuples(index=False):

        data.append(

            (

                row.paper_id,

                row.doi
                if pd.notna(row.doi)
                else None,

                row.title,

                row.abstract
                if pd.notna(row.abstract)
                else None,

                int(row.publication_year)
                if pd.notna(row.publication_year)
                else None,

                int(row.cited_by_count)
                if pd.notna(row.cited_by_count)
                else 0,

                bool(row.is_open_access)
                if pd.notna(row.is_open_access)
                else False

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
    print("LOAD PAPERS".center(70))
    print("=" * 70)

    print(f"Inserted Papers : {len(data)}")

    print()
    print("papers table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_papers()