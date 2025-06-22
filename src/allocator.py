"""Portfolio allocation helpers."""

from __future__ import annotations

from decimal import Decimal

import pandas as pd


def select_asset(scores: pd.Series, sigma: pd.Series, last_winner: str | None = None) -> str | None:
    """Select the asset to trade."""
    pass


def order_quantity(price: float, cash: float) -> Decimal:
    """Round cash to units based on price."""
    pass


def slippage_bp(quantity: Decimal, adv10: float) -> float:
    """Return slippage in basis points."""
    pass


def should_trade(fee_bp: float, slip_bp: float, cap_bp: float) -> bool:
    """Check if total trading cost is below the cap."""
    pass
