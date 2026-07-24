import csv
import numpy as np
from bertopic import BERTopic

from models.bertopic.load_data import load_papers

from utils.path import (
    MODEL_DIR,
    BERTOPIC_RESULT_DIR,
)

# ==========================================================
# Files
# ==========================================================

MODEL_PATH = MODEL_DIR / "bertopic_model"

EMBEDDING_FILE = MODEL_DIR / "embeddings.npy"

TOPIC_FILE = BERTOPIC_RESULT_DIR / "topics.csv"

PAPER_TOPIC_FILE = BERTOPIC_RESULT_DIR / "paper_topic.csv"


# ==========================================================
# Load Model
# ==========================================================

def load_topic_model():
    """
    Load trained BERTopic model.
    """

    model = BERTopic.load(MODEL_PATH)

    print(f"Loaded model : {MODEL_PATH}")

    return model


# ==========================================================
# Load Embeddings
# ==========================================================

def load_embeddings():
    """
    Load saved embeddings.
    """

    embeddings = np.load(EMBEDDING_FILE)

    print(f"Loaded embeddings : {EMBEDDING_FILE}")

    return embeddings


# ==========================================================
# Export Results
# ==========================================================

def export_results():

    papers = load_papers()

    documents = papers["abstract"].tolist()

    embeddings = load_embeddings()

    topic_model = load_topic_model()

    print("\nPredicting topics...\n")

    topics, probabilities = topic_model.transform(
        documents,
        embeddings
    )

    # ======================================================
    # paper_topic.csv
    # ======================================================

    paper_counts = {}

    with open(
        PAPER_TOPIC_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "paper_id",
            "topic_id",
            "probability"
        ])

        for paper_id, topic, probability in zip(
            papers["paper_id"],
            topics,
            probabilities
        ):

            if hasattr(probability, "__len__"):

                probability = float(np.max(probability))

            elif probability is not None:

                probability = float(probability)

            writer.writerow([
                paper_id,
                topic,
                probability
            ])

            paper_counts[topic] = (
                paper_counts.get(topic, 0) + 1
            )

    print(f"Exported : {PAPER_TOPIC_FILE}")

    # ======================================================
    # topics.csv
    # ======================================================

    topic_info = topic_model.get_topic_info()

    with open(
        TOPIC_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "topic_id",
            "topic_name",
            "keywords",
            "paper_count"
        ])

        for _, row in topic_info.iterrows():

            topic_id = row["Topic"]

            if topic_id == -1:
                continue

            words = topic_model.get_topic(topic_id)

            if words:

                keywords = ", ".join(
                    word
                    for word, _ in words[:5]
                )

            else:

                keywords = ""

            writer.writerow([

                topic_id,

                row["Name"],

                keywords,

                paper_counts.get(topic_id, 0)

            ])

    print(f"Exported : {TOPIC_FILE}")

    # ======================================================
    # Summary
    # ======================================================

    total_papers = len(papers)

    total_topics = len(topic_info) - 1

    outlier_papers = paper_counts.get(-1, 0)

    outlier_ratio = (
        outlier_papers / total_papers
    ) * 100

    avg_probability = np.mean([

        float(np.max(p))
        if hasattr(p, "__len__")
        else float(p)

        for p in probabilities

    ])

    valid_topics = {
        k: v
        for k, v in paper_counts.items()
        if k != -1
    }

    largest_topic = max(
        valid_topics,
        key=valid_topics.get
    )

    smallest_topic = min(
        valid_topics,
        key=valid_topics.get
    )

    print()
    print("=" * 70)
    print("BERTOPIC PREDICTION SUMMARY".center(70))
    print("=" * 70)

    print(f"Total Papers         : {total_papers}")
    print(f"Total Topics         : {total_topics}")

    print(f"Outlier Papers       : {outlier_papers}")
    print(f"Outlier Ratio        : {outlier_ratio:.2f}%")

    print(f"Average Probability  : {avg_probability:.4f}")

    print()

    print(
        f"Largest Topic        : "
        f"{largest_topic} ({valid_topics[largest_topic]} papers)"
    )

    print(
        f"Smallest Topic       : "
        f"{smallest_topic} ({valid_topics[smallest_topic]} papers)"
    )

    print()

    print("BERTopic results exported successfully.")


# ==========================================================
# Main
# ==========================================================

def main():

    export_results()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    main()