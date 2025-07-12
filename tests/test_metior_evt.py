import importlib.util
import sys
from pathlib import Path
import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_evt_small_sample():
    evt = metior.EVTThreshold()
    with pytest.raises(ValueError):
        evt.fit([1, 2, 3])


def test_evt_fit_lambda():
    np.random.seed(0)
    data = np.random.normal(0, 1, 100)
    evt = metior.EVTThreshold(0.95)
    thr = evt.fit(data)
    assert thr >= np.quantile(data, 0.95)
    assert evt.lambda_ > 0


