# Phase 3 – Data Validation & Quality Assessment

## Objective

The objective of this phase was to evaluate the reliability, consistency, and integrity of the Olist e-commerce dataset before performing any transformations or business analysis.

Rather than immediately cleaning the data, the goal was to understand **whether anomalies represented actual data quality problems or valid business events**. Every validation was performed using business rules, evidence-based investigation, and exploratory analysis.

---

# Learning Objectives

During this phase, I learned how professional Data Analysts validate datasets before analysis by asking questions such as:

* Is every relationship between tables valid?
* Are business events occurring in the correct chronological order?
* Are numerical values within expected ranges?
* Are anomalies genuine errors or expected business behaviour?
* Should records be removed, corrected, or retained?

This phase emphasized investigation over assumptions.

---

# Validation Workflow

Every validation followed the same analytical process:

```text
Business Rule
        ↓
Validation Query
        ↓
Identify Violations
        ↓
Investigate Evidence
        ↓
Interpret Results
        ↓
Business Decision
        ↓
Document Findings
```

This structured approach prevents accidental deletion of valuable business data.

---

# Validation Summary

| Validation                   | Result           | Decision |
| ---------------------------- | ---------------- | -------- |
| Referential Integrity        | Passed           | Keep     |
| Purchase → Approval Timeline | Passed           | Keep     |
| Approval → Carrier Timeline  | 1,359 violations | Flag     |
| Purchase → Delivery Timeline | Passed           | Keep     |
| Carrier → Delivery Timeline  | 10 violations    | Flag     |
| Late Deliveries              | 7,827 orders     | Keep     |
| Review Score Range           | Passed           | Keep     |
| Payment Value Validation     | Passed           | Keep     |
| Freight Value Validation     | Passed           | Keep     |
| Product Price Validation     | Passed           | Keep     |
| Payment Installments         | 2 anomalies      | Flag     |
| Duplicate Order IDs          | Passed           | Keep     |
| Order Status Validation      | Passed           | Keep     |

---

# 1. Referential Integrity Validation

## Objective

Verify that every foreign key correctly references an existing record in its parent table.

Relationships validated:

* Orders → Customers
* Order Items → Orders
* Order Items → Products
* Order Items → Sellers
* Payments → Orders
* Reviews → Orders

## Result

No orphan records were identified.

## Conclusion

The relational structure of the dataset is consistent and suitable for analysis.

---

# 2. Temporal Validation

Chronological consistency was validated across the order lifecycle.

Expected workflow:

```text
Purchase
    ↓
Approval
    ↓
Carrier Pickup
    ↓
Customer Delivery
```

---

## Purchase → Approval

### Business Rule

Orders cannot be approved before they are purchased.

### Result

0 violations.

### Conclusion

Timeline is valid.

---

## Approval → Carrier Pickup

### Business Rule

Payment approval should occur before the seller hands the package to the logistics carrier.

### Result

1,359 violations.

---

### Investigation

The approval delay was calculated for every violating record.

Summary statistics:

* Mean delay: ~1 day
* Median delay: ~17 hours
* Maximum delay: 171 days

Further investigation revealed:

* 451 records shared the same approval date (2018-07-05)
* 383 records shared another approval date (2018-04-24)

Instead of random errors, anomalies were clustered around specific timestamps.

Inspection of the largest violations showed:

* Most records followed a similar pattern.
* One record showed a carrier pickup occurring months before the purchase date, indicating an obvious timestamp inconsistency.

---

### Conclusion

Evidence suggests these records are more likely the result of batch updates, delayed synchronization, or timestamp recording issues rather than independent data entry errors.

These records were retained and flagged instead of removed.

---

## Purchase → Customer Delivery

### Business Rule

Customers cannot receive products before placing an order.

### Result

0 violations.

### Conclusion

Timeline is valid.

---

## Carrier Pickup → Customer Delivery

### Business Rule

Products cannot be delivered before the logistics carrier receives them.

### Result

10 violations.

### Investigation

Only ten records violated this rule among approximately 99,000 orders.

These represent roughly 0.01% of the dataset.

The extremely small number suggests isolated timestamp inconsistencies rather than a systematic issue.

### Conclusion

Records were retained and flagged.

---

# 3. Delivery Performance Validation

Business question:

Were products delivered after the promised delivery date?

### Result

7,827 late deliveries.

Delay statistics:

* Average delay: ~9.5 days
* Median delay: ~5.8 days
* Maximum delay: ~189 days

### Important Learning

Late deliveries are **not** data quality problems.

They represent genuine business performance.

These records should be preserved because they are valuable for future business analysis.

Potential analyses include:

* Delivery performance by state
* Delivery performance by seller
* Delivery performance by product category
* Average delay trends over time

---

# 4. Numerical Validation

The following validations were performed.

## Negative Payment Values

Result:

No invalid records.

---

## Negative Freight Values

Result:

No invalid records.

---

## Invalid Product Prices

Result:

No invalid records.

---

## Payment Installments

Business Rule:

Credit card installment values should be greater than zero.

Result:

2 records contained zero installments.

Both records used credit card payments.

Conclusion:

Potential recording anomaly.

Records retained and flagged.

---

# 5. Range Validation

Review scores were validated.

Expected range:

1–5

Result:

No invalid review scores.

Conclusion:

Review ratings are valid.

---

# 6. Duplicate Validation

Duplicate Order IDs were checked.

Result:

No duplicate order identifiers.

The Orders table satisfies entity uniqueness.

---

# 7. Categorical Validation

Order status values were validated.

Observed values:

* delivered
* shipped
* canceled
* unavailable
* invoiced
* processing
* created
* approved

No unexpected categories were identified.

---

# Key Findings

The dataset is of high overall quality.

Most validations passed without issues.

The majority of identified anomalies were timestamp-related and exhibited recognizable patterns rather than random inconsistencies.

Instead of deleting anomalous records, investigations were performed to determine whether they represented:

* Genuine business behaviour
* Logging delays
* Timestamp synchronization issues
* Data recording problems

Only after investigation were decisions made regarding whether records should be retained or flagged.

---

# Python & Pandas Concepts Learned

Throughout this phase, the following concepts were applied.

## Data Types

* datetime64
* Timedelta

## Pandas Functions

* `isin()`
* Boolean Indexing
* `~`
* `pd.to_datetime()`
* `.describe()`
* `.dt`
* `.value_counts()`
* `.sort_values()`
* `.between()`
* `.duplicated()`

## Validation Techniques

* Foreign key validation
* Datetime comparison
* Range validation
* Numerical validation
* Duplicate detection
* Category validation

---

# Data Analysis Skills Learned

This phase significantly improved practical analytical thinking.

Key skills developed include:

* Business rule validation
* Evidence-based investigation
* Root cause analysis
* Pattern recognition
* Outlier investigation
* Temporal consistency analysis
* Data quality assessment
* Distinguishing business events from data errors
* Decision making based on evidence instead of assumptions

---

# Phase 3 Deliverables

At the end of this phase, the dataset has been fully assessed for quality and documented.

Outputs include:

* Comprehensive validation notebook
* Validation summary tables
* Investigation of detected anomalies
* Business interpretations
* Data quality documentation
* ETL recommendations

---

# Next Phase

The next phase focuses on ETL (Extract, Transform, Load).

Goals:

1. Standardize data types.
2. Handle missing values.
3. Treat or flag anomalies.
4. Engineer analytical features.
5. Prepare clean datasets for exploratory analysis and dashboard development.

Phase 3 establishes confidence that the data is sufficiently understood before transformation begins, ensuring that future analyses are built on informed decisions rather than assumptions.
