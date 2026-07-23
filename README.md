# Olist Retail Analytics Portfolio Project

This project is the setup phase for a retail analytics and forecasting portfolio pipeline using the Olist Brazilian E-Commerce dataset.

## Overview
- Audit raw Olist CSV data without cleaning or modeling.
- Build reusable data-loading and data-quality utilities in `src/`.
- Produce an audit workbook in `notebooks/` for first-look and data-quality review.

## Structure
- `data/raw/` stores the original Kaggle source data.
- `data/processed/` is reserved for cleaned outputs and downstream artifacts.
- `src/` contains reusable Python modules for data loading and data quality checks.

## Notes
- Raw data is treated as read-only source of truth.
- No cleaning or modeling will be performed until the review phase is approved.
