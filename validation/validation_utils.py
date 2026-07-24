from pathlib import Path
import html
import re


# ==========================================================
# Report Formatting
# ==========================================================

def print_header(title: str):
    """
    Print section header.
    """

    print("\n" + "=" * 70)
    print(title.upper().center(70))
    print("=" * 70)


def print_subheader(title: str):
    """
    Print subsection header.
    """

    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)


def print_summary(label: str, value):
    """
    Print aligned summary.
    """

    print(f"{label:<35}: {value}")


# ==========================================================
# Display Helpers
# ==========================================================

def show_examples(records, limit=5):
    """
    Display the first few problematic records.
    """

    if not records:
        print("No records found.")
        return

    for i, record in enumerate(records[:limit], start=1):

        print(f"\n[{i}]")

        for key, value in record.items():
            print(f"{key:<15}: {value}")

    if len(records) > limit:

        print(f"\n... {len(records) - limit} more records.")


# ==========================================================
# Text Validation
# ==========================================================

def contains_html_entities(text: str) -> bool:
    """
    Check whether text contains HTML entities.
    """

    if not text:
        return False

    return html.unescape(text) != text


def special_character_ratio(text: str) -> float:
    """
    Calculate ratio of special characters.
    """

    if not text:
        return 0

    special = len(re.findall(r"[^A-Za-z0-9\s]", text))

    return special / len(text)


def has_many_special_characters(
    text: str,
    threshold: float = 0.30
) -> bool:
    """
    Determine whether text contains too many special characters.
    """

    return special_character_ratio(text) > threshold


# ==========================================================
# Separator
# ==========================================================

def print_separator():
    """
    Print separator line.
    """

    print("-" * 70)


# ==========================================================
# Report Output
# ==========================================================

def save_report(text: str, filename: str):
    """
    Save validation report to reports/validation.
    """

    report_dir = Path("reports") / "validation"

    report_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = report_dir / filename

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

    print(f"\nReport saved to: {output_file}")