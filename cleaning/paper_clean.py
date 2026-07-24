import json
import html
import sys
import re
from pathlib import Path

# ======================
# Project Path
# ======================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from cleaning.load_data import load_clean_data
from utils.path import (
    CLEANING_PAPER_DIR,
)

# ======================
# Files
# ======================

TITLE_FIX_FILE = CLEANING_PAPER_DIR / "paper_title_fix.json"


# =======================
# Load Title Corrections
# =======================

def load_title_fix():
    """
    Load corrected paper titles.
    """

    if not TITLE_FIX_FILE.exists():

        print("paper_title_fix.json not found.")

        return {}

    with open(
        TITLE_FIX_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    title_map = {

        item["paper_id"]: item["corrected_title"]

        for item in data

        if item.get("corrected_title")

    }

    return title_map


# =======================
# Update Titles
# =======================

def update_titles(
    papers,
    title_map
):
    """
    Update titles using paper_title_fix.json.
    """

    updated = 0

    for paper in papers:

        paper_id = paper.get("id")

        if paper_id in title_map:

            paper["title"] = title_map[paper_id]

            updated += 1

    print(f"Updated titles : {updated}")

    return papers


# =======================
# Remove HTML Entities
# =======================

def remove_html_entities(
    papers
):
    """
    Decode HTML entities in paper titles.
    """

    count = 0

    for paper in papers:

        title = paper.get("title")

        if not title:
            continue

        decoded = html.unescape(title)

        if decoded != title:

            paper["title"] = decoded

            count += 1

    print(f"HTML entities fixed : {count}")

    return papers


# =======================
# Remove Missing Titles
# =======================

def remove_missing_titles(
    papers
):
    """
    Remove records without title.
    """

    cleaned = []

    removed = 0

    for paper in papers:

        title = paper.get("title")

        if not title or not title.strip():

            removed += 1

            continue

        cleaned.append(paper)

    print(f"Removed papers : {removed}")

    return cleaned

# =============================
# Clean Abstract HTML Entities
# =============================

def clean_abstract_html_entities(papers):
    """
    Decode HTML entities in abstracts.
    """

    count = 0

    for paper in papers:

        abstract = paper.get("abstract")

        if not abstract:
            continue

        decoded = html.unescape(abstract)

        if decoded != abstract:

            paper["abstract"] = decoded

            count += 1

    print(f"Abstract HTML entities fixed : {count}")

    return papers

# =============================
# Clean Abstract Whitespaces
# =============================

def clean_abstract_whitespace(papers):
    """
    Normalize whitespaces in abstracts.
    """

    count = 0

    for paper in papers:

        abstract = paper.get("abstract")

        if not abstract:
            continue

        cleaned = re.sub(r"\s+", " ", abstract).strip()

        if cleaned != abstract:

            paper["abstract"] = cleaned

            count += 1

    print(f"Abstract whitespace fixed : {count}")

    return papers

# =============================
# Main Cleaning
# =============================
def clean_papers(papers):
    """
    Clean paper dataset.
    """

    print("=" * 70)
    print("PAPER CLEANING".center(70))
    print("=" * 70)

    title_map = load_title_fix()

    papers = update_titles(
        papers,
        title_map
    )

    papers = remove_html_entities(
        papers
    )

    papers = remove_missing_titles(
        papers
    )

    papers = clean_abstract_html_entities(
        papers
    )

    papers = clean_abstract_whitespace(
        papers
    )   

    print("\nPaper cleaning completed.")

    return papers


# =========================
# Test
# =========================
if __name__ == "__main__":
    
    papers = load_clean_data()

    papers = clean_papers(papers)

    print(f"\nRemaining papers : {len(papers)}")