from collections import Counter

from quality_check.load_data import load_cleaned_data
from validation.validation_utils import (
    print_header,
    print_subheader,
    print_summary,
    show_examples,
    contains_html_entities,
    has_many_special_characters,
)


# ==========================================================
# Paper Quality Check
# ==========================================================

def paper_quality():

    papers = load_cleaned_data()

    print_header("Paper Quality Check")

    missing_title = []
    missing_doi = []
    missing_abstract = []

    html_titles = []

    weird_titles = []
    weird_abstracts = []

    # ======================================================
    # Scan
    # ======================================================

    for paper in papers:

        paper_id = paper.get("id")
        title = paper.get("title")
        abstract = paper.get("abstract")
        doi = paper.get("doi")

        record = {

            "paper_id": paper_id,
            "title": title,
            "abstract": abstract,
            "doi": doi

        }

        # --------------------------------------------------
        # Missing Title
        # --------------------------------------------------

        if not title or not title.strip():

            missing_title.append(record)

        # --------------------------------------------------
        # Missing Abstract
        # --------------------------------------------------

        if not abstract or not abstract.strip():

            missing_abstract.append(record)

        # --------------------------------------------------
        # Missing DOI
        # --------------------------------------------------

        if not doi:

            missing_doi.append(record)

        # --------------------------------------------------
        # HTML Entities
        # --------------------------------------------------

        if title and contains_html_entities(title):

            html_titles.append(record)

        # --------------------------------------------------
        # Weird Title
        # --------------------------------------------------

        if title and has_many_special_characters(title):

            weird_titles.append(record)

        # --------------------------------------------------
        # Weird Abstract
        # --------------------------------------------------

        if abstract and has_many_special_characters(abstract):

            weird_abstracts.append(record)

    # ======================================================
    # Missing Title
    # ======================================================

    print_subheader("Missing Title")

    print_summary(
        "Found",
        len(missing_title)
    )

    show_examples(missing_title)

    # ======================================================
    # Missing Abstract
    # ======================================================

    print_subheader("Missing Abstract")

    print_summary(
        "Found",
        len(missing_abstract)
    )

    show_examples(missing_abstract)

    # ======================================================
    # Missing DOI
    # ======================================================

    print_subheader("Missing DOI")

    print_summary(
        "Found",
        len(missing_doi)
    )

    show_examples(missing_doi)

    # ======================================================
    # HTML Entities
    # ======================================================

    print_subheader("Titles Containing HTML Entities")

    print_summary(
        "Found",
        len(html_titles)
    )

    show_examples(html_titles)

    # ======================================================
    # Weird Titles
    # ======================================================

    print_subheader("Weird Titles")

    print_summary(
        "Found",
        len(weird_titles)
    )

    show_examples(weird_titles)

    # ======================================================
    # Weird Abstracts
    # ======================================================

    print_subheader("Weird Abstracts")

    print_summary(
        "Found",
        len(weird_abstracts)
    )

    show_examples(weird_abstracts)

    # ======================================================
    # Summary
    # ======================================================

    print_header("Paper Quality Summary")

    print_summary(
        "Total Papers",
        len(papers)
    )

    print_summary(
        "Missing Title",
        len(missing_title)
    )

    print_summary(
        "Missing Abstract",
        len(missing_abstract)
    )

    print_summary(
        "Missing DOI",
        len(missing_doi)
    )

    print_summary(
        "HTML Entities",
        len(html_titles)
    )

    print_summary(
        "Weird Titles",
        len(weird_titles)
    )

    print_summary(
        "Weird Abstracts",
        len(weird_abstracts)
    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    paper_quality()