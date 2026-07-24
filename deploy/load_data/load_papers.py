import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import TRANSFORMED_DATA_DIR

PAPER_FILE = TRANSFORMED_DATA_DIR / "papers.csv"


def load_papers():

    return pd.read_csv(PAPER_FILE)