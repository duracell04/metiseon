import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

SRC = Path(__file__).resolve().parents[1] / "src" / "risk.py"
spec = importlib.util.spec_from_file_location("risk", SRC)
risk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(risk)

def test_garch_sigma_positive_finite():
    np.random.seed(0)
    returns = pd.Series(np.random.normal(0, 0.01, 60))
    denom = pd.Series(1.0, index=returns.index)
    sigma = risk.garch_sigma(returns.cumsum() + 10, denom)
    assert (sigma.dropna() > 0).all()
    assert np.isfinite(sigma.dropna()).all()


def test_slipped_cost():
    from src.risk import slipped_cost
    assert round(slipped_cost(100000, 500000), 5) == 0.00045  # ~4.47bp
    assert slipped_cost(0, 1000000) == 0.0  # Zero case
