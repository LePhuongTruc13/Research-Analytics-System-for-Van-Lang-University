import pandas as pd

# ==========================================================
# AUTHOR
# ==========================================================
def node_author(
    author_id: str,
    papers_df: pd.DataFrame,
    paper_author_df: pd.DataFrame,
    authors_df: pd.DataFrame,
) -> dict:
    """
    Return detail information for the selected main author.
    """

    author = authors_df.loc[
        authors_df["author_id"].astype(str) == str(author_id)
    ].iloc[0]

    author_papers = paper_author_df[
        paper_author_df["author_id"] == author_id
    ]

    paper_ids = author_papers["paper_id"].unique()

    papers = papers_df[
        papers_df["paper_id"].isin(paper_ids)
    ]

    return {
        "author_id": author_id,
        "author_name": author["author_name"],
        "total_papers": len(paper_ids),
        "total_citations": int(
            papers["cited_by_count"].fillna(0).sum()
        ),
    }

# ==========================================================
# PAPER
# ==========================================================
def node_paper(
    paper_id: str,
    papers_df: pd.DataFrame,
    paper_author_df: pd.DataFrame,
) -> dict:
    """
    Return paper detail.
    """

    paper = papers_df.loc[
        papers_df["paper_id"] == paper_id
    ].iloc[0]

    total_authors = paper_author_df[
        paper_author_df["paper_id"] == paper_id
    ]["author_id"].nunique()

    return {
        "paper_id": paper_id,
        "title": paper["title"],
        "year": int(paper["publication_year"]),
        "citation_count": int(
            paper["cited_by_count"]
        ),
        "total_authors": int(total_authors),
        "abstract": paper["abstract"],
    }

# ==========================================================
# TOPIC
# ==========================================================
def node_topic(
    topic_id: str,
    topics_df: pd.DataFrame,
) -> dict:
    """
    Return topic detail.
    """

    topic = topics_df.loc[
        topics_df["topic_id"].astype(str) == str(topic_id)
    ].iloc[0]

    return {
        "topic_id": topic_id,
        "topic_name": topic["topic_name"],
    }

# ==========================================================
# INSTITUTION
# ==========================================================
def node_institution(
    institution_id: str,
    institutions_df: pd.DataFrame,
    author_institution_df: pd.DataFrame,
) -> dict:
    """
    Return institution detail.
    """

    institution = institutions_df.loc[
        institutions_df["institution_id"].astype(str) == str(institution_id)
    ].iloc[0]

    total_authors = author_institution_df[
        author_institution_df["institution_id"] == institution_id
    ]["author_id"].nunique()

    return {
        "institution_id": institution_id,
        "institution_name": institution["institution_name"],
        "total_authors": int(total_authors),
    }