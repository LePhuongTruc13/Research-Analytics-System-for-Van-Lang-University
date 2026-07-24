import json
import sys
from pathlib import Path
from tqdm import tqdm

# ===========================
# Project Path
# ===========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import RAW_DATA_DIR, PROCESSED_DATA_DIR

OUTPUT_FILE = PROCESSED_DATA_DIR / "clean_papers.json"


# ===========================
# Reconstruct Abstract
# ===========================

def reconstruct_abstract(abstract_index):

    if not abstract_index:
        return None

    words = []

    for word, positions in abstract_index.items():
        for pos in positions:
            words.append((pos, word))

    words.sort(key=lambda x: x[0])

    abstract = " ".join(word for _, word in words)

    return abstract.strip()


# ===========================
# Cleaning
# ===========================

def clean_paper(paper):

    paper["title"] = (paper.get("title") or "").strip()

    doi = paper.get("doi")
    if doi:
        paper["doi"] = doi.strip()

    paper["abstract"] = reconstruct_abstract(
        paper.get("abstract_inverted_index")
    )

    return paper


# ===========================
# Main
# ===========================

def main():

    print("=" * 60)
    print("Cleaning OpenAlex Data")
    print("=" * 60)

    all_papers = []
    paper_ids = set()

    json_files = sorted(RAW_DATA_DIR.glob("page_*.json"))

    print(f"Found {len(json_files)} raw files.")

    for file in tqdm(json_files):

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for paper in data["results"]:

            paper_id = paper.get("id")

            if paper_id in paper_ids:
                continue

            paper = clean_paper(paper)

            # No abstract -> leave blank.
            if not paper["abstract"]:
                continue

            paper_ids.add(paper_id)

            all_papers.append(paper)

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            all_papers,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nTotal Papers : {len(all_papers)}")
    print(f"Saved : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()