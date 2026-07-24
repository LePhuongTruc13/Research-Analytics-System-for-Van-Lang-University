import sys
from pathlib import Path

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from cleaning.load_data import load_clean_data


# ==========================================================
# Remove Short Author Names
# ==========================================================

def remove_short_author_names(papers):
    """
    Remove authors with very short names.
    """

    removed = 0

    for paper in papers:

        cleaned_authorships = []

        for authorship in paper.get("authorships", []):

            author = authorship.get("author", {})

            author_name = author.get("display_name")

            if (
                author_name
                and len(author_name.strip()) <= 1
            ):

                removed += 1
                continue

            cleaned_authorships.append(authorship)

        paper["authorships"] = cleaned_authorships

    print(f"Removed short author names : {removed}")

    return papers


# ==========================================================
# Generate LOCAL Author IDs
# ==========================================================

def generate_local_author_ids(papers):
    """
    Generate LOCAL author IDs for authors missing OpenAlex IDs.

    Authors having the same normalized name
    will receive the same LOCAL ID.
    """

    counter = 1

    updated = 0

    name_to_local_id = {}

    for paper in papers:

        for authorship in paper.get("authorships", []):

            author = authorship.get("author", {})

            # Skip existing OpenAlex ID
            if author.get("id"):

                continue

            author_name = author.get("display_name")

            if not author_name:

                continue

            # Normalize author name
            normalized_name = " ".join(
                author_name.split()
            ).casefold()

            # Existing LOCAL ID
            if normalized_name in name_to_local_id:

                author["id"] = name_to_local_id[normalized_name]

            else:

                local_id = f"LOCAL_A{counter:06d}"

                name_to_local_id[normalized_name] = local_id

                author["id"] = local_id

                counter += 1

            updated += 1

    print(f"Generated LOCAL author IDs : {updated}")

    print(f"Unique LOCAL authors       : {len(name_to_local_id)}")

    return papers


# ==========================================================
# Main Cleaning
# ==========================================================

def clean_authors(papers):
    """
    Clean author information.
    """

    print("=" * 70)
    print("AUTHOR CLEANING".center(70))
    print("=" * 70)

    papers = remove_short_author_names(
        papers
    )

    papers = generate_local_author_ids(
        papers
    )

    print("\nAuthor cleaning completed.")

    return papers


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    papers = clean_authors()

    print(f"\nRemaining papers : {len(papers)}")