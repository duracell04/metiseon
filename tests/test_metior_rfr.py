import importlib.util
import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_rfr_methods():
    mc = [1, 1]
    illiq = [0.1, 0.2]
    y = [0.02, 0.03]
    amihud = metior.RiskFreeRate.compute(mc, illiq, y)
    uniform = metior.RiskFreeRate.compute(mc, illiq, y, method="uniform")
    assert amihud != uniform
    assert np.isclose(uniform, np.mean(y))


