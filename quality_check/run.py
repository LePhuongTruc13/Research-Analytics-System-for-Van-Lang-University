from quality_check.paper_quality import paper_quality
from quality_check.author_quality import author_quality
from quality_check.institution_quality import institution_quality


# ==========================================================
# Run Quality Check Pipeline
# ==========================================================

def main():

    print("=" * 70)
    print("START QUALITY CHECK".center(70))
    print("=" * 70)

    # ------------------------------------------------------
    # Paper
    # ------------------------------------------------------

    paper_quality()

    # ------------------------------------------------------
    # Author
    # ------------------------------------------------------

    author_quality()

    # ------------------------------------------------------
    # Institution
    # ------------------------------------------------------

    institution_quality()

    print("\n" + "=" * 70)
    print("QUALITY CHECK COMPLETED".center(70))
    print("=" * 70)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    main()