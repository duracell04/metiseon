import pandas as pd
import importlib.util
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "score.py"
spec = importlib.util.spec_from_file_location("score", SRC)
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

def test_apply_scores_vector():
    df = pd.DataFrame({
        "roe": [0.15, 0.1, 0.15],
        "debt_equity": [0.5, 1.2, 1.5],
        "profit_margin": [0.2, 0.05, 0.2],
        "insider_own": [0.03, 0.005, 0.005],
        "rd_to_rev": [0.06, 0.1, 0.06],
    }, index=list("ABC"))
    expected = pd.Series([100, 30, 65], index=list("ABC"))
    result = score.apply_scores(df)
    pd.testing.assert_series_equal(result, expected)
