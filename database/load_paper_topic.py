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

PAPER_TOPIC_FILE = BERTOPIC_RESULT_DIR / "paper_topic.csv"


# ==========================================================
# Load Paper Topic
# ==========================================================

def load_paper_topic():
    """
    Load paper_topic.csv into PostgreSQL.

    Columns
    -------
    paper_id
    topic_id
    probability
    """

    paper_topic = pd.read_csv(PAPER_TOPIC_FILE)

    paper_topic = paper_topic[
        [
            "paper_id",
            "topic_id",
            "probability"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO paper_topic
    (
        paper_id,
        topic_id,
        probability
    )
    VALUES
    (
        %s,
        %s,
        %s
    );
    """

    data = []

    for row in paper_topic.itertuples(index=False):

        data.append(

            (

                row.paper_id,

                int(row.topic_id),

                float(row.probability)
                if pd.notna(row.probability)
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
    print("LOAD PAPER_TOPIC".center(70))
    print("=" * 70)

    print(f"Inserted Paper-Topic : {len(data)}")

    print()
    print("paper_topic table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_paper_topic()