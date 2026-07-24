from validation.load_data import load_clean_data

import csv
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from utils.path import AUTHOR_REPORT_DIR

from validation.validation_utils import (
    print_header,
    print_subheader,
    print_summary,
    print_separator,
    contains_html_entities
)


# ==========================================================
# Display Helper
# ==========================================================

def display_author(author):

    print(f"Author ID        : {author['author_id']}")
    print(f"Author Name      : {author['author_name']}")
    print_separator()


# ==========================================================
# Missing Validation
# ==========================================================

def validate_missing_author_id(authors):

    print_subheader("Missing Author ID")

    missing = [

        author

        for author in authors

        if not author["author_id"]

    ]

    print_summary("Found", len(missing))

    # Remove duplicates by (paper_id, author_name)
    unique_missing = []
    seen = set()

    for author in missing:

        key = (
            author["paper_id"],
            (author["author_name"] or "").strip()
        )

        if key not in seen:

            seen.add(key)

            unique_missing.append(author)

    # Export missing author IDs
    output_file = AUTHOR_REPORT_DIR / "missing_author_id.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "paper_id",
            "author_id",
            "name"
        ])

        for author in unique_missing:

            writer.writerow([
                author["paper_id"],
                author["author_id"],
                author["author_name"]
            ])

    print(f"Exported: {output_file}")

    if unique_missing:

        print()

        for author in unique_missing[:10]:

            display_author(author)


def validate_missing_author_name(authors):

    print_subheader("Missing Author Name")

    missing = [

        author

        for author in authors

        if (
            not author["author_name"]
            or not author["author_name"].strip()
        )

    ]

    print_summary("Found", len(missing))

    if missing:

        print()

        for author in missing[:10]:

            display_author(author)


# ==========================================================
# Author Name Quality
# ==========================================================

def validate_html_entities(authors):

    print_subheader("Author Names Containing HTML Entities")

    problems = []

    for author in authors:

        name = author["author_name"]

        if not name:
            continue

        if contains_html_entities(name):

            problems.append(author)

    print_summary("Found", len(problems))

    if problems:

        print()

        for author in problems[:10]:

            display_author(author)


def validate_short_author_name(authors):

    print_subheader("Very Short Author Names")

    problems = []

    for author in authors:

        name = author["author_name"]

        if not name:
            continue

        if len(name.strip()) <= 2:

            problems.append(author)

    print_summary("Found", len(problems))

    # Export short author names
    output_file = AUTHOR_REPORT_DIR / "author_short_name.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "author_id",
            "name"
        ])

        for author in problems:

            writer.writerow([
                author["author_id"],
                author["author_name"]
            ])

    print(f"Exported: {output_file}")

    if problems:

        print()

        for author in problems[:10]:

            display_author(author)


def validate_leading_trailing_spaces(authors):

    print_subheader("Author Names With Leading / Trailing Spaces")

    problems = []

    for author in authors:

        name = author["author_name"]

        if not name:
            continue

        if name != name.strip():

            problems.append(author)

    print_summary("Found", len(problems))

    if problems:

        print()

        for author in problems[:10]:

            display_author(author)


# ==========================================================
# Main
# ==========================================================

def main():

    papers = load_clean_data()

    authors = []

    for paper in papers:

        for authorship in paper.get("authorships", []):

            authors.append({

                "paper_id": paper.get("id"),

                "author_id": authorship.get("author", {}).get("id"),

                "author_name": authorship.get("author", {}).get("display_name")

            })

    print_header("Author Validation")

    validate_missing_author_id(authors)

    validate_missing_author_name(authors)

    validate_html_entities(authors)

    validate_short_author_name(authors)

    validate_leading_trailing_spaces(authors)

    print()

    print("=" * 70)

    print("VALIDATION COMPLETED".center(70))

    print("=" * 70)


if __name__ == "__main__":

    main()