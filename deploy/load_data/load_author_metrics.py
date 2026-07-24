import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import NETWORKX_RESULT_DIR

AUTHOR_METRIC_FILE = NETWORKX_RESULT_DIR / "author_metrics.csv"


def load_author_metrics():

    return pd.read_csv(AUTHOR_METRIC_FILE)