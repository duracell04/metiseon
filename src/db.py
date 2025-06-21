from __future__ import annotations

import duckdb

SCHEMA_SQL = """
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
    conn = duckdb.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(SCHEMA_SQL)
    return conn
