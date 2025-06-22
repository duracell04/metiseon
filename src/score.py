"""Durability scoring helpers."""

from __future__ import annotations

import pandas as pd


def durability_score(row: pd.Series) -> float:
    """Compute the Durability-Lite score for a single asset."""
    pass


def apply_scores(df: pd.DataFrame) -> pd.Series:
    """Apply :func:`durability_score` across a DataFrame."""
    pass
