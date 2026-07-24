import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from deploy.load_data.load_papers import load_papers
from deploy.load_data.load_authors import load_authors
from deploy.load_data.load_topics import load_topics
from deploy.load_data.load_institution import load_institutions
from deploy.load_data.load_paper_author import load_paper_author
from deploy.load_data.load_author_institution import load_author_institution
from deploy.load_data.load_author_metrics import load_author_metrics


# ==========================================================
# Summary Cards
# ==========================================================

def total_papers(papers):
    """
    Total number of papers.
    """

    return len(papers)


def total_authors(authors):
    """
    Total number of authors.
    """

    return len(authors)


def total_citations(papers):
    """
    Total citation count.
    """

    return int(
        papers["cited_by_count"].sum()
    )


def total_topics(topics):
    """
    Total BERTopic topics.
    """

    return len(topics)


def average_pagerank(author_metrics):
    """
    Average PageRank.
    """

    return round(

        author_metrics["pagerank"].mean(),

        6

    )

# ==========================================================
# International Collaboration
# ==========================================================

def international_collaboration(
    paper_author,
    author_institution,
    institutions
):
    """
    Count papers with authors from
    two or more different countries.

    Returns
    -------
    int
        Number of international collaboration papers.
    """

    # ------------------------------------------------------
    # Author -> Country
    # ------------------------------------------------------

    author_country = author_institution.merge(

        institutions,

        on="institution_id",

        how="left"

    )[
        [
            "author_id",
            "country_code"
        ]
    ]

    # ------------------------------------------------------
    # Paper -> Author -> Country
    # ------------------------------------------------------

    paper_country = paper_author.merge(

        author_country,

        on="author_id",

        how="left"

    )

    # ------------------------------------------------------
    # Count countries per paper
    # ------------------------------------------------------

    country_count = (

        paper_country

        .dropna(subset=["country_code"])

        .groupby("paper_id")["country_code"]

        .nunique()

    )

    # ------------------------------------------------------
    # >= 2 Countries
    # ------------------------------------------------------

    international = (

        country_count >= 2

    ).sum()

    return int(international)

# ==========================================================
# Charts
# ==========================================================

def publication_trend(papers):
    """
    Number of publications by year.

    Returns
    -------
    DataFrame
        publication_year
        paper_count
    """

    result = (

        papers

        .groupby("publication_year")

        .size()

        .reset_index(name="paper_count")

        .sort_values("publication_year")

    )

    return result


# ==========================================================

def citation_trend(papers):
    """
    Total citations by publication year.

    Returns
    -------
    DataFrame
        publication_year
        total_citations
    """

    result = (

        papers

        .groupby("publication_year")["cited_by_count"]

        .sum()

        .reset_index(name="total_citations")

        .sort_values("publication_year")

    )

    return result


# ==========================================================

def top_topics(topics, top_n=10):
    """
    Top topics by paper count.

    Returns
    -------
    DataFrame
    """

    result = (

        topics

        .sort_values(

            by="paper_count",

            ascending=False

        )

        .head(top_n)

    )

    return result


# ==========================================================

def top_collaboration_countries(
    author_institution,
    institutions,
    top_n=10
):
    """
    Top countries by number of affiliated authors.

    Returns
    -------
    DataFrame
        country_code
        author_count
    """

    collaboration = author_institution.merge(

        institutions,

        on="institution_id",

        how="left"

    )

    result = (

        collaboration

        .groupby("country_code")["author_id"]

        .nunique()

        .reset_index(name="author_count")

        .sort_values(

            by="author_count",

            ascending=False

        )

        .head(top_n)

    )

    return result

# ==========================================================
# Recent Publications
# ==========================================================

def recent_publications(
    papers,
    top_n=10
):
    """
    Most recent publications.

    Returns
    -------
    DataFrame
    """

    result = (

        papers

        .sort_values(

            by="publication_year",

            ascending=False

        )

        [[

            "paper_id",

            "title",

            "publication_year",

            "cited_by_count",

            "is_open_access"

        ]]

        .head(top_n)

    )

    return result


# ==========================================================
# Dashboard
# ==========================================================

def dashboard():
    """
    Dashboard Data.
    """

    # ------------------------------------------------------
    # Load Data
    # ------------------------------------------------------

    papers = load_papers()

    authors = load_authors()

    topics = load_topics()

    institutions = load_institutions()

    paper_author = load_paper_author()

    author_institution = load_author_institution()

    author_metrics = load_author_metrics()

    # ------------------------------------------------------
    # Summary Cards
    # ------------------------------------------------------

    cards = {

        "total_papers":

            total_papers(
                papers
            ),

        "total_authors":

            total_authors(
                authors
            ),

        "total_citations":

            total_citations(
                papers
            ),

        "total_topics":

            total_topics(
                topics
            ),

        "international_collaboration":

            international_collaboration(

                paper_author,

                author_institution,

                institutions

            ),

        "average_pagerank":

            average_pagerank(
                author_metrics
            )

    }

    # ------------------------------------------------------
    # Charts
    # ------------------------------------------------------

    charts = {

        "publication_trend":
            publication_trend(
                papers
            ).to_dict("records"),

        "citation_trend":
            citation_trend(
                papers
            ).to_dict("records"),

        "top_topics":
            top_topics(
                topics
            ).to_dict("records"),

        "top_collaboration_countries":
            top_collaboration_countries(
                author_institution,
                institutions
            ).to_dict("records")

    }

    # ------------------------------------------------------
    # Recent Publications
    # ------------------------------------------------------

    recent = recent_publications(
        papers
    ).to_dict("records")
    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {

        "cards": cards,

        "charts": charts,

        "recent_publications": recent

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    data = dashboard()

    print("=" * 70)
    print("DASHBOARD".center(70))
    print("=" * 70)

    print()

    print("Summary Cards")
    print("-" * 40)

    for key, value in data["cards"].items():

        print(f"{key:35} : {value}")

    print()

    print("Publication Trend")
    print("-" * 40)

    print(
        data["charts"]["publication_trend"].head()
    )

    print()

    print("Citation Trend")
    print("-" * 40)

    print(
        data["charts"]["citation_trend"].head()
    )

    print()

    print("Top Topics")
    print("-" * 40)

    print(
        data["charts"]["top_topics"].head()
    )

    print()

    print("Top Collaboration Countries")
    print("-" * 40)

    print(
        data["charts"]["top_collaboration_countries"].head()
    )

    print()

    print("Recent Publications")
    print("-" * 40)

    print(
        data["recent_publications"]
    )