import numpy as np
import importlib.util
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metior)


def test_schur_complement():
    rho = np.array([[2.0, 0.2, 0.1], [0.2, 2.0, 0.1], [0.1, 0.1, 2.0]])
    ms = metior.MonetarySpace(rho)
    ms.delist(1)
    assert ms.rho.shape == (2, 2)
    assert np.linalg.det(ms.rho) > 0


def test_jump_diffusion_sim():
    jd = metior.JumpDiffusionProcess(0.0, 0.1, 0.2, 0.0, 0.05, 1.0)
    path = jd.sample(0.0, 10)
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
