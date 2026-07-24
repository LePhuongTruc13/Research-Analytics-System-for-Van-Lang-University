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

AUTHOR_INSTITUTION_FILE = (
    TRANSFORMED_DATA_DIR / "author_institution.csv"
)


# ==========================================================
# Load Author Institution
# ==========================================================

def load_author_institution():
    """
    Load author_institution.csv into PostgreSQL.

    Columns
    -------
    author_id
    institution_id
    """

    author_institution = pd.read_csv(
        AUTHOR_INSTITUTION_FILE
    )

    author_institution = author_institution[
        [
            "author_id",
            "institution_id"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO author_institution
    (
        author_id,
        institution_id
    )
    VALUES
    (
        %s,
        %s
    );
    """

    data = []

    for row in author_institution.itertuples(index=False):

        data.append(

            (

                row.author_id,

                row.institution_id

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
    print("LOAD AUTHOR_INSTITUTION".center(70))
    print("=" * 70)

    print(
        f"Inserted Author-Institution : {len(data)}"
    )

    print()
    print(
        "author_institution table loaded successfully."
    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_author_institution()