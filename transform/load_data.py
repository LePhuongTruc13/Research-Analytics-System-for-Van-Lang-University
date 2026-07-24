import json
import sys
from pathlib import Path
from pprint import pprint

# ===========================
# Project Path
# ===========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import CLEANED_DATA_DIR


# ===========================
# Config
# ===========================

INPUT_FILE = CLEANED_DATA_DIR / "clean_papers_cleaned.json"


# ===========================
# Load Data
# ===========================

def load_clean_data():
    """
    Load cleaned OpenAlex dataset.

    Returns
    -------
    list[dict]
        List of cleaned papers.
    """

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        papers = json.load(f)

    print(f"Loaded {len(papers)} papers.")
    
    return papers


# ===========================
# Test
# ===========================

if __name__ == "__main__":

    papers = load_clean_data()
    print(papers[0].keys())
    
