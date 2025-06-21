from __future__ import annotations

import asyncio
from functools import partial
from typing import Iterable

import pandas as pd
import requests_cache
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData
from fredapi import Fred


CACHE_NAME = "metiseon_cache"


def init_cache(expire_after: int = 86400) -> None:
    requests_cache.install_cache(CACHE_NAME, expire_after=expire_after)


async def _fetch_yf(ticker: str, start: str, end: str) -> pd.DataFrame:
    return yf.download(ticker, start=start, end=end, progress=False)


async def prices(tickers: Iterable[str], start: str, end: str) -> dict[str, pd.DataFrame]:
    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, partial(yf.download, t, start=start, end=end, progress=False)) for t in tickers]
    data = await asyncio.gather(*tasks)
    return dict(zip(tickers, data))


def fundamentals(ticker: str, api_key: str) -> pd.DataFrame:
    fd = FundamentalData(key=api_key)
    data, _ = fd.get_company_overview(symbol=ticker)
    return pd.DataFrame([data])


def benchmarks(series: str, start: str, end: str, api_key: str) -> pd.Series:
    fred = Fred(api_key=api_key)
    data = fred.get_series(series, observation_start=start, observation_end=end)
    return data
