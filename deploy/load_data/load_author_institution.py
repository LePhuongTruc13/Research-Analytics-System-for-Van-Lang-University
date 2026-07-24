import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import TRANSFORMED_DATA_DIR

AUTHOR_INSTITUTION_FILE = TRANSFORMED_DATA_DIR / "author_institution.csv"


def load_author_institution():

    return pd.read_csv(AUTHOR_INSTITUTION_FILE)