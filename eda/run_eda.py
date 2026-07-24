from eda.paper_eda import main as paper_eda
from eda.author_eda import main as author_eda
from eda.institution_eda import main as institution_eda


def main():
    """
    Run all Exploratory Data Analysis (EDA).
    """

    print("=" * 60)
    print("Exploratory Data Analysis")
    print("=" * 60)

    print("\n[1/3] Running Paper EDA...")
    paper_eda()

    print("\n[2/3] Running Author EDA...")
    author_eda()

    print("\n[3/3] Running Institution EDA...")
    institution_eda()

    print("\n" + "=" * 60)
    print("EDA completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()