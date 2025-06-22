"""Portfolio allocation helpers."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

import pandas as pd


def pick_asset(scores: pd.Series, sigma: pd.Series, last_winner: str | None = None) -> str | None:
    """Return the ticker with the highest score passing the risk filter."""

    candidates = scores.index
    if last_winner is not None and last_winner in candidates:
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


def size_trade(price: float, cash: float) -> Decimal:
    """Size the trade in units rounded to four decimals."""

    if price <= 0:
        return Decimal("0")

    qty = Decimal(str(cash)) / Decimal(str(price))
    return qty.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def decision_block(quantity: Decimal, adv10: float, fee_bp: float, cap_bp: float) -> bool:
    """Return ``True`` if total cost from fee and slippage is acceptable."""

    if adv10 <= 0:
        slip_bp = 0.0
    else:
        slip_decimal = 0.001 * ((float(quantity) / adv10) ** 0.5)
        slip_bp = slip_decimal * 10000

    return fee_bp + slip_bp <= cap_bp
