import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import BERTOPIC_RESULT_DIR

TOPIC_FILE = BERTOPIC_RESULT_DIR / "topics_update.csv"


def load_topics():

    return pd.read_csv(TOPIC_FILE)