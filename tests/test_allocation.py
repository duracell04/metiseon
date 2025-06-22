import pandas as pd
import importlib.util
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "allocator.py"
spec = importlib.util.spec_from_file_location("allocator", SRC)
allocator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(allocator)

def test_pick_asset_last_ticker_excluded():
    scores = pd.Series({"A": 10, "B": 20, "C": 5})
    sigma = pd.Series({"A": 0.1, "B": 0.05, "C": 0.15})
    assert allocator.pick_asset(scores, sigma, None) == "B"
    assert allocator.pick_asset(scores, sigma, "B") == "A"
