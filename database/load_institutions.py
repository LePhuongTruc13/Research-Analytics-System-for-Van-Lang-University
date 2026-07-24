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

INSTITUTION_FILE = TRANSFORMED_DATA_DIR / "institutions.csv"


# ==========================================================
# Load Institutions
# ==========================================================

def load_institutions():
    """
    Load institutions.csv into PostgreSQL.

    Columns
    -------
    institution_id
    institution_name
    country_code
    """

    institutions = pd.read_csv(INSTITUTION_FILE)

    institutions = institutions[
        [
            "institution_id",
            "institution_name",
            "country_code"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO institutions
    (
        institution_id,
        institution_name,
        country_code
    )
    VALUES
    (
        %s,
        %s,
        %s
    );
    """

    data = []

    for row in institutions.itertuples(index=False):

        data.append(

            (

                row.institution_id,

                row.institution_name,

                row.country_code
                if pd.notna(row.country_code)
                else None

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
    print("LOAD INSTITUTIONS".center(70))
    print("=" * 70)

    print(f"Inserted Institutions : {len(data)}")

    print()
    print("institutions table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_institutions()