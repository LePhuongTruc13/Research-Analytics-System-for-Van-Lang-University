import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import TRANSFORMED_DATA_DIR

INSTITUTION_FILE = TRANSFORMED_DATA_DIR / "institutions.csv"


def load_institutions():

    return pd.read_csv(INSTITUTION_FILE)