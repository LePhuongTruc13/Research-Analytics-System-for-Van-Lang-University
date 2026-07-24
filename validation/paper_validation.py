import csv
import sys 
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from utils.path import PAPER_REPORT_DIR
from collections import Counter
from datetime import datetime

from validation.load_data import load_clean_data

from validation.validation_utils import (
    print_header,
    print_subheader,
    print_summary,
    print_separator,
    contains_html_entities,
    has_many_special_characters
)

# ==========================================================
# Constants
# ==========================================================

CURRENT_YEAR = datetime.now().year

LANGUAGE_MAP = {
    "en": "English",
    "vi": "Vietnamese",
    "lv": "Latvian",
    "fr": "French",
    "id": "Indonesian",
    "ng": "Ndonga",
    "es": "Spanish",
    "pt": "Portuguese",
    "nl": "Dutch",
    "zh": "Chinese",
    "tr": "Turkish",
    "ru": "Russian",
    "tl": "Tagalog / Filipino",
}


# ==========================================================
# Display Helper
# ==========================================================

def display_paper(paper):
    """
    Display paper information.
    """

    print(f"Paper ID          : {paper.get('id')}")
    print(f"Title             : {paper.get('title')}")
    print(f"Publication Year  : {paper.get('publication_year')}")
    print(f"Language          : {paper.get('language')}")
    print(f"DOI               : {paper.get('doi')}")
    print_separator()


# ==========================================================
# Missing Validation
# ==========================================================

def validate_missing_paper_id(papers):

    print_subheader("Missing Paper ID")

    missing = []

    for paper in papers:

        if not paper.get("id"):

            missing.append(paper)

    print_summary("Found", len(missing))

    if missing:

        print()

        for paper in missing[:5]:

            display_paper(paper)


def validate_missing_title(papers):

    print_subheader("Missing Title")

    missing = []

    for paper in papers:

        title = paper.get("title")

        if not title or not title.strip():

            missing.append(paper)

    print_summary("Found", len(missing))

    if missing:

        print()

        for paper in missing[:5]:

            display_paper(paper)


def validate_missing_abstract(papers):

    print_subheader("Missing Abstract")

    missing = []

    for paper in papers:

        abstract = paper.get("abstract")

        if not abstract or not abstract.strip():

            missing.append(paper)

    print_summary("Found", len(missing))

    if missing:

        print()

        for paper in missing[:5]:

            display_paper(paper)


def validate_missing_doi(papers):

    print_subheader("Missing DOI")

    missing = []

    for paper in papers:

        if not paper.get("doi"):

            missing.append(paper)

    print_summary("Found", len(missing))

    # Export missing DOI
    output_file = PAPER_REPORT_DIR / "missing_doi.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "paper_id",
            "doi"
        ])

        for paper in missing:

            writer.writerow([
                paper.get("id"),
                paper.get("doi")
            ])

    print(f"Exported: {output_file}")

    if missing:

        print()

        for paper in missing[:10]:

            display_paper(paper)

# ==========================================================
# Duplicate Validation
# ==========================================================

def validate_duplicate_paper_id(papers):

    print_subheader("Duplicate Paper ID")

    ids = [

        paper.get("id")

        for paper in papers

        if paper.get("id")

    ]

    duplicates = {

        key: value

        for key, value in Counter(ids).items()

        if value > 1

    }

    print_summary("Duplicate IDs", len(duplicates))

    if duplicates:

        print()

        print("Top Duplicates\n")

        for paper_id, count in list(duplicates.items())[:10]:

            print(f"{paper_id:<35} {count}")

# ==========================================================
# Invalid Validation
# ==========================================================

def validate_invalid_publication_year(papers):

    print_subheader("Invalid Publication Year")

    invalid = []

    for paper in papers:

        year = paper.get("publication_year")

        if year is None:
            continue

        if (
            not isinstance(year, int)
            or year < 1900
            or year > CURRENT_YEAR
        ):
            invalid.append(paper)

    print_summary("Found", len(invalid))

    if invalid:

        print()

        for paper in invalid[:10]:

            display_paper(paper)


def validate_invalid_cited_by_count(papers):

    print_subheader("Invalid Cited By Count")

    invalid = []

    for paper in papers:

        citation = paper.get("cited_by_count")

        if citation is None:
            continue

        if (
            not isinstance(citation, int)
            or citation < 0
        ):
            invalid.append(paper)

    print_summary("Found", len(invalid))

    if invalid:

        print()

        for paper in invalid[:10]:

            display_paper(paper)


