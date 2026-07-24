import pandas as pd

# ============================================================
# FUNCTION: FILTER PAPERS BY TOPIC
# ============================================================
def filter_papers_by_topic(
    papers_df: pd.DataFrame,
    paper_topic_df: pd.DataFrame,
    topic_id: int
) -> pd.DataFrame:
   
    # ========================================================
    # CHECK REQUIRED COLUMNS
    # ========================================================
    if "paper_id" not in papers_df.columns:
        raise ValueError(
            "Không tìm thấy column 'paper_id' trong papers dataframe"
        )

    required_columns = {
        "paper_id",
        "topic_id"
    }

    missing_columns = required_columns - set(
        paper_topic_df.columns
    )


    if missing_columns:
        raise ValueError(
            f"Thiếu column trong paper_topic dataframe: {missing_columns}"
        )

    # ========================================================
    # GET PAPER IDS OF SELECTED TOPIC
    # ========================================================
    topic_papers = paper_topic_df[
        paper_topic_df["topic_id"] == topic_id
    ]


    paper_ids = topic_papers["paper_id"].unique()

    # ========================================================
    # FILTER PAPERS
    # ========================================================

    filtered_papers = papers_df[
        papers_df["paper_id"].isin(
            paper_ids
        )
    ].copy()

    # ========================================================
    # RESET INDEX
    # ========================================================
    filtered_papers.reset_index(
        drop=True,
        inplace=True
    )

    # ========================================================
    # CONVERT ALL MISSING VALUES
    #
    # NaN
    # pd.NA
    # NaT
    #
    # ---------------> None
    # ========================================================
    filtered_papers = (
        filtered_papers
        .astype(object)
        .where(
            pd.notnull(filtered_papers),
            None
        )
    )

    return filtered_papers
