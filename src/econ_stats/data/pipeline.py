"""Placeholder for cleaning / aligning macro time series."""

from __future__ import annotations

import pandas as pd


def align_to_calendar(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Example: ensure datetime index; extend with real logic."""
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col])
    return out.sort_values(date_col)
