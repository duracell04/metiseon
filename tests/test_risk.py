import numpy as np
import pandas as pd
import importlib.util
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "risk.py"
spec = importlib.util.spec_from_file_location("risk", SRC)
risk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(risk)

def test_garch_sigma_positive_finite():
    np.random.seed(0)
    returns = pd.Series(np.random.normal(0, 0.01, 60))
    sigma = risk.garch_sigma(returns)
    assert (sigma.dropna() > 0).all()
    assert np.isfinite(sigma).all()
