"""Data-fetching utilities for the robo allocator.

This module will provide asynchronous retrieval of prices, fundamentals, and
benchmark series. Actual implementations will be added later.
"""

from __future__ import annotations

import pandas as pd


def init_cache(expire_after: int = 86400) -> None:
    """Configure local HTTP caching."""
    pass


def prices(tickers: list[str], start: str, end: str) -> dict[str, pd.DataFrame]:
    """Fetch historical prices for the given tickers."""
    pass


def fundamentals(ticker: str, api_key: str) -> pd.DataFrame:
    """Retrieve company fundamental data."""
    pass


def benchmarks(series: str, start: str, end: str, api_key: str) -> pd.Series:
    """Download benchmark data such as CPI or SOFR."""
    pass
