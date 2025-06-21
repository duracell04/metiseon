import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from decimal import Decimal

from src.score import durability_score
from src.allocator import order_quantity, slippage_bp, should_trade
from src.risk import cvar


def test_durability_score():
    row = pd.Series(
        {
            "roe": 0.15,
            "debt_equity": 0.5,
            "profit_margin": 0.2,
            "insider_own": 0.03,
            "rd_to_rev": 0.06,
        }
    )
    assert durability_score(row) == 100


def test_order_and_slippage():
    q = order_quantity(10, 105)
    slip = slippage_bp(q, adv10=1000)
    assert q == Decimal("10.5000")
    assert slip > 0
    assert should_trade(12, slip, 35)


def test_cvar():
    returns = pd.Series([-0.1, 0.02, 0.03, -0.05, 0.01])
    val = cvar(returns)
    assert val < 0
