import importlib.util
import sys
from pathlib import Path
import numpy as np
import pandas as pd

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_schur_pd():
    df = pd.DataFrame(
        [[1.0, 0.2, 0.1], [0.2, 1.0, 0.1], [0.1, 0.1, 1.0]],
        index=["a", "b", "c"],
        columns=["a", "b", "c"],
    )
    ms = metior.MonetarySpace.from_correlation(df)
    ms.delist("b")
    mat = ms.correlation
    assert mat.shape == (2, 2)
    assert np.linalg.det(mat.to_numpy()) > 0

