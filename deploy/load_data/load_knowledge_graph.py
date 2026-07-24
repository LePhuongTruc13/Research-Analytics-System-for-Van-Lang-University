import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
from utils.path import KNOWLEDGE_GRAPH_RESULT_DIR

GRAPH_FILE = KNOWLEDGE_GRAPH_RESULT_DIR / "knowledge_graph.json"


def load_knowledge_graph():

    with open(
        GRAPH_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)