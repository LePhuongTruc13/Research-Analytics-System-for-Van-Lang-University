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
# Institution Quality Check
# ==========================================================

def institution_quality():

    papers = load_cleaned_data()

    print_header("Institution Quality Check")

    missing_institution_id = []
    missing_institution_name = []
    missing_country_code = []

    # ======================================================
    # Scan
    # ======================================================

    for paper in papers:

        paper_id = paper.get("id")

        for authorship in paper.get("authorships", []):

            for institution in authorship.get("institutions", []):

                institution_id = institution.get("id")
                institution_name = institution.get("display_name")
                country_code = institution.get("country_code")

                record = {
                    "paper_id": paper_id,
                    "institution_id": institution_id,
                    "institution_name": institution_name,
                    "country_code": country_code
                }

                # Missing institution_id
                if not institution_id:
                    missing_institution_id.append(record)

                # Missing institution_name
                if not institution_name:
                    missing_institution_name.append(record)

                # Missing country_code
                if not country_code:
                    missing_country_code.append(record)

    # ======================================================
    # Details
    # ======================================================

    if missing_institution_id:

        print_subheader("Missing Institution ID")

        show_examples(missing_institution_id)

    if missing_institution_name:

        print_subheader("Missing Institution Name")

        show_examples(missing_institution_name)

    if missing_country_code:

        print_subheader("Missing Country Code")

        show_examples(missing_country_code)

    # ======================================================
    # Summary
    # ======================================================

    print_header("Institution Quality Summary")

    print_summary(
        "Total Papers",
        len(papers)
    )

    print()

    print_status(
        "Missing Institution ID",
        len(missing_institution_id)
    )

    print_status(
        "Missing Institution Name",
        len(missing_institution_name)
    )

    print_status(
        "Missing Country Code",
        len(missing_country_code)
    )

    print()

    if (
        len(missing_institution_id) == 0
        and len(missing_institution_name) == 0
        and len(missing_country_code) == 0
    ):

        print("Overall Quality               : PASS")

    else:

        print("Overall Quality               : FAIL")


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    institution_quality()