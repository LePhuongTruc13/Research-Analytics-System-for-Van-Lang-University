import csv
import sys 
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from utils.path import INSTITUTION_REPORT_DIR

from collections import Counter

from validation.load_data import load_clean_data

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

def display_institution(institution):
    """
    Display institution information.
    """

    print(f"Institution ID     : {institution['institution_id']}")
    print(f"Institution Name   : {institution['institution_name']}")
    print(f"Country Code       : {institution['country_code']}")

    print_separator()


# ==========================================================
# Missing Validation
# ==========================================================

def validate_missing_institution_id(institutions):

    print_subheader("Missing Institution ID")

    missing = [

        institution

        for institution in institutions

        if not institution["institution_id"]

    ]

    print_summary("Found", len(missing))

    if missing:

        print()

        for institution in missing[:10]:

            display_institution(institution)


def validate_missing_institution_name(institutions):

    print_subheader("Missing Institution Name")

    missing = [

        institution

        for institution in institutions

        if (
            not institution["institution_name"]
            or not institution["institution_name"].strip()
        )

    ]

    print_summary("Found", len(missing))

    if missing:

        print()

        for institution in missing[:10]:

            display_institution(institution)


def validate_missing_country_code(institutions):

    print_subheader("Missing Country Code")

    missing = [

        institution

        for institution in institutions

        if (
            not institution["country_code"]
            or not str(institution["country_code"]).strip()
        )

    ]

    print_summary("Found", len(missing))

    # Export missing country codes
    output_file = INSTITUTION_REPORT_DIR / "missing_country_code.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "institution_id",
            "institution_name",
            "country_code"
        ])

        for institution in missing:

            writer.writerow([
                institution["institution_id"],
                institution["institution_name"],
                institution["country_code"]
            ])

    print(f"Exported: {output_file}")

    if missing:

        print()

        for institution in missing[:10]:

            display_institution(institution)


# ==========================================================
# Institution Name Quality
# ==========================================================

def validate_html_entities(institutions):

    print_subheader("Institution Names Containing HTML Entities")

    problems = []

    for institution in institutions:

        name = institution["institution_name"]

        if not name:
            continue

        if contains_html_entities(name):

            problems.append(institution)

    print_summary("Found", len(problems))

    if problems:

        print()

        for institution in problems[:10]:

            display_institution(institution)


def validate_leading_trailing_spaces(institutions):

    print_subheader("Institution Names With Leading / Trailing Spaces")

    problems = []

    for institution in institutions:

        name = institution["institution_name"]

        if not name:
            continue

        if name != name.strip():

            problems.append(institution)

    print_summary("Found", len(problems))

    if problems:

        print()

        for institution in problems[:10]:

            display_institution(institution)


# ==========================================================
# Extract Institution Records
# ==========================================================

def extract_institutions(papers):
    """
    Extract institution records from cleaned papers.
    """

    institutions = []

    for paper in papers:

        for authorship in paper.get("authorships", []):

            for institution in authorship.get("institutions", []):

                institutions.append({

                    "institution_id": institution.get("id"),

                    "institution_name": institution.get("display_name"),

                    "country_code": institution.get("country_code")

                })

    return institutions


# ==========================================================
# Country Validation
# ==========================================================

def validate_country_distribution(institutions):

    print_subheader("Country Distribution")

    distribution = Counter(

        institution["country_code"]

        for institution in institutions

        if institution["country_code"]

    )

    print()

    print(f"{'Country':<15}{'Count'}")

    print("-" * 30)

    for code, count in sorted(

        distribution.items(),

        key=lambda x: x[1],

        reverse=True

    ):

        print(f"{code:<15}{count}")


def validate_lowercase_country_code(institutions):

    print_subheader("Lowercase Country Code")

    problems = []

    for institution in institutions:

        code = institution["country_code"]

        if not code:
            continue

        if code != code.upper():

            problems.append(institution)

    print_summary("Found", len(problems))

    if problems:

        print()

        for institution in problems[:10]:

            display_institution(institution)


def validate_invalid_country_code_length(institutions):

    print_subheader("Invalid Country Code Length")

    problems = []

    for institution in institutions:

        code = institution["country_code"]

        if not code:
            continue

        if len(code.strip()) != 2:

            problems.append(institution)

    print_summary("Found", len(problems))

    if problems:

        print()

        for institution in problems[:10]:

            display_institution(institution)

def validate_unexpected_country_codes(institutions):

    print_subheader("Unexpected Country Codes")

    distribution = Counter(

        institution["country_code"].strip()

        for institution in institutions

        if institution["country_code"]

    )

    unexpected = []

    for code in sorted(distribution):

        if len(code) != 2:

            unexpected.append(

                (code, distribution[code])

            )

    print_summary("Found", len(unexpected))

    if unexpected:

        print()

        print(f"{'Country Code':<20}{'Count'}")

        print("-" * 35)

        for code, count in unexpected:

            print(f"{code:<20}{count}")


# ==========================================================
# Country Code Normalization Recommendation
# ==========================================================

def recommend_country_code_normalization(institutions):

    print_subheader("Country Code Normalization Recommendation")

    recommendations = []

    for institution in institutions:

        code = institution["country_code"]

        if not code:
            continue

        original = code

        suggested = code.strip().upper()

        if original != suggested:

            recommendations.append({

                "Institution": institution["institution_name"],

                "Original": original,

                "Suggested": suggested

            })

    print_summary("Recommendations", len(recommendations))

    if recommendations:

        print()

        for item in recommendations[:10]:

            print(f"Institution : {item['Institution']}")

            print(f"Original    : {item['Original']}")

            print(f"Suggested   : {item['Suggested']}")

            print_separator()


# ==========================================================
# Main
# ==========================================================

def main():

    papers = load_clean_data()

    institutions = extract_institutions(papers)

    print_header("Institution Validation")

    # ---------------- Missing ----------------

    validate_missing_institution_id(institutions)

    validate_missing_institution_name(institutions)

    validate_missing_country_code(institutions)

    # ---------------- Institution Name ----------------

    validate_html_entities(institutions)

    validate_leading_trailing_spaces(institutions)

    # ---------------- Country ----------------

    validate_country_distribution(institutions)

    validate_lowercase_country_code(institutions)

    validate_invalid_country_code_length(institutions)

    validate_unexpected_country_codes(institutions)

    recommend_country_code_normalization(institutions)

    print()

    print("=" * 70)

    print("VALIDATION COMPLETED".center(70))

    print("=" * 70)


if __name__ == "__main__":

    main()