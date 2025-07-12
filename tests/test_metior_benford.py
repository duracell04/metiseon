import importlib.util
import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_benford_error():
    probs = np.log10(1 + 1 / np.arange(1, 10))
    data = []
    for d, p in enumerate(probs, start=1):
        data.extend([float(d)] * int(p * 100))
    err = metior.BenfordOptimizer.error(data)
    assert err < 0.01


def test_benford_uniform():
    data = np.arange(1, 10).repeat(10).astype(float)
    err = metior.BenfordOptimizer.error(data)
    assert 0.005 < err < 0.01

