import sys
from pathlib import Path

import numpy as np
from bertopic import BERTopic
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.bertopic.load_data import load_papers
from utils.path import MODEL_DIR


# ==========================================================
# Config
# ==========================================================

EMBEDDING_FILE = MODEL_DIR / "embeddings.npy"

MODEL_OUTPUT = MODEL_DIR / "bertopic_model"


# ==========================================================
# Train BERTopic
# ==========================================================

def train_model():
    """
    Train BERTopic model using precomputed embeddings.
    """

    papers = load_papers()

    documents = papers["abstract"].tolist()

    embeddings = np.load(EMBEDDING_FILE)

    print(f"\nLoaded embeddings: {embeddings.shape}")

    # ======================================================
    # UMAP
    # ======================================================

    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42
    )

    # ======================================================
    # HDBSCAN
    # ======================================================

    hdbscan_model = HDBSCAN(
        min_cluster_size=15,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True
    )

    # ======================================================
    # Vectorizer
    # ======================================================

    vectorizer_model = CountVectorizer(
        stop_words="english",
        min_df=2
    )

    # ======================================================
    # BERTopic
    # ======================================================

    topic_model = BERTopic(
        language="english",
        calculate_probabilities=True,
        verbose=True,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model
    )

    print("\nTraining BERTopic...\n")

    topics, probabilities = topic_model.fit_transform(
        documents,
        embeddings
    )

    print("\nSaving model...")

    topic_model.save(
        MODEL_OUTPUT,
        serialization="safetensors",
        save_ctfidf=True
    )

    print("\nTraining completed.")

    print(f"Model saved to: {MODEL_OUTPUT}")

    print(f"Number of Topics : {len(topic_model.get_topic_info())}")

    return topic_model


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    train_model()