import pandas as pd

# ==========================================================
# FILTER AUTHORS
# ==========================================================
def filter_authors(
    authors_df: pd.DataFrame,
) -> pd.DataFrame:
    return (
        authors_df[["author_id", "author_name"]]
        .drop_duplicates()
        .sort_values(by="author_name")
        .reset_index(drop=True)
    )

