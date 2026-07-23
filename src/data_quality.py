"""Reusable data quality check helpers for the Olist audit pipeline."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing counts and percentages per column."""
    missing = df.isna().sum()
    percent = missing / len(df) * 100
    return pd.DataFrame({"missing_count": missing, "missing_pct": percent})


def exact_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Return exact duplicate rows."""
    return df[df.duplicated(keep=False)].sort_values(list(df.columns))


def count_unique_by_key(df: pd.DataFrame, key_columns: Iterable[str]) -> pd.Series:
    """Count unique values for one or more key columns."""
    key_cols = list(key_columns)
    return df[key_cols].nunique(dropna=False)


def fk_orphan_counts(child_df: pd.DataFrame, child_key: str, parent_df: pd.DataFrame, parent_key: str) -> pd.Series:
    """Return counts of child keys that do not have a parent match."""
    orphan_keys = set(child_df[child_key].dropna().unique()) - set(parent_df[parent_key].dropna().unique())
    return pd.Series({"orphan_count": len(orphan_keys), "orphan_keys": list(orphan_keys)})


def date_range_report(df: pd.DataFrame, date_columns: Iterable[str]) -> pd.DataFrame:
    """Return min/max dates for each date column after conversion to datetime."""
    cols = list(date_columns)
    result = []
    for column in cols:
        if column in df.columns:
            converted = pd.to_datetime(df[column], errors="coerce")
            result.append(
                {
                    "column": column,
                    "min": converted.min(),
                    "max": converted.max(),
                    "null_count": converted.isna().sum(),
                }
            )
    return pd.DataFrame(result)


def find_impossible_values(df: pd.DataFrame) -> dict[str, pd.Series]:
    """Audit common impossible values across the Olist tables."""
    findings = {}

    if "price" in df.columns:
        findings["negative_price"] = df[df["price"] < 0]["price"]
    if "freight_value" in df.columns:
        findings["negative_freight"] = df[df["freight_value"] < 0]["freight_value"]
    if "review_score" in df.columns:
        findings["review_score_out_of_range"] = df[(df["review_score"] < 1) | (df["review_score"] > 5)]["review_score"]
    if {"order_purchase_timestamp", "order_delivered_customer_date"}.issubset(df.columns):
        findings["delivery_before_purchase"] = df[
            df["order_delivered_customer_date"] < df["order_purchase_timestamp"]
        ]["order_delivered_customer_date"]
    if "order_item_id" in df.columns:
        findings["zero_quantity"] = df[df["order_item_id"] == 0]["order_item_id"]

    return findings
