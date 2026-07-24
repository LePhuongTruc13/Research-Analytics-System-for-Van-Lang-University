import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import NETWORKX_RESULT_DIR

GRAPH_FILE = NETWORKX_RESULT_DIR / "network.json"


def load_network():

    with open(
        GRAPH_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)