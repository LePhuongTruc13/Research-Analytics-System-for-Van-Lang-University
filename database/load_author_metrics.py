import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.database import get_connection
from utils.path import NETWORKX_RESULT_DIR


# ==========================================================
# Config
# ==========================================================

AUTHOR_METRIC_FILE = NETWORKX_RESULT_DIR / "author_metrics.csv"


# ==========================================================
# Load Author Metrics
# ==========================================================

def load_author_metrics():
    """
    Load author_metrics.csv into PostgreSQL.

    Columns
    -------
    author_id
    degree
    betweenness
    closeness
    pagerank
    """

    metrics = pd.read_csv(AUTHOR_METRIC_FILE)

    metrics = metrics[
        [
            "author_id",
            "degree",
            "betweenness",
            "closeness",
            "pagerank"
        ]
    ]

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO author_metrics
    (
        author_id,
        degree,
        betweenness,
        closeness,
        pagerank
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s
    );
    """

    data = []

    for row in metrics.itertuples(index=False):

        data.append(

            (

                row.author_id,

                float(row.degree),

                float(row.betweenness),

                float(row.closeness),

                float(row.pagerank)

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
    print("LOAD AUTHOR_METRICS".center(70))
    print("=" * 70)

    print(f"Inserted Author Metrics : {len(data)}")

    print()
    print("author_metrics table loaded successfully.")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    load_author_metrics()