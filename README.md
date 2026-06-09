# Mutual Fund Analytics Platform

## Project Objective

Build an end-to-end Mutual Fund Analytics Platform to analyze mutual fund performance, NAV trends, SIP inflows, AUM growth, portfolio holdings, investor behavior, and fund risk metrics using Python, SQL, SQLite, Power BI, and GitHub.

---

## Technology Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* SQLite
* SQLAlchemy
* SQL
* Git & GitHub
* Power BI

---

## Project Structure

```text
bluestock_mf_capstone/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── db/
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_eda_analysis.ipynb
│
├── scripts/
│   ├── data_ingestion.py
│   ├── data_cleaning.py
│   ├── live_nav_fetch.py
│   ├── load_to_sqlite.py
│   └── day3_eda.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── dashboard/
│
├── reports/
│   ├── charts/
│   └── data_dictionary.md
│
└── README.md
```

---

# Day 1 – Data Ingestion & Validation

### Tasks Completed

* Created project folder structure
* Initialized Git repository
* Connected project to GitHub repository
* Installed project dependencies
* Loaded all provided CSV datasets using Pandas
* Performed dataset inspection
* Verified shape, columns and datatypes
* Integrated AMFI Live NAV API
* Fetched live NAV data
* Saved API output for analysis
* Validated AMFI scheme codes
* Generated data quality observations

### Deliverables

* requirements.txt
* data_ingestion.py
* live_nav_fetch.py
* GitHub repository
* Day 1 Git commit

---

# Day 2 – Data Cleaning & Database Setup

### Tasks Completed

#### NAV History Cleaning

* Converted date columns to datetime
* Sorted records by AMFI code and date
* Removed duplicate records
* Forward-filled missing NAV values
* Validated NAV values

#### Investor Transactions Cleaning

* Standardized transaction types
* Validated investment amounts
* Corrected date formats
* Verified KYC status values

#### Scheme Performance Cleaning

* Validated return columns
* Checked numeric consistency
* Verified expense ratio ranges
* Flagged anomalies

#### Database Design

Created SQLite star schema:

* dim_fund
* dim_date
* fact_nav
* fact_transactions
* fact_performance
* fact_aum

#### Documentation

* Created schema.sql
* Created queries.sql
* Created data_dictionary.md

### Deliverables

* Cleaned datasets
* SQLite database
* schema.sql
* queries.sql
* data_dictionary.md
* Day 2 Git commit

---

# Day 3 – Exploratory Data Analysis (EDA)

### Tasks Completed

Generated exploratory visualizations and business insights.

### Charts Created

1. AUM Growth by Fund House
2. Monthly SIP Trend
3. Category Inflow Heatmap
4. Investor Age Distribution
5. Investor Gender Distribution
6. State-wise Investment Distribution
7. City Tier Distribution (T30 vs B30)
8. Industry Folio Growth Trend
9. Equity vs Debt vs Hybrid Folio Growth
10. Top Funds by 5-Year Returns
11. Sector Allocation Donut Chart
12. Expense Ratio Distribution
13. Risk Grade Distribution
14. Morningstar Rating Distribution

### Key Insights

* SBI Mutual Fund maintains the highest AUM among major fund houses.
* SIP inflows show consistent growth across the analysis period.
* Equity categories dominate investor inflows.
* Folio counts increased significantly from 2022 to 2025.
* Portfolio allocations remain concentrated in key sectors.
* Higher-rated funds generally demonstrate stronger historical performance.
* Expense ratios remain within expected industry ranges.

### Deliverables

* 14 EDA charts
* EDA scripts
* Analytical insights
* Visualization outputs saved in reports/charts
* Day 3 Git commit

---

## Current Progress

### Completed

* Day 1 – Data Ingestion
* Day 2 – Data Cleaning & Database Setup
* Day 3 – Exploratory Data Analysis

### Upcoming

* Day 4 – Performance Analytics
* Day 5 – Advanced Analytics & Recommendation Engine
* Day 6 – Power BI Dashboard Development
* Day 7 – Final Report & Presentation

---

# Day 4 – Performance Analytics

## Overview

Day 4 focused on evaluating mutual fund performance using return, risk, and benchmark-based analytics. Multiple performance metrics were computed for all 40 mutual fund schemes to identify high-performing funds and rank them using a composite scorecard.

## Objectives

* Calculate daily returns from NAV history
* Compute CAGR for mutual fund schemes
* Evaluate risk-adjusted performance using Sharpe Ratio
* Measure downside risk using Sortino Ratio
* Calculate Alpha and Beta against benchmark indices
* Analyze Maximum Drawdown
* Build a Fund Scorecard for ranking schemes
* Compare top funds against benchmark indices

## Datasets Used

* 02_nav_history.csv
* 07_scheme_performance.csv
* 10_benchmark_indices.csv

## Analytics Performed

### Daily Returns

Calculated daily percentage returns for all mutual fund schemes using NAV data.

Formula:
daily_return = (NAV_t / NAV_t-1) - 1

### CAGR

Computed annualized growth rates across fund history.

Formula:
CAGR = (Ending NAV / Beginning NAV)^(1/n) - 1

### Sharpe Ratio

Measured risk-adjusted returns using a 6.5% risk-free rate.

Formula:
Sharpe Ratio = (Rp - Rf) / Std(Rp) × √252

### Sortino Ratio

Evaluated returns relative to downside volatility.

Formula:
Sortino Ratio = (Rp - Rf) / Downside Deviation × √252

### Alpha & Beta

Calculated using linear regression against NIFTY100 benchmark returns.

Outputs:

* Alpha
* Beta

### Maximum Drawdown

Measured the worst peak-to-trough decline for each scheme.

Formula:
Drawdown = NAV / Running_Max - 1

### Fund Scorecard

Created a composite ranking model using:

* CAGR Rank
* Sharpe Rank
* Alpha Rank
* Drawdown Rank

## Deliverables

### CSV Outputs

* cagr_table.csv
* sharpe_ratio.csv
* sortino_ratio.csv
* alpha_beta.csv
* max_drawdown.csv
* fund_scorecard.csv

### Visualizations

* benchmark_comparison.png

## Results

* Evaluated performance for 40 mutual fund schemes.
* Generated risk and return rankings.
* Built a composite scorecard for fund selection.
* Compared top-performing funds with benchmark indices.

## Status

Day 4 completed successfully.

## Author

Krishna Vamsi Bommireddy
Data Analytics Capstone Project
