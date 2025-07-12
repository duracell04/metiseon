import importlib.util
import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_replicator_step_simplex():
    w = np.array([0.4, 0.6])
    r = np.array([0.01, -0.02])
    s = np.array([0.1, 0.1])
    new_w = metior.ReplicatorDynamics.step(w, r, s)
    assert np.isclose(new_w.sum(), 1.0)
    assert (new_w >= 0).all() and (new_w <= 1).all()


def test_replicator_stream():
    returns = [[0.01, -0.02]] * 3
    sigmas = [[0.1, 0.1]] * 3
    stream = metior.ReplicatorDynamics.stream(returns, sigmas, [0.5, 0.5])
    out = list(stream)
    assert len(out) == 3
    assert np.isclose(out[-1].sum(), 1.0)

