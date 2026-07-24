import json
import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import (
    BERTOPIC_RESULT_DIR,
    CLEANING_TOPIC_DIR,
)

# ==========================================================
# Config
# ==========================================================

INPUT_FILE = BERTOPIC_RESULT_DIR / "topics.csv"

TOPIC_NAME_FIX_FILE = (
    CLEANING_TOPIC_DIR / "topic_name_fix.json"
)

OUTPUT_FILE = (
    BERTOPIC_RESULT_DIR / "topics_update.csv"
)


# ==========================================================
# Update Topic Names
# ==========================================================

def update_topic_names():
    """
    Update topic names using manually curated mapping.
    """

    # ------------------------------------------------------
    # Load topics.csv
    # ------------------------------------------------------

    topics = pd.read_csv(INPUT_FILE)

    # ------------------------------------------------------
    # Load topic_name_fix.json
    # ------------------------------------------------------

    with open(
        TOPIC_NAME_FIX_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        topic_name_fix = json.load(f)

    topic_name_map = {

        item["topic_id"]: item["topic_name"]

        for item in topic_name_fix

    }

    # ------------------------------------------------------
    # Replace Topic Name
    # ------------------------------------------------------

    topics["topic_name"] = topics.apply(

        lambda row:

        topic_name_map.get(
            row["topic_id"],
            row["topic_name"]
        ),

        axis=1

    )

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    topics.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    updated = topics["topic_id"].isin(
        topic_name_map.keys()
    ).sum()

    print("=" * 70)
    print("UPDATE TOPIC NAMES".center(70))
    print("=" * 70)

    print(f"Total Topics      : {len(topics)}")
    print(f"Updated Topics    : {updated}")
    print(f"Output File       : {OUTPUT_FILE}")

    print()
    print("Topic name update completed.")

    return topics


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    update_topic_names()