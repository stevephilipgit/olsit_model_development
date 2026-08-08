# Olist Brazil E-Commerce Analytics & Late Delivery Prediction

## Overview

This repository follows the Olist Brazilian e-commerce dataset from exploratory analysis through a late-delivery prediction workflow:

```text
Raw data → Data cleaning → Analysis / EDA → Feature engineering
→ Machine learning → Model evaluation → Probability calibration
→ Final prediction pipeline
```

The first part of the project develops order, customer, payment, delivery, and sales insights. The second part formulates `late_delivery_flag` as a supervised classification target and evaluates XGBoost-based models. The repository contains trained artifacts, but it does not yet contain a deployed application or production monitoring system.

## Business Problem

The predictive objective is to identify whether an order is likely to be delivered late:

```text
target = late_delivery_flag
```

Earlier identification of at-risk deliveries can support operational prioritization and decision-making. Because late deliveries are relatively uncommon, the project evaluates more than accuracy alone and examines the precision/recall trade-off at different decision thresholds.

## Dataset

The project uses the Olist Brazilian E-Commerce Public Dataset. The raw data present in `data/raw/` includes the following tables:

- customers
- orders
- order items
- order payments
- order reviews
- products
- sellers
- geolocation
- product-category translations

The ETL and feature-engineering notebooks create the project’s analytical tables, including `fact_orders.csv`, `sales_fact.csv`, and feature-engineered versions in `data/processed/final_processed_datasets/`.

## Part 1 — Data Analytics

Notebooks 01–07 document the analytics workflow:

- data familiarization, data-quality checks, relationship-integrity checks, and business-rule validation;
- ETL that combines the Olist source tables into order and sales fact tables;
- feature engineering for delivery timing, payments, order values, freight, product size/weight indicators, and review-related fields;
- exploratory analysis of sales performance, monthly revenue, orders, customers, payments, fulfilment, and review scores;
- Power BI reporting in `powerbi/olist_dashboard.pbix`, with dashboard images in `dashboard/`.

The existing dashboard documentation reports approximately 99K orders, total revenue above 13.59 million, an average order value of 136.68, an average review score of 4.09, and a late-delivery rate of 7.87%.

## Part 2 — Data Science / Machine Learning

Notebooks 08–11 convert the analytical data into a late-delivery classification problem, develop models, examine errors, and refine the final model.

### Feature Engineering

The final model uses 17 inputs derived from information available at prediction time:

- customer location: ZIP-code prefix, city, and state;
- payment information: total payment, payment count/type, maximum installments, multiple-payment-method flag, and average payment per installment;
- purchase timing: year, month, month name, quarter, day, weekday, and hour;
- estimated delivery days.

### Leakage Prevention

The final workflow uses an explicit feature allow-list and audits the model matrix for forbidden fields. Delivery-completion timestamps, delivery-duration/delay fields, review data, and other post-outcome signals are excluded from model inputs. This is important because those fields would be unavailable when making an early delivery-risk prediction and could artificially improve evaluation results.

### Class Imbalance

In `fact_orders.csv`, 7,827 of 99,441 orders (7.87%) are labelled late, versus 91,614 on time. Accuracy is therefore not sufficient: a model can appear strong while detecting few late orders. The project evaluates class-weighted XGBoost and compares precision, recall, F1, ROC AUC, and PR AUC to make the trade-off explicit.

### Model Development

The ML notebooks evaluate the following progression:

1. XGBoost V1 at the default threshold and an F1-oriented threshold.
2. Class-weighted XGBoost V2 to alter the imbalance trade-off.
3. Threshold optimization, including cost-sensitive analysis with false negatives weighted more heavily than false positives.
4. Calibrated XGBoost V2, using sigmoid calibration with `CalibratedClassifierCV` and five folds.

## Model Evaluation

| Model | Threshold | Accuracy | Precision | Recall | F1 | ROC AUC | PR AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| XGBoost V1 — Default | 0.50 | 0.9192 | 0.4545 | 0.1342 | 0.2072 | 0.7813 | 0.2739 |
| XGBoost V1 — F1 Optimized | 0.20 | 0.8800 | 0.3090 | 0.3898 | 0.3447 | 0.7813 | 0.2739 |
| XGBoost V2 — Class Weighted | 0.50 | 0.8313 | 0.2362 | 0.5125 | 0.3234 | 0.7769 | 0.2858 |
| XGBoost V2 — F1 Optimized | 0.65 | 0.8815 | 0.3059 | 0.3987 | 0.3462 | 0.7769 | 0.2858 |
| Calibrated XGBoost V2 — Final | 0.19 | 0.8871 | 0.3293 | 0.4192 | 0.3689 | 0.7929 | 0.3102 |

