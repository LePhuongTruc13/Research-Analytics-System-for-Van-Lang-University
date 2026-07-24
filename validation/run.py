from validation.paper_validation import main as paper_validation
from validation.author_validation import main as author_validation
from validation.institution_validation import main as institution_validation


def main():

    print("\n" + "=" * 80)
    print("RUNNING DATA VALIDATION".center(80))
    print("=" * 80)

    print("\n[1/3] Paper Validation")
    paper_validation()

    print("\n[2/3] Author Validation")
    author_validation()

    print("\n[3/3] Institution Validation")
    institution_validation()

    print("\n" + "=" * 80)
    print("ALL VALIDATIONS COMPLETED".center(80))
    print("=" * 80)


if __name__ == "__main__":
    main()