def validate_invalid_open_access(papers):

    print_subheader("Invalid Open Access")

    invalid = []

    for paper in papers:

        value = paper.get("open_access", {}).get("is_oa")

        if value is None:
            continue

        if not isinstance(value, bool):

            invalid.append(paper)

    print_summary("Found", len(invalid))

    if invalid:

        print()

        for paper in invalid[:10]:

            display_paper(paper)


# ==========================================================
# Language Distribution
# ==========================================================

def validate_language_distribution(papers):

    print_subheader("Language Distribution")

    languages = [

        paper.get("language")

        for paper in papers

        if paper.get("language")

    ]

    distribution = Counter(languages)

    print()

    print(f"{'Code':<8}{'Language':<25}{'Count'}")

    print("-" * 50)

    for code, count in sorted(

        distribution.items(),

        key=lambda x: x[1],

        reverse=True

    ):

        language = LANGUAGE_MAP.get(

            code,

            "Unknown"

        )

        print(f"{code:<8}{language:<25}{count}")

# ==========================================================
# Abstract Validation
# ==========================================================

import re


def validate_special_characters_in_abstract(papers):

    print_subheader("Abstracts With Many Special Characters")

    problems = []

    for paper in papers:

        abstract = paper.get("abstract")

        if not abstract:
            continue

        if has_many_special_characters(abstract):

            problems.append(paper)

    print_summary("Found", len(problems))

    if problems:

        print()

        for paper in problems[:10]:

            display_paper(paper)


def validate_abstract_whitespace(papers):

    print_subheader("Abstracts With Leading / Trailing Spaces")

    problems = []

    for paper in papers:

        abstract = paper.get("abstract")

        if not abstract:
            continue

        reason = []

        if abstract != abstract.strip():

            reason.append("Leading / trailing spaces")

        if re.search(r"\s{2,}", abstract):

            reason.append("Multiple consecutive spaces")

        if reason:

            problems.append(
                (paper, ", ".join(reason))
            )

    print_summary("Found", len(problems))

    if problems:

        print()

        for paper, reason in problems[:10]:

            display_paper(paper)

            print(f"Reason            : {reason}")

            print_separator()

# ==========================================================
# Title Quality
# ==========================================================

def validate_html_entities(papers):

    print_subheader("Titles Containing HTML Entities")

    problems = []

    for paper in papers:

        title = paper.get("title")

        if not title:
            continue

        if contains_html_entities(title):

            problems.append(paper)

    print_summary("Found", len(problems))

    if problems:

        print()

        for paper in problems[:10]:

            display_paper(paper)


def validate_weird_title(papers):

    print_subheader("Weird Titles")

    problems = []

    for paper in papers:

        title = paper.get("title")

        if not title:
            continue

        reason = []

        if has_many_special_characters(title):
            reason.append("Too many special characters")

        if len(title.split()) < 3:
            reason.append("Very short title")

        if title.strip() != title:
            reason.append("Leading / trailing spaces")

        if reason:
            problems.append(
                (paper, ", ".join(reason))
            )

    print_summary("Found", len(problems))

    # Export weird titles
    output_file = PAPER_REPORT_DIR / "weird_titles.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "paper_id",
            "title"
        ])

        for paper, _ in problems:

            writer.writerow([
                paper.get("id"),
                paper.get("title")
            ])

    print(f"Exported: {output_file}")

    if problems:

        print()

        for paper, reason in problems[:10]:

            display_paper(paper)

            print(f"Reason            : {reason}")

            print_separator()


# ==========================================================
# Main
# ==========================================================

def main():

    papers = load_clean_data()

    print_header("Paper Validation")

    # ---------------- Missing ----------------

    validate_missing_paper_id(papers)

    validate_missing_title(papers)

    validate_missing_abstract(papers)

    validate_missing_doi(papers)

    # ---------------- Duplicate ----------------

    validate_duplicate_paper_id(papers)

    # ---------------- Invalid ----------------

    validate_invalid_publication_year(papers)

    validate_invalid_cited_by_count(papers)

    validate_invalid_open_access(papers)

    # ---------------- Language ----------------

    validate_language_distribution(papers)

    # ---------------- Title Quality ----------------

    validate_html_entities(papers)

    validate_weird_title(papers)

    # ---------------- Abstract Validation ----------------

    validate_special_characters_in_abstract(papers)

    validate_abstract_whitespace(papers)

    print()

    print("=" * 70)

    print("VALIDATION COMPLETED".center(70))

    print("=" * 70)


if __name__ == "__main__":

    main()