import pandas as pd

from utils.helper import extract_openalex_id


def transform_author_institution(papers):

    rows = []

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

            for institution in authorship.get("institutions", []):

                institution_id = extract_openalex_id(
                    institution.get("id")
                )

                if institution_id is None:
                    continue

                rows.append({

                    "author_id": author_id,

                    "institution_id": institution_id

                })

    df = (
        pd.DataFrame(rows)
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return df