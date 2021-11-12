from pathlib import Path
from difflib import SequenceMatcher

def get_project_root() -> Path:
    return Path(__file__).parent

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

