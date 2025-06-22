"""Durability scoring helpers.

This module provides a minimal implementation of the so called
"Durability‑Lite" factor used throughout the project.  The calculation is a
simple piece wise deterministic rule set based on a few fundamental ratios.

The expected columns in the input data are ``roe``, ``debt_equity``,
``profit_margin``, ``insider_own`` and ``rd_to_rev`` with values expressed in
fractions (for example ``0.15`` for 15 %).  The resulting score is clamped to
``[0, 100]``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

BASE_SCORE = 25

FACTOR_WEIGHTS = {
    "roe": 20,  # ROE > 12%
    "debt_equity": 15,  # Debt/Equity < 1
    "profit_margin": 15,  # Profit margin > 10%
    "insider_own": 10,  # Insider ownership > 2%
    "rd_to_rev": 15,  # R&D to revenue > 5%
}

_PENALTY = 10


def durability_score(row: pd.Series) -> float:
    """Compute the Durability-Lite score for a single asset."""

    score = BASE_SCORE
    if row.get("roe", 0) > 0.12:
        score += FACTOR_WEIGHTS["roe"]
    if row.get("debt_equity", 0) < 1:
        score += FACTOR_WEIGHTS["debt_equity"]
    if row.get("profit_margin", 0) > 0.10:
        score += FACTOR_WEIGHTS["profit_margin"]
    if row.get("insider_own", 0) > 0.02:
        score += FACTOR_WEIGHTS["insider_own"]
    if row.get("rd_to_rev", 0) > 0.05:
        score += FACTOR_WEIGHTS["rd_to_rev"]

    if row.get("debt_equity", 0) > 1 and row.get("insider_own", 0) < 0.01:
        score -= _PENALTY

    return float(np.clip(score, 0, 100))


def apply_scores(df: pd.DataFrame) -> pd.Series:
    """Apply :func:`durability_score` across a DataFrame."""

    score = (
        BASE_SCORE
        + (df["roe"] > 0.12) * FACTOR_WEIGHTS["roe"]
        + (df["debt_equity"] < 1) * FACTOR_WEIGHTS["debt_equity"]
        + (df["profit_margin"] > 0.10) * FACTOR_WEIGHTS["profit_margin"]
        + (df["insider_own"] > 0.02) * FACTOR_WEIGHTS["insider_own"]
        + (df["rd_to_rev"] > 0.05) * FACTOR_WEIGHTS["rd_to_rev"]
    )

    penalty_mask = (df["debt_equity"] > 1) & (df["insider_own"] < 0.01)
    score = score - penalty_mask * _PENALTY

    return score.clip(0, 100)
