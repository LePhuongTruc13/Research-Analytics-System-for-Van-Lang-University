import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

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

MODEL_NAME = "all-MiniLM-L6-v2"

OUTPUT_FILE = MODEL_DIR / "embeddings.npy"


# ==========================================================
# Generate Embeddings
# ==========================================================

def generate_embeddings():
    """
    Generate sentence embeddings from paper abstracts.
    """

    papers = load_papers()

    documents = papers["abstract"].tolist()

    print(f"\nLoading model: {MODEL_NAME}")

    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...\n")

    embeddings = model.encode(
        documents,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
        batch_size=32
    )

    np.save(OUTPUT_FILE, embeddings)

    print("\nEmbedding completed.")
    print(f"Embedding shape : {embeddings.shape}")
    print(f"Saved to        : {OUTPUT_FILE}")

    return embeddings


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    generate_embeddings()