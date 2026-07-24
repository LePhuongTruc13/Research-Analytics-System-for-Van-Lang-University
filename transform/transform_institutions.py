import pandas as pd
from utils.helper import extract_openalex_id

def transform_institutions(papers):

    institutions = {}

    for paper in papers:

        for authorship in paper.get("authorships", []):

            for institution in authorship.get("institutions", []):

                institution_id = extract_openalex_id(
                    institution.get("id")
                )

                if institution_id not in institutions:

                    institutions[institution_id] = {

                        "institution_id": institution_id,

                        "institution_name": institution.get("display_name"),

                        "country_code": institution.get("country_code")
                    }

    df = pd.DataFrame(institutions.values())

    return df