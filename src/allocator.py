from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

import pandas as pd


def select_asset(scores: pd.Series, sigma: pd.Series, last_winner: str | None = None) -> str | None:
    """Return ticker with highest score passing risk filter."""
    candidates = scores.index
    if last_winner in candidates:
        candidates = candidates.drop(last_winner)
    risk_gate = sigma.loc[candidates] <= sigma.median()
    filtered = scores.loc[candidates][risk_gate]
    if filtered.empty:
        return None
    max_score = filtered.max()
    best = filtered[filtered == max_score]
    if len(best) > 1:
        sig_sub = sigma[best.index]
        return sig_sub.idxmin()
    return best.idxmax()


def order_quantity(price: float, cash: float) -> Decimal:
    q = Decimal(cash) / Decimal(price)
    return q.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def slippage_bp(quantity: Decimal, adv10: float) -> float:
    if adv10 <= 0:
        return 0.0
    slip_decimal = 0.001 * ((float(quantity) / adv10) ** 0.5)
    return slip_decimal * 10000


def should_trade(fee_bp: float, slip_bp: float, cap_bp: float) -> bool:
    return fee_bp + slip_bp <= cap_bp
