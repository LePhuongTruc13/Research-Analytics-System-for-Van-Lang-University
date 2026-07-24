import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import TRANSFORMED_DATA_DIR

AUTHOR_FILE = TRANSFORMED_DATA_DIR / "authors.csv"


def load_authors():

    return pd.read_csv(AUTHOR_FILE)