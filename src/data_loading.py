"""Data loading helpers for the Olist retail analytics portfolio project."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def load_all_tables(data_dir: Path = DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load all raw Olist CSV tables into a dictionary of DataFrames.

    The files are expected to live in the raw data directory under their original
    Kaggle names, and they are loaded read-only for audit purposes.
    """
    table_map = {
        "customers": "olist_customers_dataset.csv",
        "geolocation": "olist_geolocation_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "order_payments": "olist_order_payments_dataset.csv",
        "order_reviews": "olist_order_reviews_dataset.csv",
        "orders": "olist_orders_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "category_name_translation": "product_category_name_translation.csv",
    }

    return {
        name: pd.read_csv(data_dir / file_name)
        for name, file_name in table_map.items()
    }
