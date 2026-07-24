import sys
from pathlib import Path

import numpy as np
import pandas as pd
from bertopic import BERTopic

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.bertopic.load_data import load_papers
from utils.path import (
    MODEL_DIR,
    BERTOPIC_RESULT_DIR,
)

# ==========================================================
# Config
# ==========================================================

MODEL_PATH = MODEL_DIR / "bertopic_model"
EMBEDDING_FILE = MODEL_DIR / "embeddings.npy"

TOPIC_OUTPUT = BERTOPIC_RESULT_DIR / "topics.csv"
PAPER_TOPIC_OUTPUT = BERTOPIC_RESULT_DIR / "paper_topic.csv"


# ==========================================================
# Predict
# ==========================================================

def predict_topics():

    papers = load_papers()

    documents = papers["abstract"].tolist()

    embeddings = np.load(EMBEDDING_FILE)

    print("\nLoading BERTopic model...")

    topic_model = BERTopic.load(MODEL_PATH)

    print("Predicting topics...\n")

    topics, probabilities = topic_model.transform(
        documents,
        embeddings
    )

    # ======================================================
    # paper_topic dataframe
    # ======================================================

    paper_topic_df = pd.DataFrame({

        "paper_id": papers["paper_id"],

        "topic_id": topics,

        "probability": [

            float(np.max(p))
            if hasattr(p, "__len__")
            else float(p)

            for p in probabilities
        ]
    })

    # ======================================================
    # Statistics BEFORE removing outliers
    # ======================================================

    total_papers = len(paper_topic_df)

    outlier_papers = (
        paper_topic_df["topic_id"] == -1
    ).sum()

    outlier_ratio = (
        outlier_papers / total_papers
    ) * 100

    average_probability = (
        paper_topic_df["probability"]
        .mean()
    )

    # ======================================================
    # Remove Outlier Papers
    # ======================================================

    paper_topic_df = paper_topic_df[
        paper_topic_df["topic_id"] != -1
    ].reset_index(drop=True)

    # ======================================================
    # Count papers per topic
    # ======================================================

    topic_sizes = (
        paper_topic_df
        .groupby("topic_id")
        .size()
        .to_dict()
    )

    # ======================================================
    # topics.csv
    # ======================================================

    topic_info = topic_model.get_topic_info()

    rows = []

    for _, row in topic_info.iterrows():

        topic_id = row["Topic"]

        if topic_id == -1:
            continue

        words = topic_model.get_topic(topic_id)

        keywords = ", ".join(

            word

            for word, _ in words[:5]

        )

        rows.append({

            "topic_id": topic_id,

            "topic_name": row["Name"],

            "keywords": keywords,

            "paper_count": topic_sizes.get(topic_id, 0)

        })

    topics_df = pd.DataFrame(rows)

    topics_df = topics_df.sort_values(
        by="topic_id"
    ).reset_index(drop=True)

    # ======================================================
    # Save CSV
    # ======================================================

    topics_df.to_csv(
        TOPIC_OUTPUT,
        index=False
    )

    paper_topic_df.to_csv(
        PAPER_TOPIC_OUTPUT,
        index=False
    )

    # ======================================================
    # Largest / Smallest Topic
    # ======================================================

    largest_topic = topics_df.loc[
        topics_df["paper_count"].idxmax()
    ]

    smallest_topic = topics_df.loc[
        topics_df["paper_count"].idxmin()
    ]

    # ======================================================
    # Summary
    # ======================================================

    print("=" * 70)
    print("BERTOPIC PREDICTION SUMMARY".center(70))
    print("=" * 70)

    print(f"Total Papers         : {total_papers}")
    print(f"Total Topics         : {len(topics_df)}")

    print(f"Outlier Papers       : {outlier_papers}")
    print(f"Outlier Ratio        : {outlier_ratio:.2f}%")

    print(f"Average Probability  : {average_probability:.4f}")

    print()

    print(
        f"Largest Topic        : "
        f"{largest_topic['topic_id']} "
        f"({largest_topic['paper_count']} papers)"
    )

    print(
        f"Smallest Topic       : "
        f"{smallest_topic['topic_id']} "
        f"({smallest_topic['paper_count']} papers)"
    )

    print()

    print("Saved Files")
    print(f"✔ {TOPIC_OUTPUT}")
    print(f"✔ {PAPER_TOPIC_OUTPUT}")

    return topics_df, paper_topic_df


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    predict_topics()