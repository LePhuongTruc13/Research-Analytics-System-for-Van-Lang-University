from quality_check.load_data import load_cleaned_data
from validation.validation_utils import (
    print_header,
    print_subheader,
    print_summary,
    show_examples,
)


# ==========================================================
# Helper
# ==========================================================

def print_status(name, count):
    """
    Print PASS / FAIL status.
    """

    status = "PASS" if count == 0 else "FAIL"

    print(f"{name:<30}: {status}")

    if count > 0:

        print(f"{'Remaining':<30}: {count}")


# ==========================================================
# Author Quality Check
# ==========================================================

def author_quality():

    papers = load_cleaned_data()

    print_header("Author Quality Check")

    missing_author_id = []
    short_author_name = []

    # ======================================================
    # Scan
    # ======================================================

    for paper in papers:

        paper_id = paper.get("id")

        for authorship in paper.get("authorships", []):

            author = authorship.get("author", {})

            author_id = author.get("id")
            author_name = author.get("display_name")

            record = {

                "paper_id": paper_id,
                "author_id": author_id,
                "author_name": author_name

            }

            # Missing author ID
            if not author_id:

                missing_author_id.append(record)

            # Very short author name
            if (
                author_name
                and len(author_name.strip()) <= 1
            ):

                short_author_name.append(record)

    # ======================================================
    # Details
    # ======================================================

    if missing_author_id:

        print_subheader("Missing Author ID")

        show_examples(missing_author_id)

    if short_author_name:

        print_subheader("Very Short Author Name")

        show_examples(short_author_name)

    # ======================================================
    # Summary
    # ======================================================

    print_header("Author Quality Summary")

    print_summary(
        "Total Papers",
        len(papers)
    )

    print()

    print_status(
        "Missing Author ID",
        len(missing_author_id)
    )

    print_status(
        "Very Short Author Name",
        len(short_author_name)
    )

    print()

    if (

        len(missing_author_id) == 0
        and len(short_author_name) == 0

    ):

        print("Overall Quality               : PASS")

    else:

        print("Overall Quality               : FAIL")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    author_quality()