from __future__ import annotations

import pandas as pd


def durability_score(row: pd.Series) -> float:
    """Compute Durability-Lite score for a single asset.

    Parameters
    ----------
    row : pd.Series
        Must contain columns: 'roe', 'debt_equity', 'profit_margin',
        'insider_own', 'rd_to_rev'.

    Returns
    -------
    float
        Score clamped to [0, 100].
    """
    score = 25
    if row.get("roe", 0) > 0.12:
        score += 20
    if row.get("debt_equity", float("inf")) < 1:
        score += 15
    if row.get("profit_margin", 0) > 0.10:
        score += 15
    if row.get("insider_own", 0) > 0.02:
        score += 10
    if row.get("rd_to_rev", 0) > 0.05:
        score += 15
    if row.get("debt_equity", 0) > 1 and row.get("insider_own", 1) < 0.01:
        score -= 10
    return max(0.0, min(100.0, score))


def apply_scores(df: pd.DataFrame) -> pd.Series:
    """Return Durability scores for all rows."""
    return df.apply(durability_score, axis=1)
