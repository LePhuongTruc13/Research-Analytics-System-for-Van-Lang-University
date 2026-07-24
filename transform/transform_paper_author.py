import pandas as pd

from utils.helper import extract_openalex_id

def transform_paper_author(papers):

    rows = []

    for paper in papers:

        paper_id = extract_openalex_id(
            paper.get("id")
        )

        if paper_id is None:
            continue

        for authorship in paper.get("authorships", []):

            author = authorship.get("author")

            if not author:
                continue

            author_id = extract_openalex_id(
                author.get("id")
            )

            if author_id is None:
                continue

            rows.append({

                "paper_id": paper_id,

                "author_id": author_id

            })

    df = (
        pd.DataFrame(rows)
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return df