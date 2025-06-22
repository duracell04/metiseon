"""Risk calculations such as volatility and CVaR."""

from __future__ import annotations

import pandas as pd


def garch_volatility(prices: pd.Series) -> pd.Series:
    """Return conditional volatility from a GARCH(1,1) model."""
    pass


def rolling_std(prices: pd.Series, window: int) -> pd.Series:
    """Simple rolling standard deviation."""
    pass


def fx_beta(asset_returns: pd.Series, fx_returns: pd.Series) -> float:
    """Estimate currency beta."""
    pass


def cvar(returns: pd.Series, level: float = 0.95) -> float:
    """Compute conditional value at risk."""
    pass
