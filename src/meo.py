import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import Tuple, Dict

import requests
import yfinance as yf
from fredapi import Fred

# Mapping of fiat symbols to FRED M2 series codes
M2_MAP: Dict[str, str] = {
    "USD": "M2SL",
    "EUR": "MYAGM2EZM196N",
    "JPY": "MYAGM2JPM196N",
    "CHF": "MYAGM2CHM196N",
}

_GOLD_STOCK_T = 205_000
_SILVER_STOCK_T = 1_600_000
_OZ_PER_TON = 32150.7


def _fred_series(code: str, as_of: date) -> float | None:
    fred = Fred()
    start = as_of - timedelta(days=90)
    s = fred.get_series(code, observation_start=start)
    s = s.dropna()
    if s.empty:
        return None
    val = s.iloc[-1]
    if (as_of - s.index[-1].date()).days > 60:
        return None
    return float(val)


def _fx_rate(sym: str, as_of: date) -> float:
    if sym == "USD":
        return 1.0
    pair = f"{sym}USD=X"
    df = yf.download(
        pair,
        start=as_of - timedelta(days=7),
        end=as_of + timedelta(days=1),
        progress=False,
        auto_adjust=True,
        threads=False,
    )
    if df.empty:
        return float("nan")
    return float(df["Adj Close"].iloc[-1])


def _crypto_caps(as_of: date) -> Dict[str, float]:
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "ids": "bitcoin,ethereum"}
    data = requests.get(url, params=params, timeout=10).json()
    return {d["symbol"].upper(): d["market_cap"] / 1e9 for d in data}


def fetch_meo_components(as_of: date) -> Tuple[pd.DataFrame, float]:
    rows = []
    for sym, code in M2_MAP.items():
        m2 = _fred_series(code, as_of)
        if m2 is None:
            continue
        fx = _fx_rate(sym, as_of)
        mc_usd = m2 * fx
        rows.append({"symbol": sym, "mc_native": m2, "fx_usd": fx, "mc_usd": mc_usd})

    gold_price = _fred_series("GOLDAMGBD228NLBM", as_of)
    if gold_price:
        mc = _GOLD_STOCK_T * _OZ_PER_TON * gold_price / 1e9
        rows.append({"symbol": "XAU", "mc_native": mc, "fx_usd": 1.0, "mc_usd": mc})

    silver_price = _fred_series("SLVPRUSD", as_of)
    if silver_price:
        mc = _SILVER_STOCK_T * _OZ_PER_TON * silver_price / 1e9
        rows.append({"symbol": "XAG", "mc_native": mc, "fx_usd": 1.0, "mc_usd": mc})

    rows.extend(
        {"symbol": k, "mc_native": v, "fx_usd": 1.0, "mc_usd": v}
        for k, v in _crypto_caps(as_of).items()
    )

    df = pd.DataFrame(rows).set_index("symbol")
    df = df.sort_index()
    m_world = float(df["mc_usd"].sum())
    df["weight"] = df["mc_usd"] / m_world
    df = df.ffill()
    return df, m_world


def meo_price_usd(m_world_usd: float, kappa: float = 1e-6) -> float:
    return kappa * m_world_usd


def meo_cross_price(px_meo_usd: float, fx_j_usd: float) -> float:
    if fx_j_usd == 0:
        return float("nan")
    return px_meo_usd / fx_j_usd
