from __future__ import annotations

import asyncio
from datetime import datetime

import pandas as pd
import requests_cache
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData

# Enable local HTTP caching for all network calls
requests_cache.install_cache("metiseon_cache", expire_after=86400)

async def fetch_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Fetch Yahoo Finance prices asynchronously.

    Parameters
    ----------
    tickers : list[str]
        Symbols understood by Yahoo Finance.
    start : str
        Inclusive start date (YYYY-MM-DD).
    end : str
        Exclusive end date (YYYY-MM-DD).

    Returns
    -------
    pd.DataFrame
        Multi-index columns ``(ticker, field)`` with fields ``adj_close`` and
        ``volume``. Missing values are forward-filled.
    """

    async def _download(ticker: str) -> pd.DataFrame:
        return await asyncio.to_thread(
            yf.download,
            ticker,
            start=start,
            end=end,
            progress=False,
            auto_adjust=True,
            threads=False,
        )

    results = await asyncio.gather(*[_download(t) for t in tickers])

    frames = []
    for t, df in zip(tickers, results):
        if df.empty:
            continue
        df = df[["Adj Close", "Volume"]].rename(
            columns={"Adj Close": "adj_close", "Volume": "volume"}
        )
        df.columns = pd.MultiIndex.from_product([[t], df.columns])
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, axis=1).sort_index()
    return combined.ffill()


async def fetch_fundamentals(tickers: list[str]) -> pd.DataFrame:
    """Retrieve fundamental ratios using the AlphaVantage demo API.

    Parameters
    ----------
    tickers : list[str]
        Company symbols to query.

    Returns
    -------
    pd.DataFrame
        Frame indexed by ticker with columns ``date``, ``roe``, ``debt_equity``,
        ``profit_margin``, ``rd_to_rev`` and ``insider_own``. Missing values are
        forward-filled.
    """

    today = pd.Timestamp.utcnow().normalize()

    async def _fetch(ticker: str) -> pd.Series:
        fd = FundamentalData(key="demo")
        overview, _ = await asyncio.to_thread(fd.get_company_overview, ticker)
        income, _ = await asyncio.to_thread(fd.get_income_statement_annual, ticker)
        balance, _ = await asyncio.to_thread(fd.get_balance_sheet_annual, ticker)

        roe = pd.to_numeric(overview.get("ReturnOnEquityTTM"), errors="coerce")
        profit_margin = pd.to_numeric(overview.get("ProfitMargin"), errors="coerce")

        debt_equity = pd.NA
        if not balance.empty:
            latest = balance.iloc[0]
            liabilities = pd.to_numeric(latest.get("totalLiabilities"), errors="coerce")
            equity = pd.to_numeric(
                latest.get("totalShareholderEquity"), errors="coerce"
            )
            if pd.notna(liabilities) and pd.notna(equity) and equity != 0:
                debt_equity = liabilities / equity

        rd_to_rev = pd.NA
        if not income.empty:
            latest = income.iloc[0]
            rd = pd.to_numeric(latest.get("researchAndDevelopment"), errors="coerce")
            rev = pd.to_numeric(latest.get("totalRevenue"), errors="coerce")
            if pd.notna(rd) and pd.notna(rev) and rev != 0:
                rd_to_rev = rd / rev

        insider_own = pd.NA  # not available from demo endpoint

        return pd.Series(
            {
                "ticker": ticker,
                "date": today,
                "roe": roe,
                "debt_equity": debt_equity,
                "profit_margin": profit_margin,
                "rd_to_rev": rd_to_rev,
                "insider_own": insider_own,
            }
        )

    rows = await asyncio.gather(*[_fetch(t) for t in tickers])
    df = pd.DataFrame(rows).set_index("ticker")
    return df.ffill()
