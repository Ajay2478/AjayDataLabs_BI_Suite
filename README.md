# 💎 AjayDataLabs: Enterprise BI & Logistics Suite
### *An AI-Powered Command Center for E-Commerce Intelligence*

---

## 📖 Executive Summary
**AjayDataLabs BI Suite** is a full-stack Business Intelligence solution that transforms raw, messy e-commerce transaction logs into actionable strategic insights. Built for high-volume retailers, this suite moves beyond simple descriptive charts to provide **predictive forecasting**, **geospatial logistics mapping**, and **algorithmic customer segmentation**.

---

## 🚀 Key Features

### 1. 📈 Predictive Revenue Forecasting
* **Engine:** Utilizes **Ordinary Least Squares (OLS) Linear Regression** via Scikit-Learn.
* **Insight:** Analyzes historical "Revenue Velocity" and projects future performance 6 months ahead.
* **Tech:** Automated time-series resampling from daily transactions to monthly aggregates.

### 2. 🌍 Geospatial Logistics Intelligence
* **Engine:** High-fidelity USA State-level Choropleth mapping.
* **Insight:** Identifies "Shipping Friction" hotspots where delivery delays impact customer satisfaction.
* **Tech:** Dynamic Plotly Express integration with state-code normalization.

### 3. 🎯 RFM Customer Segmentation
* **Engine:** Algorithmic clustering based on **Recency, Frequency, and Monetary** value.
* **Insight:** Automatically labels customers into tiers: *Champions, Loyalists, Regulars,* and *At Risk*.
* **Tech:** Custom quantile-based scoring to identify customers who require immediate retention marketing.

### 4. 💬 Product Sentiment Lab
* **Engine:** Quadrant Analysis mapping Sales Volume against Shipping Efficiency.
* **Insight:** An "AI Insight Generator" flags high-revenue categories with logistics bottlenecks.

---

## 🛠️ Tech Stack & Engineering
| Layer | Technologies |
| :--- | :--- |
| **Language** | Python 3.13.9 |
| **Frontend** | Streamlit (Multi-page Navigation API) |
| **Data Processing** | Pandas (Vectorized Operations), NumPy |
| **Machine Learning** | Scikit-Learn (Linear Models) |
| **Visualization** | Plotly Express, Matplotlib |

---

## 🏗️ Data Pipeline (ETL)
The project includes a robust `data_engineer.py` script that handles the **Extraction, Transformation, and Loading** of the dataset:
1.  **Cleaning:** Strips hidden whitespace from headers and standardizes naming conventions.
2.  **Temporal Engineering:** Parses inconsistent date formats (DD/MM/YYYY vs MM/DD/YYYY) using `dayfirst=True` logic.
3.  **Feature Engineering:** Calculates `Days_to_Ship` and `Months_Since_Start` to power the ML models.

---