import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from utils.path import TRANSFORMED_DATA_DIR

from transform.load_data import load_clean_data
from transform.export_csv import export_csv

from transform.transform_papers import transform_papers
from transform.transform_authors import transform_authors
from transform.transform_institutions import transform_institutions
from transform.transform_paper_author import transform_paper_author
from transform.transform_author_institution import transform_author_institution


def main():

    print("=" * 50)
    print("Transform OpenAlex Data")
    print("=" * 50)

    # Load cleaned data
    papers = load_clean_data()

    # Transform
    papers_df = transform_papers(papers)
    authors_df = transform_authors(papers)
    institutions_df = transform_institutions(papers)
    paper_author_df = transform_paper_author(papers)
    author_institution_df = transform_author_institution(papers)

    # Export CSV
    export_csv(
        papers_df,
        TRANSFORMED_DATA_DIR / "papers.csv"
    )

    export_csv(
        authors_df,
        TRANSFORMED_DATA_DIR / "authors.csv"
    )

    export_csv(
        institutions_df,
        TRANSFORMED_DATA_DIR / "institutions.csv"
    )

    export_csv(
        paper_author_df,
        TRANSFORMED_DATA_DIR / "paper_author.csv"
    )

    export_csv(
        author_institution_df,
        TRANSFORMED_DATA_DIR / "author_institution.csv"
    )

    print("\nTransform completed!")


if __name__ == "__main__":
    main()