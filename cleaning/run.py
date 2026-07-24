import json
import sys
from pathlib import Path
from cleaning.load_data import load_clean_data

from cleaning.paper_clean import clean_papers
from cleaning.author_clean import clean_authors
from cleaning.institution_clean import clean_institutions

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from utils.path import CLEANED_DATA_DIR


# ==========================================================
# Output File
# ==========================================================

OUTPUT_FILE = (
    CLEANED_DATA_DIR /
    "clean_papers_cleaned.json"
)


# ==========================================================
# Save JSON
# ==========================================================

def save_clean_data(papers):
    """
    Save cleaned papers.
    """

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            papers,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nSaved to: {OUTPUT_FILE}")


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 70)
    print("START CLEANING PIPELINE".center(70))
    print("=" * 70)

    # Load data
    papers = load_clean_data()

    # Cleaning
    papers = clean_papers(papers)

    papers = clean_authors(papers)

    papers = clean_institutions(papers)

    # Save
    save_clean_data(papers)

    print("\nCleaning pipeline completed successfully.")


if __name__ == "__main__":

    main()