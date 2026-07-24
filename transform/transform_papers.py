import pandas as pd
from utils.helper import extract_openalex_id

def transform_papers(papers: list) -> pd.DataFrame:
    
    rows = []

    for paper in papers:

        rows.append({
            "paper_id": extract_openalex_id(paper.get("id")),
            "doi": paper.get("doi"),                                                                                                                                    
            "title": paper.get("title"),
            "abstract": paper.get("abstract"),
            "publication_year": paper.get("publication_year"),
            "cited_by_count": paper.get("cited_by_count"),
            "is_open_access": paper.get("open_access", {}).get("is_oa")
        })

    df = pd.DataFrame(rows)

    return df



























2355555555557