# Existing Project Structure (Evolution Plan)

We will **continue building on the existing Olist project** instead of creating a new repository. The goal is to evolve it from a Data Analytics project into a complete **Enterprise E-Commerce Intelligence Platform**.

---

## Updated Project Structure

```text
project/

│
├── dashboard/
│     olist-report1.png
│     olist-report2.png
│
├── data/
│     raw/
│     processed/
│
├── notebooks/
│     01_first_look.ipynb
│     02_data_quality.ipynb
│     03_relation_integrity.ipynb
│     04_data_validation.ipynb
│     05_ETL_Data_Preparation.ipynb
│     06_feature_engineering.ipynb
│     07_EDA.ipynb
│
│     ---------- NEW ----------
│
│     08_model_building.ipynb
│     09_model_evaluation.ipynb
│     10_model_interpretation.ipynb
│
├── models/
│
├── app/
│
├── reports/
│
├── src/
│
├── powerbi/
│
├── Dockerfile
│
├── README.md
│
└── requirements.txt
```

---

# New Folders

Create the following folders:

```text
models/

app/

reports/
```

---

# Update the `src/` Directory

Create the following production-ready modules:

```text
src/

├── preprocessing/
├── training/
├── evaluation/
├── prediction/
├── api/
└── utils/
```

As the project grows, the structure will naturally evolve into:

```text
src/

├── preprocessing/
├── training/
├── evaluation/
├── prediction/
├── api/
├── rag/
├── agents/
└── monitoring/
```

---

# Project Roadmap

## Phase 1 — Data Analytics ✅ (Completed)

- Data Cleaning
- ETL
- Feature Engineering
- Power BI Dashboard
- Business Insights

---

## Phase 2 — Machine Learning

Notebook:

```text
08_model_building.ipynb
```

Focus:

- Problem Definition
- Feature Selection
- Model Training
- Baseline Model

---

## Phase 3 — Model Evaluation

Notebook:

```text
09_model_evaluation.ipynb
```

Topics:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
- Cross Validation

---

## Phase 4 — Model Explainability

Notebook:

```text
10_model_interpretation.ipynb
```

Topics:

- Feature Importance
- SHAP
- Business Interpretation
- Why the Model Predicted a Late Delivery

---

## Phase 5 — Model Persistence

Store trained artifacts inside:

```text
models/

late_delivery_model.pkl

preprocessor.pkl
```

---

## Phase 6 — API Development

Create:

```text
app/

main.py

predict.py
```

Technology:

- FastAPI

Purpose:

- Expose the trained model through REST APIs.

---

## Phase 7 — Containerization

Use the existing:

```text
Dockerfile
```

Enhance it to package the API and model into a production-ready container.

---

## Phase 8 — Cloud Deployment

Deploy the application to a cloud platform such as AWS, Azure, or Render.

---

## Phase 9 — Generative AI

Build an AI-powered analytics assistant capable of answering business questions using natural language.

Example:

> "Why were deliveries delayed last month?"

---

## Phase 10 — Retrieval-Augmented Generation (RAG)

Allow the assistant to answer questions from:

- Shipping Policies
- Seller Agreements
- Delivery SLAs
- Company Documentation

---

## Phase 11 — Multi-Agent System

Introduce specialized AI agents such as:

- Data Analyst Agent
- Machine Learning Agent
- Business Consultant Agent
- Report Generation Agent

---

# Learning Outcomes

This project will progressively cover:

### Machine Learning

- Classification
- Feature Selection
- Feature Engineering
- Data Leakage
- Train/Test Split
- Cross Validation
- Hyperparameter Tuning
- Random Forest
- XGBoost

---

### Model Explainability

- Feature Importance
- SHAP
- Business Interpretation

---

### Software Engineering

- Reusable Preprocessing Pipelines
- Model Serialization
- Production Project Structure

---

### Deployment

- FastAPI
- Docker
- Cloud Deployment

---

### AI Engineering

- LLM Integration
- RAG
- Multi-Agent Systems

---

# Development Philosophy

Notebooks will be used **only for experimentation**.

Reusable business logic should be moved into the `src/` directory.

Example:

Instead of writing all training code directly inside a notebook:

```python
train_model()
```

The notebook should call reusable production code:

```python
from src.training.train import train_model

train_model()
```

This keeps notebooks lightweight while ensuring that all reusable logic resides inside the production codebase.

---

# Sprint 1 — Machine Learning

The first sprint will focus on:

- Understanding the business problem
- Defining the prediction target
- Identifying suitable features
- Detecting data leakage
- Building a baseline classification model

Only after achieving a reliable model will we proceed with API development, Docker, cloud deployment, and AI-powered enhancements.