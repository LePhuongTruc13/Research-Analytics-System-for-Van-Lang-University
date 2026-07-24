import pandas as pd

def filter_papers_by_year(
    papers_df: pd.DataFrame,
    year: int
) -> pd.DataFrame:

    if "publication_year" not in papers_df.columns:
        raise ValueError(
            "Không tìm thấy column 'publication_year'"
        )

    filtered_papers = papers_df[
        papers_df["publication_year"] == year
    ]

    return filtered_papers.reset_index(
        drop=True
    )
