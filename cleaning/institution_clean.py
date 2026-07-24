import json
import sys
from pathlib import Path

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from cleaning.load_data import load_clean_data
from utils.path import (
    CLEANING_INSTITUTION_DIR
)

# ==========================================================
# Files
# ==========================================================

COUNTRY_FIX_FILE = (
    CLEANING_INSTITUTION_DIR /
    "institution_country_fix.json"
)


# ==========================================================
# Load Country Fix
# ==========================================================

def load_country_fix():
    """
    Load institution country corrections.
    """

    if not COUNTRY_FIX_FILE.exists():

        print("institution_country_fix.json not found.")

        return {}

    with open(
        COUNTRY_FIX_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    country_map = {

        item["institution_id"]: item["country_code"]

        for item in data

        if item.get("institution_id")
        and item.get("country_code")

    }

    return country_map


# ==========================================================
# Remove Empty Institutions
# ==========================================================

def remove_empty_institutions(papers):
    """
    Remove institutions having:
        - id = None
        - display_name = None
        - country_code = None
    """

    removed = 0

    for paper in papers:

        for authorship in paper.get("authorships", []):

            cleaned_institutions = []

            for institution in authorship.get("institutions", []):

                if (
                    institution.get("id") is None
                    and institution.get("display_name") is None
                    and institution.get("country_code") is None
                ):

                    removed += 1
                    continue

                cleaned_institutions.append(institution)

            authorship["institutions"] = cleaned_institutions

    print(f"Removed empty institutions : {removed}")

    return papers


# ==========================================================
# Update Country Code
# ==========================================================

def update_country_code(
    papers,
    country_map
):
    """
    Update missing country_code.
    """

    updated = 0

    for paper in papers:

        for authorship in paper.get("authorships", []):

            for institution in authorship.get("institutions", []):

                institution_id = institution.get("id")

                if not institution_id:
                    continue

                if institution.get("country_code"):
                    continue

                if institution_id in country_map:

                    institution["country_code"] = (
                        country_map[institution_id]
                    )

                    updated += 1

    print(f"Updated country codes : {updated}")

    return papers


# ==========================================================
# Main Cleaning
# ==========================================================

def clean_institutions(papers):
    """
    Clean institution information.
    """

    print("=" * 70)
    print("INSTITUTION CLEANING".center(70))
    print("=" * 70)

    country_map = load_country_fix()

    papers = remove_empty_institutions(
        papers
    )

    papers = update_country_code(
        papers,
        country_map
    )

    print("\nInstitution cleaning completed.")

    return papers


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    papers = clean_institutions()

    print(f"\nRemaining papers : {len(papers)}")