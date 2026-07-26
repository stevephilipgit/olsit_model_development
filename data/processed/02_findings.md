I actually love this question. This is how senior engineers and data scientists build project documentation. They don't write "I checked missing values." They document **the methodology**.

I'd organize your README like this.

---

# 📊 Phase 2 — Data Quality Assessment

## Objective

Before cleaning, joining, or modeling the data, perform a comprehensive **Data Quality Assessment (DQA)** to understand the structure, reliability, and integrity of each dataset.

---

# 1. Dataset Inventory

### Goal

Understand what data is available before analysis.

### Checks Performed

* Loaded all datasets
* Verified dataset dimensions (rows × columns)
* Checked memory usage
* Inspected column names
* Verified data types

### Why?

This provides a high-level understanding of the data and helps identify potential issues before deeper analysis.

---

# 2. Missing Value Analysis

### Goal

Identify incomplete information.

### Checks Performed

For every column:

* Missing Count
* Missing Percentage

### Key Learning

> Missing values are **not automatically bad data**.

Before handling missing values, always ask:

* Why is the value missing?
* Is it expected?
* Is it optional?
* Does it represent a business event?
* Can it be recovered?

### Examples

* `review_comment_message`

  * 58.7% missing
  * Expected because customers are not required to write comments.

* `order_delivered_customer_date`

  * Missing because some orders were not delivered or were cancelled.

* `product_weight_g`

  * Only two missing values.
  * Candidate for removal or imputation.

### Decision

No missing values were modified during this phase.

Only observations were documented.

---

# 3. Duplicate Analysis

### Goal

Determine whether duplicate records indicate data quality issues or expected business behavior.

### Types of Duplicate Checks

## A. Duplicate Records

Checked whether entire rows were repeated.

```python
df.duplicated()
```

Purpose:

Detect accidental duplicate records.

---

## B. Primary Key Duplicates

Checked whether primary keys were unique.

Examples

* customer_id
* product_id
* seller_id
* review_id

Purpose:

Every entity should have one unique identifier.

---

## C. Composite Key Validation

Some tables naturally contain repeated values.

Example

`order_items`

One order

↓

Many products

Instead of checking

```text
order_id
```

we validated

```text
(order_id, order_item_id)
```

as the composite key.

---

## D. Business Duplicate Investigation

Instead of deleting duplicate review IDs immediately, we investigated the cause.

This follows the principle:

```text
Detect

↓

Investigate

↓

Understand

↓

Decide
```

instead of

```text
Detect

↓

Delete
```

---

# 4. Data Investigation

Instead of assuming duplicate review IDs were errors, we performed an investigation.

This involved multiple evidence-based checks.

---

## Investigation 1

Question:

Are duplicated review IDs identical?

Checked:

* review score
* review text
* timestamps

Observation:

Everything matched except `order_id`.

---

## Investigation 2

Question:

Do duplicated reviews belong to different orders?

Answer:

Yes.

---

## Investigation 3

Question:

Do those orders belong to different customers?

Initially appeared to be yes.

---

## Investigation 4

Question:

Do those customer IDs represent different people?

Joined

Orders

↓

Customers

↓

customer_unique_id

Observation:

Different `customer_id`s mapped to the same `customer_unique_id`.

Conclusion:

The duplicated reviews belonged to the **same real customer**.

---

# 5. Business Understanding

One of the biggest discoveries during analysis.

Understanding the difference between

```text
customer_id
```

and

```text
customer_unique_id
```

---

## customer_id

Represents

> A customer record associated with a specific order.

One customer may receive multiple customer IDs.

---

## customer_unique_id

Represents

> The real customer.

Remains constant across purchases.

---

# 6. Analytical Thinking Process

Throughout the investigation, we followed an evidence-driven workflow.

```text
Observation

↓

Question

↓

Hypothesis

↓

Evidence Collection

↓

Analysis

↓

Conclusion
```

Example

Observation

Duplicate review IDs detected.

↓

Hypothesis

A customer may have submitted one review for multiple purchases.

↓

Evidence

* Compared review contents
* Compared timestamps
* Checked order ownership
* Verified customer_unique_id

↓

Conclusion

The duplicated review IDs represent valid business behavior rather than accidental duplicate records.

---

# 7. Key Concepts Learned

* Data Quality Assessment (DQA)
* Missing Value Analysis
* Duplicate Record Detection
* Primary Key Validation
* Composite Key Validation
* Business Rule Validation
* Exploratory Data Analysis (EDA)
* Root Cause Analysis (RCA)
* Evidence-Based Investigation
* Relational Data Understanding
* Business Context Analysis

---

# 8. Important Principles

### Principle 1

Never clean data before understanding it.

---

### Principle 2

Missing values are not always errors.

---

### Principle 3

Duplicate records are not always duplicates.

---

### Principle 4

Always understand the business meaning behind every column.

---

### Principle 5

Never delete data without evidence.

---

### Principle 6

Validate assumptions using data.

---

# About "Hypothesis Testing"

This is a really good question because people often misuse this term.

## What we did

We used the **scientific method for data investigation**:

```text
Observation
      ↓
Question
      ↓
Hypothesis
      ↓
Collect Evidence
      ↓
Analyze
      ↓
Conclusion
```

This is often called:

* **Hypothesis-driven analysis**
* **Evidence-based investigation**
* **Investigative data analysis**

These are common in analytics and data science.

## What we did NOT do

We did **not** perform **statistical hypothesis testing**.

When people in statistics or machine learning say "hypothesis testing," they usually mean tests such as:

* t-test
* Chi-square test
* ANOVA
* Mann-Whitney U test
* Kolmogorov-Smirnov test

Those involve:

* Null hypothesis (H₀)
* Alternative hypothesis (H₁)
* p-value
* Significance level (α)
* Statistical decision

For example:

> H₀: Average delivery time is the same in two regions.

Then you'd calculate a test statistic and a p-value.

So it's better to describe what we did as **hypothesis-driven investigation** or **evidence-based data investigation**, not statistical hypothesis testing.

---

This is very close to how senior data analysts and data scientists document their exploratory and quality assessment work before moving into ETL, feature engineering, and modeling.
