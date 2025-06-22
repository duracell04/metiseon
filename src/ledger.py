"""Portfolio ledger backed by DuckDB."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

import duckdb

from . import db


class Ledger:
    """Simple trading ledger.

    Parameters
    ----------
    path : str
        File path to the DuckDB database.
    """

    def __init__(self, path: str) -> None:
        self.con: duckdb.DuckDBPyConnection = db.connect(path)

    def book_trade(
        self,
        ts: datetime,
        ticker: str,
        qty: float | Decimal,
        price: float,
        fee: float = 0.0,
    ) -> None:
        """Record a trade and update positions."""

        quantity = float(qty)
        self.con.execute(
            "INSERT INTO trades VALUES (?, ?, ?, ?, ?)",
            (ts, ticker, quantity, price, fee),
        )

        prev = self.con.execute(
            "SELECT qty, cost_basis FROM positions WHERE ticker = ? ORDER BY ts DESC LIMIT 1",
            (ticker,),
        ).fetchone()
        if prev is None:
            prev_qty = 0.0
            prev_cost = 0.0
        else:
            prev_qty = float(prev[0])
            prev_cost = float(prev[1])

        new_qty = prev_qty + quantity
        if new_qty == 0:
            new_cost = 0.0
        else:
            new_cost = (prev_qty * prev_cost + quantity * price + fee) / new_qty

        nav = new_qty * price
        self.con.execute(
            "INSERT INTO positions VALUES (?, ?, ?, ?, ?)",
            (ts, ticker, new_qty, new_cost, nav),
        )
        self.con.commit()

    def nav(self) -> float:
        """Return current portfolio NAV."""

        result = self.con.execute(
            """
            SELECT SUM(nav) FROM (
                SELECT nav, ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY ts DESC) AS r
                FROM positions
            ) WHERE r = 1
            """
        ).fetchone()
        return float(result[0]) if result and result[0] is not None else 0.0

    def last_ticker(self) -> str | None:
        """Return the most recently traded ticker, if any."""

        row = self.con.execute(
            "SELECT ticker FROM trades ORDER BY ts DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else None
