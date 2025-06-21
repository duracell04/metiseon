from __future__ import annotations

import pandas as pd
import numpy as np
from arch import arch_model


def garch_volatility(prices: pd.Series) -> pd.Series:
    """Return conditional volatility from a simple GARCH(1,1) model."""
    returns = np.log(prices / prices.shift(1)).dropna() * 100
    if len(returns) < 10:
        return pd.Series(dtype=float)
    am = arch_model(returns, p=1, q=1)
    res = am.fit(disp="off")
    vol = res.conditional_volatility / 100
    vol.index = prices.index[1:]
    return vol


def rolling_std(prices: pd.Series, window: int) -> pd.Series:
    returns = np.log(prices / prices.shift(1))
    return returns.rolling(window).std().dropna()


def fx_beta(asset_returns: pd.Series, fx_returns: pd.Series) -> float:
    common = pd.concat([asset_returns, fx_returns], axis=1).dropna()
    if common.empty:
        return 0.0
    cov = common.iloc[:, 0].cov(common.iloc[:, 1])
    var = common.iloc[:, 1].var()
    return 0.0 if var == 0 else cov / var


def cvar(returns: pd.Series, level: float = 0.95) -> float:
    if returns.empty:
        return 0.0
    cutoff = returns.quantile(1 - level)
    tail = returns[returns <= cutoff]
    return tail.mean()
