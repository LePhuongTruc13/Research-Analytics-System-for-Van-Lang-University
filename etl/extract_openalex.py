import json
import math
import requests
from pathlib import Path
from tqdm import tqdm
import sys

# ===========================
# Project Path
# ===========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.path import RAW_DATA_DIR

# ===========================
# Config
# ===========================

BASE_URL = "https://api.openalex.org/works"

INSTITUTION_ID = "I4210123993"      # Van Lang University
PER_PAGE = 200                      # OpenAlex max 200 records/page
TIMEOUT = 30

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ===========================
# Fetch Data
# ===========================

def fetch_page(page: int) -> dict:
    """
    Download one page from OpenAlex
    """

    params = {
        "filter": f"institutions.id:{INSTITUTION_ID}",
        "per-page": PER_PAGE,
        "page": page
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=TIMEOUT
    )

    response.raise_for_status()

    return response.json()


# ===========================
# Save JSON
# ===========================

def save_json(data: dict, page: int):

    file_path = RAW_DATA_DIR / f"page_{page}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


# ===========================
# Main
# ===========================

def main():

    print("=" * 60)
    print("Downloading OpenAlex Data")
    print("=" * 60)

    # -------------------------
    # Lấy trang đầu tiên
    # -------------------------

    first_page = fetch_page(1)

    total_papers = first_page["meta"]["count"]

    total_pages = math.ceil(total_papers / PER_PAGE)

    print(f"Total Papers : {total_papers}")
    print(f"Total Pages  : {total_pages}")

    # Lưu trang đầu
    save_json(first_page, 1)

    # -------------------------
    # Download các trang còn lại
    # -------------------------

    for page in tqdm(range(2, total_pages + 1), desc="Downloading"):

        try:

            data = fetch_page(page)

            save_json(data, page)

        except Exception as e:

            print(f"\nError at page {page}")

            print(e)

            break

    print("\nDownload Completed!")
    print(f"Saved Folder : {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()