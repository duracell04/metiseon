import numpy as np
import pandas as pd
import importlib.util
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_schur_complement():
    df = pd.DataFrame(
        [[2.0, 0.2, 0.1], [0.2, 2.0, 0.1], [0.1, 0.1, 2.0]],
        index=["a", "b", "c"],
        columns=["a", "b", "c"],
    )
    ms = metior.MonetarySpace.from_correlation(df)
    ms.delist("b")
    mat = ms.correlation
    assert mat.shape == (2, 2)
    assert np.linalg.det(mat.to_numpy()) > 0


def test_jump_diffusion_sim():
    jd = metior.JumpDiffusionProcess(0.0, 0.1, 0.2, 0.0, 0.05, 1.0)
    path = jd.sample(10, 0.0)
    assert len(path) == 11
    assert np.isfinite(path).all()


def test_evt_threshold():
    np.random.seed(0)
    data = np.random.normal(0, 1, 1000)
    evt = metior.EVTThreshold(0.99)
    thr = evt.fit(data)
    assert thr >= np.quantile(data, 0.99)


def test_benford_error():
    # generate approximate Benford set
    probs = np.log10(1 + 1 / np.arange(1, 10))
    nums = []
    for d, p in enumerate(probs, start=1):
        nums.extend([float(d)] * int(p * 100))
    err = metior.BenfordOptimizer.error(nums)
    assert err < 0.01

