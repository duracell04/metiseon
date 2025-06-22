"""Slippage and trading cost helpers."""

from __future__ import annotations

import math


def adv_slip_bps(order_notional: float, adv: float) -> float:
    """Return market impact from order size and ADV.

    Parameters
    ----------
    order_notional : float
        Notional value of the order.
    adv : float
        Average daily traded value (ADV) for the asset.

    Returns
    -------
    float
        Estimated slippage expressed as a decimal fraction where ``0.01``
        corresponds to 1 % (100 bps).  The model applies a square‐root
        volume impact ``0.001 * sqrt(order_notional / adv)`` and enforces
        a 10 bps minimum.
    """

    if order_notional <= 0 or adv <= 0:
        return 0.001

    slip = 0.001 * math.sqrt(order_notional / adv)
    return max(slip, 0.001)
