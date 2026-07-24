import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import BERTOPIC_RESULT_DIR

PAPER_TOPIC_FILE = BERTOPIC_RESULT_DIR / "paper_topic.csv"


def load_paper_topic():

    return pd.read_csv(PAPER_TOPIC_FILE)