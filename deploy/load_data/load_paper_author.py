import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import TRANSFORMED_DATA_DIR

PAPER_AUTHOR_FILE = TRANSFORMED_DATA_DIR / "paper_author.csv"


def load_paper_author():

    return pd.read_csv(PAPER_AUTHOR_FILE)