## Probability Calibration

The raw XGBoost probabilities were evaluated for calibration, then recalibrated using sigmoid calibration. The final threshold is selected from the project’s calibrated-probability evaluation rather than assumed to be `0.50`.

## Final Model

**Calibrated XGBoost V2** is the final saved model, with a threshold of **0.19**.

| Metric | Final result |
|---|---:|
| Accuracy | 88.71% |
| Precision | 32.93% |
| Recall | 41.92% |
| F1 | 36.89% |
| ROC AUC | 79.29% |
| PR AUC | 31.02% |

Final confusion matrix (`[[TN, FP], [FN, TP]]`):

```text
[[16988, 1336],
 [  909,  656]]
```

- True negatives: 16,988 on-time orders correctly predicted as on time.
- False positives: 1,336 on-time orders predicted as late.
- False negatives: 909 late orders not identified by the model.
- True positives: 656 late orders correctly identified.

The high accuracy mainly reflects the majority on-time class. Recall, F1, and PR AUC are more informative for the late-delivery objective.

## Key Findings and Lessons

- Accuracy can be misleading for an imbalanced late-delivery target.
- Leakage-prone post-delivery features can artificially inflate model performance and must be audited.
- Class weighting changes the precision/recall balance rather than universally improving every metric.
- Threshold selection should reflect the classification objective and the cost of false negatives versus false positives.
- Calibration makes predicted probabilities more interpretable for threshold-based decisions.

## Project Structure

```text
.
├── dashboard/                         # Power BI dashboard images
├── data/
│   ├── raw/                           # Olist source tables
│   └── processed/
│       └── final_processed_datasets/  # Feature-engineered fact tables
├── models/                            # Saved calibrated model, threshold, and feature config
├── notebooks/
│   ├── 01_first_look.ipynb … 07_EDA.ipynb
│   └── 08_model_building.ipynb … 11_final_new_features.ipynb
├── powerbi/olist_dashboard.pbix
├── reports/                           # Model benchmark and feature-importance exports
├── src/                               # Data-loading and data-quality modules
├── app.py                             # Present but no implemented deployment app
├── Dockerfile                         # Present but not configured
├── requirements.txt
└── README.md
```

## How to Run

The repository provides `requirements.txt` for the Python dependencies. The Python version is not pinned in the repository.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter notebook
```

For the complete analytical progression, run notebooks in numerical order:

1. `01_first_look.ipynb` through `07_EDA.ipynb` for data understanding, validation, ETL, feature engineering, and EDA.
2. `08_model_building.ipynb` through `11_final_new_features.ipynb` for model development, final-model evaluation, error analysis, and calibration.

Some notebooks contain project-local paths established during development. Confirm their data paths resolve to this repository before re-running them. Re-running training notebooks retrains models and may overwrite saved artifacts.

## Model Artifacts

The `models/` directory contains:

- `late_delivery_xgboost_calibrated_v2.joblib` — final calibrated estimator.
- `late_delivery_threshold.joblib` — final threshold (`0.19`).
- `late_delivery_feature_config.joblib` — final feature groups, target, and threshold configuration.
- `xgboost_v2_calibrated.joblib` and `final_threshold.joblib` — duplicate saved names produced by the final notebook.

`notebooks/models/late_delivery_xgboost_pipeline.joblib` is retained because the error-analysis notebook references that earlier pipeline.

## Limitations

- The dataset is historical and may not reflect current operating conditions.
- Late deliveries are imbalanced, and the final model does not identify every late order.
- False-positive and false-negative errors have different operational consequences.
- Deployment monitoring, drift detection, and a production feedback loop are not implemented in this repository.

## Future Improvements

- Implement an inference API or application around the saved artifacts.
- Add model and data-drift monitoring.
- Tune thresholds using validated operational costs.
- Add temporal validation and a repeatable retraining strategy.
- Incorporate production feedback when it becomes available.

## Source

Olist Brazilian E-Commerce Public Dataset: <https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>
