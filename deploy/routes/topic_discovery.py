import sys
from pathlib import Path

import pandas as pd

# ==========================================================
# Project Path
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# Load Data
# ==========================================================

from deploy.load_data.load_topics import load_topics
from deploy.load_data.load_papers import load_papers
from deploy.load_data.load_authors import load_authors
from deploy.load_data.load_paper_topic import load_paper_topic
from deploy.load_data.load_author_metrics import load_author_metrics
from deploy.load_data.load_paper_author import load_paper_author


# ==========================================================
# Topic List
# ==========================================================

def topic_list(
    topics,
    top_n=30
):
    """
    Return topic list for sidebar.

    Parameters
    ----------
    topics : DataFrame

    top_n : int

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

        [[

            "topic_id",

            "topic_name",

            "paper_count"

        ]]

        .head(top_n)

        .reset_index(drop=True)

    )

    return result


# ==========================================================
# Search Topics
# ==========================================================

def search_topics(
    topics,
    keyword
):
    """
    Search topic by name.

    Parameters
    ----------
    topics : DataFrame

    keyword : str

    Returns
    -------
    DataFrame
    """

    if keyword is None:

        return topic_list(topics)

    keyword = keyword.strip()

    if keyword == "":

        return topic_list(topics)

    result = (

        topics[

            topics["topic_name"]

            .str.contains(

                keyword,

                case=False,

                na=False

            )

        ]

        [[

            "topic_id",

            "topic_name",

            "paper_count"

        ]]

        .sort_values(

            by="paper_count",

            ascending=False

        )

        .reset_index(drop=True)

    )

    return result


# ==========================================================
# Load All Data
# ==========================================================

def load_topic_data():
    """
    Load all datasets required
    for Topic Discovery page.

    Returns
    -------
    dict
    """

    data = {

        "topics":

            load_topics(),

        "papers":

            load_papers(),

        "authors":

            load_authors(),

        "paper_topic":

            load_paper_topic(),

        "author_metrics":

            load_author_metrics(),

        "paper_author":

            load_paper_author()

    }

    return data

# ==========================================================
# Topic Summary
# ==========================================================

def topic_summary(
    topic_id,
    papers,
    paper_topic,
    paper_author,
    author_metrics
):
    """
    Calculate summary metrics
    for one topic.

    Parameters
    ----------
    topic_id : str

    Returns
    -------
    dict
    """

    # ------------------------------------------------------
    # Papers of Topic
    # ------------------------------------------------------

    topic_papers = (

        paper_topic[

            paper_topic["topic_id"] == topic_id

        ][

            "paper_id"

        ]

        .unique()

    )

    # ------------------------------------------------------
    # Paper Table
    # ------------------------------------------------------

    paper_df = papers[

        papers["paper_id"]

        .isin(topic_papers)

    ]

    # ------------------------------------------------------
    # Authors of Topic
    # ------------------------------------------------------

    topic_authors = (

        paper_author[

            paper_author["paper_id"]

            .isin(topic_papers)

        ][

            "author_id"

        ]

        .unique()

    )

    # ------------------------------------------------------
    # Author Metrics
    # ------------------------------------------------------

    metric_df = author_metrics[

        author_metrics["author_id"]

        .isin(topic_authors)

    ]

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    summary = {

        "papers":

            len(topic_papers),

        "authors":

            len(topic_authors),

        "citations":

            int(

                paper_df["cited_by_count"]

                .sum()

            ),

        "average_pagerank":

            round(

                metric_df["pagerank"]

                .mean(),

                6

            )

            if len(metric_df) > 0

            else 0

    }

    return summary

# ==========================================================
# Publication Trend
# ==========================================================

def publication_trend_by_topic(
    topic_id,
    papers,
    paper_topic
):
    """
    Publication trend of one topic.

    Parameters
    ----------
    topic_id : str

    Returns
    -------
    DataFrame

        publication_year

        paper_count
    """

    # ------------------------------------------------------
    # Papers of Topic
    # ------------------------------------------------------

    topic_papers = (

        paper_topic[

            paper_topic["topic_id"] == topic_id

        ][

            "paper_id"

        ]

        .unique()

    )

    # ------------------------------------------------------
    # Paper Table
    # ------------------------------------------------------

    topic_df = papers[

        papers["paper_id"]

        .isin(topic_papers)

    ]

    # ------------------------------------------------------
    # Publication Trend
    # ------------------------------------------------------

    result = (

        topic_df

        .groupby("publication_year")

        .size()

        .reset_index(

            name="paper_count"

        )

        .sort_values(

            by="publication_year"

        )

        .reset_index(drop=True)

    )

    return result

# ==========================================================
# Top Authors
# ==========================================================

def top_authors_by_topic(
    topic_id,
    papers,
    paper_topic,
    paper_author,
    authors,
    top_n=5
):
    """
    Top authors with the most papers
    in one topic.

    Parameters
    ----------
    topic_id : str

    Returns
    -------
    DataFrame

        author_id

        author_name

        paper_count

        citation_count
    """

    # ------------------------------------------------------
    # Papers of Topic
    # ------------------------------------------------------

    topic_papers = (

        paper_topic[

            paper_topic["topic_id"] == topic_id

        ][

            "paper_id"

        ]

        .unique()

    )

    # ------------------------------------------------------
    # Paper -> Author
    # ------------------------------------------------------

    topic_author = (

        paper_author[

            paper_author["paper_id"]

            .isin(topic_papers)

        ]

    )

    # ------------------------------------------------------
    # Paper Citation
    # ------------------------------------------------------

    paper_citation = (

        papers[

            [

                "paper_id",

                "cited_by_count"

            ]

        ]

    )

    # ------------------------------------------------------
    # Merge Citation
    # ------------------------------------------------------

    topic_author = (

        topic_author

        .merge(

            paper_citation,

            on="paper_id",

            how="left"

        )

    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    author_stat = (

        topic_author

        .groupby("author_id")

        .agg(

            paper_count=(

                "paper_id",

                "nunique"

            ),

            citation_count=(

                "cited_by_count",

                "sum"

            )

        )

        .reset_index()

    )

    # ------------------------------------------------------
    # Merge Author Name
    # ------------------------------------------------------

    result = (

        author_stat

        .merge(

            authors,

            on="author_id",

            how="left"

        )

        [[

            "author_id",

            "author_name",

            "paper_count",

            "citation_count"

        ]]

        .sort_values(

            by=[

                "paper_count",

                "citation_count"

            ],

            ascending=False

        )

        .head(top_n)

        .reset_index(drop=True)

    )

    return result

# ==========================================================
# Topic Keywords
# ==========================================================

def topic_keywords(
    topic_id,
    topics,
    top_n=10
):
    """
    Return keywords of one topic.

    Parameters
    ----------
    topic_id : str

    topics : DataFrame

    top_n : int

    Returns
    -------
    list
    """

    # ------------------------------------------------------
    # Find Topic
    # ------------------------------------------------------

    topic = topics[

        topics["topic_id"] == topic_id

    ]

    if topic.empty:

        return []

    # ------------------------------------------------------
    # Get Keywords
    # ------------------------------------------------------

    keywords = topic.iloc[0]["keywords"]

    if pd.isna(keywords):

        return []

    keywords = str(keywords)

    # ------------------------------------------------------
    # Remove []
    # ------------------------------------------------------

    keywords = keywords.replace("[", "")
    keywords = keywords.replace("]", "")
    keywords = keywords.replace("'", "")
    keywords = keywords.replace('"', "")

    # ------------------------------------------------------
    # Split
    # ------------------------------------------------------

    keyword_list = [

        keyword.strip()

        for keyword in keywords.split(",")

        if keyword.strip() != ""

    ]

    return keyword_list[:top_n]

# ==========================================================
# Topic Discovery
# ==========================================================

def topic_discovery(
    topic_id,
    keyword=None
):
    """
    Topic Discovery Page

    Parameters
    ----------
    topic_id : int

    keyword : str

    Returns
    -------
    dict
    """

    # ------------------------------------------------------
    # Load Data
    # ------------------------------------------------------

    data = load_topic_data()

    topics = data["topics"]

    papers = data["papers"]

    authors = data["authors"]

    paper_topic = data["paper_topic"]

    author_metrics = data["author_metrics"]

    paper_author = data["paper_author"]

    # ------------------------------------------------------
    # Topic List
    # ------------------------------------------------------

    if keyword:

        topic_sidebar = search_topics(

            topics,

            keyword

        )

    else:

        topic_sidebar = topic_list(

            topics

        )

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    summary = topic_summary(

        topic_id,

        papers,

        paper_topic,

        paper_author,

        author_metrics

    )

    # ------------------------------------------------------
    # Publication Trend
    # ------------------------------------------------------

    publication = publication_trend_by_topic(

        topic_id,

        papers,

        paper_topic

    )

    # ------------------------------------------------------
    # Top Authors
    # ------------------------------------------------------

    top_authors = top_authors_by_topic(

        topic_id,

        papers,

        paper_topic,

        paper_author,

        authors

    )

    # ------------------------------------------------------
    # Keywords
    # ------------------------------------------------------

    keywords = topic_keywords(

        topic_id,

        topics

    )

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {

        "topics":

            topic_sidebar.to_dict(
                "records"
            ),

        "summary":

            summary,

        "publication_trend":

            publication.to_dict(
                "records"
            ),

        "top_authors":

            top_authors.to_dict(
                "records"
            ),

        "keywords":

            keywords

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    # lấy topic đầu tiên để test

    data = load_topic_data()

    first_topic = data["topics"].iloc[0]["topic_id"]

    result = topic_discovery(

        topic_id=first_topic

    )

    print("=" * 70)
    print("TOPIC DISCOVERY".center(70))
    print("=" * 70)

    print()

    print("Summary")
    print("-" * 40)

    for key, value in result["summary"].items():

        print(f"{key:25}: {value}")

    print()

    print("Publication Trend")
    print("-" * 40)

    print(

        pd.DataFrame(

            result["publication_trend"]

        )

    )

    print()

    print("Top Authors")
    print("-" * 40)

    print(

        pd.DataFrame(

            result["top_authors"]

        )

    )

    print()

    print("Keywords")
    print("-" * 40)

    print(

        result["keywords"]

    )

    print()

    print("Topic List")
    print("-" * 40)

    print(

        pd.DataFrame(

            result["topics"]

        ).head()

    )