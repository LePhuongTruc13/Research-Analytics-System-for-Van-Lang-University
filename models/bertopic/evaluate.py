import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from bertopic import BERTopic

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import (
    MODEL_DIR,
    BERTOPIC_RESULT_DIR,
)

# ==========================================================
# Config
# ==========================================================

MODEL_PATH = MODEL_DIR / "bertopic_model"

PAPER_TOPIC_FILE = BERTOPIC_RESULT_DIR / "paper_topic.csv"

EVALUATION_FILE = BERTOPIC_RESULT_DIR / "evaluation.txt"

DISTRIBUTION_FIGURE = BERTOPIC_RESULT_DIR / "topic_distribution.png"


# ==========================================================
# Evaluate BERTopic
# ==========================================================

def evaluate():

    print("=" * 70)
    print("BERTOPIC EVALUATION".center(70))
    print("=" * 70)

    topic_model = BERTopic.load(MODEL_PATH)

    paper_topic = pd.read_csv(PAPER_TOPIC_FILE)

    topic_info = topic_model.get_topic_info()

    # ======================================================
    # Basic Statistics
    # ======================================================

    total_papers = len(paper_topic)

    total_topics = len(
        topic_info[
            topic_info["Topic"] != -1
        ]
    )

    outlier_papers = (
        paper_topic["topic_id"] == -1
    ).sum()

    outlier_ratio = (
        outlier_papers / total_papers
    ) * 100

    average_probability = (
        paper_topic["probability"].mean()
    )

    topic_sizes = (
        paper_topic[
            paper_topic["topic_id"] != -1
        ]
        .groupby("topic_id")
        .size()
    )

    average_topic_size = topic_sizes.mean()

    median_topic_size = topic_sizes.median()

    largest_topic = topic_sizes.idxmax()

    largest_size = topic_sizes.max()

    smallest_topic = topic_sizes.idxmin()

    smallest_size = topic_sizes.min()

    # ======================================================
    # Console
    # ======================================================

    print(f"Total Papers         : {total_papers}")
    print(f"Total Topics         : {total_topics}")

    print()

    print(f"Outlier Papers       : {outlier_papers}")
    print(f"Outlier Ratio        : {outlier_ratio:.2f}%")

    print()

    print(f"Average Probability  : {average_probability:.4f}")

    print()

    print(f"Average Topic Size   : {average_topic_size:.2f}")

    print(f"Median Topic Size    : {median_topic_size:.2f}")

    print()

    print(
        f"Largest Topic        : "
        f"{largest_topic} ({largest_size} papers)"
    )

    print(
        f"Smallest Topic       : "
        f"{smallest_topic} ({smallest_size} papers)"
    )

    # ======================================================
    # Save evaluation.txt
    # ======================================================

    with open(
        EVALUATION_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("=" * 60 + "\n")
        f.write("BERTopic Evaluation\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Total Papers         : {total_papers}\n")
        f.write(f"Total Topics         : {total_topics}\n\n")

        f.write(f"Outlier Papers       : {outlier_papers}\n")
        f.write(f"Outlier Ratio        : {outlier_ratio:.2f}%\n\n")

        f.write(f"Average Probability  : {average_probability:.4f}\n\n")

        f.write(f"Average Topic Size   : {average_topic_size:.2f}\n")
        f.write(f"Median Topic Size    : {median_topic_size:.2f}\n\n")

        f.write(
            f"Largest Topic        : "
            f"{largest_topic} ({largest_size} papers)\n"
        )

        f.write(
            f"Smallest Topic       : "
            f"{smallest_topic} ({smallest_size} papers)\n"
        )

    # ======================================================
    # Plot Distribution
    # ======================================================

    topic_sizes.sort_values(
        ascending=False
    ).plot(
        kind="bar",
        figsize=(12, 6)
    )

    plt.title("Paper Distribution by Topic")

    plt.xlabel("Topic ID")

    plt.ylabel("Number of Papers")

    plt.tight_layout()

    plt.savefig(
        DISTRIBUTION_FIGURE,
        dpi=300
    )

    plt.close()

    print()

    print("Saved Files")

    print(f"✔ {EVALUATION_FILE}")

    print(f"✔ {DISTRIBUTION_FIGURE}")

    print()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    evaluate()