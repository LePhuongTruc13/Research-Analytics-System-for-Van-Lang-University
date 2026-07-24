import pandas as pd

from utils.helper import extract_openalex_id


def transform_authors(papers):

    authors = {}

    for paper in papers:

        for authorship in paper.get("authorships", []):

            author = authorship.get("author")

            if not author:
                continue

            author_id = extract_openalex_id(
                author.get("id")
            )

            if author_id is None:
                continue

            if author_id not in authors:

                authors[author_id] = {

                    "author_id": author_id,

                    "author_name": author.get("display_name")
                }

    df = (
        pd.DataFrame(authors.values())
        .sort_values("author_name")
        .reset_index(drop=True)
    )

    return df