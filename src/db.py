"""DuckDB helper functions."""

from __future__ import annotations

import duckdb


SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS trades (
    ts TIMESTAMP,
    ticker TEXT,
    qty DOUBLE,
    price DOUBLE,
    fee DOUBLE,
    PRIMARY KEY (ts, ticker)
);

CREATE TABLE IF NOT EXISTS positions (
    ts TIMESTAMP,
    ticker TEXT,
    qty DOUBLE,
    cost_basis DOUBLE,
    nav DOUBLE
);
"""


def connect(path: str) -> duckdb.DuckDBPyConnection:
    """Return a connection to the portfolio database."""
    con = duckdb.connect(path)
    con.execute(SCHEMA_SQL)
    return con
