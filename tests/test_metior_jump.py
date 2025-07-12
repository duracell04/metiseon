import importlib.util
import sys
from pathlib import Path
import numpy as np

SRC = Path(__file__).resolve().parents[1] / "src" / "metior.py"
spec = importlib.util.spec_from_file_location("metior", SRC)
metior = importlib.util.module_from_spec(spec)
sys.modules["metior"] = metior
spec.loader.exec_module(metior)


def test_jump_variance():
    jd = metior.JumpDiffusionProcess(0.0, 0.1, 0.2, 0.0, 0.05)
    x0 = np.zeros(50000)
    path = jd.sample(1, x0)
    final = path[1]
    emp_var = final.var()
    theo_var = (jd.sigma ** 2 + jd.lam * (jd.jump_mu ** 2 + jd.jump_delta ** 2)) * jd.dt
    assert abs(emp_var - theo_var) / theo_var < 0.01



