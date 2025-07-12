from decimal import Decimal
from datetime import datetime
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src import ledger


def test_nav_meo_basic(tmp_path):
    db_path = tmp_path / "p.db"
    book = ledger.Ledger(str(db_path))
    ts = datetime(2024, 1, 1)
    book.book_trade(ts, "AAA", Decimal("1"), 10.0)
    book.book_trade(ts, "BBB", Decimal("2"), 20.0)
    prices = pd.Series({"AAA": 10.0, "BBB": 20.0})
    meo_usd = 10.0
    nav = book.nav_meo(prices, meo_usd)
    assert nav == Decimal("5")
