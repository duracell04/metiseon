"""Risk calculations such as volatility, FX beta and CVaR."""

from __future__ import annotations

import numpy as np
import pandas as pd
from arch import arch_model


def garch_sigma(prices: pd.Series, denom_series: pd.Series) -> pd.Series:
    """Estimate conditional volatility via a GARCH(1,1) model.

    Parameters
    ----------
    prices : pandas.Series
        Price series.
    denom_series : pandas.Series
        Series of MEΩ prices aligned to ``prices``.

    Returns
    -------
    pandas.Series
        Conditional volatility aligned with ``log_ret``. Returns an empty
        series when the model cannot be fitted.
    """

    rel = prices / denom_series
    r = np.log(rel).diff().dropna()
    if len(r) < 20:
        return pd.Series(index=prices.index, dtype=float)

    scale = 100.0
    model = arch_model(r * scale, p=1, q=1, mean="zero", vol="GARCH", rescale=False)
    try:
        res = model.fit(disp="off")
    except Exception:
        return pd.Series(index=prices.index, dtype=float)

    sigma = pd.Series(res.conditional_volatility / scale, index=r.index)
    return sigma.reindex(prices.index)


def realised_sigma(
    prices: pd.Series, window: int = 63, denom_series: pd.Series | None = None
) -> pd.Series:
    """Compute historical volatility from a price series.

    Parameters
    ----------
    prices : pandas.Series
        Price observations ordered by time.
    window : int, default 63
        Size of the rolling window in days.

    Returns
    -------
    pandas.Series
        Rolling standard deviation of log returns with NaN for the first
        ``window`` elements.
    """

    prices = prices.sort_index()
    if denom_series is None:
        denom_series = pd.Series(1.0, index=prices.index)
    rel = prices / denom_series
    log_ret = np.log(rel).diff()
    return log_ret.rolling(window=window, min_periods=window).std()


def fx_beta(asset_returns: pd.Series, fx_returns: pd.Series) -> float:
    """Estimate currency beta from asset and FX returns."""

    data = pd.concat([asset_returns, fx_returns], axis=1).dropna()
    if data.empty:
        return float("nan")

    cov = data.iloc[:, 0].cov(data.iloc[:, 1])
    var = data.iloc[:, 1].var()
    return float(cov / var) if var != 0 else float("nan")


def cvar(returns: pd.Series, level: float = 0.95) -> float:
    """Compute the conditional value at risk (CVaR)."""

    r = returns.dropna()
    if r.empty:
        return float("nan")

    var = r.quantile(1 - level)
    tail = r[r <= var]
    if tail.empty:
        return float("nan")

    return float(-tail.mean())


def slipped_cost(qty: float, adv: float) -> float:
    """Almgren-Chriss square-root impact in decimal fraction (e.g., 0.001 = 10bp).
    cost = 0.001 * sqrt(qty / adv)
    """
    if adv <= 0:
        return 0.0
    return float(0.001 * (qty / adv) ** 0.5)
