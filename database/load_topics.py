import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.database import get_connection
from utils.path import BERTOPIC_RESULT_DIR


# ==========================================================
# Config
# ==========================================================

TOPIC_FILE = BERTOPIC_RESULT_DIR / "topics_update.csv"


# ==========================================================
# Load Topics
# ==========================================================

def load_topics():
    """
    Load topics_update.csv into PostgreSQL.

    Columns
    -------
    topic_id
    topic_name
    keywords
    paper_count
    """

    topics = pd.read_csv(TOPIC_FILE)

    topics = topics[
        [
            "topic_id",
            "topic_name",
            "keywords",
            "paper_count"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO topics
    (
        topic_id,
        topic_name,
        keywords,
        paper_count
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    );
    """

    data = []

    for row in topics.itertuples(index=False):

        data.append(

            (

                int(row.topic_id),

                row.topic_name,

                row.keywords
                if pd.notna(row.keywords)
                else None,

                int(row.paper_count)
                if pd.notna(row.paper_count)
                else 0

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
    print("LOAD TOPICS".center(70))
    print("=" * 70)

    print(f"Inserted Topics : {len(data)}")

    print()
    print("topics table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_topics()